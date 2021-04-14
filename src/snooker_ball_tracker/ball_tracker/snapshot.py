from __future__ import annotations

import typing

import cv2
import snooker_ball_tracker.settings as s

from .logging import Ball, BallColour
from .util import dist_between_two_balls


class SnapShot():
    def __init__(self, balls: dict=None, ball_colours: dict=s.COLOUR_DETECTION_SETTINGS["BALL_COLOURS"]):
        """Creates an instance of this class that contains ball counts for all
        possible ball colours

        :param balls: dict of balls, where each key value pair 
                      is a ball colour and its count, defaults to None
        :type balls: dict, optional
        """
        if balls:
            self._colours = { colour: BallColour(keypoints) for colour, keypoints in balls.items()}
        else:
            self._colours = {
                colour: BallColour() for colour in ball_colours if ball_colours[colour]
            }

    @property
    def colours(self) -> typing.Dict[str, BallColour]:
        """Dict of colours where each key is a ball colour, and each
        value is a BallColour instance

        :return: colours dict
        :rtype: typing.Dict[str, BallColour]
        """
        return self._colours

    @property
    def white(self) -> typing.Optional[Ball]:
        """White ball property

        :return: white ball
        :rtype: typing.Optional[Ball]
        """
        return self._colours["WHITE"].balls[0] if self._colours["WHITE"].balls else None

    def assign_balls_from_dict(self, balls: typing.Dict[str, typing.List[cv2.KeyPoint]]):
        """Assign balls to their appropriate ball colour instances from a dict

        :param balls: dict of colour and ball list pairs
        :type balls: typing.Dict[str, typing.List[cv2.KeyPoint]]
        """
        for colour, keypoints in balls.items():
            self._colours[colour].assign([Ball(pt) for pt in keypoints])

    def assign_balls_from_snapshot(self, snapshot: SnapShot):
        """Assign balls to their appropriate ball colour instances from a SnapShot

        :param snapshot: snapshot to take balls from
        :type snapshot: SnapShot
        """
        for colour, ball_colours in snapshot.colours.items():
            self._colours[colour].assign(ball_colours.balls)

    def compare_ball_diff(self, ball_colour: str, snapshot: SnapShot) -> int:
        """Compares the ball difference with `snapshot` for `ball_colour`

        :param ball_colour: colour of ball to compare with `snapshot`
        :type ball_colour: str
        :param snapshot: other snapshot to compare ball difference with
        :type snapshot: SnapShot
        :return: the ball difference of provided `ball_colour`
        :rtype: int
        """
        prev_total = self._colours[ball_colour].count
        new_total = snapshot.colours[ball_colour].count
        diff = prev_total - new_total
        return diff
