import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui


class Ui_Player(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.setMaximumSize(QtCore.QSize(800, 16777215))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.selectVideoFile_btn = QtWidgets.QPushButton("Select Video File", self)
        self.selectVideoFile_btn.setMaximumSize(QtCore.QSize(200, 16777215))
        self.selectVideoFile_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout.addWidget(self.selectVideoFile_btn)