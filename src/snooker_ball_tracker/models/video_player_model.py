import numpy as np
import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s


class VideoPlayerModel(QtCore.QObject):
    def __init__(self):
        """Creates an instance of this class that contains properties used by the
        video player to display frames processed by the ball tracker"""
        super().__init__()
        self._player_width = 1000
        self._play_video = False
        self._restart_video = False
        self._crop_frames = False
        self._show_threshold = False
        self._perform_morph = False
        self._detect_table = False
        self._frame = np.array([])

    @property
    def player_width(self) -> int:
        """Player width property

        :return: player width
        :rtype: int
        """
        return self._player_width

    player_widthChanged = QtCore.pyqtSignal(int)

    @player_width.setter
    def player_width(self, value: int):
        """Player width setter

        :param value: value to set
        :type value: int
        """
        self._player_width = value
        self.player_widthChanged.emit(self._player_width)

    @property
    def play_video(self) -> bool:
        """Play video property

        :return: play video
        :rtype: bool
        """
        return self._play_video

    play_videoChanged = QtCore.pyqtSignal(bool)

    @play_video.setter
    def play_video(self, value: bool):
        """Play video setter

        :param value: value to set
        :type value: bool
        """
        self._play_video = value
        self.play_videoChanged.emit(self._play_video)

    @property
    def restart_video(self) -> bool:
        """Restart video property

        :return: restart video
        :rtype: bool
        """
        return self._restart_video

    restart_videoChanged = QtCore.pyqtSignal(bool)

    @restart_video.setter
    def restart_video(self, value: bool):
        """Restart video setter

        :param value: value to set
        :type value: bool
        """
        self._restart_video = value
        self.restart_videoChanged.emit(self._restart_video)

    @property
    def crop_frames(self) -> bool:
        """Crop frames property

        :return: crop frames
        :rtype: bool
        """
        return self._crop_frames

    crop_framesChanged = QtCore.pyqtSignal(bool)

    @crop_frames.setter
    def crop_frames(self, value: bool):
        """Crop frames setter

        :param value: value to set
        :type value: bool
        """
        self._crop_frames = value
        self.crop_framesChanged.emit(self._crop_frames)

    @property
    def show_threshold(self) -> bool:
        """Show threshold property

        :return: show threshold
        :rtype: bool
        """
        return self._show_threshold

    show_thresholdChanged = QtCore.pyqtSignal(bool)

    @show_threshold.setter
    def show_threshold(self, value: bool):
        """Show threshold setter

        :param value: value to set
        :type value: bool
        """
        self._show_threshold = value
        self.show_thresholdChanged.emit(self._show_threshold)

    @property
    def perform_morph(self) -> bool:
        """Perform morph property

        :return: perform morph
        :rtype: bool
        """
        return self._perform_morph

    perform_morphChanged = QtCore.pyqtSignal(bool)

    @perform_morph.setter
    def perform_morph(self, value: bool):
        self._perform_morph = value
        self.perform_morphChanged.emit(self._perform_morph)

    @property
    def detect_table(self) -> bool:
        """Detect table property

        :return: detect table
        :rtype: bool
        """
        return self._detect_table

    detect_tableChanged = QtCore.pyqtSignal(bool)

    @detect_table.setter
    def detect_table(self, value: bool):
        """Detect table setter

        :param value: value to set
        :type value: bool
        """
        self._detect_table = value
        self.detect_tableChanged.emit(self._detect_table)

    @property
    def frame(self) -> np.ndarray:
        """Frame property

        :return: frame
        :rtype: np.ndarray
        """
        return self._frame

    frameChanged = QtCore.pyqtSignal(np.ndarray)

    @frame.setter
    def frame(self, value: np.ndarray):
        """Frame setter

        :param value: value to set
        :type value: np.ndarray
        """
        self._frame = value
        self.frameChanged.emit(self._frame)
