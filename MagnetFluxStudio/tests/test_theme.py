"""Tests for theme selection (pure strings, no Qt import)."""

import pytest

from magnetflux.ui.theme import ACCENT, Theme, stylesheet


def test_stylesheet_light_and_dark_differ():
    light = stylesheet(Theme.LIGHT)
    dark = stylesheet(Theme.DARK)
    assert light != dark
    assert ACCENT in light and ACCENT in dark
    assert "background" in light.lower()


def test_stylesheet_accepts_string_value():
    assert stylesheet("dark") == stylesheet(Theme.DARK)
    assert stylesheet("light") == stylesheet(Theme.LIGHT)


def test_invalid_theme_raises():
    with pytest.raises(ValueError):
        stylesheet("neon")
