import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.models import LoggingModel

from .components import Ui_Label, Ui_Line, Ui_PushButton
from .logging import Ui_BallsPotted, Ui_SnapshotInfo


class LoggingView(QtWidgets.QGroupBox):
    def __init__(self, model: LoggingModel):
        super().__init__("Logging")
        self.model = model

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(30)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumWidth(700)
        self.widget_layout = QtWidgets.QHBoxLayout(self.widget)
        self.widget_layout.setSpacing(15)

        self.widget_layout.addLayout(Ui_BallsPotted(self.model))
        self.widget_layout.addLayout(Ui_SnapshotInfo(self.model))
        self.layout.addWidget(self.widget)
