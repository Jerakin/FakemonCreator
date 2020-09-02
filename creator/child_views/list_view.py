from PyQt5 import QtWidgets, uic, QtGui, QtCore
import creator.utils.util as util


class ListView(QtWidgets.QWidget):
    def __init__(self, list_class):
        super(ListView, self).__init__()
        uic.loadUi(util.RESOURCE_UI / 'ListSelector.ui', self)  # Load the .ui file
        exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        exit_shortcut.activated.connect(self.close)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.finish_function = None
        # Skip the error entries
        for entry in list_class.list:
            if entry:
                self.listWidget.addItem(entry)

        self.pushButton.clicked.connect(self.open)
        self.listWidget.itemDoubleClicked.connect(self.open)

    def open(self):
        if self.finish_function:
            self.finish_function(self.listWidget.selectedItems()[0].text())
            self.close()

