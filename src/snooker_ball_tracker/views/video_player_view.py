import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker import ColourDetectionSettings, VideoPlayer

from .video_player import Options, Player


class VideoPlayerView(QtWidgets.QGroupBox):
    def __init__(self, video_player: VideoPlayer, colours: ColourDetectionSettings):
        super().__init__("Video Player")
        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.layout = QtWidgets.QHBoxLayout(self)

        self.video_player_layout = QtWidgets.QGridLayout()
        self.video_player_layout.addWidget(Player(video_player, colours), 0, 0, 1, 1)
        self.video_player_layout.addWidget(Options(video_player), 1, 0, 1, 1)

        self.layout.addStretch(5)
        self.layout.addLayout(self.video_player_layout, 90)
        self.layout.addStretch(5)
