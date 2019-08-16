import sys
from pathlib import Path
import logging as log

from PyQt5 import QtWidgets, uic, QtGui

from creator.data import Data
from creator.child_views import move_tab
from creator.child_views import ability_tab
from creator.child_views import pokemon_tab
from creator.child_views import metadata_tab
from creator.child_views import shared
from creator import __version__ as version
from creator.child_views import exception
import qtmodern.windows
import qtmodern.styles

from zipfile import BadZipFile

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)
    qtmodern.styles._STYLESHEET = root / 'qtmodern/style.qss'
    qtmodern.windows._FL_STYLESHEET = root / 'qtmodern/frameless.qss'


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(root / 'res/ui/FakemonCreator.ui', self)
        exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        exit_shortcut.activated.connect(self.close)
        debug_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("."), self)
        debug_shortcut.activated.connect(self.update_tab_names)
        self.data = Data(self)

        self.started = False
        self.hp_help_window = None
        self.pokemon_tab = None
        self.move_tab = None
        self.ability_tab = None
        self.metadata_tab = None

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

        self.actionExit.triggered.connect(self.close)
        self.actionAbout_Hp_Calculation.triggered.connect(self.hp_help)

        self.actionValidate.triggered.connect(self.validate)

    def start(self):
        self.started = True
        # Tabs
        self.pokemon_tab = pokemon_tab.PokemonTab(self.data)
        self.move_tab = move_tab.MoveTab(self.data)
        self.ability_tab = ability_tab.AbilityTab(self.data)
        self.metadata_tab = metadata_tab.MetaDataTab(self.data)
        self.metadata_tab = metadata_tab.MetaDataTab(self.data)

        self.tab_pokemon_layout.addWidget(self.pokemon_tab)
        self.tab_move_layout.addWidget(self.move_tab)
        self.tab_abilities_layout.addWidget(self.ability_tab)
        self.tab_settings_layout.addWidget(self.metadata_tab)

        self.pokemon_tab.attribute_changed_signal.connect(self.update_tab_names)
        self.move_tab.attribute_changed_signal.connect(self.update_tab_names)
        self.ability_tab.attribute_changed_signal.connect(self.update_tab_names)
        self.metadata_tab.attribute_changed_signal.connect(self.update_tab_names)

        self.pokemon_tab.update_list_signal.connect(self.update_user_lists)
        self.move_tab.update_list_signal.connect(self.update_user_lists)
        self.ability_tab.update_list_signal.connect(self.update_user_lists)

        self.ability_tab.save_project_signal.connect(self._save)

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
            self.tabWidget.setTabText(3, "Meta data*")
        else:
            self.tabWidget.setTabText(3, "Meta data")

    def closeEvent(self, event):
        if self.data.edited:
            button_reply = self.save_on_quit()
            if button_reply == QtWidgets.QMessageBox.Yes:
                self._save()
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
        if not force and not self.data.edited:
            log.info("No changes found")
            return
        if self.data.container:
            log.info("Container exists")
            self._save()
        else:
            self.save_as()

    def save_as(self):
        if not self.data.container:
            self.start()
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

    def hp_help(self):
        self.hp_help_window = qtmodern.windows.ModernWindow(shared.HPHelp(self))
        self.hp_help_window.show()

    def update_user_lists(self):
        self.pokemon_tab.update_custom_list()
        self.move_tab.update_custom_list()
        self.ability_tab.update_custom_list()

    def validate(self):
        errors = self.data.validate()
        if errors:
            QtWidgets.QMessageBox.about(None, "Validate", "\n\n".join(errors))
        elif not self.data.container:
            QtWidgets.QMessageBox.about(None, "Validate", "No package loaded!")
        else:
            QtWidgets.QMessageBox.about(None, "Validate", "No Errors found")


def handle_exception(extype, value, tb):
    log.critical(
        'Global error:\n'
          'Launcher version: {version}\n'
          'Type: {extype}\n'
          'Value: {value}\n'
          'Traceback:\n{traceback}'
        .format(version=version, extype=str(extype), value=str(value),traceback=tb_io.getvalue())
    )
    ui_exception(extype, value, tb)


def ui_exception(extype, value, tb):
    main_app = QtWidgets.QApplication.instance()

    if main_app is not None:
        main_app_still_up = True
        main_app.closeAllWindows()
    else:
        main_app_still_up = False
        main_app = QtWidgets.QApplication(sys.argv)

    ex_win = exception.ExceptionWindow(main_app, extype, value, tb)
    ex_win.show()
    main_app.ex_win = ex_win

    if not main_app_still_up:
        sys.exit(main_app.exec_())


def main():
    sys.excepthook = ui_exception
    app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
    win = MainWindow()  # Create an instance of our class
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())  # Start the application


if __name__ == "__main__":
    log.getLogger().setLevel(log.INFO)

    main()
