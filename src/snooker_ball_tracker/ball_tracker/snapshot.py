import cv2
import imutils
import snooker_ball_tracker.settings as s
import numpy as np
import time

from .util import dist_between_two_balls

class SnapShot:
    def __init__(self, balls=None):
        """
        Creates a instance of SnapShot using `balls`

        :param balls: list of balls to store in the snapshot
        """
        if balls is None:
            self.balls = {
                'WHITE': [],
                'RED': [],
                'YELLOW': [],
                'GREEN': [],
                'BROWN': [],
                'BLUE': [],
                'PINK': [],
                'BLACK': []
            }
        else:
            self.balls = balls
        if self.balls['WHITE']:
            self.white_pt = self.balls['WHITE'][0]
        else:
            self.white_pt = None
        self.white_is_moving = False

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
                    ball_colour.lower(), len(self.balls[ball_colour]))
        return snapshot_info

    def compare_ball_diff(self, ball_colour, snapshot):
        """
        Compares the ball difference with `snapshot` for `ball_colour`

        :param ball_colour: colour of ball to compare with `snapshot`
        :param snapshot: other snapshot to compare with
        :returns: `ball_colour` and the ball difference of `ball_colour`
        """
        prev_totals = len(self.balls[ball_colour])
        new_total = len(snapshot.balls[ball_colour])
        diff = prev_totals - new_total
        return ball_colour, diff

    def __ne__(self, other):
        """
        Determine if the snapshot is not equal to `other`

        :param other: other snapshot to compare with
        :returns: True if the ball count if different both snapshots, else False
        """
        if isinstance(other, SnapShot):
            is_not_equal = False

            if len(self.balls['RED']) != len(other.balls['RED']):
                is_not_equal = True

            if len(self.balls['YELLOW']) != len(other.balls['YELLOW']):
                is_not_equal = True

            if len(self.balls['GREEN']) != len(other.balls['GREEN']):
                is_not_equal = True

            if len(self.balls['BROWN']) != len(other.balls['BROWN']):
                is_not_equal = True

            if len(self.balls['BLUE']) != len(other.balls['BLUE']):
                is_not_equal = True

            if len(self.balls['PINK']) != len(other.balls['PINK']):
                is_not_equal = True

            if len(self.balls['BLACK']) != len(other.balls['BLACK']):
                is_not_equal = True

            return is_not_equal

    def has_shot_started(self, snapshot):
        """
        Determine if the shot has started by comparing `snapshot` white ball
        with own white ball

        :param snapshot: snapshot to compare with
        :returns: True if the shot has started, else False
        """
        if len(self.balls['WHITE']) > 0:
            if len(snapshot.balls['WHITE']) == len(self.balls['WHITE']):
                if self.white_pt and snapshot.white_pt:
                    if self.has_ball_moved(self.white_pt, snapshot.white_pt):
                        print('===========================================')
                        print('WHITE STATUS: moving...')
                        self.white_is_moving = True
                        return True
                return False
        return False

    def has_shot_finished(self, snapshot):
        """
        Determine if the shot has finished by comparing `snapshot` white ball
        with own white ball

        :param snapshot: snapshot to compare with
        :returns: True if the shot has finished, else False
        """
        if len(self.balls['WHITE']) > 0:
            if len(snapshot.balls['WHITE']) == len(self.balls['WHITE']):
                if self.white_pt and snapshot.white_pt:
                    if self.has_ball_stopped(self.white_pt, snapshot.white_pt):
                        print('WHITE STATUS: stopped...\n')
                        self.white_is_moving = False
                        return True
                else:
                    return True
        return False

    def has_ball_stopped(self, ball_1, ball_2):
        """
        Determine if a specific ball has stopped

        :param ball_1: first ball
        :param ball_2: second ball
        :returns: True if the ball has stopped, else False
        """
        dist = dist_between_two_balls(ball_1, ball_2)
        if self.white_is_moving:
            if dist <= 0.1:
                return True
            else:
                return False
        else:
            return False

    def has_ball_moved(self, ball_1, ball_2):
        """
        Determine if a specific ball has moved

        :param ball_1: first ball
        :param ball_2: second ball
        :returns: True if the ball has moved, else False
        """
        dist = dist_between_two_balls(ball_1, ball_2)
        if not self.white_is_moving:
            if dist > 0.1:
                return True
            else:
                return False
        else:
            return False
