import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s


class BallDetectionSettingModel(QtCore.QObject):
    def __init__(self, name, parent=None, multiplier=100):
        super().__init__(parent)
        self._name = name
        self._multiplier = multiplier
        self._min_value = 0
        self._max_value = 0
        self._filter_by = False

    @property
    def name(self):
        return self._name

    @property
    def multiplier(self):
        return self._multiplier

    @property
    def min_value(self):
        return self._min_value

    min_valueChanged = QtCore.pyqtSignal(int, name="min_valueChanged")

    @min_value.setter
    def min_value(self, value):
        self._min_value = value
        self.min_valueChanged.emit(self._min_value)

    @property
    def max_value(self):
        return self._max_value

    max_valueChanged = QtCore.pyqtSignal(int, name="max_valueChanged")

    @max_value.setter
    def max_value(self, value):
        self._max_value = value
        self.max_valueChanged.emit(self._max_value)

    @property
    def filter_by(self):
        return self._filter_by

    filter_byChanged = QtCore.pyqtSignal(bool, name="filter_byChanged")

    @filter_by.setter
    def filter_by(self, value):
        self._filter_by = value
        self.filter_byChanged.emit(self._filter_by)

    def reset(self):
        self.min_value = (s.BLOB_DETECTOR["MIN_" + self._name.upper()] * self._multiplier)
        self.max_value = (s.BLOB_DETECTOR["MAX_" + self._name.upper()] * self._multiplier)
        self.filter_by = (s.BLOB_DETECTOR["FILTER_BY_" + self._name.upper()])
