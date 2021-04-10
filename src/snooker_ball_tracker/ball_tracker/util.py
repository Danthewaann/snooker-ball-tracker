import cv2
import numpy as np
import settings as s


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


def get_mask_contours_for_colour(frame: np.ndarray, colour: str, colour_settings: dict=s.COLOURS) -> tuple:
    """Obtains the colour mask of `colour` from `frame`

    :param frame: frame to process
    :type frame: np.ndarray
    :param colour: colour to extract contours from `frame`
    :type colour: str
    :param colour_settings: colours settings to obtain colour values from, defaults to s.COLOURS
    :type colour_settings: dict, optional
    :return: colour mask of `colour` and a list of contours
    :rtype: tuple
    """
    colour_mask = None
    contours = None
    if colour in colour_settings:
        colour_mask = cv2.inRange(
            frame, colour_settings[colour]['LOWER'],
            colour_settings[colour]['UPPER']
        )
        contours, _ = cv2.findContours(
            colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
    return colour_mask, contours
