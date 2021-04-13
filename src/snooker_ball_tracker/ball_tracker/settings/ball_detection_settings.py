import typing
from collections import OrderedDict
from copy import deepcopy

import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s

from .ball_detection_setting_group import BallDetectionSettingGroup


class BallDetectionSettings(QtCore.QObject):
    def __init__(self):
        """Creates and instance of this class that contains ball detection 
        properties used by the ball tracker"""
        super().__init__()
        self._blob_detector = deepcopy(s.BLOB_DETECTOR)
        self.groups = OrderedDict([
            ("convexity", BallDetectionSettingGroup("convexity")),
            ("inertia", BallDetectionSettingGroup("inertia")),
            ("circularity", BallDetectionSettingGroup("circularity")),
            ("area", BallDetectionSettingGroup("area", multiplier=1))
        ])

        for model in self.groups.values():
            model.filter_byChanged[str, bool].connect(self.update_blob_detector)
            model.min_valueChanged[str, int].connect(self.update_blob_detector)
            model.max_valueChanged[str, int].connect(self.update_blob_detector)

    @property
    def blob_detector(self) -> dict:
        """Copy of blob detector values loaded from settings

        :return: blob detector
        :rtype: dict
        """
        return self._blob_detector

    blob_detectorChanged = QtCore.pyqtSignal()

    @blob_detector.setter
    def blob_detector(self, value: dict):
        """Blob detector setter

        :param value: value to set
        :type value: dict
        """
        for model in self.groups.values():
            model.update(value)

    def update_blob_detector(self, key: str, value: typing.Any):
        """Update blob detector key value setting

        :param key: name of setting to update
        :type key: str
        :param value: value to apply to setting
        :type value: typing.Any
        """
        self._blob_detector[key] = value
        self.blob_detectorChanged.emit()
