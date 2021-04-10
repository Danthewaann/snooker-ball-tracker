import numpy as np
import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s


class VideoPlayer(QtCore.QObject):
    def __init__(self):
        """Creates an instance of this class that contains properties used by the
        video player to display frames processed by the ball tracker"""
        super().__init__()
        self._width = 1000
        self._play = False
        self._restart = False
        self._crop_frames = False
        self._show_threshold = False
        self._perform_morph = False
        self._detect_table = False
        self._queue_size = 0
        self._fps = 0
        self._frame = np.array([])
        self._hsv_frame = np.array([])

    @property
    def width(self) -> int:
        """Width property

        :return: player width
        :rtype: int
        """
        return self._width

    widthChanged = QtCore.pyqtSignal(int)

    @width.setter
    def width(self, value: int):
        """Width setter

        :param value: value to set
        :type value: int
        """
        self._width = value
        self.widthChanged.emit(self._width)

    @property
    def play(self) -> bool:
        """Play property

        :return: play video
        :rtype: bool
        """
        return self._play

    playChanged = QtCore.pyqtSignal(bool)

    @play.setter
    def play(self, value: bool):
        """Play setter

        :param value: value to set
        :type value: bool
        """
        self._play = value
        self.playChanged.emit(self._play)

    @property
    def restart(self) -> bool:
        """Restart property

        :return: restart video
        :rtype: bool
        """
        return self._restart

    restartChanged = QtCore.pyqtSignal(bool)

    @restart.setter
    def restart(self, value: bool):
        """Restart setter

        :param value: value to set
        :type value: bool
        """
        self._restart = value
        self.play = False
        self.restartChanged.emit(self._restart)

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
        """Perform morph setter

        :param value: value to set
        :type value: bool
        """
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
    def queue_size(self) -> int:
        """Queue size property

        :return: queue size
        :rtype: int
        """
        return self._queue_size

    queue_sizeChanged = QtCore.pyqtSignal(int)

    @queue_size.setter
    def queue_size(self, value: int):
        """Queue size setter

        :param value: value to set
        :type value: int
        """
        self._queue_size = value
        self.queue_sizeChanged.emit(self._queue_size)

    @property
    def fps(self) -> int:
        """FPS property

        :return: fps
        :rtype: int
        """
        return self._fps

    fpsChanged = QtCore.pyqtSignal(int)

    @fps.setter
    def fps(self, value: int):
        """FPS setter

        :param value: value to set
        :type value: int
        """
        self._fps = value
        self.fpsChanged.emit(self._fps)

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

    @property
    def hsv_frame(self) -> np.ndarray:
        """HSV frame property

        :return: hsv frame
        :rtype: np.ndarray
        """
        return self._hsv_frame

    hsv_frameChanged = QtCore.pyqtSignal(np.ndarray)

    @hsv_frame.setter
    def hsv_frame(self, value: np.ndarray):
        """HSV frame setter

        :param value: value to set
        :type value: np.ndarray
        """
        self._hsv_frame = value
        self.hsv_frameChanged.emit(self._hsv_frame)
