import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.ball_tracker import VideoPlayer

from .video_player import Player, Options


class VideoPlayerView(QtWidgets.QGroupBox):
    def __init__(self, model: VideoPlayer):
        super().__init__("Video Player")
        self.model = model

        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.addWidget(Player(self.model), 0, 0, 1, 1)
        self.layout.addWidget(Options(self.model), 1, 0, 1, 1)
