from PyQt5 import QtWidgets, uic
import qtmodern.windows
import qtmodern.styles

from creator.utils import util
from creator.child_views import shared
from creator.child_views import list_view


class MetaDataTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(MetaDataTab, self).__init__()
        uic.loadUi(util.RESOURCE_UI / 'SettingsTab.ui', self)
        self.data = data
        self.child = None

        self.update_existing.clicked.connect(self.update_package)

        self.package_description.textChanged.connect(self.description_changed)
        self.package_author.textEdited.connect(lambda x: self.setattr(self.data.metadata, "author", x))
        self.package_name.textEdited.connect(lambda x: self.setattr(self.data.metadata, "name", x))
        self.package_author.setMaxLength(20)
        self.package_name.setMaxLength(16)

    def description_changed(self):
        max_input = 120
        text = self.package_description.toPlainText()
        if len(text) > max_input:
            text = text[:max_input]
            self.package_description.setText(text)

            cursor = self.package_description.textCursor()
            cursor.setPosition(max_input)
            self.package_description.setTextCursor(cursor)

        self.setattr(self.data.metadata, "description", text)

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

        self.child = list_view.ListView([entry["name"] for entry in self.data.package_index])
        self.modern = qtmodern.windows.ModernWindow(self.child)
        self.child.finish_function = self._update_package
        self.modern.show()

    def refresh(self):
        self.data.package_index = util.get_package_index()
