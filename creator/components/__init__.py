from PyQt5 import QtWidgets, QtCore


class ExtendedComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)
        self.active = False

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setEditable(True)
        self.view().setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setStyleSheet("combobox-popup: 0;")
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        # add a filter model to filter matching items
        self.pFilterModel = QtCore.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QtWidgets.QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

        self.installEventFilter(self)

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

    def showPopup(self):
        self.active = True
        super(ExtendedComboBox, self).showPopup()
        
    def hidePopup(self):
        self.active = False
        super(ExtendedComboBox, self).hidePopup()

    def eventFilter(self, obj, event):
        if self.active:
            return super(ExtendedComboBox, self).eventFilter(obj, event)
        return False