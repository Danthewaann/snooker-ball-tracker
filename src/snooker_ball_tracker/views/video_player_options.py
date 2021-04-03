import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

class Ui_VideoPlayerOptions(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        btnSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.setMaximumSize(QtCore.QSize(400, 16777215))
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setHorizontalSpacing(10)

        self.play_btn = QtWidgets.QPushButton("Play", self)
        self.play_btn.setMaximumSize(QtCore.QSize(150, 16777215))
        self.play_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.play_btn.setSizePolicy(btnSizePolicy)
        self.layout.addWidget(self.play_btn, 0, 3, 1, 1)

        self.restart_btn = QtWidgets.QPushButton("Restart", self)
        self.restart_btn.setMaximumSize(QtCore.QSize(150, 16777215))
        self.restart_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.restart_btn.setSizePolicy(btnSizePolicy)
        self.layout.addWidget(self.restart_btn, 1, 3, 1, 1)

        self.detectTable_btn = QtWidgets.QPushButton("Detect Table", self)
        self.detectTable_btn.setMaximumSize(QtCore.QSize(150, 16777215))
        self.detectTable_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.detectTable_btn.setSizePolicy(btnSizePolicy)
        self.layout.addWidget(self.detectTable_btn, 2, 3, 1, 1)

        self.showThreshold_label = QtWidgets.QLabel("Show Threshold", self)
        self.showThreshold_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.showThreshold_label, 0, 2, 1, 1)

        self.showThreshold_yradio = QtWidgets.QRadioButton("Yes", self)
        self.showThreshold_yradio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout.addWidget(self.showThreshold_yradio, 0, 1, 1, 1)

        self.showThreshold_nradio = QtWidgets.QRadioButton("No", self)
        self.showThreshold_nradio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout.addWidget(self.showThreshold_nradio, 0, 0, 1, 1)

        self.showThreshold_btnGroup = QtWidgets.QButtonGroup()
        self.showThreshold_btnGroup.addButton(self.showThreshold_yradio)
        self.showThreshold_btnGroup.addButton(self.showThreshold_nradio)

        self.cropFrames_label = QtWidgets.QLabel("Crop Frames", self)
        self.cropFrames_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.cropFrames_label, 1, 2, 1, 1)

        self.cropFrames_yradio = QtWidgets.QRadioButton("Yes", self)
        self.cropFrames_yradio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout.addWidget(self.cropFrames_yradio, 1, 1, 1, 1)

        self.cropFrames_nradio = QtWidgets.QRadioButton("No", self)
        self.cropFrames_nradio.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.layout.addWidget(self.cropFrames_nradio, 1, 0, 1, 1)

        self.cropFrames_btnGroup = QtWidgets.QButtonGroup()
        self.cropFrames_btnGroup.addButton(self.cropFrames_yradio)
        self.cropFrames_btnGroup.addButton(self.cropFrames_nradio)

        self.cropFrames_nradio.setChecked(True)
        self.showThreshold_nradio.setChecked(True)
