import logging as log
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
from pathlib import Path

import qtmodern.windows
import qtmodern.styles

from creator.data import Data
from creator.utils import util
from creator.child_views import move_tab
from creator.child_views import ability_tab
from creator.child_views import pokemon_tab
from creator.child_views import metadata_tab
from creator.child_views import gender_tab
from creator.child_views import item_tab
from creator.child_views import stats_calculator
from creator.child_views import shared
from creator.child_views import exception

from zipfile import BadZipFile
from creator import __version__ as version


class ScrollMessageBox(QtWidgets.QMessageBox):
    def __init__(self, l, *args, **kwargs):
        super(ScrollMessageBox, self).__init__(*args, **kwargs)
        self.setMinimumSize(800, 400)
        scroll = QtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content = QtWidgets.QWidget()
        scroll.setWidget(self.content)
        lay = QtWidgets.QVBoxLayout(self.content)
        for item in l:
            lay.addWidget(QtWidgets.QLabel(item, self))
        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setStyleSheet("QScrollArea{min-width:800 px; min-height: 400px}")


class MainWindow(QtWidgets.QMainWindow):
    ModernWindow = None

    def __init__(self):
        super(MainWindow, self).__init__()
        sys.excepthook = self.handle_exception
        uic.loadUi(util.RESOURCE_UI / 'FakemonCreator.ui', self)
        exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        exit_shortcut.activated.connect(self.close)
        debug_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("."), self)
        debug_shortcut.activated.connect(self.update_tab_names)
        self.settings = QtCore.QSettings("Pokedex5E", "FakemonCreator")
        self.setGeometry(0, 0, 1100, 800)
        self.data = Data(self)
        self.crashed = False
        self.started = False
        self.hp_help_window = None
        self.pokemon_tab = None
        self.move_tab = None
        self.ability_tab = None
        self.metadata_tab = None
        self.item_tab = None
        self.gender_tab = None
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.removeTab(5)

        self.setWindowTitle("untitled | Fakemon Creator")
        self.menubar.setNativeMenuBar(False)

        # Menu
        self.actionSave.triggered.connect(self.save)
        self.actionSave_As.triggered.connect(self.save_as)

        self.actionOpen.triggered.connect(self.open_project)

        self.actionOpen_Standard_Pokemon.triggered.connect(self.open_pokemon)
        self.actionNew_Pokemon.triggered.connect(self.new_fakemon)

        self.actionOpen_Ability.triggered.connect(self.open_ability)
        self.actionNew_Ability.triggered.connect(self.new_ability)

        self.actionOpen_Move.triggered.connect(self.open_move)
        self.actionNew_Move.triggered.connect(self.new_move)

        self.actionOpen_Item.triggered.connect(self.open_item)
        self.actionNew_Item.triggered.connect(self.new_item)

        self.actionExit.triggered.connect(self.close)
        self.actionAbout_Hp_Calculation.triggered.connect(self.hp_help)
        self.actionRestore_window_size.triggered.connect(self.restore_size)
        self.actionDark_Theme.triggered.connect(self.dark_theme)
        self.actionLight_Theme.triggered.connect(self.light_theme)

        self.actionStat_Calculator.triggered.connect(self.open_stat_calculator)

        self.actionValidate.triggered.connect(self.validate)
        self.statusBar().addPermanentWidget(QtWidgets.QLabel("v{}".format(version)))

    def setWindowTitle(self, p_str):
        if self.ModernWindow:
            self.ModernWindow.setWindowTitle(p_str)
        else:
            super(MainWindow, self).setWindowTitle(p_str)

    def set_theme(self, theme):
        # 0=Dark, 1=Light
        if theme == 0:
            qtmodern.styles.dark(QtWidgets.QApplication.instance())
        elif theme == 1:
            qtmodern.styles.light(QtWidgets.QApplication.instance())

        self.settings.setValue("activeTheme", theme)
        self.actionLight_Theme.setChecked(theme == 1)
        self.actionDark_Theme.setChecked(theme == 0)

    def light_theme(self):
        self.set_theme(1)

    def dark_theme(self):
        self.set_theme(0)

    def restore_size(self):
        if self.ModernWindow:
            size = self.centralWidget().minimumSizeHint()
            self.ModernWindow.setGeometry(0, 0, max(1100, size.width()), max(800, size.height()))

    def start(self):
        self.started = True
        # Tabs
        self.pokemon_tab = pokemon_tab.PokemonTab(self.data)
        self.move_tab = move_tab.MoveTab(self.data)
        self.ability_tab = ability_tab.AbilityTab(self.data)
        self.metadata_tab = metadata_tab.MetaDataTab(self.data)
        self.item_tab = item_tab.ItemTab(self.data)
        self.gender_tab = gender_tab.GenderTab(self.data)

        self.tab_pokemon_layout.addWidget(self.pokemon_tab)
        self.tab_move_layout.addWidget(self.move_tab)
        self.tab_abilities_layout.addWidget(self.ability_tab)
        self.tab_settings_layout.addWidget(self.metadata_tab)
        self.tab_items_layout.addWidget(self.item_tab)
        self.tab_gender_layout.addWidget(self.gender_tab)

        self.pokemon_tab.attribute_changed_signal.connect(self.update_tab_names)
        self.move_tab.attribute_changed_signal.connect(self.update_tab_names)
        self.ability_tab.attribute_changed_signal.connect(self.update_tab_names)
        self.metadata_tab.attribute_changed_signal.connect(self.update_tab_names)
        self.item_tab.attribute_changed_signal.connect(self.update_tab_names)
        self.gender_tab.attribute_changed_signal.connect(self.update_tab_names)

        self.pokemon_tab.update_list_signal.connect(self.update_user_lists)
        self.move_tab.update_list_signal.connect(self.update_user_lists)
        self.ability_tab.update_list_signal.connect(self.update_user_lists)
        self.item_tab.update_list_signal.connect(self.update_user_lists)
        self.gender_tab.update_list_signal.connect(self.update_user_lists)

        self.pokemon_tab.save_project_signal.connect(self.save)
        self.move_tab.save_project_signal.connect(self.save)
        self.ability_tab.save_project_signal.connect(self.save)
        self.item_tab.save_project_signal.connect(self.save)
        self.gender_tab.save_project_signal.connect(self.save)

    def save_and_continue(self):
        button_reply = QtWidgets.QMessageBox.question(None, 'Save', "Save changes before continuing?",
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)
        if button_reply == QtWidgets.QMessageBox.Yes:
            self._save()

        return button_reply

    def save_on_quit(self):
        button_reply = QtWidgets.QMessageBox.question(None, 'Save', "Save changes before quiting?",
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel,
                                                      QtWidgets.QMessageBox.Cancel)
        return button_reply

    def update_tab_names(self):
        if self.data.datamon.edited:
            self.tabWidget.setTabText(0, "Pokémon*")
        else:
            self.tabWidget.setTabText(0, "Pokémon")

        if self.data.move.edited:
            self.tabWidget.setTabText(1, "Moves*")
        else:
            self.tabWidget.setTabText(1, "Moves")

        if self.data.ability.edited:
            self.tabWidget.setTabText(2, "Abilities*")
        else:
            self.tabWidget.setTabText(2, "Abilities")

        if self.data.metadata.edited:
            self.tabWidget.setTabText(4, "Meta data*")
        else:
            self.tabWidget.setTabText(4, "Meta data")

        if self.data.item.edited:
            self.tabWidget.setTabText(3, "Items*")
        else:
            self.tabWidget.setTabText(3, "Item")

        if self.data.gender.edited:
            self.tabWidget.setTabText(5, "Genders*")
        else:
            self.tabWidget.setTabText(5, "Genders")

    def closeEvent(self, event):
        self.settings.sync()
        if self.data.edited:
            if self.crashed:
                self.crash_save()
                event.accept()
            else:
                button_reply = self.save_on_quit()
                if button_reply == QtWidgets.QMessageBox.Yes:
                    self.save()
                    event.accept()
                elif button_reply == QtWidgets.QMessageBox.No:
                    event.accept()
                elif button_reply == QtWidgets.QMessageBox.Cancel:
                    event.ignore()
        else:
            event.accept()

    def _save(self):
        self.data.save()
        self.update_user_lists()
        self.update_tab_names()
        self.pokemon_tab.reload_lists()

    def save(self, force=False):
        log.info("Saving project")
        if not force and not self.data.edited and (self.data.container and not self.data.container.cleaned):
            log.info("No changes found")
            return
        if self.data.container:
            log.info("Container exists")
            self._save()
        else:
            self.save_as()

    def crash_save(self):
        path = util.get_recovery_file_name()
        if path:
            if self.data.container is None or self.data.container.is_empty:
                log.info("No container found")
                self.data.new_container()
                self.data.container.new(path)
            else:
                self.data.container.path = path
            self._save()

    def save_as(self):
        if not self.data.container:
            self.data.new_container()
        path = QtWidgets.QFileDialog.getSaveFileName(None, "Open Selected file", '', 'FKMN(*.fkmn)', None, QtWidgets.QFileDialog.DontUseNativeDialog)
        if path[0] != '':
            path = Path(path[0] if path[0].endswith(".fkmn") else path[0] + ".fkmn")
            if self.data.container is None or self.data.container.is_empty:
                log.info("No container found")
                self.data.new_container()
                self.data.container.new(path)
            else:
                self.data.container.path = path
            self.setWindowTitle("{} | Fakemon Creator".format(path.name))
            self._save()
            if not self.started:
                self.start()

    def open_project(self):
        try:
            self._open_project()
        except BadZipFile:
            QtWidgets.QMessageBox.about(None, "Invalid file", "Error opening file.")

    def _open_project(self):
        if self.data.edited:
            if self.save_and_continue() == QtWidgets.QMessageBox.Cancel:
                return

        path = QtWidgets.QFileDialog.getOpenFileName(None, "Select output file", '', "FKMN(*.fkmn)", None, QtWidgets.QFileDialog.DontUseNativeDialog)
        if path[0] != '':
            if not self.started:
                self.start()
            path = Path(path[0])
            self.data.load(path)
            self.setWindowTitle("{} | Fakemon Creator".format(path.name))

            self.update_user_lists()
            self.update_tab_names()
            self.pokemon_tab.reload_lists()
            self.metadata_tab.reload()

            log.info("Opened {}".format(path))

    def open_stat_calculator(self):
        if not self.started:
            self.start()
        self.tabWidget.setCurrentIndex(0)
        self.hp_help_window = qtmodern.windows.ModernWindow(stats_calculator.StatsCalculator(self.pokemon_tab))
        self.hp_help_window.show()

    def open_pokemon(self):
        if not self.started:
            self.start()
        self.pokemon_tab.open_pokemon()
        self.tabWidget.setCurrentIndex(0)

    def new_fakemon(self):
        if not self.started:
            self.start()
        self.pokemon_tab.new_fakemon()
        self.tabWidget.setCurrentIndex(0)

    def open_ability(self):
        if not self.started:
            self.start()
        self.ability_tab.open_ability()
        self.tabWidget.setCurrentIndex(2)

    def new_ability(self):
        if not self.started:
            self.start()
        self.ability_tab.new_ability()
        self.tabWidget.setCurrentIndex(2)

    def open_move(self):
        if not self.started:
            self.start()
        self.move_tab.open_move()
        self.tabWidget.setCurrentIndex(1)

    def new_move(self):
        if not self.started:
            self.start()
        self.move_tab.new_move()
        self.tabWidget.setCurrentIndex(1)

    def open_item(self):
        if not self.started:
            self.start()
        self.item_tab.open_item()
        self.tabWidget.setCurrentIndex(3)

    def new_item(self):
        if not self.started:
            self.start()
        self.item_tab.new_item()
        self.tabWidget.setCurrentIndex(3)

    def hp_help(self):
        self.hp_help_window = qtmodern.windows.ModernWindow(shared.HPHelp(self))
        self.hp_help_window.show()

    def update_user_lists(self):
        if self.pokemon_tab:
            self.pokemon_tab.update_custom_list()
        if self.move_tab:
            self.move_tab.update_custom_list()
        if self.ability_tab:
            self.ability_tab.update_custom_list()
        if self.item_tab:
            self.item_tab.update_custom_list()
        if self.gender_tab:
            self.gender_tab.update_custom_list()

    def validate(self):
        errors = self.data.validate()
        if errors:
            msg = ScrollMessageBox(errors, None)
            msg.exec_()
        elif not self.data.container:
            QtWidgets.QMessageBox.about(None, "Validate", "No package loaded!")
        else:
            QtWidgets.QMessageBox.about(None, "Validate", "No Errors found")

    def handle_exception(self, ex_type, value, tb):
        self.crashed = True
        util.log_exception(ex_type, value, tb)
        exception.ui_exception(ex_type, value, tb)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    qtmodern.styles.dark(app)
    settings = QtCore.QSettings("Pokedex5E", "FakemonCreator")
    theme = settings.value("activeTheme", 0)
    win.set_theme(theme)
    mw = qtmodern.windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    log.getLogger().setLevel(log.INFO)

    main()
