import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

from .Model_options import Model_Options
from .Model_player import Model_VideoPlayer


class Model_VideoPlayerGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Video Player")

        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.addWidget(Ui_VideoPlayer(), 0, 0, 1, 1)
        self.layout.addWidget(Ui_Options(), 1, 0, 1, 1)
