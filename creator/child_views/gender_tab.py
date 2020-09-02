import logging as log

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

from creator.utils import util
from creator.child_views import shared
from creator.child_views import list_view

GENDERLESS = 0
MALE = 1
FEMALE = 2


class GenderTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(GenderTab, self).__init__()
        uic.loadUi(util.RESOURCE_UI / 'GenderTab.ui', self)
        self.data = data
        self.extended = False
        self.list_gender.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_gender.customContextMenuRequested.connect(self.context_menu)

        self.pkmn_list = util.pokemon_list()

        self.speciesDropdown.addItems(self.pkmn_list)
        self.speciesDropdown.activated.connect(self.extend_dropdown)
        self.add_button.clicked.connect(self.add)

    def extend_dropdown(self):
        data = self.data.container.data() if self.data and self.data.container else None
        if data and not self.extended:
            self.pkmn_list.extend(data["pokemon.json"])
            self.extended = True
            self.speciesDropdown.clear()
            self.speciesDropdown.addItems(self.pkmn_list)

    def add(self):
        species = self.speciesDropdown.currentText()
        gender = GENDERLESS if self.radioNoGender.isChecked() else None
        gender = MALE if self.radioMale.isChecked() else gender
        gender = FEMALE if self.radioFemale.isChecked() else gender
        self.setattr(self.data.gender, "species", species)
        self.setattr(self.data.gender, "gender", gender)

    def context_menu(self, pos):
        context = QtWidgets.QMenu()
        delete_action = context.addAction("delete")
        action = context.exec_(self.list_gender.mapToGlobal(pos))
        if action == delete_action:
            self.delete_gender(self.list_gender.selectedItems()[0])

    def delete_gender(self, widget_item):
        species_name = widget_item.text()
        button_reply = QtWidgets.QMessageBox.question(None, 'Delete',
                                                      "Would you like to remove {}".format(species_name),
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)

        if button_reply == QtWidgets.QMessageBox.Yes:
            self.data.container.delete_entry("gender.json", species_name)
            self.list_gender.takeItem(self.list_gender.currentRow())
            self.data._edited = True
            if species_name == self.data.gender.species:
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
