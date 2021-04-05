import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.models import LoggingModel, Observer

from ..components import Ui_Label, Ui_Line


class Ui_SnapshotInfo(QtWidgets.QGridLayout):
    def __init__(self, model: LoggingModel, parent=None):
        super().__init__(parent)
        self.model = model

        self.setHorizontalSpacing(10)
        self.setVerticalSpacing(5)

        self.whiteStatus_label = Ui_Label("White Ball Status", parent=parent, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.whiteStatus = Ui_Label("stopped...", parent=parent, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.lastShotCount_label = Ui_Label("Last Shot\nSnapshot", parent=parent, alignment=QtCore.Qt.AlignCenter)
        self.curBallCount_label = Ui_Label("Current\nSnapshot", parent=parent, alignment=QtCore.Qt.AlignCenter)

        self.observers = [
            Observer([(self.whiteStatus, "text"), (self.model, "white_status")])
        ]
        
        self.addWidget(self.whiteStatus_label, 0, 0, 1, 2)
        self.addWidget(self.whiteStatus, 0, 2, 1, 1)
        self.addWidget(Ui_Line(), 1, 0, 1, 3)
        self.addWidget(self.lastShotCount_label, 2, 1, 1, 1)
        self.addWidget(self.curBallCount_label, 2, 2, 1, 1)
        self.addWidget(Ui_Line(), 11, 0, 1, 3)

        start_row = 3
        for colour in s.DETECT_COLOURS:
            if s.DETECT_COLOURS[colour]:
                label = Ui_Label(colour.lower() + 's', parent=parent, alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                lastShot_ballCount = Ui_Label("0", parent=parent, alignment=QtCore.Qt.AlignCenter)
                curBallCount = Ui_Label("0", parent=parent, alignment=QtCore.Qt.AlignCenter)

                self.observers.append([
                    Observer([(lastShot_ballCount, "text"), (self.model.last_shot_snapshot.__getattribute__(colour.lower() + "s"), "count")]),
                    Observer([(curBallCount, "text"), (self.model.cur_shot_snapshot.__getattribute__(colour.lower() + "s"), "count")])
                ])

                self.addWidget(label, start_row, 0, 1, 1)
                self.addWidget(lastShot_ballCount, start_row, 1, 1, 1)
                self.addWidget(curBallCount, start_row, 2, 1, 1)
                start_row += 1
