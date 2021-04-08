import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.ball_tracker import VideoPlayer

from ..components import Ui_Label, Ui_PushButton


class Player(QtWidgets.QFrame):

    resized = QtCore.pyqtSignal()

    def __init__(self, model: VideoPlayer):
        super().__init__()
        self.model = model

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.setMaximumWidth(self.model.width)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # self.selectVideoFile_btn = Ui_PushButton("Select Video File", parent=self, width=(200, 200))
        self.output = Ui_Label("", parent=self)
        self.layout.addWidget(self.output)
        # self.layout.addWidget(self.selectVideoFile_btn)
        self.model.frameChanged.connect(self.show_frame)
        # self.model.player_widthChanged.connect(lambda width: self.setMinimumSize(QtCore.QSize(width, self.model.frame.shape[1])))

    def show_frame(self, frame):
        self.setStyleSheet("background-color: black")
        frame = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        self.output.setPixmap(QtGui.QPixmap.fromImage(frame))
