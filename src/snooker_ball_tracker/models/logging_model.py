import PyQt5.QtCore as QtCore

from .logging import BallsPottedListModel, SnapshotModel


class LoggingModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._balls_potted = BallsPottedListModel()
        self._white_status = "stopped..."
        self._last_shot_snapshot = SnapshotModel()
        self._cur_shot_snapshot = SnapshotModel()

    @property
    def balls_potted(self) -> BallsPottedListModel:
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
    def last_shot_snapshot(self) -> SnapshotModel:
        """Last shot snapshot property

        :return: last shot snapshot model
        :rtype: SnapshotModel
        """
        return self._last_shot_snapshot

    @property
    def cur_shot_snapshot(self) -> SnapshotModel:
        """Current shot snapshot property

        :return: current shot snapshot model
        :rtype: SnapshotModel
        """
        return self._cur_shot_snapshot
