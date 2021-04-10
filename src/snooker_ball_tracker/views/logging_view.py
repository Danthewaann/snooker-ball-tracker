import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.ball_tracker import Logger

from .components import Ui_Label, Ui_Line, Ui_PushButton
from .logging import BallsPottedList, BallInfo


class LoggingView(QtWidgets.QGroupBox):
    def __init__(self, model: Logger):
        super().__init__("Logging")
        self.model = model

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumWidth(700)
        self.widget_layout = QtWidgets.QHBoxLayout(self.widget)
        self.widget_layout.setSpacing(15)

        self.widget_layout.addLayout(BallsPottedList(self.model))
        self.widget_layout.addLayout(BallInfo(self.model))
        self.layout.addWidget(self.widget)
