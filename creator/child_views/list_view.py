import sys
from pathlib import Path
from PyQt5 import QtWidgets, uic, QtGui

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)

class ListView(QtWidgets.QWidget):
    def __init__(self, list_class):
        super(ListView, self).__init__()
        uic.loadUi(root / 'res/ui/ListSelector.ui', self)  # Load the .ui file
        exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        exit_shortcut.activated.connect(self.close)

        self.finish_function = None

        # Skip the error entries
        for entry in list_class.list:
            self.listWidget.addItem(entry)

        self.pushButton.clicked.connect(self.open)
        self.listWidget.itemDoubleClicked.connect(self.open)

    def open(self):
        if self.finish_function:
            self.finish_function(self.listWidget.selectedItems()[0].text())
            self.close()

