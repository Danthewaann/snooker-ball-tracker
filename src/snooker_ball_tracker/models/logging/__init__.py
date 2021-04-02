import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

from .Model_snapshot_info import Model_SnapshotInfo
from .Model_balls_potted import Model_BallsPotted


class Model_LoggingGroup(QtCore.QObject):
    def __init__(self):
        super().__init__("Logging")
        font = QtGui.QFont("Logging", pointSize=11)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)
        self.logging_widget = QtWidgets.QWidget(self)
        self.logging_widget.setMaximumSize(QtCore.QSize(567, 16777215))
        self.logging_widget_layout = QtWidgets.QHBoxLayout(self.logging_widget)
        self.logging_widget_layout.setSpacing(15)
        self.logging_widget_layout.addLayout(Ui_BallsPottedList(self.logging_widget))
        self.logging_widget_layout.addLayout(Ui_Snapshot(self.logging_widget))
        self.layout.addWidget(self.logging_widget)