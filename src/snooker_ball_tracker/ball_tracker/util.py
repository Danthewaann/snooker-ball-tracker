import numpy as np


def dist_between_two_balls(ball_1, ball_2):
    """
    Obtains the distance between two balls in millimetres

    :param ball_1: first ball
    :param ball_2: second ball
    :returns: distance between `ball_1` and `ball_2` in millimetres
    """
    # create numpy array with keypoint positions
    arr = np.array([ball_1.pt, ball_2.pt])
    # scale array to mm
    arr = arr * 40 / 1280
    # return distance, calculated by pythagoras
    return np.sqrt(np.sum((arr[0] - arr[1]) ** 2))