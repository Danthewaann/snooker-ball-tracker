from __future__ import annotations

from typing import Any

import PyQt5.QtCore as QtCore

from snooker_ball_tracker.settings import settings as s


class BallDetectionSettingGroup(QtCore.QObject):
    def __init__(self, name: str, multiplier: int = 100) -> None:
        """Creates an instance of this class that contains properties for a specific
        setting group that is used for ball detection by the ball tracker

        :param name: name of ball detection setting group
        :param multiplier: multiplier used to scale min/max values for sliders,
                           defaults to 100
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
        """
        return self._name

    @property
    def multiplier(self) -> int:
        """Multiplier property used to scale min/max values for sliders

        :return: multiplier
        """
        return self._multiplier

    min_valueChanged = QtCore.pyqtSignal([str, int], [int])

    @property
    def min_value(self) -> int:
        """Min value property

        :return: min value
        """
        return self._min_value

    @min_value.setter
    def min_value(self, value: int) -> None:
        """Min value setter

        :param value: value to set
        """
        self._min_value = value
        self.min_valueChanged[str, int].emit(
            "MIN_" + self.name.upper(), self._min_value / self.multiplier
        )
        self.min_valueChanged[int].emit(self._min_value)

    max_valueChanged = QtCore.pyqtSignal([str, int], [int])

    @property
    def max_value(self) -> int:
        """Max value property

        :return: max value
        """
        return self._max_value

    @max_value.setter
    def max_value(self, value: int) -> None:
        """Max value setter

        :param value: value to set
        """
        self._max_value = value
        self.max_valueChanged[str, int].emit(
            "MAX_" + self.name.upper(), self._max_value / self.multiplier
        )
        self.max_valueChanged[int].emit(self._max_value)

    filter_byChanged = QtCore.pyqtSignal([str, bool], [bool])

    @property
    def filter_by(self) -> bool:
        """Filter by property

        :return: filter by
        """
        return self._filter_by

    @filter_by.setter
    def filter_by(self, value: bool) -> None:
        """Filter by setter

        :param value: value to set
        """
        self._filter_by = value
        self.filter_byChanged[str, bool].emit(
            "FILTER_BY_" + self.name.upper(), self._filter_by
        )
        self.filter_byChanged[bool].emit(self._filter_by)

    def update(self, settings: dict[str, Any]) -> None:
        """Update properties with values in `settings`

        :param settings: settings to obtain values from
        """
        self.min_value = settings["MIN_" + self._name.upper()] * self._multiplier
        self.max_value = settings["MAX_" + self._name.upper()] * self._multiplier
        self.filter_by = settings["FILTER_BY_" + self._name.upper()]

    def reset(self) -> None:
        """Reset properties to their previous values from settings"""
        self.min_value = (
            s.BALL_DETECTION_SETTINGS["MIN_" + self._name.upper()] * self._multiplier
        )
        self.max_value = (
            s.BALL_DETECTION_SETTINGS["MAX_" + self._name.upper()] * self._multiplier
        )
        self.filter_by = s.BALL_DETECTION_SETTINGS["FILTER_BY_" + self._name.upper()]
