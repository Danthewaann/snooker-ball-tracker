import typing

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.ball_tracker import (ColourDetectionSettings,
                                               VideoPlayer)

from .video_player import Options, Player


class VideoPlayerView(QtWidgets.QGroupBox):
    def __init__(self, video_player: VideoPlayer, colours: ColourDetectionSettings, 
                 videoFileOnClick: typing.Callable[[], typing.Any]):
        super().__init__("Video Player")
        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.addWidget(Player(video_player, colours, videoFileOnClick), 0, 0, 1, 1)
        self.layout.addWidget(Options(video_player), 1, 0, 1, 1)
