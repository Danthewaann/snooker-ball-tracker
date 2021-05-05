import typing
from collections import OrderedDict
from copy import deepcopy

import PyQt5.QtCore as QtCore
from snooker_ball_tracker.settings import settings as s

from .ball_detection_setting_group import BallDetectionSettingGroup


class BallDetectionSettings(QtCore.QObject):
    def __init__(self):
        """Creates and instance of this class that contains ball detection 
        properties used by the ball tracker"""
        super().__init__()
        self._settings = deepcopy(s.BALL_DETECTION_SETTINGS)
        self.groups = OrderedDict([
            ("convexity", BallDetectionSettingGroup("convexity")),
            ("inertia", BallDetectionSettingGroup("inertia")),
            ("circularity", BallDetectionSettingGroup("circularity")),
            ("area", BallDetectionSettingGroup("area", multiplier=1))
        ])

        for model in self.groups.values():
            model.filter_byChanged[str, bool].connect(self.update_settings)
            model.min_valueChanged[str, int].connect(self.update_settings)
            model.max_valueChanged[str, int].connect(self.update_settings)

    @property
    def settings(self) -> dict:
        """Copy of ball detection settings loaded from settings

        :return: blob detector
        :rtype: dict
        """
        return self._settings

    settingsChanged = QtCore.pyqtSignal()

    @settings.setter
    def settings(self, value: dict):
        """Settings setter

        :param value: value to set
        :type value: dict
        """
        for model in self.groups.values():
            model.update(value)

    def update_settings(self, key: str, value: typing.Any):
        """Update settings key value setting

        :param key: name of setting to update
        :type key: str
        :param value: value to apply to setting
        :type value: typing.Any
        """
        self._settings[key] = value
        self.settingsChanged.emit()
