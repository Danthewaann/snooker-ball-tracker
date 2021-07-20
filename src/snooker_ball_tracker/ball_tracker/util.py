from collections import namedtuple

import cv2
import imutils
import numpy as np
from snooker_ball_tracker.settings import settings as s

Image = namedtuple("Image", "frame binary_frame hsv_frame")


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


def get_mask_contours_for_colour(frame: np.ndarray, colour: str, 
                                 colour_settings: dict=s.COLOUR_DETECTION_SETTINGS["COLOURS"]) -> tuple:
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


def transform_frame(frame: np.ndarray, width: int) -> Image:
    """Performs initial operations on `frame` before it is properly processed

    :param frame: frame to process
    :type frame: np.ndarray
    :param width: width to resize frame to
    :type width: int
    :param morph: perform morphology to cleanup noise on binary frame, defaults to False
    :type morph: bool, optional
    :return: processed `frame`, binary version of `frame` and HSV version of `frame`
    :rtype: Image
    """
    if frame is not None:
        # resize the frame if width is provided
        frame = imutils.resize(frame, width=width)

        return frame

    return None
