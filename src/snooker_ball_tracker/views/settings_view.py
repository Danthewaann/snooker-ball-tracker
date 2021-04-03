import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import snooker_ball_tracker.settings as s

from .settings_colour_detection_tab import Ui_ColourDetectionTab
from .settings_ball_detection_tab import Ui_BallDetectionTab
from snooker_ball_tracker.models.settings.ball_detection import BallDetectionTabModel
from snooker_ball_tracker.models.settings.colour_detection import ColourDetectionTabModel


class SettingsView(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Settings")
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.settings_tabs = QtWidgets.QTabWidget(self)
        self.settings_tabs.setMaximumWidth(700)

        self.colour_detection_tab = Ui_ColourDetectionTab(ColourDetectionTabModel())
        self.ball_detection_tab = Ui_BallDetectionTab(BallDetectionTabModel())

        self.settings_tabs.addTab(self.colour_detection_tab, "Colour Detection")
        self.settings_tabs.addTab(self.ball_detection_tab, "Ball Detection")
        self.layout.addWidget(self.settings_tabs)