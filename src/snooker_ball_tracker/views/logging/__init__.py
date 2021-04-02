import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

from .Ui_snapshot_info import Ui_SnapshotInfo
from .Ui_balls_potted import Ui_BallsPotted


class Ui_Logging(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Logging")
        font = QtGui.QFont("Logging", pointSize=11)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(30)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumWidth(700)
        self.widget_layout = QtWidgets.QHBoxLayout(self.widget)
        self.widget_layout.setSpacing(15)

        self.widget_layout.addLayout(Ui_BallsPotted(self.widget))
        self.widget_layout.addLayout(Ui_SnapshotInfo(self.widget))
        self.layout.addWidget(self.widget)