import sys
from pathlib import Path

from PyQt5 import QtWidgets, uic, QtGui, QtCore

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)


class HPHelp(QtWidgets.QWidget):
    def __init__(self, parent):
        super(HPHelp, self).__init__()
        uic.loadUi(root / 'res/ui/CalculateHP.ui', self)
        exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        exit_shortcut.activated.connect(self.close)
        self.parent = parent

    def closeEvent(self, event):
        self.parent.hp_help_window = None
        event.accept()


class Tab:
    attribute_changed_signal = QtCore.pyqtSignal()
    update_list_signal = QtCore.pyqtSignal()
    save_project_signal = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def setattr(self, obj, name, value):
        setattr(obj, name, value)
        self.attribute_changed_signal.emit()

    def save_and_continue(self):
        button_reply = QtWidgets.QMessageBox.question(None, 'Save', "Save changes before continuing?",
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No |
                                                      QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)
        if button_reply == QtWidgets.QMessageBox.Yes:
            self.save_project_signal.emit()

        return button_reply