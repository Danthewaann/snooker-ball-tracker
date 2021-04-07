import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.ball_tracker import Observer, VideoPlayer

from ..components import Ui_Label, Ui_PushButton, Ui_RadioButton


class Options(QtWidgets.QWidget):
    def __init__(self, model: VideoPlayer):
        super().__init__()
        self.model = model

        self.setMaximumSize(QtCore.QSize(450, 16777215))
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setHorizontalSpacing(10)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.play_btn = Ui_PushButton("Play", self, height=(0, 30), objectName="play_btn")
        self.restart_btn = Ui_PushButton("Restart", self, height=(0, 30), objectName="restart_btn")
        self.detectTable_btn = Ui_PushButton("Detect Table", self, height=(0, 30), objectName="detectTable_btn")
        
        self.showThreshold_label = Ui_Label("Show Threshold", self, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.showThreshold_yradio = Ui_RadioButton("Yes", parent=self, value=True)
        self.showThreshold_nradio = Ui_RadioButton("No", parent=self, value=False, checked=True)
        self.showThreshold_btnGroup = QtWidgets.QButtonGroup()
        self.showThreshold_btnGroup.addButton(self.showThreshold_yradio)
        self.showThreshold_btnGroup.addButton(self.showThreshold_nradio)

        self.cropFrames_label = Ui_Label("Crop Frames", self, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.cropFrames_yradio = Ui_RadioButton("Yes", parent=self, value=True)
        self.cropFrames_nradio = Ui_RadioButton("No", parent=self, value=False, checked=True)
        self.cropFrames_btngroup = QtWidgets.QButtonGroup()
        self.cropFrames_btngroup.addButton(self.cropFrames_yradio)
        self.cropFrames_btngroup.addButton(self.cropFrames_nradio)

        self.performMorph_label = Ui_Label("Perform Morphology", self, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.performMorph_yradio = Ui_RadioButton("Yes", parent=self, value=True)
        self.performMorph_nradio = Ui_RadioButton("No", parent=self, value=False, checked=True)
        self.performMorph_btngroup = QtWidgets.QButtonGroup()
        self.performMorph_btngroup.addButton(self.performMorph_yradio)
        self.performMorph_btngroup.addButton(self.performMorph_nradio)

        self.observers = [
            Observer([(self.cropFrames_yradio, "state"), (self.cropFrames_nradio, "state"), (self.model, "crop_frames")]),
            Observer([(self.showThreshold_yradio, "state"), (self.showThreshold_nradio, "state"), (self.model, "show_threshold")]),
            Observer([(self.performMorph_yradio, "state"), (self.performMorph_nradio, "state"), (self.model, "perform_morph")])
        ]

        self.layout.addWidget(self.play_btn,             0, 3, 1, 1)
        self.layout.addWidget(self.restart_btn,          1, 3, 1, 1)
        self.layout.addWidget(self.detectTable_btn,      2, 3, 1, 1)
        self.layout.addWidget(self.showThreshold_label,  0, 2, 1, 1)
        self.layout.addWidget(self.showThreshold_yradio, 0, 1, 1, 1)
        self.layout.addWidget(self.showThreshold_nradio, 0, 0, 1, 1)
        self.layout.addWidget(self.cropFrames_label,     1, 2, 1, 1)
        self.layout.addWidget(self.cropFrames_yradio,    1, 1, 1, 1)
        self.layout.addWidget(self.cropFrames_nradio,    1, 0, 1, 1)
        self.layout.addWidget(self.performMorph_label,   2, 2, 1, 1)
        self.layout.addWidget(self.performMorph_yradio,  2, 1, 1, 1)
        self.layout.addWidget(self.performMorph_nradio,  2, 0, 1, 1)

        self.model.play_videoChanged.connect(lambda value: self.play_btn.setText("Pause") if value else self.play_btn.setText("Play"))
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot()
    def on_play_btn_pressed(self):
        if self.play_btn.text() == "Play":
            self.model.play_video = True
            self.play_btn.setText("Pause")
        else:
            self.model.play_video = False
            self.play_btn.setText("Play")

    @QtCore.pyqtSlot()
    def on_restart_btn_pressed(self):
        self.model.restart_video = True

    @QtCore.pyqtSlot()
    def on_detectTable_btn_pressed(self):
        self.model.detect_table = True
