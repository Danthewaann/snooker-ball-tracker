import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.models.ball_detection_model import \
    BallDetectionTabModel
from snooker_ball_tracker.models.colour_detection_model import \
    ColourDetectionTabModel
from snooker_ball_tracker.models.settings_model import SettingsModel

from .settings_ball_detection_tab import BallDetectionTabView
from .settings_colour_detection_tab import ColourDetectionTabView


class SettingsView(QtWidgets.QGroupBox):
    def __init__(self, model: SettingsModel):
        super().__init__("Settings")
        self.model = model

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.settings_tabs = QtWidgets.QTabWidget(self)
        self.settings_tabs.setMaximumWidth(700)

        self.settings_tabs.addTab(ColourDetectionTabView(self.model.models["colour_detection"]), "Colour Detection")
        self.settings_tabs.addTab(BallDetectionTabView(self.model.models["ball_detection"]), "Ball Detection")
        self.layout.addWidget(self.settings_tabs)
