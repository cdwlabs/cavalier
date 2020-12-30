import cavalier
import pytest
import tkinter


def test_basic():
    root = tkinter.Tk()
    root.withdraw()
    root.title("Cavalier")
    c = cavalier.Cavalier(parent=root)
