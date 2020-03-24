import sys
from pathlib import Path
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import qtmodern.windows
import qtmodern.styles
import logging as log

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)


class StatsCalculator(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(StatsCalculator, self).__init__()
        self.parent = parent
        uic.loadUi(root / 'res/ui/StatsCalculator.ui', self)  # Load the .ui file
        exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        exit_shortcut.activated.connect(self.close)
        self.strength_overruled = False
        self.dexterity_overruled = False
        self.constitution_overruled = False
        self.ac_overruled = False

        self.health.textEdited.connect(self.recalculate_stat)
        self.attack.textEdited.connect(self.recalculate_stat)
        self.defense.textEdited.connect(self.recalculate_stat)
        self.s_attack.textEdited.connect(self.recalculate_stat)
        self.s_defense.textEdited.connect(self.recalculate_stat)
        self.speed.textEdited.connect(self.recalculate_stat)

        self.copy_stats.clicked.connect(self.copy_to_active_pokemon)

        self.health.setValidator(QtGui.QIntValidator())
        self.attack.setValidator(QtGui.QIntValidator())
        self.defense.setValidator(QtGui.QIntValidator())
        self.s_attack.setValidator(QtGui.QIntValidator())
        self.s_defense.setValidator(QtGui.QIntValidator())
        self.speed.setValidator(QtGui.QIntValidator())

        self.STR.textEdited.connect(lambda: self.overrule_value("strength_overruled", self.STR_label))
        self.DEX.textEdited.connect(lambda: self.overrule_value("dexterity_overruled", self.DEX_label))
        self.CON.textEdited.connect(lambda: self.overrule_value("constitution_overruled", self.CON_label))
        self.AC.textEdited.connect(lambda: self.overrule_value("ac_overruled", self.AC_label))
        self.STR.setValidator(QtGui.QIntValidator())
        self.DEX.setValidator(QtGui.QIntValidator())
        self.CON.setValidator(QtGui.QIntValidator())
        self.AC.setValidator(QtGui.QIntValidator())

        self.STR_label.clicked.connect(lambda: self.restore_value("strength_overruled", self.STR_label))
        self.DEX_label.clicked.connect(lambda: self.restore_value("dexterity_overruled", self.DEX_label))
        self.CON_label.clicked.connect(lambda: self.restore_value("constitution_overruled", self.CON_label))
        self.AC_label.clicked.connect(lambda: self.restore_value("ac_overruled", self.AC_label))

    def overrule_value(self, attribute, label):
        self.__dict__[attribute] = True
        label.setStyleSheet("QLabel { color: rgba(0, 0, 255, 255); }")

    def restore_value(self, attribute, label):
        self.__dict__[attribute] = False
        self.recalculate_stat()
        label.setStyleSheet("QLabel { color: rgba(0, 0, 0, 255); }")

    def recalculate_stat(self):
        health = get_value(self.health)
        attack = get_value(self.attack)
        defense = get_value(self.defense)
        s_defense = get_value(self.s_defense)
        s_attack = get_value(self.s_attack)
        speed = get_value(self.speed)

        strength = 0.2 * attack + 0.4*defense + 0.4*s_defense/0.8
        dexterity = 0.1 * attack + 0.4*s_attack + 0.4*speed/0.8
        constitution = 0.7 * health + 0.05*defense + 0.25*s_defense/0.8
        ac = (0.4*defense + 0.4*s_defense + 0.2*speed/10.5) + 8
        if not self.strength_overruled:
            self.STR.setText(str(static_remap(strength)))
        if not self.dexterity_overruled:
            self.DEX.setText(str(static_remap(dexterity)))
        if not self.constitution_overruled:
            self.CON.setText(str(static_remap(constitution)))
        if not self.ac_overruled:
            self.AC.setText(str(static_remap(ac)))

    def copy_to_active_pokemon(self):
        if self.parent:
            self.parent.set_attributes(
                [self.STR.text(), self.DEX.text(), self.CON.text(), self.INT.text(), self.WIS.text(), self.CHA.text(),
                 self.AC.text()])


def get_value(text_edit):
    return int(text_edit.text() if text_edit.text() != "" else 0)


def remap(value, low1, high1, low2, high2):
    return low2 + (value - low1) * (high2 - low2) / (high1 - low1)


def static_remap(value):
    return int(remap(value, 0, 240, 5, 30))


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = StatsCalculator()
    mw = qtmodern.windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    log.getLogger().setLevel(log.INFO)
    root = Path().cwd().parent
    main()
