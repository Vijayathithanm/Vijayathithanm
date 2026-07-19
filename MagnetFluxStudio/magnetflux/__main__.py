"""Console entry point: launch the MagnetFlux Studio GUI.

Kept thin so the numerical core never imports Qt. The GUI is imported lazily
and a helpful message is printed if the optional GUI dependencies are missing.
"""

from __future__ import annotations

import sys

from magnetflux.config import AppConfig
from magnetflux.logging_setup import configure_logging, install_crash_handler


def main() -> int:
    """Launch the desktop application. Returns a process exit code."""
    config = AppConfig()
    config.ensure_dirs()
    logger = configure_logging(config.log_level, config.log_dir)
    install_crash_handler()
    logger.info("Starting MagnetFlux Studio")

    try:
        from magnetflux.ui.app import run_app
    except ImportError as exc:  # GUI extras not installed
        logger.error("GUI dependencies not available: %s", exc)
        print(
            "MagnetFlux Studio GUI requires the 'gui' extras.\n"
            "Install with:  pip install -e .[gui]",
            file=sys.stderr,
        )
        return 1

    return run_app(config)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
