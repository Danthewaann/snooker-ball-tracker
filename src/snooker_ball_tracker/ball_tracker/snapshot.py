from __future__ import annotations

from typing import TYPE_CHECKING, Any

from snooker_ball_tracker.settings import settings as s

from .balls import Ball, BallColour

if TYPE_CHECKING:
    from .types import Keypoints


class SnapShot:
    def __init__(
        self,
        balls: Keypoints | None = None,
        ball_colours: dict[str, Any] = s.COLOUR_DETECTION_SETTINGS["BALL_COLOURS"],
    ) -> None:
        """Creates an instance of this class that contains ball counts for all
        possible ball colours

        :param balls: dict of balls, where each key value pair
                      is a ball colour and its count, defaults to None
        """
        if balls:
            self._colours = {
                colour: BallColour(keypoints) for colour, keypoints in balls.items()
            }
        else:
            self._colours = {
                colour: BallColour() for colour in ball_colours if ball_colours[colour]
            }

    @property
    def colours(self) -> dict[str, BallColour]:
        """Dict of colours where each key is a ball colour, and each
        value is a BallColour instance

        :return: colours dict
        """
        return self._colours

    @property
    def white(self) -> Ball | None:
        """White ball property

        :return: white ball
        """
        return self._colours["WHITE"].balls[0] if self._colours["WHITE"].balls else None

    def assign_balls_from_dict(self, balls: Keypoints) -> None:
        """Assign balls to their appropriate ball colour instances from a dict

        :param balls: dict of colour and ball list pairs
        """
        for colour, keypoints in balls.items():
            self._colours[colour].assign([Ball(pt) for pt in keypoints])

    def assign_balls_from_snapshot(self, snapshot: SnapShot) -> None:
        """Assign balls to their appropriate ball colour instances from a SnapShot

        :param snapshot: snapshot to take balls from
        """
        for colour, ball_colours in snapshot.colours.items():
            self._colours[colour].assign(ball_colours.balls)

    def compare_ball_diff(self, ball_colour: str, snapshot: SnapShot) -> int:
        """Compares the ball difference with `snapshot` for `ball_colour`

        :param ball_colour: colour of ball to compare with `snapshot`
        :param snapshot: other snapshot to compare ball difference with
        :return: the ball difference of provided `ball_colour`
        """
        prev_total = self._colours[ball_colour].count
        new_total = snapshot.colours[ball_colour].count
        diff = prev_total - new_total
        return diff
