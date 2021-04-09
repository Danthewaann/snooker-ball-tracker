import cv2
import PyQt5.QtCore as QtCore
from copy import copy


class Ball(QtCore.QObject):

    is_movingChanged = QtCore.pyqtSignal(int)

    def __init__(self, keypoint: cv2.KeyPoint=None):
        """Creates an instance of this class that keeps track of an individual ball

        :param keypoint: keypoint of ball, defaults to None
        :type keypoint: cv2.KeyPoint, optional
        """
        super().__init__()
        self._keypoint = keypoint
        self._is_moving = False

    def __deepcopy__(self, memo):
        keypoint = cv2.KeyPoint(x = self._keypoint.pt[0], y = self._keypoint.pt[1], 
            _size = self._keypoint.size, _angle = self._keypoint.angle, 
            _response = self._keypoint.response, _octave = self._keypoint.octave, 
            _class_id = self._keypoint.class_id)
        ball = Ball(keypoint)
        ball.is_moving = self._is_moving
        return ball

    @property
    def keypoint(self) -> cv2.KeyPoint:
        return self._keypoint

    @property
    def is_moving(self) -> int:
        """Count of balls

        :return: count
        :rtype: int
        """
        return self._is_moving

    @is_moving.setter
    def is_moving(self, value: int):
        """Count setter

        :param value: value to set
        :type value: int
        """
        self._is_moving = value
        self.is_movingChanged.emit(self._is_moving)
