"""PySide6 desktop GUI layer (optional; imported only when the GUI runs).

Importing this package requires the ``gui`` extras (PySide6, pyvista). The
entry point (:mod:`magnetflux.__main__`) imports :func:`magnetflux.ui.app.run_app`
lazily and degrades gracefully when those extras are absent.
"""
