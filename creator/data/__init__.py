from pathlib import Path
from PyQt5 import QtWidgets

from creator.data import move
from creator.data import pokemon
from creator.data import ability
from creator.data import container
from creator.data import metadata
from creator.data import item
from creator.utils import util
import logging as log


class Data:
    # Move this somewhere else later
    def __init__(self, window):
        self.window = window

        self._edited = False
        self.container = None
        self.move = None
        self.ability = None
        self.datamon = None
        self.metadata = None
        self.item = None

        self.package_index = util.get_package_index()

        self.new_move()
        self.new_ability()
        self.new_pokemon()
        self.new_metadata()
        self.new_item()

    def validate(self):
        if self.container:
            return self.container.validate()
        return []

    def new_container(self):
        self.container = container.Container()

    def new_move(self):
        self.move = move.Move()
        self.move.new()

    def new_ability(self):
        self.ability = ability.Ability()
        self.ability.new()

    def new_pokemon(self):
        self.datamon = pokemon.Pokemon()
        self.datamon.new()

    def new_metadata(self):
        self.metadata = metadata.Metadata()
        self.metadata.new()

    def new_item(self):
        self.item = item.Item()
        self.item.new()

    @property
    def edited(self):
        return self._edited or self.datamon.edited or self.ability.edited or self.move.edited or self.metadata.edited

    def load(self, path):
        path = Path(path)
        self.container = container.Container()
        self.container.load(path)
        self.metadata.edited = False
        self.datamon.edited = False
        self.ability.edited = False
        self.move.edited = False
        self.item.edited = False

    def save(self):
        log.info("Saving")
        metadata_edited = self.metadata.edited
        _edited = self._edited
        if not self.container:
            self.new_container()
            data = {"pokemon.json": {}, "evolve.json": {}, "pokedex_extra.json": {}, "moves.json": {},
                    "abilities.json": {}, "items.json": {}}
        elif self.container.is_empty:
            data = {"pokemon.json": {}, "evolve.json": {}, "pokedex_extra.json": {}, "moves.json": {},
                    "abilities.json": {}, "items.json": {}}
        else:
            data = self.container.data()

        if self.datamon.edited:
            if self.datamon.species in data["pokemon.json"]:
                button_reply = QtWidgets.QMessageBox.question(self.window, 'Overwrite',
                                                    "Overwrite existing Fakemon?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                    QtWidgets.QMessageBox.Cancel)
                if button_reply == QtWidgets.QMessageBox.Cancel:
                    return

            self.datamon.serialize()
            self.datamon.edited = False
            data["pokemon.json"][self.datamon.species] = self.datamon.data
            data["evolve.json"][self.datamon.species] = self.datamon.evolve
            data["pokedex_extra.json"][self.datamon.index] = self.datamon.extra

        if self.ability.edited:
            if self.ability.name in data["abilities.json"]:
                button_reply = QtWidgets.QMessageBox.question(self.window, 'Overwrite',
                                                    "Overwrite existing Ability?",
                                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                    QtWidgets.QMessageBox.Cancel)
                if button_reply == QtWidgets.QMessageBox.Cancel:
                    return
            self.ability.serialize()
            self.ability.edited = False
            data["abilities.json"][self.ability.name] = self.ability.data

        if self.move.edited:
            if self.move.name in data["moves.json"]:
                button_reply = QtWidgets.QMessageBox.question(self.window, 'Overwrite',
                                                    "Overwrite existing Move?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                    QtWidgets.QMessageBox.Cancel)
                if button_reply == QtWidgets.QMessageBox.Cancel:
                    return
            self.move.serialize()
            self.move.edited = False
            data["moves.json"][self.move.name] = self.move.data

        if self.item.edited:
            if self.item.name in data["items.json"]:
                button_reply = QtWidgets.QMessageBox.question(self.window, 'Overwrite',
                                                    "Overwrite existing Item?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                    QtWidgets.QMessageBox.Cancel)
                if button_reply == QtWidgets.QMessageBox.Cancel:
                    return
            self.item.serialize()
            self.item.edited = False
            data["items.json"][self.item.name] = self.item.data

        if self.metadata.edited:
            self.metadata.validate()
            self.container.add("index.json", self.metadata.data)
            self.metadata.edited = False

        self._edited = False
        self.container.add("data.json", data)
        res = self.container.save()
        if not res:
            self.metadata.edited = metadata_edited
            self._edited =_edited
            QtWidgets.QMessageBox.about(None, "Failed", "Saving failed because file is locked")