import typing
from copy import deepcopy

import PyQt5.QtCore as QtCore

from .ball import Ball


class BallColour(QtCore.QObject):
    def __init__(self, keypoints: list=None):
        """Creates an instance of this class that keeps track of the balls
        for a specific colour

        :param keypoints: lists of balls to manage, defaults to None
        :type keypoints: list, optional
        """
        super().__init__()
        if keypoints:
            self._balls = [Ball(pt) for pt in keypoints]
        else:
            self._balls = []

    @property
    def balls(self) -> typing.List[Ball]:
        """Balls property

        :return: balls list
        :rtype: typing.List[Ball]
        """
        return self._balls

    @property
    def count(self) -> int:
        """Count of balls

        :return: count
        :rtype: int
        """
        return len(self._balls)

    countChanged = QtCore.pyqtSignal(int)

    def clear(self):
        """Clear underlying balls list"""
        self._balls.clear()
        self.countChanged.emit(self.count)

    def assign(self, balls: typing.List[Ball]):
        """Override own Ball list with `balls`

        :param balls: list of Ball instances
        :type balls: typing.List[Ball]
        """
        self._balls.clear()
        self._balls = deepcopy(balls)
        self.countChanged.emit(self.count)
