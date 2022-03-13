import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker.settings import (
    BallDetectionSettings,
    ColourDetectionSettings,
)

from .settings import BallDetectionTab, ColourDetectionTab


class SettingsView(QtWidgets.QGroupBox):
    def __init__(
        self,
        colour_settings: ColourDetectionSettings,
        ball_settings: BallDetectionSettings,
    ):
        super().__init__("Settings")
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)

        self.settings_tabs = QtWidgets.QTabWidget(self)
        # self.settings_tabs.setMaximumWidth(600)

        self.settings_tabs.addTab(
            ColourDetectionTab(colour_settings), "Colour Detection"
        )
        self.settings_tabs.addTab(BallDetectionTab(ball_settings), "Ball Detection")
        self.layout.addWidget(self.settings_tabs)
