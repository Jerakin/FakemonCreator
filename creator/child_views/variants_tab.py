import json
import logging as log

from PyQt5 import QtWidgets, uic, QtGui, sip
from PyQt5.QtCore import Qt, pyqtSignal

from creator.data import fields
from creator.utils import util
from creator.child_views import shared
from creator.child_views import list_view

import creator.components  ## This needs to be here for the promoted QComboBoxes

import qtmodern.windows
import qtmodern.styles


class VariantTab(QtWidgets.QWidget, shared.Tab):
    def __init__(self, data):
        super(VariantTab, self).__init__()
        uic.loadUi(util.RESOURCE_UI / 'VariantTab.ui', self)

    def update_custom_list(self):
        pass