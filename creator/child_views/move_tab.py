import sys
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


class MoveTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(MoveTab, self).__init__()
        uic.loadUi(root / 'res/ui/MoveTab.ui', self)
        self.data = data
        self.move_list = util.JsonToList(root / "res/data/moves.json")
        self.child = None

        self.move_pp.setValidator(QtGui.QIntValidator())
        self.die_at_1.setValidator(QtGui.QIntValidator())
        self.die_at_5.setValidator(QtGui.QIntValidator())
        self.die_at_10.setValidator(QtGui.QIntValidator())
        self.die_at_17.setValidator(QtGui.QIntValidator())

        self.move_power1.addItem("None")
        self.move_power2.addItem("None")
        self.move_power3.addItem("None")
        self.move_type.addItem("None")
        self.move_save.addItem("None")

        self.die_type_1.addItem("")
        self.die_type_5.addItem("")
        self.die_type_10.addItem("")
        self.die_type_17.addItem("")

        self.move_save.addItems(fields.Attributes)
        self.move_power1.addItems(fields.Attributes)
        self.move_power2.addItems(fields.Attributes)
        self.move_power3.addItems(fields.Attributes)

        self.move_type.addItems(fields.Type)

        self.die_type_1.addItems(fields.Dice)
        self.die_type_5.addItems(fields.Dice)
        self.die_type_10.addItems(fields.Dice)
        self.die_type_17.addItems(fields.Dice)

        self.list_moves.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_moves.customContextMenuRequested.connect(self.move_context_menu)
        self.delete_damage.clicked.connect(self.clear_damage)
        self.list_moves.itemDoubleClicked.connect(self.open_custom_move)

        self.move_name.textEdited.connect(lambda x: self.setattr(self.data.move, "name", x))
        self.move_entry.textChanged.connect(
            lambda: self.setattr(self.data.move, "description", self.move_entry.toPlainText()))
        self.move_duration.textEdited.connect(lambda x: self.setattr(self.data.move, "duration", x))
        self.move_duration.textEdited.connect(lambda x: self.setattr(self.data.move, "casting_time", x))
        self.move_range.textEdited.connect(lambda x: self.setattr(self.data.move, "range", x))
        self.move_pp.textEdited.connect(lambda x: self.setattr(self.data.move, "PP", x))

        self.die_at_1.textEdited.connect(lambda x: self.data.move.set_damage_die_property("amount", "1", x))
        self.die_at_5.textEdited.connect(lambda x: self.data.move.set_damage_die_property("amount", "5", x))
        self.die_at_10.textEdited.connect(lambda x: self.data.move.set_damage_die_property("amount", "10", x))
        self.die_at_17.textEdited.connect(lambda x: self.data.move.set_damage_die_property("amount", "17", x))
        self.times_1.textEdited.connect(lambda x: self.data.move.set_damage_die_property("times", "1", x))
        self.times_5.textEdited.connect(lambda x: self.data.move.set_damage_die_property("times", "5", x))
        self.times_10.textEdited.connect(lambda x: self.data.move.set_damage_die_property("times", "10", x))
        self.times_17.textEdited.connect(lambda x: self.data.move.set_damage_die_property("times", "17", x))

        self.die_type_1.activated[str].connect(lambda x: self.data.move.set_damage_die_property("dice_max", "1", x))
        self.die_type_5.activated[str].connect(lambda x: self.data.move.set_damage_die_property("dice_max", "5", x))
        self.die_type_10.activated[str].connect(lambda x: self.data.move.set_damage_die_property("dice_max", "10", x))
        self.die_type_17.activated[str].connect(lambda x: self.data.move.set_damage_die_property("dice_max", "17", x))

        self.move_save.activated[str].connect(lambda x: self.setattr(self.data.move, "save", x))
        self.move_power1.activated[str].connect(lambda x: self.setattr(self.data.move, "move_power1", x))
        self.move_power2.activated[str].connect(lambda x: self.setattr(self.data.move, "move_power2", x))
        self.move_power3.activated[str].connect(lambda x: self.setattr(self.data.move, "move_power3", x))
        self.move_type.activated[str].connect(lambda x: self.setattr(self.data.move, "type", x))

        self.move_1.stateChanged.connect(lambda x: self.data.move.set_damage_die_property("move", "1", x))
        self.move_5.stateChanged.connect(lambda x: self.data.move.set_damage_die_property("move", "5", x))
        self.move_10.stateChanged.connect(lambda x: self.data.move.set_damage_die_property("move", "10", x))
        self.move_17.stateChanged.connect(lambda x: self.data.move.set_damage_die_property("move", "17", x))
        self.level_1.stateChanged.connect(lambda x: self.data.move.set_damage_die_property("level", "1", x))
        self.level_5.stateChanged.connect(lambda x: self.data.move.set_damage_die_property("level", "5", x))
        self.level_10.stateChanged.connect(lambda x: self.data.move.set_damage_die_property("level", "10", x))
        self.level_17.stateChanged.connect(lambda x: self.data.move.set_damage_die_property("level", "17", x))

    def new_move(self):
        if self.data.move.edited:
            if not self.save_and_continue():
                return

        self.data.new_move()
        self.load_move_view()

    def delete_move(self, widget_item):
        move_name = widget_item.text()
        button_reply = QtWidgets.QMessageBox.question(None, 'Delete', "Would you like to delete {}".format(move_name),
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)

        if button_reply == QtWidgets.QMessageBox.Yes:
            self.data.container.delete_entry("moves.json", move_name)
            self.list_moves.takeItem(self.list_moves.currentRow())
            self.data._edited = True
            if move_name == self.data.move.name:
                self.data.move.new()
                self.load_move_view()

            self.update_list_signal.emit()
            log.info("Deleted {}".format(move_name))

    def _open_move(self, _move):
        self.data.new_move()
        self.data.move.load(_move)
        self.load_move_view()
        self.child = None

    def open_move(self):
        if self.data.move.edited:
            response = self.save_and_continue()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        if self.child:
            self.child.close()

        self.child = list_view.ListView(util.JsonToList(root / "res/data/moves.json"))
        self.modern = qtmodern.windows.ModernWindow(self.child)
        self.child.finish_function = self._open_move
        self.modern.show()

    def open_custom_move(self, widget_item):
        name = widget_item.text()
        if self.data.move.edited:
            response = self.save_and_continue()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        self.data.new_move()
        self.data.move.custom(self.data.container.data(), name)
        self.load_move_view()

    def move_context_menu(self, pos):
        context = QtWidgets.QMenu()
        remove_fakemon = context.addAction("delete")
        action = context.exec_(self.list_moves.mapToGlobal(pos))
        if action == remove_fakemon:
            self.delete_move(self.list_moves.selectedItems()[0])

    def clear_damage(self):
        self.data.move.delete_damage()
        self.die_at_1.setText("")
        self.die_at_5.setText("")
        self.die_at_10.setText("")
        self.die_at_17.setText("")

        self.die_type_1.setCurrentText("")
        self.die_type_5.setCurrentText("")
        self.die_type_10.setCurrentText("")
        self.die_type_17.setCurrentText("")

        self.move_1.setChecked(False)
        self.move_5.setChecked(False)
        self.move_10.setChecked(False)
        self.move_17.setChecked(False)
        self.level_1.setChecked(False)
        self.level_5.setChecked(False)
        self.level_10.setChecked(False)
        self.level_17.setChecked(False)

    def load_move_view(self):
        self.clear_move_view()

        self.move_name.setText(self.data.move.name)
        self.move_entry.blockSignals(True)
        self.move_entry.setText(self.data.move.description)
        self.move_entry.blockSignals(False)
        self.move_duration.setText(self.data.move.duration)
        self.move_casting_time.setText(self.data.move.casting_time)
        self.move_range.setText(self.data.move.range)
        self.move_pp.setText(self.data.move.PP)
        self.die_at_1.setText(self.data.move.get_damage_die_property("amount", "1"))
        self.die_at_5.setText(self.data.move.get_damage_die_property("amount", "5"))
        self.die_at_10.setText(self.data.move.get_damage_die_property("amount", "10"))
        self.die_at_17.setText(self.data.move.get_damage_die_property("amount", "17"))
        self.times_1.setText(self.data.move.get_damage_die_property("times", "1"))
        self.times_5.setText(self.data.move.get_damage_die_property("times", "5"))
        self.times_10.setText(self.data.move.get_damage_die_property("times", "10"))
        self.times_17.setText(self.data.move.get_damage_die_property("times", "17"))

        self.die_type_1.setCurrentText(self.data.move.get_damage_die_property("dice_max", "1"))
        self.die_type_5.setCurrentText(self.data.move.get_damage_die_property("dice_max", "5"))
        self.die_type_10.setCurrentText(self.data.move.get_damage_die_property("dice_max", "10"))
        self.die_type_17.setCurrentText(self.data.move.get_damage_die_property("dice_max", "17"))

        self.move_save.setCurrentText(self.data.move.save)
        self.move_power1.setCurrentText(self.data.move.move_power1)
        self.move_power2.setCurrentText(self.data.move.move_power2)

        self.move_type.setCurrentText(self.data.move.type)

        self.move_1.setChecked(bool(self.data.move.get_damage_die_property("move", "1")))
        self.move_5.setChecked(bool(self.data.move.get_damage_die_property("move", "5")))
        self.move_10.setChecked(bool(self.data.move.get_damage_die_property("move", "10")))
        self.move_17.setChecked(bool(self.data.move.get_damage_die_property("move", "17")))
        self.level_1.setChecked(bool(self.data.move.get_damage_die_property("level", "1")))
        self.level_5.setChecked(bool(self.data.move.get_damage_die_property("level", "5")))
        self.level_10.setChecked(bool(self.data.move.get_damage_die_property("level", "10")))
        self.level_17.setChecked(bool(self.data.move.get_damage_die_property("level", "17")))

    def clear_move_view(self):
        self.move_name.setText("")
        self.move_entry.blockSignals(True)
        self.move_entry.setText("")
        self.move_entry.blockSignals(False)
        self.move_duration.setText("")
        self.move_casting_time.setText("")
        self.move_range.setText("")
        self.move_pp.setText("")
        self.die_at_1.setText("")
        self.die_at_5.setText("")
        self.die_at_10.setText("")
        self.die_at_17.setText("")
        self.times_1.setText("")
        self.times_5.setText("")
        self.times_10.setText("")
        self.times_17.setText("")

        self.die_type_1.setCurrentText("")
        self.die_type_5.setCurrentText("")
        self.die_type_10.setCurrentText("")
        self.die_type_17.setCurrentText("")

        self.move_save.setCurrentText("None")
        self.move_power1.setCurrentText("None")
        self.move_power2.setCurrentText("None")

        self.move_type.setCurrentText("None")

        self.move_1.setChecked(False)
        self.move_5.setChecked(False)
        self.move_10.setChecked(False)
        self.move_17.setChecked(False)
        self.level_1.setChecked(False)
        self.level_5.setChecked(False)
        self.level_10.setChecked(False)
        self.level_17.setChecked(False)

    def update_custom_list(self):
        data = self.data.container.data() if self.data.container else None
        if not data:
            return
        moves_data = data["moves.json"]

        self.list_moves.clear()

        for _move, _ in moves_data.items():
            self.list_moves.addItem(_move)

