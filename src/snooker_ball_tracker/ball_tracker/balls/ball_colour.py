from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

import PyQt5.QtCore as QtCore

from .ball import Ball

if TYPE_CHECKING:
    import cv2


class BallColour(QtCore.QObject):
    def __init__(self, keypoints: list[cv2.Keypoint] | None = None):
        """Creates an instance of this class that keeps track of the balls
        for a specific colour

        :param keypoints: lists of balls to manage, defaults to None
        """
        super().__init__()
        if keypoints:
            self._balls = [Ball(pt) for pt in keypoints]
        else:
            self._balls = []

    @property
    def balls(self) -> list[Ball]:
        """Balls property

        :return: balls list
        """
        return self._balls

    @property
    def count(self) -> int:
        """Count of balls

        :return: count
        """
        return len(self._balls)

    countChanged = QtCore.pyqtSignal(int)

    def clear(self) -> None:
        """Clear underlying balls list"""
        self._balls.clear()
        self.countChanged.emit(self.count)

    def assign(self, balls: list[Ball]) -> None:
        """Override own Ball list with `balls`

        :param balls: list of Ball instances
        """
        self._balls.clear()
        self._balls = deepcopy(balls)
        self.countChanged.emit(self.count)
