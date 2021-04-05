import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.models import VideoPlayerModel

class Ui_VideoPlayer(QtWidgets.QFrame):
    def __init__(self, model: VideoPlayerModel):
        super().__init__()
        self.model = model

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        self.selectVideoFile_btn = QtWidgets.QPushButton("Select Video File", self)
        self.selectVideoFile_btn.setMaximumSize(QtCore.QSize(200, 16777215))
        self.selectVideoFile_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout.addWidget(self.selectVideoFile_btn)
