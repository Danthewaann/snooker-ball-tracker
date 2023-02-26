from __future__ import annotations

from collections import OrderedDict
from copy import deepcopy
from typing import Any

import PyQt5.QtCore as QtCore

from snooker_ball_tracker.settings import settings as s

from .ball_detection_setting_group import BallDetectionSettingGroup


class BallDetectionSettings(QtCore.QObject):
    def __init__(self) -> None:
        """Creates and instance of this class that contains ball detection
        properties used by the ball tracker"""
        super().__init__()
        self._settings: dict[str, Any] = deepcopy(s.BALL_DETECTION_SETTINGS)
        self.groups = OrderedDict(
            [
                ("convexity", BallDetectionSettingGroup("convexity")),
                ("inertia", BallDetectionSettingGroup("inertia")),
                ("circularity", BallDetectionSettingGroup("circularity")),
                ("area", BallDetectionSettingGroup("area", multiplier=1)),
            ]
        )

        for model in self.groups.values():
            model.filter_byChanged[str, bool].connect(self.update_settings)
            model.min_valueChanged[str, int].connect(self.update_settings)
            model.max_valueChanged[str, int].connect(self.update_settings)

    settingsChanged = QtCore.pyqtSignal()

    @property
    def settings(self) -> dict[str, Any]:
        """Copy of ball detection settings loaded from settings

        :return: blob detector
        """
        return self._settings

    @settings.setter
    def settings(self, value: dict[str, Any]) -> None:
        """Settings setter

        :param value: value to set
        """
        for model in self.groups.values():
            model.update(value)

    def update_settings(self, key: str, value: Any) -> None:
        """Update settings key value setting

        :param key: name of setting to update
        :param value: value to apply to setting
        """
        self._settings[key] = value
        self.settingsChanged.emit()
