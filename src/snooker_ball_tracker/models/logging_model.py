import PyQt5.QtCore as QtCore


class BallCountModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._count = 0

    @property
    def count(self):
        return self._count

    countChanged = QtCore.pyqtSignal(int)

    @count.setter
    def count(self, value):
        self._count = value
        self.countChanged.emit(self._count)


class SnapshotModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._whites = BallCountModel()
        self._reds = BallCountModel()
        self._yellows = BallCountModel()
        self._greens = BallCountModel()
        self._browns = BallCountModel()
        self._blues = BallCountModel()
        self._pinks = BallCountModel()
        self._blacks = BallCountModel()

    @property
    def whites(self):
        return self._whites

    @property
    def reds(self):
        return self._reds

    @property
    def yellows(self):
        return self._yellows

    @property
    def greens(self):
        return self._greens

    @property
    def browns(self):
        return self._browns

    @property
    def blues(self):
        return self._blues

    @property
    def pinks(self):
        return self._pinks

    @property
    def blacks(self):
        return self._blacks


class BallsPottedListModel(QtCore.QAbstractListModel):
    def __init__(self, balls_potted=None):
        super().__init__()
        self._balls_potted = balls_potted or []

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            text = self._balls_potted[index.row()]
            return text

    def rowCount(self, index):
        return len(self._balls_potted)

    def appendData(self, data):
        self._balls_potted.append(data)
        self.layoutChanged.emit()

    def clear(self):
        self._balls_potted.clear()
        self.layoutChanged.emit()


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
