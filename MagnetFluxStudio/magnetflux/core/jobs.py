"""Background job runner with progress reporting and cooperative cancellation.

The solver, mesher and optimizer are long-running and must not block the GUI
thread. This module provides a Qt-independent job abstraction so the numerical
layers stay testable; the UI layer adapts it to Qt signals.

A :class:`Job` runs a callable that receives a :class:`ProgressHandle`. Work
should periodically call :meth:`ProgressHandle.report` (which also raises
:class:`JobCancelled` if cancellation was requested), giving cooperative
cancellation without killing threads.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class JobState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobCancelled(Exception):
    """Raised inside a job body when cancellation has been requested."""


@dataclass(slots=True)
class ProgressHandle:
    """Passed to a job body for progress reporting and cancellation checks."""

    _cancel_event: threading.Event
    _callback: Callable[[float, str], None] | None = None

    def report(self, fraction: float, message: str = "") -> None:
        """Report progress in ``[0, 1]``; raises if cancellation was requested."""
        if self._cancel_event.is_set():
            raise JobCancelled()
        if self._callback is not None:
            self._callback(max(0.0, min(1.0, fraction)), message)

    @property
    def cancelled(self) -> bool:
        return self._cancel_event.is_set()


class Job(Generic[T]):
    """A cancellable unit of work executed on a worker thread.

    Args:
        fn: Callable taking a :class:`ProgressHandle` and returning a result.
        on_progress: Optional ``(fraction, message)`` callback.
        on_done: Optional callback receiving the result on success.
        on_error: Optional callback receiving the exception on failure.
    """

    def __init__(
        self,
        fn: Callable[[ProgressHandle], T],
        *,
        on_progress: Callable[[float, str], None] | None = None,
        on_done: Callable[[T], None] | None = None,
        on_error: Callable[[BaseException], None] | None = None,
    ) -> None:
        self._fn = fn
        self._on_progress = on_progress
        self._on_done = on_done
        self._on_error = on_error
        self._cancel_event = threading.Event()
        self._thread: threading.Thread | None = None
        self.state: JobState = JobState.PENDING
        self.result: T | None = None
        self.error: BaseException | None = None

    def _run(self) -> None:
        self.state = JobState.RUNNING
        handle = ProgressHandle(self._cancel_event, self._on_progress)
        try:
            self.result = self._fn(handle)
            self.state = JobState.DONE
            if self._on_done is not None:
                self._on_done(self.result)
        except JobCancelled:
            self.state = JobState.CANCELLED
        except BaseException as exc:  # noqa: BLE001 - report all failures
            self.error = exc
            self.state = JobState.FAILED
            if self._on_error is not None:
                self._on_error(exc)

    def start(self) -> "Job[T]":
        """Start the job on a daemon worker thread."""
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def cancel(self) -> None:
        """Request cooperative cancellation."""
        self._cancel_event.set()

    def join(self, timeout: float | None = None) -> None:
        """Block until the job finishes (mainly for tests)."""
        if self._thread is not None:
            self._thread.join(timeout)

    def run_sync(self) -> T:
        """Run synchronously on the current thread and return the result."""
        self._run()
        if self.state == JobState.FAILED and self.error is not None:
            raise self.error
        return self.result  # type: ignore[return-value]


def run_now(fn: Callable[[ProgressHandle], T], **kwargs: Any) -> T:
    """Convenience: build and run a :class:`Job` synchronously."""
    return Job(fn, **kwargs).run_sync()
