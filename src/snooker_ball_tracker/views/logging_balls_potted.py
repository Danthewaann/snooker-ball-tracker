import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

from .components.label import Ui_Label
from .components.pushbutton import Ui_PushButton
from snooker_ball_tracker.models.logging_model import LoggingModel
from snooker_ball_tracker.models.observer import Observer


class Ui_BallsPotted(QtWidgets.QVBoxLayout):
    def __init__(self, model: LoggingModel, parent=None):
        super().__init__(parent)
        self.model = model

        self.setSpacing(10)

        self.label = Ui_Label("Balls Potted", alignment=QtCore.Qt.AlignCenter)
        self.list = QtWidgets.QListView()
        self.list.setModel(self.model.balls_potted)
        self.clear_btn = Ui_PushButton("Clear", width=(100, 100), objectName="clear_btn")

        self.clear_btn.pressed.connect(self.on_clear_btn_pressed)

        self.addWidget(self.label)
        self.addWidget(self.list)
        self.addWidget(self.clear_btn)

        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot()
    def on_clear_btn_pressed(self):
        self.model.balls_potted.clear()
