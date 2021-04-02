import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

from .Ui_options import Ui_Options
from .Ui_player import Ui_Player


class Ui_VideoPlayer(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Video Player")

        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.addWidget(Ui_Player(), 0, 0, 1, 1)
        self.layout.addWidget(Ui_Options(), 1, 0, 1, 1)
