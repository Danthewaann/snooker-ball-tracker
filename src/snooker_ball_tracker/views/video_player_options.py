import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

from .components.pushbutton import Ui_PushButton
from .components.label import Ui_Label
from .components.radiobutton import Ui_RadioButton

from snooker_ball_tracker.models.video_player_model import VideoPlayerModel
from snooker_ball_tracker.models.observer import Observer


class Ui_VideoPlayerOptions(QtWidgets.QWidget):
    def __init__(self, model: VideoPlayerModel):
        super().__init__()
        self.model = model

        btnSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.setMaximumSize(QtCore.QSize(450, 16777215))
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setHorizontalSpacing(10)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.play_btn = Ui_PushButton("Play", self, height=(0, 150))
        self.layout.addWidget(self.play_btn, 0, 3, 1, 1)

        self.restart_btn = Ui_PushButton("Restart", self, height=(0, 150))
        self.layout.addWidget(self.restart_btn, 1, 3, 1, 1)

        self.detectTable_btn = Ui_PushButton("Detect Table", self, height=(0, 150))
        self.layout.addWidget(self.detectTable_btn, 2, 3, 1, 1)

        self.showThreshold_label = Ui_Label("Show Threshold", self, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.showThreshold_label, 0, 2, 1, 1)

        self.showThreshold_yradio = Ui_RadioButton("Yes", parent=self, value=True)
        self.layout.addWidget(self.showThreshold_yradio, 0, 1, 1, 1)

        self.showThreshold_nradio = Ui_RadioButton("No", parent=self, value=False, checked=True)
        self.layout.addWidget(self.showThreshold_nradio, 0, 0, 1, 1)

        self.showThreshold_btnGroup = QtWidgets.QButtonGroup()
        self.showThreshold_btnGroup.addButton(self.showThreshold_yradio)
        self.showThreshold_btnGroup.addButton(self.showThreshold_nradio)

        self.cropFrames_label = Ui_Label("Crop Frames", self, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.cropFrames_label, 1, 2, 1, 1)

        self.cropFrames_yradio = Ui_RadioButton("Yes", parent=self, value=True)
        self.layout.addWidget(self.cropFrames_yradio, 1, 1, 1, 1)

        self.cropFrames_nradio = Ui_RadioButton("No", parent=self, value=False, checked=True)
        self.layout.addWidget(self.cropFrames_nradio, 1, 0, 1, 1)

        self.cropFrames_btnGroup = QtWidgets.QButtonGroup()
        self.cropFrames_btnGroup.addButton(self.cropFrames_yradio)
        self.cropFrames_btnGroup.addButton(self.cropFrames_nradio)

        self.observers = [
            Observer([(self.cropFrames_yradio, "state"), (self.cropFrames_nradio, "state"), (self.model, "crop_frames")]),
            Observer([(self.showThreshold_yradio, "state"), (self.showThreshold_nradio, "state"), (self.model, "show_threshold")])
        ]
