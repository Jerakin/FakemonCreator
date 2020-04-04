import sys
from pathlib import Path

from PyQt5 import QtWidgets, uic

from creator.utils import util
from creator.child_views import shared
from creator.child_views import list_view

import qtmodern.windows
import qtmodern.styles

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)


class MetaDataTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(MetaDataTab, self).__init__()
        uic.loadUi(root / 'res/ui/SettingsTab.ui', self)
        self.data = data
        self.child = None

        self.update_existing.clicked.connect(self.update_package)

        self.package_description.textChanged.connect(
            lambda: self.setattr(self.data.metadata, "description", self.package_description.toPlainText()))
        self.package_author.textEdited.connect(lambda x: self.setattr(self.data.metadata, "author", x))
        self.package_name.textEdited.connect(lambda x: self.setattr(self.data.metadata, "name", x))

    def reload(self):
        self.data.metadata.load(self.data.container.index())
        self.package_description.blockSignals(True)
        self.package_description.setText(self.data.metadata.description)
        self.package_description.blockSignals(False)
        self.package_author.setText(self.data.metadata.author)
        self.package_name.setText(self.data.metadata.name)
        self.package_version.setText(self.data.metadata.version)

    def _update_package(self, name):
        self.data.package_index = util.get_package_index()
        for entry in self.data.package_index:
            if entry["name"] == name:
                self.package_name.setText(entry["name"])
                self.package_version.setText(
                    "{} -> {}".format(self.data.metadata.version, entry["version"] + 1))

                self.data.metadata.version = entry["version"] + 1
                break

    def update_package(self):
        self.data.package_index = util.get_package_index()
        if self.data.package_index is None:
            return
        _list = [entry["name"] for entry in self.data.package_index]
        list_class = util.SimpleList(_list)

        self.child = list_view.ListView(list_class)
        self.modern = qtmodern.windows.ModernWindow(self.child)
        self.child.finish_function = self._update_package
        self.modern.show()

    def refresh(self):
        self.data.package_index = util.get_package_index()
