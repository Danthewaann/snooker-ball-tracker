from __future__ import annotations

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker import ColourDetectionSettings, Logger

from .components import Ui_Label, Ui_Line, Ui_PushButton


class LoggingView(QtWidgets.QGroupBox):
    def __init__(self, logger: Logger, colour_settings: ColourDetectionSettings):
        super().__init__("Logging")
        self.logger = logger
        self.colour_settings = colour_settings
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setSpacing(10)

        self.balls_potted_label = Ui_Label(
            "Balls Potted", alignment=QtCore.Qt.AlignCenter
        )
        self.balls_potted_list = QtWidgets.QListView()
        self.balls_potted_list.setAutoScroll(True)
        self.balls_potted_list.setModel(self.logger.balls_potted)

        self.logger.balls_potted.layoutChanged.connect(
            lambda: self.balls_potted_list.scrollToBottom()
        )
        self.clear_btn = Ui_PushButton("Clear", objectName="clear_btn")

        self.whiteStatus_label = Ui_Label(
            "White Ball Status:",
            alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
        )
        self.whiteStatus = Ui_Label(
            "stopped...",
            width=(0, 150),
            alignment=QtCore.Qt.AlignCenter,
            sizePolicy=(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Preferred,
            ),
        )
        self.lastShotCount_label = Ui_Label(
            "Last Shot\nSnapshot", alignment=QtCore.Qt.AlignCenter
        )
        self.curBallCount_label = Ui_Label(
            "Current\nSnapshot", alignment=QtCore.Qt.AlignCenter
        )

        self.layout.addWidget(self.balls_potted_label, 0, 0, 1, 4)
        self.layout.addWidget(self.balls_potted_list, 2, 0, 9, 4)
        self.layout.addWidget(self.clear_btn, 11, 0)
        self.layout.addWidget(self.whiteStatus_label, 0, 4, 1, 2)
        self.layout.addWidget(self.whiteStatus, 0, 6, 1, 1)
        self.layout.addWidget(Ui_Line(), 1, 0, 1, 7)
        self.layout.addWidget(self.lastShotCount_label, 2, 5, 1, 1)
        self.layout.addWidget(self.curBallCount_label, 2, 6, 1, 1)

        start_row = 3
        for colour, properties in self.colour_settings.settings["BALL_COLOURS"].items():
            if properties["DETECT"]:
                label = Ui_Label(
                    colour[0].upper() + colour[1:].lower() + "s",
                    alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter,
                )
                lastShot_ballCount = Ui_Label("0", alignment=QtCore.Qt.AlignCenter)
                curBallCount = Ui_Label("0", alignment=QtCore.Qt.AlignCenter)

                self.logger.last_shot_snapshot.colours[colour].countChanged.connect(
                    lastShot_ballCount.setNum
                )
                self.logger.cur_shot_snapshot.colours[colour].countChanged.connect(
                    curBallCount.setNum
                )

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
