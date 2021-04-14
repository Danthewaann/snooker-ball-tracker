import threading
from copy import deepcopy

import cv2
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import (BallDetectionSettings,
                                               BallTracker,
                                               ColourDetectionSettings, Logger,
                                               VideoPlayer)
from snooker_ball_tracker.video_file_stream import VideoFileStream
from snooker_ball_tracker.video_processor import VideoProcessor

from .logging_view import LoggingView
from .settings_view import SettingsView
from .video_player_view import VideoPlayerView


class MainView(QtWidgets.QMainWindow):
    def __init__(self, args):
        super().__init__()

        self.settings_file = args.settings_file

        if self.settings_file:
            s.load(self.settings_file)

        self.setWindowTitle("Snooker Ball Tracker Demo")
        self.showMaximized()

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget_layout = QtWidgets.QGridLayout(self.central_widget)
        self.central_widget_layout.setContentsMargins(30, 30, 30, 30)
        self.central_widget_layout.setSpacing(30)

        self.video_processor_lock = threading.Lock()
        self.video_processor_stop_event = threading.Event()
        self.video_processor = None
        self.video_file_stream = None
        self.video_file = None

        self.logger = Logger()
        self.colour_settings = ColourDetectionSettings()
        self.ball_settings = BallDetectionSettings()
        self.video_player = VideoPlayer()
        self.video_player.restartSignal.connect(self.restart_video_player)
        self.ball_tracker = BallTracker(logger=self.logger, 
            colour_settings=self.colour_settings, ball_settings=self.ball_settings)

        self.settings_view = SettingsView(colour_settings=self.colour_settings, ball_settings=self.ball_settings)
        self.logging_view = LoggingView(self.logger)
        self.video_player_view = VideoPlayerView(self.video_player, 
            self.colour_settings, videoFileOnClick=self.select_file_onclick)

        self.central_widget_layout.addWidget(self.logging_view, 0, 0, 1, 1)
        self.central_widget_layout.addWidget(self.settings_view, 1, 0, 1, 1)
        self.central_widget_layout.addWidget(self.video_player_view, 0, 1, 2, 1)
        self.central_widget_layout.setColumnStretch(1, 2)

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

    def closeEvent(self, event: QtGui.QCloseEvent):
        """Handle the close event by closing child threads before
        accepting the close event

        :param event: close event instance
        :type event: QtGui.QCloseEvent
        """
        self.__destroy_video_threads()
        event.accept()

    def select_file_onclick(self):
        """Select video file event handler.

        Gets a video file provided by the user and attempts to validate
        that it is in fact a valid video file.

        Passes the video file to the VideoProcessor thread for processing
        and display.

        :raises TypeError: If the video file is not valid will display an error box
        """
        self.video_file, _ = QtWidgets.QFileDialog().getOpenFileName(self, "Select Video File", "")

        if not self.video_file:
            return

        self.__destroy_video_threads()

        try:
            self.video_file_stream = cv2.VideoCapture(self.video_file)
            if not self.video_file_stream.isOpened():
                raise TypeError
        except:
            error = QtWidgets.QMessageBox(self)
            error.setWindowTitle("Invalid Video File!")
            error.setText('Invalid file, please select a video file!')
            error.exec_()
            return

        self.video_player.play = False
        self.start_video_player()

    def start_video_player(self):
        """Creates VideoProcessor and VideoFileStream instances to handle 
        the selected video file.

        The VideoFileStream is the producer thread and the VideoProcessor
        is the consumer thread, where the VideoFileStream instance reads
        frames from the video file and puts them into a queue for the
        VideoProcessor to obtain frames to process from.

        The VideoProcessor then passes processed frames to the VideoPlayer
        to display to the user.
        """
        self.video_processor_stop_event.clear()

        self.video_file_stream = VideoFileStream(
            self.video_file, video_player=self.video_player,
            colours=self.colour_settings.colours, queue_size=1)

        self.video_processor = VideoProcessor(
            video_stream=self.video_file_stream, 
            logger=self.logger, video_player=self.video_player, 
            colour_settings=self.colour_settings,
            ball_tracker=self.ball_tracker, lock=self.video_processor_lock, 
            stop_event=self.video_processor_stop_event)

        self.video_processor.start()

    def restart_video_player(self):
        """Restart the video player by destroying the VideoProcessor
        and VideoFileStream instances and creating new ones before 
        starting the video player again."""
        self.__destroy_video_threads()
        self.start_video_player()

    def __destroy_video_threads(self):
        """Destroy the VideoProcessor and VideoFileStream thread instances"""
        if self.video_processor is not None:
            if self.video_file_stream is not None:
                with self.video_processor_lock:
                    self.video_file_stream.stop()
            self.video_processor_stop_event.set()
            self.video_processor.join()

    def load_settings(self):
        """Load settings from user provided file"""
        settings_file, _ = QtWidgets.QFileDialog().getOpenFileName(self, "Load Settings", "")
        if not settings_file:
            return

        success, error = s.load(settings_file)
        if success:
            self.settings_file = settings_file
            self.colour_settings.colours = deepcopy(s.COLOURS)
            self.ball_settings.blob_detector = deepcopy(s.BLOB_DETECTOR)
        else:
            error = QtWidgets.QMessageBox(self)
            error.setWindowTitle("Invalid Settings File!")
            error.setText('Invalid file, please select a valid json file!')
            error.exec_()

    def save_settings(self):
        """Save settings to user provided file"""
        settings_file, _ = QtWidgets.QFileDialog().getSaveFileName(self, "Save Settings", self.settings_file)

        if not settings_file:
            return

        s.COLOURS = self.colour_settings.colours
        s.BLOB_DETECTOR = self.ball_settings.blob_detector
        success, error = s.save(settings_file)
        if success:
            self.settings_file = settings_file
        else:
            error = QtWidgets.QMessageBox(self)
            error.setWindowTitle("Failed to Save Settings!")
            error.setText(f"Failed to save settings to '{settings_file}'\nReason: {error}")
            error.exec_()
