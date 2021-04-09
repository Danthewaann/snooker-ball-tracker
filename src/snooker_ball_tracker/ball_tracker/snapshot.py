import snooker_ball_tracker.settings as s

from .logging import Ball, BallColour
from .util import dist_between_two_balls


class SnapShot():
    def __init__(self, balls: dict=None):
        """Creates an instance of this class that contains ball counts for all
        possible ball colours

        :param balls: dict of balls, where each key value pair 
                      is a ball colour and its count, defaults to None
        :type balls: dict, optional
        """
        if balls:
            self._ball_colours = { colour: BallColour(keypoints) for colour, keypoints in balls.items()}
        else:
            self._ball_colours = {
                colour: BallColour() for colour in s.DETECT_COLOURS if s.DETECT_COLOURS[colour]
            }

    def assign(self, balls: dict):
        balls = { colour: BallColour(ball_list) for colour, ball_list in balls.items()}
        for colour in self._ball_colours:
            self._ball_colours[colour].assign(balls[colour].balls)

    def assign_snapshot(self, snapshot):
        for colour in self._ball_colours:
            self._ball_colours[colour].assign(snapshot.ball_colours[colour].balls)

    @property
    def ball_colours(self) -> dict:
        return self._ball_colours

    @property
    def white(self) -> Ball:
        """White ball property

        :return: white ball
        :rtype: Ball
        """
        return self.whites.balls[0] if self.whites.balls else None

    @property
    def whites(self) -> BallColour:
        """Whites property

        :return: whites
        :rtype: BallColour
        """
        return self._ball_colours["WHITE"]

    @property
    def reds(self) -> BallColour:
        """Reds property

        :return: reds
        :rtype: BallColour
        """
        return self._ball_colours["RED"]

    @property
    def yellows(self) -> BallColour:
        """Yellows property

        :return: yellows
        :rtype: BallColour
        """
        return self._ball_colours["YELLOW"]

    @property
    def greens(self) -> BallColour:
        """Greens property

        :return: greens
        :rtype: BallColour
        """
        return self._ball_colours["GREEN"]

    @property
    def browns(self) -> BallColour:
        """Browns property

        :return: browns
        :rtype: BallColour
        """
        return self._ball_colours["BROWN"]

    @property
    def blues(self) -> BallColour:
        """Blues property

        :return: blues
        :rtype: BallColour
        """
        return self._ball_colours["BLUE"]

    @property
    def pinks(self) -> BallColour:
        """Pinks property

        :return: pinks
        :rtype: BallColour
        """
        return self._ball_colours["PINK"]

    @property
    def blacks(self) -> BallColour:
        """Blacks property

        :return: blacks
        :rtype: BallColour
        """
        return self._ball_colours["BLACK"]

    def get_snapshot_info(self, title='SNAPSHOT INFO'):
        """
        Output the snapshot ball info

        :param title: title for snapshot info
        :returns: snapshot ball info
        """
        snapshot_info = ''
        for ball_colour in s.DETECT_COLOURS:
            if s.DETECT_COLOURS[ball_colour]:
                snapshot_info += '{}s: {}\n'.format(
                    ball_colour.lower(), self._ball_colours[ball_colour].count)
        return snapshot_info

    def compare_ball_diff(self, ball_colour, snapshot):
        """
        Compares the ball difference with `snapshot` for `ball_colour`

        :param ball_colour: colour of ball to compare with `snapshot`
        :param snapshot: other snapshot to compare with
        :returns: `ball_colour` and the ball difference of `ball_colour`
        """
        prev_totals = self._ball_colours[ball_colour].count
        new_total = snapshot.ball_colours[ball_colour].count
        diff = prev_totals - new_total
        return ball_colour, diff
