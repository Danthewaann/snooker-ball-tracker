import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s


class VideoPlayerModel(QtCore.QObject):
    def __init__(self):
        """Creates an instance of this class that contains properties used by the
        video player to display frames processed by the ball tracker"""
        super().__init__()
        self._crop_frames = False
        self._show_threshold = False

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
