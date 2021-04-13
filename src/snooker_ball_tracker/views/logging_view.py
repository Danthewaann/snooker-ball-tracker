import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import Logger

from .components import Ui_Label, Ui_Line, Ui_PushButton


class LoggingView(QtWidgets.QGroupBox):
    def __init__(self, logger: Logger):
        super().__init__("Logging")
        self.logger = logger
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)

        self.balls_potted_label = Ui_Label("Balls Potted", alignment=QtCore.Qt.AlignCenter)
        self.balls_potted_list = QtWidgets.QListView()
        self.balls_potted_list.setAutoScroll(True)
        self.balls_potted_list.setModel(self.logger.balls_potted)
        
        self.logger.balls_potted.layoutChanged.connect(lambda: self.balls_potted_list.scrollToBottom())
        self.clear_btn = Ui_PushButton("Clear", width=(100, 100), objectName="clear_btn")

        self.whiteStatus_label = Ui_Label("White Ball Status", alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.whiteStatus = Ui_Label("stopped...", width=(100, 100), alignment=QtCore.Qt.AlignCenter)
        self.lastShotCount_label = Ui_Label("Last Shot\nSnapshot", alignment=QtCore.Qt.AlignCenter)
        self.curBallCount_label = Ui_Label("Current\nSnapshot", alignment=QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.balls_potted_label, 0, 0, 1, 4)
        self.layout.addWidget(self.balls_potted_list, 2, 0, 9, 4)
        self.layout.addWidget(self.clear_btn, 11, 0)
        self.layout.addWidget(self.whiteStatus_label, 0, 4, 1, 2)
        self.layout.addWidget(self.whiteStatus, 0, 6, 1, 1)
        self.layout.addWidget(Ui_Line(), 1, 0, 1, 7)
        self.layout.addWidget(self.lastShotCount_label, 2, 5, 1, 1)
        self.layout.addWidget(self.curBallCount_label, 2, 6, 1, 1)

        start_row = 3
        for colour in s.DETECT_COLOURS:
            if s.DETECT_COLOURS[colour]:
                label = Ui_Label(colour.lower() + 's', alignment=QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                lastShot_ballCount = Ui_Label("0", alignment=QtCore.Qt.AlignCenter)
                curBallCount = Ui_Label("0", alignment=QtCore.Qt.AlignCenter)
                tempBallcount = Ui_Label("0", alignment=QtCore.Qt.AlignCenter)

                self.logger.last_shot_snapshot.colours[colour].countChanged.connect(lastShot_ballCount.setNum)
                self.logger.cur_shot_snapshot.colours[colour].countChanged.connect(curBallCount.setNum)

                self.layout.addWidget(label, start_row, 4, 1, 1)
                self.layout.addWidget(lastShot_ballCount, start_row, 5, 1, 1)
                self.layout.addWidget(curBallCount, start_row, 6, 1, 1)
                start_row += 1

        self.logger.white_statusChanged.connect(self.set_white_status)
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot()
    def on_clear_btn_pressed(self):
        self.logger.balls_potted.clear()

    def set_white_status(self, is_moving):
        if is_moving:
            self.whiteStatus.setText("moving...")
        else:
            self.whiteStatus.setText("stopped...")
