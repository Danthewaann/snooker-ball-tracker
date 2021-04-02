import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

from .colour_detection import ColourDetectionTabModel
from .ball_detection import BallDetectionTabModel
import snooker_ball_tracker.settings as s


class Model_SettingsGroup(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Settings")
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.settings_tabs = QtWidgets.QTabWidget(self)
        self.settings_tabs.setMaximumSize(QtCore.QSize(589, 16777215))
        self.settings_tabs.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.settings_tabs.addTab(Ui_ColourDetectionTab(), "Colour Detection")
        self.settings_tabs.addTab(Ui_BallDetectionTab(), "Ball Detection")
        self.layout.addWidget(self.settings_tabs)