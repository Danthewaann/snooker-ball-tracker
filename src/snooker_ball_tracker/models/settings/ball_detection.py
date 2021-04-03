import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import snooker_ball_tracker.settings as s

from collections import OrderedDict


class BallDetectionSettingGroupModel(QtCore.QObject):
    def __init__(self, name, parent=None, multiplier=100):
        super().__init__(parent)
        self._name = name
        self._multiplier = multiplier
        self._min_value = 0
        self._max_value = 0
        self._filter_by = False

    min_valueChanged = QtCore.pyqtSignal(int, name="min_valueChanged")
    max_valueChanged = QtCore.pyqtSignal(int, name="max_valueChanged")
    filter_byChanged = QtCore.pyqtSignal(bool, name="filter_byChanged")

    @property
    def name(self):
        return self._name

    @property
    def multiplier(self):
        return self._multiplier

    @property
    def min_value(self):
        return self._min_value

    @min_value.setter
    def min_value(self, value):
        self._min_value = value
        self.min_valueChanged.emit(self._min_value)

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        self._max_value = value
        self.max_valueChanged.emit(self._max_value)

    @property
    def filter_by(self):
        return self._filter_by

    @filter_by.setter
    def filter_by(self, value):
        """ C++: int setFilterBy(int) """
        self._filter_by = value
        self.filter_byChanged.emit(self._filter_by)

    def reset(self):
        self.setMinValue(s.BLOB_DETECTOR["MIN_" + self._name.upper()] * self._multiplier)
        self.setMaxValue(s.BLOB_DETECTOR["MAX_" + self._name.upper()] * self._multiplier)
        self.setFilterBy(s.BLOB_DETECTOR["FILTER_BY_" + self._name.upper()])


class BallDetectionTabModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.models = OrderedDict([
            ("convexity", BallDetectionSettingGroupModel("convexity", multiplier=100)),
            ("inertia", BallDetectionSettingGroupModel("inertia", multiplier=100)),
            ("circularity", BallDetectionSettingGroupModel("circularity", multiplier=100)),
            ("area", BallDetectionSettingGroupModel("area"))
        ])

    def reset_model(self, model):
        self.models[model].reset()
