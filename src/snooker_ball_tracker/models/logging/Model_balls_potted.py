import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui


class Model_BallsPotted(QtCore.QObject):
    def __init__(self, parent):
        super().__init__()

        self.setSpacing(10)
        self.label = QtWidgets.QLabel("Balls Potted", parent)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.list = QtWidgets.QListWidget(parent)

        self.addWidget(self.label)
        self.addWidget(self.list)
