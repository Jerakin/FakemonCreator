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

GENDERLESS = 0
MALE = 1
FEMALE = 2


class GenderTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(GenderTab, self).__init__()
        uic.loadUi(root / 'res/ui/GenderTab.ui', self)
        self.data = data

        self.list_gender.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_gender.customContextMenuRequested.connect(self.context_menu)
        # self.list_gender.itemDoubleClicked.connect(self.open_custom_ability)

        self.pkmn_list = util.JsonToList(root / "res/data/pokemon.json")
        data = self.data.container.data() if self.data and self.data.container else None
        if data:
            self.pkmn_list.extend(data["pokemon.json"])
        self.speciesDropdown.addItems(self.pkmn_list.list)

        self.add_button.clicked.connect(self.add)

    def add(self):
        species = self.speciesDropdown.currentText()
        gender = GENDERLESS if self.radioNoGender.isChecked() else None
        gender = MALE if self.radioMale.isChecked() else gender
        gender = FEMALE if self.radioFemale.isChecked() else gender
        self.setattr(self.data.gender, "species", species)
        self.setattr(self.data.gender, "gender", gender)

    def load_gender_view(self):
        pass

    def clear_genderview(self):
        pass

    def context_menu(self, pos):
        context = QtWidgets.QMenu()
        delete_action = context.addAction("delete")
        action = context.exec_(self.list_gender.mapToGlobal(pos))
        if action == delete_action:
            self.delete_ability(self.list_gender.selectedItems()[0])

    def _open_ability(self, _ability):
        pass

    def open_ability(self):
        pass

    def open_custom_ability(self, widget_item):
        pass

    def new_ability(self):
        pass

    def delete_ability(self, widget_item):
        species_name = widget_item.text()
        button_reply = QtWidgets.QMessageBox.question(None, 'Delete',
                                                      "Would you like to remove {}".format(species_name),
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)

        if button_reply == QtWidgets.QMessageBox.Yes:
            self.data.container.delete_entry("gender.json", species_name)
            self.list_gender.takeItem(self.list_gender.currentRow())
            self.data._edited = True
            if species_name == self.data.gender.name:
                self.data.gender.new()
                self.load_gender_view()
            self.update_list_signal.emit()
            log.info("Deleted {}".format(species_name))

    def update_custom_list(self):
        data = self.data.container.data() if self.data.container else None
        if not data or "gender.json" not in data:
            return
        gender_data = data["gender.json"]

        self.list_gender.clear()

        for _species, _ in gender_data.items():
            self.list_gender.addItem(_species)
