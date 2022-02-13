import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker import VideoPlayer
from snooker_ball_tracker.observer import Observer

from ..components import Ui_Label, Ui_Line, Ui_PushButton, Ui_RadioButton


class Options(QtWidgets.QWidget):
    def __init__(self, video_player: VideoPlayer):
        super().__init__()
        self.video_player = video_player

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setHorizontalSpacing(10)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)
        self.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.video_stream_queue_label = Ui_Label(
            "Queue Size:", alignment=QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.video_stream_queue_value = Ui_Label("0", alignment=QtCore.Qt.AlignCenter)

        self.video_fps_label = Ui_Label(
            "FPS:", alignment=QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.video_fps_value = Ui_Label("0", alignment=QtCore.Qt.AlignCenter)

        self.play_btn = Ui_PushButton("Play", self, objectName="play_btn")
        self.restart_btn = Ui_PushButton("Restart", self, objectName="restart_btn")
        self.detectTable_btn = Ui_PushButton(
            "Detect Table", self, objectName="detectTable_btn"
        )

        self.showThreshold_label = Ui_Label(
            "Show Threshold",
            self,
            alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
        )
        self.showThreshold_yradio = Ui_RadioButton("Yes", parent=self, value=True)
        self.showThreshold_nradio = Ui_RadioButton(
            "No", parent=self, value=False, checked=True
        )
        self.showThreshold_btnGroup = QtWidgets.QButtonGroup()
        self.showThreshold_btnGroup.addButton(self.showThreshold_yradio)
        self.showThreshold_btnGroup.addButton(self.showThreshold_nradio)

        self.cropFrames_label = Ui_Label(
            "Crop Frames", self, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        )
        self.cropFrames_yradio = Ui_RadioButton("Yes", parent=self, value=True)
        self.cropFrames_nradio = Ui_RadioButton(
            "No", parent=self, value=False, checked=True
        )
        self.cropFrames_btngroup = QtWidgets.QButtonGroup()
        self.cropFrames_btngroup.addButton(self.cropFrames_yradio)
        self.cropFrames_btngroup.addButton(self.cropFrames_nradio)

        self.performMorph_label = Ui_Label(
            "Perform\nMorphology",
            self,
            alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
        )
        self.performMorph_yradio = Ui_RadioButton("Yes", parent=self, value=True)
        self.performMorph_nradio = Ui_RadioButton(
            "No", parent=self, value=False, checked=True
        )
        self.performMorph_btngroup = QtWidgets.QButtonGroup()
        self.performMorph_btngroup.addButton(self.performMorph_yradio)
        self.performMorph_btngroup.addButton(self.performMorph_nradio)

        self.observers = [
            Observer(
                [
                    (self.cropFrames_yradio, "state"),
                    (self.cropFrames_nradio, "state"),
                    (self.video_player, "crop_frames"),
                ]
            ),
            Observer(
                [
                    (self.showThreshold_yradio, "state"),
                    (self.showThreshold_nradio, "state"),
                    (self.video_player, "show_threshold"),
                ]
            ),
            Observer(
                [
                    (self.performMorph_yradio, "state"),
                    (self.performMorph_nradio, "state"),
                    (self.video_player, "perform_morph"),
                ]
            ),
            Observer(
                [
                    (self.video_stream_queue_value, "text"),
                    (self.video_player, "queue_size"),
                ]
            ),
        ]

        self.layout.addItem(
            QtWidgets.QSpacerItem(
                0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
            ),
            0,
            8,
            3,
            1,
        )
        self.layout.addWidget(self.video_stream_queue_label, 0, 7)
        self.layout.addWidget(self.video_stream_queue_value, 0, 6)
        self.layout.addWidget(self.video_fps_label, 1, 7)
        self.layout.addWidget(self.video_fps_value, 1, 6)
        self.layout.addWidget(Ui_Line(shape=QtWidgets.QFrame.VLine), 0, 5, 3, 1)
        self.layout.addWidget(self.play_btn, 0, 4)
        self.layout.addWidget(self.restart_btn, 1, 4)
        self.layout.addWidget(self.detectTable_btn, 2, 4)
        self.layout.addWidget(Ui_Line(shape=QtWidgets.QFrame.VLine), 0, 3, 3, 1)
        self.layout.addWidget(self.showThreshold_label, 0, 2)
        self.layout.addWidget(self.showThreshold_yradio, 0, 1)
        self.layout.addWidget(self.showThreshold_nradio, 0, 0)
        self.layout.addWidget(self.cropFrames_label, 1, 2)
        self.layout.addWidget(self.cropFrames_yradio, 1, 1)
        self.layout.addWidget(self.cropFrames_nradio, 1, 0)
        self.layout.addWidget(self.performMorph_label, 2, 2)
        self.layout.addWidget(self.performMorph_yradio, 2, 1)
        self.layout.addWidget(self.performMorph_nradio, 2, 0)
        self.layout.addItem(
            QtWidgets.QSpacerItem(
                0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
            ),
            3,
            0,
            1,
            5,
        )

        self.video_player.playChanged.connect(self.update_on_play_changed)
        self.video_player.fpsChanged.connect(self.video_fps_value.setNum)
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot(bool)
    def update_on_play_changed(self, playing: bool):
        if playing:
            self.play_btn.setText("Pause")
            self.video_player.start_fps()
        else:
            self.play_btn.setText("Play")

    @QtCore.pyqtSlot()
    def on_play_btn_pressed(self):
        if self.play_btn.text() == "Play":
            self.video_player.play = True
            self.play_btn.setText("Pause")
            self.video_player.start_fps()
        else:
            self.video_player.play = False
            self.play_btn.setText("Play")

    @QtCore.pyqtSlot()
    def on_restart_btn_pressed(self):
        self.video_player.restart()

    @QtCore.pyqtSlot()
    def on_detectTable_btn_pressed(self):
        self.video_player.detect_table = True
