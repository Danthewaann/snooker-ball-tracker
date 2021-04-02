import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

import snooker_ball_tracker.settings as s

class Model_SnapshotInfo(QtCore.QObject):
    def __init__(self, parent):
        super().__init__(parent)
        font = QtGui.QFont()
        font.setPointSize(11)

        self.setHorizontalSpacing(10)
        self.setVerticalSpacing(5)

        self.whiteStatus_label = QtWidgets.QLabel("White Ball Status", parent)
        self.whiteStatus_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.addWidget(self.whiteStatus_label, 0, 0, 1, 2)

        self.whiteStatus = QtWidgets.QLabel("stopped...", parent)
        self.whiteStatus.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.addWidget(self.whiteStatus, 0, 2, 1, 1)

        self.snapshot_horz_line1 = QtWidgets.QFrame(parent)
        self.snapshot_horz_line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.snapshot_horz_line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.addWidget(self.snapshot_horz_line1, 1, 0, 1, 3)

        self.lastShotCount_label = QtWidgets.QLabel("Last Shot Ball Count", parent)
        self.lastShotCount_label.setFont(font)
        self.lastShotCount_label.setAlignment(QtCore.Qt.AlignCenter)
        self.addWidget(self.lastShotCount_label, 2, 1, 1, 1)

        self.curBallCount_label = QtWidgets.QLabel("Current Ball Count", parent)
        self.curBallCount_label.setFont(font)
        self.curBallCount_label.setAlignment(QtCore.Qt.AlignCenter)
        self.addWidget(self.curBallCount_label, 2, 2, 1, 1)

        self.snapshot_horz_line2 = QtWidgets.QFrame(parent)
        self.snapshot_horz_line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.snapshot_horz_line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.addWidget(self.snapshot_horz_line2, 11, 0, 1, 3)

        start_row = 3
        for colour in s.DETECT_COLOURS:
            if s.DETECT_COLOURS[colour]:
                label = QtWidgets.QLabel(colour.lower() + 's', parent)
                label.setFont(font)
                label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
                self.addWidget(label, start_row, 0, 1, 1)

                lastShot_ballCount = QtWidgets.QLabel("0", parent)

                lastShot_ballCount.setFont(font)
                lastShot_ballCount.setAlignment(QtCore.Qt.AlignCenter)
                self.addWidget(lastShot_ballCount, start_row, 1, 1, 1)

                curBallCount = QtWidgets.QLabel("0", parent)
                curBallCount.setFont(font)
                curBallCount.setAlignment(QtCore.Qt.AlignCenter)
                self.addWidget(curBallCount, start_row, 2, 1, 1)
                start_row += 1
