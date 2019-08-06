import sys
from pathlib import Path
import logging as log

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

from creator.utils import util
from creator.child_views import shared
from creator.child_views import list_view

import qtmodern.windows
import qtmodern.styles

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)


class AbilityTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(AbilityTab, self).__init__()
        uic.loadUi(root / 'res/ui/AbilityTab.ui', self)
        self.data = data
        self.ability_list = util.JsonToList(root / "res/data/abilities.json")
        self.child = None

        self.list_abilities.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_abilities.customContextMenuRequested.connect(self.context_menu)
        self.list_abilities.itemDoubleClicked.connect(self.open_custom_ability)

        self.ability_name.textEdited.connect(lambda x: self.setattr(self.data.ability, "name", x))
        self.ability_entry.textChanged.connect(
            lambda: self.setattr(self.data.ability, "description", self.ability_entry.toPlainText()))

    def load_ability_view(self):
        self.clear_ability_view()
        self.ability_name.setText(self.data.ability.name)
        self.ability_entry.blockSignals(True)
        self.ability_entry.setText(self.data.ability.description)
        self.ability_entry.blockSignals(False)

    def clear_ability_view(self):
        self.ability_name.setText("")
        self.ability_entry.blockSignals(True)
        self.ability_entry.setText("")
        self.ability_entry.blockSignals(False)

    def context_menu(self, pos):
        context = QtWidgets.QMenu()
        delete_action = context.addAction("delete")
        action = context.exec_(self.list_abilities.mapToGlobal(pos))
        if action == delete_action:
            self.delete_ability(self.list_abilities.selectedItems()[0])

    def _open_ability(self, _ability):
        self.data.new_ability()
        self.data.ability.load(_ability)
        self.load_ability_view()

    def open_ability(self):
        if self.data.ability.edited:
            response = self.save_and_continue()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        self.child = list_view.ListView(util.JsonToList(root / "res/data/abilities.json"))
        modern = qtmodern.windows.ModernWindow(self.child)
        self.child.finish_function = self._open_ability
        modern.show()

    def open_custom_ability(self, widget_item):
        name = widget_item.text()
        if self.data.ability.edited:
            response = self.save_and_continue()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        self.data.new_ability()
        self.data.ability.custom(self.container.data(), name)
        self.load_ability_view()

    def new_ability(self):
        if self.data.ability.edited:
            if not self.save_and_continue():
                return
        self.data.new_ability()
        self.data.ability.new()
        self.tabWidget.setCurrentIndex(2)
        self.update_list_signal.emit()
        self.load_ability_view()

    def delete_ability(self, widget_item):
        ability_name = widget_item.text()
        button_reply = QtWidgets.QMessageBox.question(None, 'Delete',
                                                      "Would you like to delete {}".format(ability_name),
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)

        if button_reply == QtWidgets.QMessageBox.Yes:
            self.container.delete_entry("moves.json", ability_name)
            self.list_abilities.takeItem(self.list_abilities.currentRow())
            self.data._edited = True
            if ability_name == self.data.ability.name:
                self.data.ability.new()
                self.load_ability_view()
            self.update_list_signal.emit()
            log.info("Deleted {}".format(ability_name))

    def update_custom_list(self):
        data = self.data.container.data()
        ability_data = data["abilities.json"]

        self.list_abilities.clear()

        for _ability, _ in ability_data.items():
            self.list_abilities.addItem(_ability)
