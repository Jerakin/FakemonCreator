import sys
import json
from pathlib import Path
import logging as log

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt

from creator.data import fields
from creator.utils import util
from creator.child_views import shared
from creator.child_views import list_view

import qtmodern.windows
import qtmodern.styles

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)


class PokemonTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(PokemonTab, self).__init__()
        uic.loadUi(root / 'res/ui/PokemonTab.ui', self)
        self.data = data

        # Forward Declare
        self.child = None

        # List of all entries
        self.pkmn_list = util.JsonToList(root / "res/data/pokemon.json")
        self.move_list = util.JsonToList(root / "res/data/moves.json")
        self.ability_list = util.JsonToList(root / "res/data/abilities.json")

        self.tm_list = [""]
        move_machine_path = Path(root / "res/data/move_machines.json")
        with move_machine_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            for index, name in data.items():
                self.tm_list.append("{} - {}".format(index, name))

        context_menu = QtWidgets.QMenu("context")
        context_menu.addAction("Delete")

        self.sprite_image.setPixmap(QtGui.QPixmap(str(root / 'res/ui/default_sprite.png')))
        self.icon_image.setPixmap(QtGui.QPixmap(str(root / 'res/ui/default_icon.png')))

        # Restrict text inputs
        self.index_number.setValidator(QtGui.QIntValidator())
        self.armor_class.setValidator(QtGui.QIntValidator())
        self.hit_points.setValidator(QtGui.QIntValidator())
        self.level.setValidator(QtGui.QIntValidator())
        self.evolve_level_gain.setValidator(QtGui.QIntValidator())
        self.evolve_points_gain.setValidator(QtGui.QIntValidator())
        self.STR.setValidator(QtGui.QIntValidator())
        self.DEX.setValidator(QtGui.QIntValidator())
        self.CON.setValidator(QtGui.QIntValidator())
        self.INT.setValidator(QtGui.QIntValidator())
        self.WIS.setValidator(QtGui.QIntValidator())
        self.CHA.setValidator(QtGui.QIntValidator())
        self.darkvision.setValidator(QtGui.QIntValidator())
        self.tremorsense.setValidator(QtGui.QIntValidator())
        self.blindsight.setValidator(QtGui.QIntValidator())
        self.truesight.setValidator(QtGui.QIntValidator())
        self.walking.setValidator(QtGui.QIntValidator())
        self.climbing.setValidator(QtGui.QIntValidator())
        self.flying.setValidator(QtGui.QIntValidator())
        self.swimming.setValidator(QtGui.QIntValidator())
        self.weight.setValidator(QtGui.QDoubleValidator())
        self.pokemon_height.setValidator(QtGui.QDoubleValidator())
        self.total_stages.setValidator(QtGui.QIntValidator())
        self.current_stage.setValidator(QtGui.QIntValidator())

        # Add default items
        self.saving_throw1_pokemon.addItem("None")
        self.saving_throw2_pokemon.addItem("None")

        self.type1_pokemon.addItems(fields.Type)
        self.type2_pokemon.addItem("None")
        self.type2_pokemon.addItems(fields.Type)

        self.sr_pokemon.addItems(fields.SR)

        self.saving_throw1_pokemon.addItems(fields.Attributes)
        self.saving_throw2_pokemon.addItems(fields.Attributes)

        self.hit_dice.addItems(fields.Dice)

        self.add_skill.addItems(fields.SKILLS)

        self.add_level_2_moves.addItems(self.move_list.list)
        self.add_level_6_moves.addItems(self.move_list.list)
        self.add_starting_moves.addItems(self.move_list.list)
        self.add_level_10_moves.addItems(self.move_list.list)
        self.add_level_14_moves.addItems(self.move_list.list)
        self.add_level_18_moves.addItems(self.move_list.list)

        self.add_evolution.addItems(self.pkmn_list.list)
        self.add_ability.addItems(self.ability_list.list)
        self.hidden_ability.addItems(self.ability_list.list)
        self.add_tms.addItems(self.tm_list)

        # add interactions
        self.list_pokemon.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_pokemon.customContextMenuRequested.connect(self.context_menu)

        self.browse_icon.clicked.connect(self.add_icon)
        self.browse_sprite.clicked.connect(self.add_sprite)
        self.list_pokemon.itemDoubleClicked.connect(self.open_fakemon)

        # ComboBox Enter pressed
        self.add_tms.lineEdit().returnPressed.connect(lambda: self.set_item_list("moves_tm", self.moves_tm_list, self.add_tms, self.add_tms.currentText()))
        self.add_level_2_moves.lineEdit().returnPressed.connect(lambda: self.set_item_list("moves_level2", self.moves_2_list, self.add_level_2_moves, self.add_level_2_moves.currentText()))
        self.add_level_6_moves.lineEdit().returnPressed.connect(lambda: self.set_item_list("moves_level6", self.moves_6_list, self.add_level_6_moves, self.add_level_6_moves.currentText()))
        self.add_level_10_moves.lineEdit().returnPressed.connect(lambda: self.set_item_list("moves_level10", self.moves_10_list, self.add_level_10_moves, self.add_level_10_moves.currentText()))
        self.add_level_14_moves.lineEdit().returnPressed.connect(lambda: self.set_item_list("moves_level14", self.moves_14_list, self.add_level_14_moves, self.add_level_14_moves.currentText()))
        self.add_level_18_moves.lineEdit().returnPressed.connect(lambda: self.set_item_list("moves_level18", self.moves_18_list, self.add_level_18_moves, self.add_level_18_moves.currentText()))
        self.add_starting_moves.lineEdit().returnPressed.connect(lambda: self.set_item_list("moves_starting", self.moves_starting_list, self.add_starting_moves, self.add_starting_moves.currentText()))
        self.add_ability.lineEdit().returnPressed.connect(lambda: self.set_item_list("abilities", self.abilities_list, self.add_ability, self.add_ability.currentText()))
        self.add_evolution.lineEdit().returnPressed.connect(lambda: self.set_item_list("evolve_into", self.evolve_into_list, self.add_evolution, self.add_evolution.currentText()))
        self.add_skill.lineEdit().returnPressed.connect(lambda: self.set_item_list("skills", self.skills_list, self.add_skill, self.add_skill.currentText()))

        # Item selected with mouse
        self.add_tms.view().pressed.connect(lambda x: self.set_item_list("moves_tm", self.moves_tm_list, self.add_tms, self.add_tms.model().itemFromIndex(x).text()))
        self.add_level_2_moves.view().pressed.connect(lambda x: self.set_item_list("moves_level2", self.moves_2_list, self.add_level_2_moves, self.add_level_2_moves.model().itemFromIndex(x).text()))
        self.add_level_6_moves.view().pressed.connect(lambda x: self.set_item_list("moves_level6", self.moves_6_list, self.add_level_6_moves, self.add_level_6_moves.model().itemFromIndex(x).text()))
        self.add_level_10_moves.view().pressed.connect(lambda x: self.set_item_list("moves_level10", self.moves_10_list, self.add_level_10_moves, self.add_level_10_moves.model().itemFromIndex(x).text()))
        self.add_level_14_moves.view().pressed.connect(lambda x: self.set_item_list("moves_level14", self.moves_14_list, self.add_level_14_moves, self.add_level_14_moves.model().itemFromIndex(x).text()))
        self.add_level_18_moves.view().pressed.connect(lambda x: self.set_item_list("moves_level18", self.moves_18_list, self.add_level_18_moves, self.add_level_18_moves.model().itemFromIndex(x).text()))
        self.add_starting_moves.view().pressed.connect(lambda x: self.set_item_list("moves_starting", self.moves_starting_list, self.add_starting_moves, self.add_starting_moves.model().itemFromIndex(x).text()))
        self.add_ability.view().pressed.connect(lambda x: self.set_item_list("abilities", self.abilities_list, self.add_ability, self.add_ability.model().itemFromIndex(x).text()))
        self.add_evolution.view().pressed.connect(lambda x: self.set_item_list("evolve_into", self.evolve_into_list, self.add_evolution, self.add_evolution.model().itemFromIndex(x).text()))
        self.add_skill.view().pressed.connect(lambda x: self.set_item_list("skills", self.skills_list, self.add_skill, self.add_skill.model().itemFromIndex(x).text()))

        self.type1_pokemon.activated[str].connect(lambda x: self.setattr(self.data.datamon, "type1", x))
        self.type2_pokemon.activated[str].connect(lambda x: self.setattr(self.data.datamon, "type2", x))
        self.sr_pokemon.activated[str].connect(lambda x: self.setattr(self.data.datamon, "sr", x))
        self.saving_throw1_pokemon.activated[str].connect(lambda x: self.setattr(self.data.datamon, "saving_throw1", x))
        self.saving_throw2_pokemon.activated[str].connect(lambda x: self.setattr(self.data.datamon, "saving_throw2", x))
        self.hit_dice.activated[str].connect(lambda x: self.setattr(self.data.datamon,"hit_dice", x))
        self.hidden_ability.activated[str].connect(lambda x: self.setattr(self.data.datamon, "hidden_ability", x))

        self.species.textEdited.connect(lambda x: self.setattr(self.data.datamon, "species", x))
        self.hit_points.textEdited.connect(lambda x: self.setattr(self.data.datamon, "hit_points", x))
        self.armor_class.textEdited.connect(lambda x: self.setattr(self.data.datamon, "armor_class", x))
        self.level.textEdited.connect(lambda x: self.setattr(self.data.datamon, "level", x))
        self.index_number.textEdited.connect(lambda x: self.setattr(self.data.datamon, "index", x))
        self.walking.textEdited.connect(lambda x: self.setattr(self.data.datamon, "walking", x))
        self.climbing.textEdited.connect(lambda x: self.setattr(self.data.datamon, "climbing", x))
        self.flying.textEdited.connect(lambda x: self.setattr(self.data.datamon, "flying", x))
        self.swimming.textEdited.connect(lambda x: self.setattr(self.data.datamon, "swimming", x))
        self.darkvision.textEdited.connect(lambda x: self.setattr(self.data.datamon, "darkvision", x))
        self.tremorsense.textEdited.connect(lambda x: self.setattr(self.data.datamon, "tremorsense", x))
        self.blindsight.textChanged.connect(lambda x: self.setattr(self.data.datamon, "blindsight", x))
        self.truesight.textEdited.connect(lambda x: self.setattr(self.data.datamon, "truesight", x))
        self.STR.textEdited.connect(lambda x: self.setattr(self.data.datamon, "STR", x))
        self.DEX.textEdited.connect(lambda x: self.setattr(self.data.datamon, "DEX", x))
        self.CON.textEdited.connect(lambda x: self.setattr(self.data.datamon, "CON", x))
        self.INT.textEdited.connect(lambda x: self.setattr(self.data.datamon, "INT", x))
        self.WIS.textEdited.connect(lambda x: self.setattr(self.data.datamon, "WIS", x))
        self.CHA.textEdited.connect(lambda x: self.setattr(self.data.datamon, "CHA", x))
        self.pokedex_entry.textChanged.connect(lambda: self.setattr(self.data.datamon, "flavor", self.pokedex_entry.toPlainText()))
        self.weight.textEdited.connect(lambda x: self.setattr(self.data.datamon, "weight", x))
        self.pokemon_height.textEdited.connect(lambda x: self.setattr(self.data.datamon, "height", x))
        self.genus.textEdited.connect(lambda x: self.setattr(self.data.datamon, "genus", x))
        self.evolve_level_gain.textEdited.connect(lambda x: self.setattr(self.data.datamon, "evolve_level", x))
        self.evolve_points_gain.textEdited.connect(lambda x: self.setattr(self.data.datamon, "evolve_points", x))
        self.total_stages.textEdited.connect(lambda x: self.setattr(self.data.datamon, "evolve_total_stages", x))
        self.current_stage.textEdited.connect(lambda x: self.setattr(self.data.datamon, "evolve_current_stages", x))

        self.moves_2_list.itemDoubleClicked.connect(lambda x: self.remove_level_move(self.moves_2_list, "2", x))
        self.moves_6_list.itemDoubleClicked.connect(lambda x: self.remove_level_move(self.moves_6_list, "6", x))
        self.moves_10_list.itemDoubleClicked.connect(lambda x: self.remove_level_move(self.moves_10_list, "10", x))
        self.moves_14_list.itemDoubleClicked.connect(lambda x: self.remove_level_move(self.moves_14_list, "14", x))
        self.moves_18_list.itemDoubleClicked.connect(lambda x: self.remove_level_move(self.moves_18_list, "18", x))
        self.moves_tm_list.itemDoubleClicked.connect(lambda x: self.remove_move(self.moves_tm_list, "TM", int(x.text().split(" ")[0])))
        self.moves_starting_list.itemDoubleClicked.connect(lambda x: self.remove_move(self.moves_starting_list, "Starting Moves", x.text()))

        self.skills_list.itemDoubleClicked.connect(lambda x: self.remove_entry(self.skills_list, "Skill", x))
        self.abilities_list.itemDoubleClicked.connect(lambda x: self.remove_entry(self.abilities_list, "Abilities", x))
        self.evolve_into_list.itemDoubleClicked.connect(lambda x: self.remove_evolution(self.evolve_into_list, x))

    def context_menu(self, pos):
        context = QtWidgets.QMenu()
        remove_fakemon = context.addAction("delete")
        action = context.exec_(self.list_pokemon.mapToGlobal(pos))
        if action == remove_fakemon:
            self.delete_fakemon(self.list_pokemon.selectedItems()[0])

    def new_fakemon(self):
        if self.data.datamon.edited:
            if not self.save_and_continue():
                return

        self.data.new_pokemon()
        self.data.datamon.new()
        self.load_fakemon_view()

    def open_fakemon(self, widget_item):
        species = widget_item.text()
        if self.data.datamon.edited:
            response = self.save_and_continue()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        self.data.new_pokemon()
        self.data.datamon.fakemon(self.data.container.data(), species)
        self.load_fakemon_view()

    def delete_fakemon(self, widget_item):
        species = widget_item.text()
        button_reply = QtWidgets.QMessageBox.question(None, 'Delete', "Would you like to delete {}".format(species),
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)

        if button_reply == QtWidgets.QMessageBox.Yes:
            self.data.container.delete_entry("pokemon.json", species)
            self.data.container.delete_entry("evolve.json", species)

            self.list_pokemon.takeItem(self.list_pokemon.currentRow())
            self.data._edited = True
            if species == self.data.datamon.species:
                self.data.datamon.new()
                self.load_fakemon_view()
            log.info("Deleted {}".format(species))
            self.update_list_signal.emit()

    def _open_pokemon(self, species):
        log.info("Open {}".format(species))
        self.data.new_pokemon()
        self.data.datamon.load(species)
        self.load_fakemon_view()
        self.child = None

    def open_pokemon(self):
        if self.data.datamon.edited:
            response = self.save_and_continue()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        if self.child:
            self.child.close()

        self.child = list_view.ListView(util.JsonToList(root / "res/data/pokemon.json"))
        modern = qtmodern.windows.ModernWindow(self.child)
        self.child.finish_function = self._open_pokemon
        modern.show()

    def clear_fakemon_view(self):
        self.sprite_image.setPixmap(QtGui.QPixmap(str(root / 'res/ui/default_sprite.png')))
        self.icon_image.setPixmap(QtGui.QPixmap(str(root / 'res/ui/default_icon.png')))

        self.species.setText("")
        self.sr_pokemon.setCurrentText("")
        self.type1_pokemon.setCurrentText("Normal")
        self.type2_pokemon.setCurrentText("None")
        self.saving_throw1_pokemon.setCurrentText("None")
        self.saving_throw2_pokemon.setCurrentText("None")
        self.hidden_ability.setCurrentText("None")
        self.hit_dice.setCurrentText("6")

        self.moves_2_list.clear()
        self.moves_6_list.clear()
        self.moves_10_list.clear()
        self.moves_14_list.clear()
        self.moves_18_list.clear()
        self.moves_tm_list.clear()
        self.moves_starting_list.clear()
        self.skills_list.clear()
        self.abilities_list.clear()
        self.evolve_into_list.clear()

        self.armor_class.setText("")
        self.hit_points.setText("")
        self.level.setText("")
        self.index_number.setText("")

        self.darkvision.setText("")
        self.tremorsense.setText("")
        self.blindsight.setText("")
        self.truesight.setText("")

        self.evolve_level_gain.setText("")
        self.evolve_points_gain.setText("")

        self.walking.setText("")
        self.climbing.setText("")
        self.flying.setText("")
        self.swimming.setText("")

        self.pokedex_entry.blockSignals(True)
        self.pokedex_entry.setText("")
        self.pokedex_entry.blockSignals(False)
        self.weight.setText("")
        self.pokemon_height.setText("")
        self.genus.setText("")

        self.STR.setText("")
        self.DEX.setText("")
        self.CON.setText("")
        self.INT.setText("")
        self.WIS.setText("")
        self.CHA.setText("")

        self.total_stages.setText("1")
        self.current_stage.setText("1")

    def load_fakemon_view(self):
        self.clear_fakemon_view()
        if self.data.datamon.sprite:
            px = QtGui.QPixmap()
            px.loadFromData(bytearray(self.data.container.image(self.data.datamon.sprite)))
            self.sprite_image.setPixmap(px)
        if self.data.datamon.icon:
            px = QtGui.QPixmap()
            px.loadFromData(bytearray(self.data.container.image(self.data.datamon.sprite)))
            self.icon_image.setPixmap(px)

        self.species.setText(self.data.datamon.species)
        self.sr_pokemon.setCurrentText(self.data.datamon.sr)

        self.type1_pokemon.setCurrentText(self.data.datamon.type1)
        self.type2_pokemon.setCurrentText(self.data.datamon.type2)

        self.saving_throw1_pokemon.setCurrentText(self.data.datamon.saving_throw1)
        self.saving_throw2_pokemon.setCurrentText(self.data.datamon.saving_throw2)

        self.hidden_ability.setCurrentText(self.data.datamon.hidden_ability)

        self.armor_class.setText(self.data.datamon.armor_class)
        self.hit_dice.setCurrentText(self.data.datamon.hit_dice)
        self.hit_points.setText(self.data.datamon.hit_points)
        self.level.setText(self.data.datamon.level)
        self.index_number.setText(self.data.datamon.index)

        self.moves_2_list.addItems(self.data.datamon.moves_level2)
        self.moves_6_list.addItems(self.data.datamon.moves_level6)
        self.moves_10_list.addItems(self.data.datamon.moves_level10)
        self.moves_14_list.addItems(self.data.datamon.moves_level14)
        self.moves_18_list.addItems(self.data.datamon.moves_level18)

        move_machine_path = Path(root / "res/data/move_machines.json")
        with move_machine_path.open("r") as f:
            data = json.load(f)
            for index in self.data.datamon.moves_tm:
                name = data[index]
                self.moves_tm_list.addItem("{} - {}".format(index, name))

        self.moves_starting_list.addItems(self.data.datamon.moves_starting)

        self.skills_list.addItems(self.data.datamon.skills)
        self.abilities_list.addItems(self.data.datamon.abilities)

        self.darkvision.setText(self.data.datamon.darkvision)
        self.tremorsense.setText(self.data.datamon.tremorsense)
        self.blindsight.setText(self.data.datamon.blindsight)
        self.truesight.setText(self.data.datamon.truesight)

        self.evolve_into_list.addItems(self.data.datamon.evolve_into)
        self.evolve_level_gain.setText(self.data.datamon.evolve_level)
        self.evolve_points_gain.setText(self.data.datamon.evolve_points)

        self.walking.setText(self.data.datamon.walking)
        self.climbing.setText(self.data.datamon.climbing)
        self.flying.setText(self.data.datamon.flying)
        self.swimming.setText(self.data.datamon.swimming)

        self.pokedex_entry.blockSignals(True)
        self.pokedex_entry.setText(self.data.datamon.flavor)
        self.pokedex_entry.blockSignals(False)
        self.weight.setText(self.data.datamon.weight)
        self.pokemon_height.setText(self.data.datamon.height)
        self.genus.setText(self.data.datamon.genus)

        self.STR.setText(self.data.datamon.STR)
        self.DEX.setText(self.data.datamon.DEX)
        self.CON.setText(self.data.datamon.CON)
        self.INT.setText(self.data.datamon.INT)
        self.WIS.setText(self.data.datamon.WIS)
        self.CHA.setText(self.data.datamon.CHA)

        self.total_stages.setText(self.data.datamon.evolve_total_stages)
        self.current_stage.setText(self.data.datamon.evolve_current_stages)

    def remove_level_move(self, current_list, level, item):
        self.data.datamon.remove_level_move(level, item.text())
        current_list.takeItem(current_list.currentRow())
        self.attribute_changed_signal.emit()

    def remove_move(self, current_list, p, item_text):
        self.data.datamon.remove_move(p, item_text)
        current_list.takeItem(current_list.currentRow())
        self.attribute_changed_signal.emit()

    def remove_evolution(self, current_list, item):
        self.data.datamon.remove_evolution(item.text())
        current_list.takeItem(current_list.currentRow())
        self.attribute_changed_signal.emit()

    def remove_entry(self, current_list, entry, item):
        self.data.datamon.remove_entry(entry, item.text())
        current_list.takeItem(current_list.currentRow())
        self.attribute_changed_signal.emit()

    def set_item_list(self, value, to_list, dropdown, item):
        if item and item in [dropdown.itemText(i) for i in range(dropdown.count())]:
            for i in range(to_list.count()):
                if to_list.item(i).text() == item:
                    dropdown.setCurrentText("")
                    return
            self.setattr(self.data.datamon, value, item)
            to_list.addItem(item)
            dropdown.setCurrentText("")

    def _get_image(self, width, height):
        path = QtWidgets.QFileDialog.getOpenFileName(None, "Open Selected file", str(Path().home()), 'PNG(*.png)')[0]
        if path != '':
            if util.is_png(path):
                w, h = util.get_image_size(path)
                if w != width or h != height:
                    QtWidgets.QMessageBox.warning(None, "Invalid dimensions", "Image doesn't have the correct dimensions")
                else:
                    if not self.data.container:
                        button_reply = QtWidgets.QMessageBox.question(None, 'Save',
                                                                      "Changes needs to be saved before adding image",
                                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                                      QtWidgets.QMessageBox.Cancel)
                        if button_reply == QtWidgets.QMessageBox.Yes:
                            self.save(force=True)
                        else:
                            return False
                    return Path(path)
            else:
                QtWidgets.QMessageBox.warning(None, "Invalid format", "File isn't PGN", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
        return False

    def add_sprite(self):
        image = self._get_image(126, 126)
        if image:
            self.data.container.add(image)
            self.data.datamon.sprite = image.name
            self.sprite_image.setPixmap(QtGui.QPixmap(str(image)))

    def add_icon(self):
        image = self._get_image(30, 40)
        if image:
            self.data.container.add(image)
            self.data.datamon.icon = image.name
            self.icon_image.setPixmap(QtGui.QPixmap(str(image)))

    def update_custom_list(self):
        data = self.data.container.data() if self.data.container else None
        if not data:
            return
        fakemon_data = data["pokemon.json"]

        self.list_pokemon.clear()

        for species, _ in fakemon_data.items():
            self.list_pokemon.addItem(species)

    def reload_lists(self):
        data = self.data.container.data() if self.data.container else None
        if not data:
            return
        self.pkmn_list.extend(data["pokemon.json"])
        self.move_list.extend(data["moves.json"])
        self.ability_list.extend(data["abilities.json"])

        self.add_level_2_moves.clear()
        self.add_level_6_moves.clear()
        self.add_starting_moves.clear()
        self.add_level_10_moves.clear()
        self.add_level_14_moves.clear()
        self.add_level_18_moves.clear()
        self.add_evolution.clear()
        self.add_ability.clear()
        self.hidden_ability.clear()

        self.add_level_2_moves.addItems(self.move_list.list)
        self.add_level_6_moves.addItems(self.move_list.list)
        self.add_starting_moves.addItems(self.move_list.list)
        self.add_level_10_moves.addItems(self.move_list.list)
        self.add_level_14_moves.addItems(self.move_list.list)
        self.add_level_18_moves.addItems(self.move_list.list)
        self.add_evolution.addItems(self.pkmn_list.list)
        self.add_ability.addItems(self.ability_list.list)
        self.hidden_ability.addItems(self.ability_list.list)

