import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.models import VideoPlayerModel

from .video_player import Ui_VideoPlayer, Ui_VideoPlayerOptions


class VideoPlayerView(QtWidgets.QGroupBox):
    def __init__(self, model: VideoPlayerModel):
        super().__init__("Video Player")
        self.model = model

        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.addWidget(Ui_VideoPlayer(self.model), 0, 0, 1, 1)
        self.layout.addWidget(Ui_VideoPlayerOptions(self.model), 1, 0, 1, 1)
