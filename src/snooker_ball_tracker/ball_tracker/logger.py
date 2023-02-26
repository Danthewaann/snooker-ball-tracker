import PyQt5.QtCore as QtCore

from .balls import BallsPotted
from .snapshot import SnapShot


class Logger(QtCore.QObject):
    def __init__(self) -> None:
        """Creates an instance of this class that contains properties for logging
        output from the ball tracker"""
        super().__init__()
        self._balls_potted = BallsPotted()
        self._last_shot_snapshot = SnapShot()
        self._cur_shot_snapshot = SnapShot()
        self._temp_snapshot = SnapShot()

    @property
    def balls_potted(self) -> BallsPotted:
        """Balls potted property

        :return: balls potted list model
        """
        return self._balls_potted

    @property
    def white_status(self) -> bool:
        """White status property

        :return: white status
        """
        return (
            self._cur_shot_snapshot.white.is_moving
            if self._cur_shot_snapshot.white
            else False
        )

    white_statusChanged = QtCore.pyqtSignal(bool)

    def set_white_status(self, value: bool) -> None:
        """White status setter

        :param value: value to set
        """
        if self._cur_shot_snapshot.white:
            self._cur_shot_snapshot.white.is_moving = value
            self.white_statusChanged.emit(value)

    @property
    def last_shot_snapshot(self) -> SnapShot:
        """Last shot snapshot property

        :return: last shot snapshot model
        """
        return self._last_shot_snapshot

    @property
    def cur_shot_snapshot(self) -> SnapShot:
        """Current shot snapshot property

        :return: current shot snapshot model
        """
        return self._cur_shot_snapshot

    @property
    def temp_snapshot(self) -> SnapShot:
        """Temporary snapshot property

        :return: temp shot snapshot model
        """
        return self._temp_snapshot
