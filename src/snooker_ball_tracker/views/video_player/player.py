import numpy as np
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker import ColourDetectionSettings, VideoPlayer

from ..actions import select_video_file_action
from ..components import Ui_Label, Ui_PushButton


class Player(QtWidgets.QFrame):
    def __init__(self, video_player: VideoPlayer, colours: ColourDetectionSettings):
        super().__init__()
        self.video_player = video_player
        self.colours = colours

        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
            )
        )
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.selectVideoFile_btn = Ui_PushButton(
            "Select Video File",
            parent=self,
            sizePolicy=QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            ),
        )
        self.output_frame = Ui_Label("", parent=self)
        self.output_frame.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.output_frame.mousePressEvent = self.output_frame_onclick

        self.selectVideoFile_btn.pressed.connect(self.select_video_file_btn_pressed)

        self.layout.addWidget(self.selectVideoFile_btn)
        self.video_player.output_frameChanged.connect(self.display_output_frame)
        self.video_player.heightChanged.connect(self.setMaximumHeight)

    def select_video_file_btn_pressed(self):
        try:
            video_file = select_video_file_action()
            if video_file:
                self.video_player.start(video_file)
        except TypeError as exc:
            print(exc)
            error = QtWidgets.QMessageBox(None)
            error.setWindowTitle("Invalid Video File!")
            error.setText("Invalid file, please select a video file!")
            error.exec_()

    def output_frame_onclick(self, event: QtGui.QMouseEvent):
        if self.colours.selected_colour != "NONE":
            x = event.pos().x()
            y = event.pos().y()

            lower_y = y - 5 if y - 5 >= 0 else 0
            upper_y = (
                y + 5 if y + 5 < self.video_player.height else self.video_player.height
            )

            lower_x = x - 5 if x - 5 >= 0 else 0
            upper_x = (
                x + 5 if x + 5 < self.video_player.width else self.video_player.width
            )

            pixels = self.video_player.hsv_frame[lower_y:upper_y, lower_x:upper_x]
            min_pixel = np.min(pixels, axis=0)[0]
            max_pixel = np.max(pixels, axis=0)[0]

            colour = {"LOWER": min_pixel, "UPPER": max_pixel}

            self.colours.colour_model.update(colour)

    def display_output_frame(self, output_frame):
        self.layout.removeWidget(self.selectVideoFile_btn)
        self.layout.addWidget(self.output_frame, alignment=QtCore.Qt.AlignCenter)
        self.setStyleSheet("background-color: black")
        output_frame = QtGui.QImage(
            output_frame.data,
            output_frame.shape[1],
            output_frame.shape[0],
            QtGui.QImage.Format_RGB888,
        ).rgbSwapped()
        self.output_frame.setPixmap(QtGui.QPixmap.fromImage(output_frame))
