"""Centralised logging configuration and a crash reporter (Milestone 0).

A single :func:`configure_logging` call wires up a console handler and an
optional rotating file handler. :func:`install_crash_handler` routes uncaught
exceptions to the log (and an optional callback) so the GUI can show a dialog
instead of dying silently.
"""

from __future__ import annotations

import logging
import sys
import traceback
from collections.abc import Callable
from logging.handlers import RotatingFileHandler
from pathlib import Path
from types import TracebackType

_CONFIGURED = False

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    level: str = "INFO",
    log_dir: Path | None = None,
    *,
    to_file: bool = True,
) -> logging.Logger:
    """Configure the root ``magnetflux`` logger (idempotent).

    Args:
        level: Logging level name.
        log_dir: Directory for the rotating log file (ignored if not
            ``to_file``).
        to_file: Whether to also write a rotating log file.

    Returns:
        The configured ``magnetflux`` package logger.
    """
    global _CONFIGURED
    logger = logging.getLogger("magnetflux")
    if _CONFIGURED:
        logger.setLevel(level)
        return logger

    logger.setLevel(level)
    formatter = logging.Formatter(_FORMAT, datefmt=_DATE_FORMAT)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    if to_file and log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / "magnetflux.log",
            maxBytes=2_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    _CONFIGURED = True
    logger.debug("Logging configured (level=%s, to_file=%s)", level, to_file)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger of the ``magnetflux`` namespace."""
    return logging.getLogger(f"magnetflux.{name}")


def install_crash_handler(
    on_crash: Callable[[str], None] | None = None,
) -> None:
    """Route uncaught exceptions to the log and an optional callback.

    Args:
        on_crash: Optional callable receiving the formatted traceback string
            (e.g. to display a GUI dialog). ``KeyboardInterrupt`` is passed
            through to the default handler so Ctrl-C still works.
    """
    logger = logging.getLogger("magnetflux")

    def _hook(
        exc_type: type[BaseException],
        exc: BaseException,
        tb: TracebackType | None,
    ) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc, tb)
            return
        text = "".join(traceback.format_exception(exc_type, exc, tb))
        logger.critical("Uncaught exception:\n%s", text)
        if on_crash is not None:
            try:
                on_crash(text)
            except Exception:  # pragma: no cover - defensive
                logger.exception("crash handler callback failed")

    sys.excepthook = _hook
