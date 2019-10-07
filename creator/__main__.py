#!/usr/bin/env python
import sys
from creator.child_views import exception
sys.excepthook = exception.tkinter_exception

from creator import mainwindow

if __name__ == "__main__":
    mainwindow.main()
