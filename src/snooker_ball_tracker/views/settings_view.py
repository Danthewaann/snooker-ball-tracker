import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import Settings

from .settings import BallDetectionTab, ColourDetectionTab


class SettingsView(QtWidgets.QGroupBox):
    def __init__(self, model: Settings):
        super().__init__("Settings")
        self.model = model

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.settings_tabs = QtWidgets.QTabWidget(self)
        self.settings_tabs.setMaximumWidth(700)

        self.settings_tabs.addTab(ColourDetectionTab(self.model.models["colour_detection"]), "Colour Detection")
        self.settings_tabs.addTab(BallDetectionTab(self.model.models["ball_detection"]), "Ball Detection")
        self.layout.addWidget(self.settings_tabs)
