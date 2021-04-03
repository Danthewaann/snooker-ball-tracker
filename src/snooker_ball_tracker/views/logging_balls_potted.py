import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

from .components.label import Ui_Label
from .components.pushbutton import Ui_PushButton

class Ui_BallsPotted(QtWidgets.QVBoxLayout):
    def __init__(self, parent):
        super().__init__()

        self.setSpacing(10)
        self.label = Ui_Label("Balls Potted", parent)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.list = QtWidgets.QListWidget(parent)
        self.list.addItems(["Potted 1 red/s", "Potted 1 black/s"])
        self.clear_btn = Ui_PushButton("Clear", parent, width=(100, 100))

        self.addWidget(self.label)
        self.addWidget(self.list)
        self.addWidget(self.clear_btn)
