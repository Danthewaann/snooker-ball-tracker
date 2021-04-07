import PyQt5.QtCore as QtCore

from .logging import BallsPotted, Snapshot


class Logger(QtCore.QObject):
    def __init__(self):
        """Creates an instance of this class that contains properties for logging
        output from the ball tracker"""
        super().__init__()
        self._balls_potted = BallsPotted()
        self._white_status = "stopped..."
        self._last_shot_snapshot = Snapshot()
        self._cur_shot_snapshot = Snapshot()

    @property
    def balls_potted(self) -> BallsPotted:
        """Balls potted property

        :return: balls potted list model
        :rtype: BallsPottedListModel
        """
        return self._balls_potted

    @property
    def white_status(self) -> str:
        """White status property

        :return: white status
        :rtype: str
        """
        return self._white_status

    white_statusChanged = QtCore.pyqtSignal(str)

    @white_status.setter
    def white_status(self, value: str):
        """White status setter

        :param value: value to set
        :type value: str
        """
        self._white_status = value
        self.white_statusChanged.emit(self._white_status)

    @property
    def last_shot_snapshot(self) -> Snapshot:
        """Last shot snapshot property

        :return: last shot snapshot model
        :rtype: SnapshotModel
        """
        return self._last_shot_snapshot

    @property
    def cur_shot_snapshot(self) -> Snapshot:
        """Current shot snapshot property

        :return: current shot snapshot model
        :rtype: SnapshotModel
        """
        return self._cur_shot_snapshot
