"""Tests for the background job runner."""

import time

import pytest

from magnetflux.core.jobs import Job, JobCancelled, JobState, ProgressHandle, run_now


def test_run_sync_returns_result_and_reports_progress():
    seen = []

    def work(p: ProgressHandle) -> int:
        for i in range(5):
            p.report(i / 4, f"step {i}")
        return 42

    result = run_now(work, on_progress=lambda f, m: seen.append((f, m)))
    assert result == 42
    assert seen[0][0] == 0.0
    assert seen[-1][0] == 1.0


def test_error_is_captured_and_reraised_in_sync():
    def boom(p: ProgressHandle):
        raise RuntimeError("nope")

    job = Job(boom)
    with pytest.raises(RuntimeError):
        job.run_sync()
    assert job.state == JobState.FAILED
    assert isinstance(job.error, RuntimeError)


def test_cooperative_cancellation():
    started = []

    def work(p: ProgressHandle):
        for i in range(1000):
            p.report(i / 1000)
            started.append(i)
            time.sleep(0.001)
        return "done"

    job = Job(work).start()
    while not started:
        time.sleep(0.001)
    job.cancel()
    job.join(timeout=2.0)
    assert job.state == JobState.CANCELLED
    assert job.result is None


def test_progress_report_raises_when_cancelled():
    import threading

    ev = threading.Event()
    ev.set()
    handle = ProgressHandle(ev)
    with pytest.raises(JobCancelled):
        handle.report(0.5)
