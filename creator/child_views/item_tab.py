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


class ItemTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(ItemTab, self).__init__()
        uic.loadUi(root / 'res/ui/ItemTab.ui', self)
        self.data = data
        self.item_list = util.JsonToList(root / "res/data/items.json")
        self.child = None

        self.list_items.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_items.customContextMenuRequested.connect(self.context_menu)
        self.list_items.itemDoubleClicked.connect(self.open_custom_item)

        self.item_name.textEdited.connect(lambda x: self.setattr(self.data.item, "name", x))
        self.item_entry.textChanged.connect(
            lambda: self.setattr(self.data.item, "description", self.item_entry.toPlainText()))

    def load_item_view(self):
        self.clear_item_view()
        self.item_name.setText(self.data.item.name)
        self.item_entry.blockSignals(True)
        self.item_entry.setText(self.data.item.description)
        self.item_entry.blockSignals(False)

    def clear_item_view(self):
        self.item_name.setText("")
        self.item_entry.blockSignals(True)
        self.item_entry.setText("")
        self.item_entry.blockSignals(False)

    def context_menu(self, pos):
        context = QtWidgets.QMenu()
        delete_action = context.addAction("delete")
        action = context.exec_(self.list_items.mapToGlobal(pos))
        if action == delete_action:
            self.delete_item(self.list_items.selectedItems()[0])

    def _open_item(self, _item):
        self.data.new_item()
        self.data.item.load(_item)
        self.load_item_view()
        self.child = None

    def open_item(self):
        if self.data.item.edited:
            response = self.save_and_continue()
            if response == QtWidgets.QMessageBox.Cancel:
                return
        print(self.child)
        if self.child:
            self.child.close()

        self.child = list_view.ListView(util.JsonToList(root / "res/data/items.json"))
        modern = qtmodern.windows.ModernWindow(self.child)
        self.child.finish_function = self._open_item
        modern.show()

    def open_custom_item(self, widget_item):
        name = widget_item.text()
        if self.data.item.edited:
            response = self.save_and_continue()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        self.data.new_item()
        self.data.item.custom(self.data.container.data(), name)
        self.load_item_view()

    def new_item(self):
        if self.data.item.edited:
            if not self.save_and_continue():
                return
        self.data.new_item()
        self.data.item.new()
        self.update_list_signal.emit()
        self.load_item_view()

    def delete_item(self, widget_item):
        item_name = widget_item.text()
        button_reply = QtWidgets.QMessageBox.question(None, 'Delete',
                                                      "Would you like to delete {}".format(item_name),
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)

        if button_reply == QtWidgets.QMessageBox.Yes:
            self.data.container.delete_entry("abilities.json", item_name)
            self.list_items.takeItem(self.list_items.currentRow())
            self.data._edited = True
            if item_name == self.data.item.name:
                self.data.item.new()
                self.load_item_view()
            self.update_list_signal.emit()
            log.info("Deleted {}".format(item_name))

    def update_custom_list(self):
        data = self.data.container.data() if self.data.container else None
        if not data:
            return
        item_data = data["items.json"]

        self.list_items.clear()

        for _item, _ in item_data.items():
            self.list_items.addItem(_item)
