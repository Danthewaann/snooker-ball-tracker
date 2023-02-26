from __future__ import annotations

from functools import partial
from typing import Any

import cv2
import numpy as np

from snooker_ball_tracker.enums import SnookerColour

from .logger import Logger
from .settings import BallDetectionSettings, ColourDetectionSettings
from .snapshot import SnapShot
from .types import Frame, Image, Keypoints
from .util import dist_between_two_balls, get_mask_contours_for_colour


def max_table_bound(el: Frame) -> Frame:
    bounds: Frame = cv2.contourArea(el)
    return bounds


def setup_blob_detector(ball_tracker: BallTracker, **kwargs: dict[str, Any]) -> None:
    """Setup underlying blob detector with provided kwargs"""
    params = cv2.SimpleBlobDetector_Params()
    params.filterByConvexity = kwargs.get(
        "FILTER_BY_CONVEXITY",
        ball_tracker.ball_settings.settings["FILTER_BY_CONVEXITY"],
    )
    params.minConvexity = kwargs.get(
        "MIN_CONVEXITY", ball_tracker.ball_settings.settings["MIN_CONVEXITY"]
    )
    params.maxConvexity = kwargs.get(
        "MAX_CONVEXITY", ball_tracker.ball_settings.settings["MAX_CONVEXITY"]
    )
    params.filterByCircularity = kwargs.get(
        "FILTER_BY_CIRCULARITY",
        ball_tracker.ball_settings.settings["FILTER_BY_CIRCULARITY"],
    )
    params.minCircularity = kwargs.get(
        "MIN_CIRCULARITY", ball_tracker.ball_settings.settings["MIN_CIRCULARITY"]
    )
    params.maxCircularity = kwargs.get(
        "MAX_CIRCULARITY", ball_tracker.ball_settings.settings["MAX_CIRCULARITY"]
    )
    params.filterByInertia = kwargs.get(
        "FILTER_BY_INERTIA", ball_tracker.ball_settings.settings["FILTER_BY_INERTIA"]
    )
    params.minInertiaRatio = kwargs.get(
        "MIN_INERTIA", ball_tracker.ball_settings.settings["MIN_INERTIA"]
    )
    params.maxInertiaRatio = kwargs.get(
        "MAX_INERTIA", ball_tracker.ball_settings.settings["MAX_INERTIA"]
    )
    params.filterByArea = kwargs.get(
        "FILTER_BY_AREA", ball_tracker.ball_settings.settings["FILTER_BY_AREA"]
    )
    params.minArea = kwargs.get(
        "MIN_AREA", ball_tracker.ball_settings.settings["MIN_AREA"]
    )
    params.maxArea = kwargs.get(
        "MAX_AREA", ball_tracker.ball_settings.settings["MAX_AREA"]
    )
    params.filterByColor = kwargs.get(
        "FILTER_BY_COLOUR", ball_tracker.ball_settings.settings["FILTER_BY_COLOUR"]
    )
    params.blobColor = kwargs.get(
        "BLOB_COLOR", ball_tracker.ball_settings.settings["BLOB_COLOUR"]
    )
    params.minDistBetweenBlobs = kwargs.get(
        "MIN_DEST_BETWEEN_BLOBS",
        ball_tracker.ball_settings.settings["MIN_DIST_BETWEEN_BLOBS"],
    )
    blob_detector: cv2.SimpleBlobDetector = cv2.SimpleBlobDetector_create(params)
    ball_tracker.blob_detector = blob_detector


class BallTracker:
    def __init__(
        self,
        logger: Logger | None = None,
        colour_settings: ColourDetectionSettings | None = None,
        ball_settings: BallDetectionSettings | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        """Creates an instance of BallTracker that detects balls in images
        provided to it and maps colours to each ball detected.

        :param logger: logger that contains snapshots to log to, defaults to None
        :param colour_settings: colour detection settings instance, defaults to None
        :param ball_settings: ball detection settings instance, defaults to None
        :param **kwargs: dictionary of options to use to configure
                         the underlying blob detector to detect balls with
        """
        self.logger = logger or Logger()
        self.__last_shot_snapshot = self.logger.last_shot_snapshot
        self.__cur_shot_snapshot = self.logger.cur_shot_snapshot
        self.__temp_snapshot = self.logger.temp_snapshot
        self.__white_status_setter = self.logger.set_white_status
        self.blob_detector: cv2.SimpleBlobDetector = cv2.SimpleBlobDetector_create()
        self.colour_settings = colour_settings or ColourDetectionSettings()
        self.ball_settings = ball_settings or BallDetectionSettings()
        self.ball_settings.settingsChanged.connect(
            partial(setup_blob_detector, self, **kwargs)
        )
        setup_blob_detector(self, **kwargs)
        self.table_bounds: Frame | None = None
        self.table_bounds_mask: Frame | None = None
        self.__keypoints: Keypoints = {}
        self.__image_counter = 0
        self.__shot_in_progess = False

    def get_snapshot_report(self) -> str:
        """Creates a report of  snapshots to show the difference between them

        :return: table comparision between `last_shot_snapshot`
                 and `cur_shot_snapshot` in a string format
        """
        report = "--------------------------------------\n"
        report += "PREVIOUS SNAPSHOT | CURRENT SNAPSHOT \n"
        report += "------------------|-------------------\n"
        for colour in self.__last_shot_snapshot.colours:
            prev_ball_status = (
                f"{colour.lower()}s: {self.__last_shot_snapshot.colours[colour].count}"
            )
            while len(prev_ball_status) < 17:
                prev_ball_status += " "
            cur_ball_status = (
                f"{colour.lower()}s: {self.__cur_shot_snapshot.colours[colour].count}"
            )
            report += prev_ball_status + " | " + cur_ball_status + "\n"
        report += "--------------------------------------\n"
        return report

    def draw_balls(self, frame: Frame, balls: Keypoints) -> None:
        """Draws each ball from `balls` onto `frame`

        :param frame: frame to process
        :param balls: list of balls to draw onto `frame`
        """
        for ball_colour, ball_list in balls.items():
            for ball in ball_list:
                cv2.putText(
                    frame,
                    ball_colour,
                    (int(ball.pt[0] + 10), int(ball.pt[1])),
                    0,
                    0.6,
                    (0, 255, 0),
                    thickness=2,
                )
                cv2.circle(
                    frame,
                    (int(ball.pt[0]), int(ball.pt[1])),
                    int(ball.size / 2),
                    (0, 255, 0),
                )

    def update_balls(self, balls: Keypoints, cur_balls: Keypoints) -> Keypoints:
        """Updates `balls` with previously detected `cur_balls`
        If a ball from `cur_balls` is close enough to a ball in `balls`,
        it is deemed to be the same ball and the ball in `balls` is updated
        with the ball colour info from `cur_balls`

        :param balls: list of newly detected balls
        :param cur_balls: list of balls that are were detected previously
        :return: list of newly detected balls mapped to their appropriate colours
        """
        for cur_ball in cur_balls:
            matched = False
            for ball_colour in balls:
                if not matched:
                    for i, ball in enumerate(balls[ball_colour]):
                        dist = dist_between_two_balls(cur_ball, ball)
                        if dist <= 0.3:
                            balls[ball_colour][i] = cur_ball
                            matched = True
                            break
                else:
                    break
        return balls

    def process_frame(
        self,
        frame: Frame,
        show_threshold: bool = False,
        detect_table: bool = False,
        crop_frames: bool = False,
        perform_morph: bool = False,
        detect_colour: str | None = None,
        mask_colour: bool = False,
    ) -> tuple[Image, str | None, int]:
        """Process `frame` to detect/track balls, determine if a shot has
        started/finished and determine if a ball was potted

        We store 3 different Snapshots:
        - Previous shot SnapShot
        - Current shot SnapShot
        - Temporary shot SnapShot

        The `Last shot SnapShot` stores info about the state of the table
        of the last shot taken

        The `Current shot SnapShot` stores info about the state of the table
        currently in play before the shot is taken

        The `Temporary SnapShot` is used to determine when a shot has
        started and finished, which is determined by comparing the
        Temporary SnapShot with the Current SnapShot

        :param frame: frame to process
        :param show_threshold: if True return a binary version of `frame`,
                               defaults to False
        :return: processed frame, ball potted if any were and the number
                                  of balls potted
        """
        ball_potted: str | None = None
        pot_count = 0

        # convert frame into HSV colour space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # get mask of table cloth colour
        mask, contours = get_mask_contours_for_colour(
            hsv, SnookerColour.TABLE, self.colour_settings.colours
        )
        if mask is None:
            raise ValueError("no mask found")
        if not contours:
            raise ValueError("no contours found")

        threshold: Frame = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        threshold = cv2.bitwise_not(threshold)

        # perform closing morphology if `morph` is True
        if perform_morph:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

        # get the bounds of the table
        if detect_table:
            self.create_table_boundary(frame, contours)

        # draw the bounds of the table if we have it
        if self.table_bounds is not None and not crop_frames:
            cv2.drawContours(frame, [self.table_bounds], -1, (255, 255, 255), 3)

        # fill frame, hsv and threshold
        if crop_frames and self.table_bounds is not None:
            frame = self.fill(frame)
            hsv = self.fill(hsv)
            threshold = self.fill(threshold)

        # Every 5 images run the colour detection phase,
        # otherwise just update ball positions
        if self.__image_counter == 0 or self.__image_counter % 5 == 0:
            self.__keypoints = self.perform_colour_detection(threshold, hsv)
        else:
            cur_keypoints = self.blob_detector.detect(threshold)
            self.update_balls(self.__keypoints, cur_keypoints)

        if self.__image_counter == 0:
            self.__cur_shot_snapshot.assign_balls_from_dict(self.__keypoints)
            self.__last_shot_snapshot.assign_balls_from_dict(self.__keypoints)

        # Swap output frame with binary frame if show threshold is True
        if show_threshold:
            frame = threshold

        # Draw contours around a colour to detect if not None
        if detect_colour:
            colour_mask, contours = self.detect_colour(
                hsv,
                self.colour_settings.colours[detect_colour]["LOWER"],
                self.colour_settings.colours[detect_colour]["UPPER"],
            )

            # Show only the detected colour in the output frame
            if mask_colour:
                frame = cv2.bitwise_and(frame, frame, mask=colour_mask)

            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        # Draw only the balls for the detected colour
        # if we are only showing the detected colour
        if (
            detect_colour
            and detect_colour in self.colour_settings.settings["BALL_COLOURS"]
            and mask_colour
        ):
            self.draw_balls(frame, {detect_colour: self.__keypoints[detect_colour]})
        else:
            # Otherwise just draw all detected balls
            self.draw_balls(frame, self.__keypoints)

        # Every 5 images run the snapshot comparision/generation phase
        if self.__image_counter == 0 or self.__image_counter % 5 == 0:
            ball_status = None

            self.__temp_snapshot.assign_balls_from_dict(self.__keypoints)

            if not self.__shot_in_progess:
                self.__shot_in_progess = self.has_shot_started(
                    self.__temp_snapshot, self.__cur_shot_snapshot
                )

            if self.__shot_in_progess:
                if self.has_shot_finished(
                    self.__temp_snapshot, self.__cur_shot_snapshot
                ):
                    for ball_colour in self.__last_shot_snapshot.colours:
                        count = self.__last_shot_snapshot.compare_ball_diff(
                            ball_colour, self.__temp_snapshot
                        )
                        if ball_colour != "WHITE" and count > 0:
                            ball_potted = ball_colour
                            pot_count = count
                            ball_status = "Potted {} {}/s".format(
                                pot_count, ball_potted.lower()
                            )

                    if ball_status is not None:
                        print(ball_status)
                    print("===========================================\n")
                    self.__last_shot_snapshot.assign_balls_from_snapshot(
                        self.__cur_shot_snapshot
                    )
                    self.__shot_in_progess = False

                if self.__cur_shot_snapshot.white and self.__temp_snapshot.white:
                    self.__cur_shot_snapshot.white.is_moving = (
                        self.__temp_snapshot.white.is_moving
                    )
            self.__cur_shot_snapshot.assign_balls_from_snapshot(self.__temp_snapshot)

        self.__image_counter += 1

        return Image(frame, threshold, hsv), ball_potted, pot_count

    def perform_colour_detection(
        self, binary_frame: Frame, hsv_frame: Frame
    ) -> Keypoints:
        """Performs the colour detection process

        This method handles the colour detection phase and returns a list of
        detected balls in the image and maps the appropriate colour to each ball

        :param binary_frame: binary frame where detected balls are
                             white on a black background
        :param hsv_frame: HSV frame to detect colours with
        :return: list of keypoints mapped to an appropriate colour
                 found in `binary_frame`
        """
        balls: Keypoints = {
            colour: list() for colour in self.colour_settings.settings["BALL_COLOURS"]
        }

        colour_contours: Keypoints = {
            colour: list() for colour in self.colour_settings.settings["BALL_COLOURS"]
        }

        # Detect balls in the binary image (White circles on a black background)
        keypoints = self.blob_detector.detect(binary_frame)

        # Obtain colours contours for each ball colour from the
        # HSV colour space of the image
        for colour, properties in self.colour_settings.settings["BALL_COLOURS"].items():
            if properties["DETECT"]:
                _, contours = get_mask_contours_for_colour(
                    hsv_frame, colour, self.colour_settings.colours
                )
                if contours:
                    colour_contours[colour] = contours

        def order_value(colour: str) -> int:
            val: int = self.colour_settings.settings["BALL_COLOURS"][colour]["ORDER"]
            return val

        # Get colours in their detection order
        colours = sorted(
            self.colour_settings.settings["BALL_COLOURS"],
            key=order_value,
        )

        # For each ball found, determine what colour it is and add
        # it to the list of balls. If a ball is not mapped to an
        # appropriate colour, it is discarded
        for keypoint in keypoints:
            for colour in colours:
                if self.colour_settings.settings["BALL_COLOURS"][colour]["DETECT"]:
                    if self.__keypoint_is_ball(
                        colour, colour_contours[colour], keypoint, balls
                    ):
                        break

        return balls

    def __keypoint_is_ball(
        self,
        colour: str,
        colour_contours: list[Frame],
        keypoint: cv2.KeyPoint,
        balls: Keypoints,
        biggest_contour: bool = False,
    ) -> bool:
        """Determine if `keypoint` is a ball of `colour`

        :param colour: colour to check `keypoint` against
        :param colour_contours: contours of `colour`
        :param keypoint: keypoint to check
        :param balls: list of balls already detected
        :param biggest_contour: use only the biggest contour in `colour_contours`
                                to determine if `keypoint` is a ball of `colour`,
                                defaults to False
        :return: True if `keypoint` is within `contour`, False otherwise
        """
        if len(colour_contours) > 1 and biggest_contour:
            colour_contour = max(colour_contours, key=max_table_bound)
            if self.__keypoint_in_contour(keypoint, colour_contour):
                balls[colour].append(keypoint)
                return True
        else:
            for contour in colour_contours:
                if self.__keypoint_in_contour(keypoint, contour):
                    balls[colour].append(keypoint)
                    return True
        return False

    def __keypoint_in_contour(self, keypoint: cv2.KeyPoint, contour: Frame) -> bool:
        """Determine if `keypoint` is contained within `contour`

        :param keypoint: keypoint to check
        :param contour: contour to check
        :return: True if `keypoint` is within `contour`, False otherwise
        """
        dist = cv2.pointPolygonTest(contour, keypoint.pt, False)
        return True if dist == 1 else False

    def detect_colour(
        self, frame: Frame, lower: Frame, upper: Frame
    ) -> tuple[Frame, list[Frame]]:
        """Detects a colour in `frame` based on the `lower` and `upper` HSV values

        :param frame: frame to process
        :param lower: lower range of colour HSV values
        :param upper: upper range of colour HSV values
        :return: colour mask of `lower` and `upper` HSV values and a list of contours
        """
        colour_mask = cv2.inRange(frame, lower, upper)
        contours, _ = cv2.findContours(
            colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )
        return colour_mask, contours

    def has_shot_started(
        self, first_snapshot: SnapShot, second_snapshot: SnapShot
    ) -> bool:
        """Determine if the shot has started by comparing `first_snapshot` white ball
        with `second_snapshot` white ball

        :param first_snapshot: first snapshot
        :param second_snapshot: second snapshot
        :return: True if the shot has started, otherwise False
        """
        if first_snapshot.colours["WHITE"].count > 0:
            if (
                first_snapshot.colours["WHITE"].count
                == second_snapshot.colours["WHITE"].count
            ):
                if first_snapshot.white and second_snapshot.white:
                    if self.has_ball_moved(
                        first_snapshot.white.keypoint, second_snapshot.white.keypoint
                    ):
                        print("===========================================")
                        print("WHITE STATUS: moving...")
                        self.__white_status_setter(True)
                        return True
                return False
        return False

    def has_shot_finished(
        self, first_snapshot: SnapShot, second_snapshot: SnapShot
    ) -> bool:
        """Determine if the shot has finished by comparing `first_snapshot` white ball
        with `second_snapshot` white ball

        :param first_snapshot: first snapshot
        :param second_snapshot: second snapshot
        :return: True if the shot has finished, otherwise False
        """
        if first_snapshot.colours["WHITE"].count > 0:
            if (
                first_snapshot.colours["WHITE"].count
                == second_snapshot.colours["WHITE"].count
            ):
                if first_snapshot.white and second_snapshot.white:
                    if self.has_ball_stopped(
                        first_snapshot.white.keypoint, second_snapshot.white.keypoint
                    ):
                        print("WHITE STATUS: stopped...\n")
                        self.__white_status_setter(False)
                        return True
                else:
                    return True
        return False

    def has_ball_stopped(
        self, first_ball: cv2.KeyPoint, second_ball: cv2.KeyPoint
    ) -> bool:
        """Determine if a specific ball has stopped

        :param first_ball: first ball
        :param second_ball: second ball
        :return: True if the ball has stopped, otherwise False
        """
        dist = dist_between_two_balls(first_ball, second_ball)
        return True if dist <= 0.1 else False

    def has_ball_moved(
        self, first_ball: cv2.KeyPoint, second_ball: cv2.KeyPoint
    ) -> bool:
        """Determine if a specific ball has moved

        :param first_ball: first ball
        :param second_ball: second ball
        :return: True if the ball has moved, otherwise False
        """
        dist = dist_between_two_balls(first_ball, second_ball)
        return True if dist > 0.1 else False

    def create_table_boundary(
        self, frame: Frame, contours: list[cv2.KeyPoint] | None = None
    ) -> None:
        """Creates the table boundary mask from `frame`

        :param frame: frame to process
        :param contours: list of contours to possibly use for the table boundary,
                         defaults to None
        """
        # Create mask where white is what we want, black otherwise
        self.table_bounds_mask = np.zeros_like(frame)

        if contours:
            if len(contours) > 1:
                self.table_bounds = max(contours, key=max_table_bound)
            elif len(contours) == 1:
                self.table_bounds = contours[0]
        else:
            self.table_bounds = None
        if self.table_bounds is not None:
            cv2.drawContours(
                self.table_bounds_mask, [self.table_bounds], -1, (255, 255, 255), -1
            )

    def fill(self, frame: Frame) -> Frame:
        """Fill `frame` using the detected table boundary

        :param frame: frame to process
        :return: frame filled around table boundary
        """
        # Extract out the object and place into output image
        out: Frame = np.zeros(frame.shape).astype(frame.dtype)
        out[self.table_bounds_mask == 255] = frame[self.table_bounds_mask == 255]
        frame = cv2.bitwise_and(frame, out)
        return frame

    def crop(self, frame: Frame) -> Frame:
        """Crops `frame` using the detected table boundary

        :param frame: frame to process
        :return: frame cropped around table boundary
        """
        # Extract out the object and place into output image
        out: Frame = np.zeros(frame.shape).astype(frame.dtype)
        out[self.table_bounds_mask == 255] = frame[self.table_bounds_mask == 255]
        (x, y, _) = np.where(self.table_bounds_mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        frame = out[topx : bottomx + 1, topy : bottomy + 1]
        return frame
