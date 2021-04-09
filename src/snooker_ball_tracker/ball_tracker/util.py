import cv2
import numpy as np


def dist_between_two_balls(first_ball: cv2.KeyPoint, second_ball: cv2.KeyPoint) -> float:
    """Obtains the distance between two balls in millimetres

    :param first_ball: first ball
    :type first_ball: cv2.KeyPoint
    :param second_ball: second ball
    :type second_ball: cv2.KeyPoint
    :return: distance between `first_ball` and `second_ball` in millimetres
    :rtype: float
    """
    # create numpy array with keypoint positions
    arr = np.array([first_ball.pt, second_ball.pt])
    # scale array to mm
    arr = arr * 40 / 1280
    # return distance, calculated by pythagoras
    return np.sqrt(np.sum((arr[0] - arr[1]) ** 2))
