from __future__ import annotations

from typing import Any

import cv2
import PyQt5.QtCore as QtCore


class Ball(QtCore.QObject):

    is_movingChanged = QtCore.pyqtSignal(bool)

    def __init__(self, keypoint: cv2.KeyPoint | None = None) -> None:
        """Creates an instance of this class that keeps track of an individual ball

        :param keypoint: keypoint of ball, defaults to None
        """
        super().__init__()
        self._keypoint = keypoint
        self._is_moving = False

    def __deepcopy__(self, memo: dict[str, Any]) -> Ball:
        """Return a deepcopy of self

        :param memo: memo
        :return: Ball instance copy of self
        """
        if self._keypoint:
            keypoint = cv2.KeyPoint(
                x=self._keypoint.pt[0],
                y=self._keypoint.pt[1],
                _size=self._keypoint.size,
                _angle=self._keypoint.angle,
                _response=self._keypoint.response,
                _octave=self._keypoint.octave,
                _class_id=self._keypoint.class_id,
            )
            ball = Ball(keypoint)
            ball.is_moving = self._is_moving
        else:
            ball = Ball()
        return ball

    @property
    def keypoint(self) -> cv2.KeyPoint:
        """Keypoint property

        :return: keypoint
        """
        return self._keypoint

    @property
    def is_moving(self) -> bool:
        """Count of balls

        :return: count
        """
        return self._is_moving

    @is_moving.setter
    def is_moving(self, value: bool) -> None:
        """Count setter

        :param value: value to set
        """
        self._is_moving = value
        self.is_movingChanged.emit(self._is_moving)
