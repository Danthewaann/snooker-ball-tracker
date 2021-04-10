import typing

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.ball_tracker import VideoPlayer
from snooker_ball_tracker.ball_tracker.settings import ColourDetectionSettings

from .video_player import Options, Player


class VideoPlayerView(QtWidgets.QGroupBox):
    def __init__(self, model: VideoPlayer, colours: ColourDetectionSettings, 
                 videoFileOnClick: typing.Callable[[], typing.Any]):
        super().__init__("Video Player")
        self.model = model

        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(Player(self.model, colours, videoFileOnClick), 0, 0, 1, 1)
        self.layout.addWidget(Options(self.model), 1, 0, 1, 1)
