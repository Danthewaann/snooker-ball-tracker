import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

from .components.label import Ui_Label
from .components.line import Ui_Line
from .components.pushbutton import Ui_PushButton
from .logging_balls_potted import Ui_BallsPotted
from .logging_snapshot_info import Ui_SnapshotInfo
from snooker_ball_tracker.models.logging_model import LoggingModel


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
