import os
import pytest

tk = pytest.importorskip("tkinter")

from roman.gui import RomanApp


def _has_display():
    if os.name == "nt":
        return True
    return bool(os.environ.get("DISPLAY")) or os.uname().sysname == "Darwin"


pytestmark = pytest.mark.skipif(not _has_display(), reason="no display available")


def test_int_to_roman_updates_field():
    root = tk.Tk()
    try:
        app = RomanApp(root)
        app.int_var.set("4")
        root.update()
        assert app.roman_var.get() == "IV"
    finally:
        root.destroy()


def test_roman_to_int_updates_field():
    root = tk.Tk()
    try:
        app = RomanApp(root)
        app.roman_var.set("IX")
        root.update()
        assert app.int_var.get() == "9"
    finally:
        root.destroy()
