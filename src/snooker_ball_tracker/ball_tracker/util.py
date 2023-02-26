from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import cv2
import imutils
import numpy as np
import numpy.typing as npt

from snooker_ball_tracker.settings import settings as s

if TYPE_CHECKING:
    from .types import Frame


def dist_between_two_balls(
    first_ball: cv2.KeyPoint, second_ball: cv2.KeyPoint
) -> float:
    """Obtains the distance between two balls in millimetres

    :param first_ball: first ball
    :param second_ball: second ball
    :return: distance between `first_ball` and `second_ball` in millimetres
    """
    # create numpy array with keypoint positions
    arr: npt.NDArray[np.float64] = np.array([first_ball.pt, second_ball.pt])
    # scale array to mm
    arr = cast(npt.NDArray[np.float64], arr * 40 / 1280)
    # return distance, calculated by pythagoras
    dist: float = np.sqrt(np.sum((arr[0] - arr[1]) ** 2))
    return dist


def get_mask_contours_for_colour(
    frame: Frame,
    colour: str,
    colour_settings: dict[str, Any] = s.COLOUR_DETECTION_SETTINGS["COLOURS"],
) -> tuple[Frame | None, list[cv2.KeyPoint] | None]:
    """Obtains the colour mask of `colour` from `frame`

    :param frame: frame to process
    :param colour: colour to extract contours from `frame`
    :param colour_settings: colours settings to obtain colour values from,
                            defaults to s.COLOURS
    :return: colour mask of `colour` and a list of contours
    """
    colour_mask = None
    contours = None
    if colour in colour_settings:
        colour_mask = cv2.inRange(
            frame, colour_settings[colour]["LOWER"], colour_settings[colour]["UPPER"]
        )
        contours, _ = cv2.findContours(
            colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
    return colour_mask, contours


def transform_frame(frame: Frame | None, width: int) -> Frame | None:
    """Performs initial operations on `frame` before it is properly processed

    :param frame: frame to process
    :param width: width to resize frame to
    :param morph: perform morphology to cleanup noise on binary frame, defaults to False
    :return: processed `frame`, binary version of `frame` and HSV version of `frame`
    """
    if frame is not None:
        # resize the frame if width is provided
        frame = imutils.resize(frame, width=width)
        return frame
    return None
