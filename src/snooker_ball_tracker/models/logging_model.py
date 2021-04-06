import PyQt5.QtCore as QtCore

from .logging import BallsPottedListModel, SnapshotModel


class LoggingModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._balls_potted = BallsPottedListModel(["Potted 1 red/s", "Potted 1 black/s"])
        self._white_status = "stopped..."
        self._last_shot_snapshot = SnapshotModel()
        self._cur_shot_snapshot = SnapshotModel()

    @property
    def balls_potted(self):
        return self._balls_potted

    @property
    def white_status(self):
        return self._white_status

    white_statusChanged = QtCore.pyqtSignal(str)

    @white_status.setter
    def white_status(self, value):
        self._white_status = value
        self.white_statusChanged.emit(self._white_status)

    @property
    def last_shot_snapshot(self):
        return self._last_shot_snapshot

    @property
    def cur_shot_snapshot(self):
        return self._cur_shot_snapshot
