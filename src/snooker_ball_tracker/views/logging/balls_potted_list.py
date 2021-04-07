import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
from snooker_ball_tracker.ball_tracker import Logger, Observer

from ..components import Ui_Label, Ui_PushButton


class BallsPottedList(QtWidgets.QVBoxLayout):
    def __init__(self, model: Logger, parent=None):
        super().__init__(parent)
        self.model = model

        self.setSpacing(10)

        self.label = Ui_Label("Balls Potted", alignment=QtCore.Qt.AlignCenter)
        self.list = QtWidgets.QListView()
        self.list.setAutoScroll(True)
        self.list.setModel(self.model.balls_potted)
        self.model.balls_potted.layoutChanged.connect(lambda: self.list.scrollToBottom())
        self.clear_btn = Ui_PushButton("Clear", width=(100, 100), objectName="clear_btn")

        self.clear_btn.pressed.connect(self.on_clear_btn_pressed)

        self.addWidget(self.label)
        self.addWidget(self.list)
        self.addWidget(self.clear_btn)

        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot()
    def on_clear_btn_pressed(self):
        self.model.balls_potted.clear()
