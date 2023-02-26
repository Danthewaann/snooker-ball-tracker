import os.path
from argparse import Namespace

import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker import BallTracker, VideoPlayer
from snooker_ball_tracker.settings import settings as s

from .actions import (
    load_settings_action,
    save_settings_action,
    select_video_file_action,
)
from .logging_view import LoggingView
from .settings_view import SettingsView
from .video_player_view import VideoPlayerView


class MainView(QtWidgets.QMainWindow):
    def __init__(self, args: Namespace, icon: QtGui.QIcon):
        super().__init__()

        self.setWindowIcon(icon)
        self.settings_file = args.settings_file
        self.menuBar().setStyleSheet("background-color: #e6e6e6")
        self.statusBar().show()
        self.statusBar().setStyleSheet("background-color: #e6e6e6")

        if self.settings_file is not None:
            s.load(self.settings_file)
            self.statusBar().showMessage(
                f'Loaded settings from "{os.path.basename(self.settings_file)}"'
            )

        self.setWindowTitle("Snooker Ball Tracker Demo")
        self.showMaximized()

        self.central_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_widget_layout = QtWidgets.QHBoxLayout()
        self.column_1 = QtWidgets.QVBoxLayout()
        self.column_2 = QtWidgets.QVBoxLayout()
        self.central_widget_layout.setContentsMargins(15, 15, 15, 15)

        self.ball_tracker = BallTracker()
        self.video_player = VideoPlayer(self.ball_tracker)

        self.settings_view = SettingsView(
            colour_settings=self.ball_tracker.colour_settings,
            ball_settings=self.ball_tracker.ball_settings,
        )
        self.logging_view = LoggingView(
            self.ball_tracker.logger, self.ball_tracker.colour_settings
        )
        self.video_player_view = VideoPlayerView(
            self.video_player, self.ball_tracker.colour_settings
        )

        self.column_1.addWidget(self.logging_view, 40)
        self.column_1.addWidget(self.settings_view, 40)
        self.column_2.addWidget(self.video_player_view, 100)

        self.central_widget_layout.addStretch(15)
        self.central_widget_layout.addLayout(self.column_1, 25)
        self.central_widget_layout.addLayout(self.column_2, 45)
        self.central_widget_layout.addStretch(15)

        self.main_layout.addLayout(self.central_widget_layout)

        self.setCentralWidget(self.central_widget)

        menu = self.menuBar().addMenu("Video")
        action = menu.addAction("Select Video File")
        action.triggered.connect(self.select_file_onclick)

        menu = self.menuBar().addMenu("Settings")
        action = menu.addAction("Load")
        action.triggered.connect(self.load_settings)
        action = menu.addAction("Save")
        action.triggered.connect(self.save_settings)

        action = self.menuBar().addAction("Exit")
        action.triggered.connect(self.close)

        self.menuBar().setNativeMenuBar(False)

        if args.video is not None:
            try:
                self.video_player.start(args.video)
            except TypeError:
                error = QtWidgets.QMessageBox(None)
                error.setWindowTitle("Invalid Video File!")
                error.setText("Invalid file, please select a video file!")
                error.exec_()

    def closeEvent(self, event: QtGui.QCloseEvent):
        """Handle the close event by closing child threads before
        accepting the close event

        :param event: close event instance
        """
        self.video_player.destroy_video_threads()
        event.accept()

    def select_file_onclick(self):
        """Select video file event handler.

        Gets a video file provided by the user and attempts to validate
        that it is in fact a valid video file.

        Passes the video file to the VideoProcessor thread for processing
        and display.
        """
        video_file = select_video_file_action()
        if video_file:
            try:
                self.video_player.start(video_file)
            except TypeError:
                error = QtWidgets.QMessageBox(None)
                error.setWindowTitle("Invalid Video File!")
                error.setText("Invalid file, please select a video file!")
                error.exec_()

    def load_settings(self):
        """Load settings from user provided file"""
        loaded_settings = load_settings_action()
        if loaded_settings:
            settings_file, colour_settings, ball_settings = loaded_settings
            self.statusBar().showMessage(
                f'Loaded settings from "{os.path.basename(settings_file)}"'
            )
            self.settings_file = settings_file
            self.ball_tracker.colour_settings.settings = colour_settings
            self.ball_tracker.ball_settings.settings = ball_settings

    def save_settings(self):
        """Save settings to user provided file"""
        settings_file = save_settings_action(
            self.ball_tracker.colour_settings,
            self.ball_tracker.ball_settings,
            self.settings_file,
        )
        if settings_file:
            self.settings_file = settings_file
            self.statusBar().showMessage(
                f'Saved settings to "{os.path.basename(self.settings_file)}"'
            )
