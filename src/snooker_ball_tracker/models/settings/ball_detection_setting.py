import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s


class BallDetectionSettingModel(QtCore.QObject):
    def __init__(self, name: str, multiplier: int=100):
        """Creates an instance of this class that contains properties for a specific 
        setting group that is used for ball detection by the ball tracker

        :param name: name of ball detection setting group
        :type name: str
        :param multiplier: multiplier used to scale min/max values for sliders, defaults to 100
        :type multiplier: int, optional
        """
        super().__init__()
        self._name = name
        self._multiplier = multiplier
        self._min_value = 0
        self._max_value = 0
        self._filter_by = False

    @property
    def name(self) -> str:
        """Name property

        :return: name
        :rtype: str
        """
        return self._name

    @property
    def multiplier(self) -> int:
        """Multiplier property used to scale min/max values for sliders

        :return: multiplier
        :rtype: int
        """
        return self._multiplier

    @property
    def min_value(self) -> int:
        """Min value property

        :return: min value
        :rtype: int
        """
        return self._min_value

    min_valueChanged = QtCore.pyqtSignal(int, name="min_valueChanged")

    @min_value.setter
    def min_value(self, value: int):
        """Min value setter

        :param value: value to set
        :type value: int
        """
        self._min_value = value
        self.min_valueChanged.emit(self._min_value)

    @property
    def max_value(self) -> int:
        """Max value property

        :return: max value
        :rtype: int
        """
        return self._max_value

    max_valueChanged = QtCore.pyqtSignal(int, name="max_valueChanged")

    @max_value.setter
    def max_value(self, value: int):
        """Max value setter

        :param value: value to set
        :type value: int
        """
        self._max_value = value
        self.max_valueChanged.emit(self._max_value)

    @property
    def filter_by(self) -> bool:
        """Filter by property

        :return: filter by
        :rtype: bool
        """
        return self._filter_by

    filter_byChanged = QtCore.pyqtSignal(bool, name="filter_byChanged")

    @filter_by.setter
    def filter_by(self, value: bool):
        """Filter by setter

        :param value: value to set
        :type value: int
        """
        self._filter_by = value
        self.filter_byChanged.emit(self._filter_by)

    def update(self, settings: dict):
        """Update properties with values in `settings`

        :param settings: settings to obtain values from
        :type settings: dict
        """
        self.min_value = settings["MIN_" + self._name.upper()] * self._multiplier
        self.max_value = settings["MAX_" + self._name.upper()] * self._multiplier
        self.filter_by = settings["FILTER_BY_" + self._name.upper()]

    def reset(self):
        """Reset properties to their previous values from settings"""
        self.min_value = s.BLOB_DETECTOR["MIN_" + self._name.upper()] * self._multiplier
        self.max_value = s.BLOB_DETECTOR["MAX_" + self._name.upper()] * self._multiplier
        self.filter_by = s.BLOB_DETECTOR["FILTER_BY_" + self._name.upper()]
