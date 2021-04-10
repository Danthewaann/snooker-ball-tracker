import typing

import cv2
import numpy as np
import snooker_ball_tracker.settings as s

from .logger import Logger
from .tracker_settings import Settings
from .logging import BallsPotted
from .snapshot import SnapShot
from .util import dist_between_two_balls

Keypoints = typing.Dict[str, typing.List[cv2.KeyPoint]]


class BallTracker():
    def __init__(self, logger: Logger=None, settings: Settings=None, **kwargs):
        """Creates an instance of BallTracker

        :param logger: logger that contains snapshots to log to, defaults to None
        :type logger: Logger, optional
        :param settings: ball and colour detection settings instance, defaults to None
        :type settings: Settings, optional
        :param **kwargs: dictionary of options to use to configure
                         the underlying blob detector to detect balls with
        """
        if logger:
            self.__last_shot_snapshot = logger.last_shot_snapshot
            self.__cur_shot_snapshot = logger.cur_shot_snapshot
            self.__temp_snapshot = logger.temp_snapshot
            self.__white_status_setter = logger.set_white_status
        else:
            self.__last_shot_snapshot = SnapShot()
            self.__cur_shot_snapshot = SnapShot()
            self.__temp_snapshot = SnapShot()
            self.__white_status_setter = lambda value: value
        if settings:
            self.__colour_settings = settings.models["colour_detection"].colours
            # self.__ball_settings = settings.models["ball_detection"].
        else:
            self.__colour_settings = s.COLOURS
            
        self.__keypoints: Keypoints = {}
        self.__blob_detector: cv2.SimpleBlobDetector = None
        self.__image_counter = 0
        self.__shot_in_progess = False
        self.setup_blob_detector(**kwargs)

    def setup_blob_detector(self, **kwargs):
        """Setup underlying blob detector with provided kwargs"""
        params = cv2.SimpleBlobDetector_Params()
        params.filterByConvexity = kwargs.get('filter_by_convexity', s.BLOB_DETECTOR["FILTER_BY_CONVEXITY"])
        params.minConvexity = kwargs.get('min_convexity', s.BLOB_DETECTOR["MIN_CONVEXITY"])
        params.maxConvexity = kwargs.get('max_convexity', s.BLOB_DETECTOR["MAX_CONVEXITY"])
        params.filterByCircularity = kwargs.get('filter_by_circularity', s.BLOB_DETECTOR["FILTER_BY_CIRCULARITY"])
        params.minCircularity = kwargs.get('min_circularity', s.BLOB_DETECTOR["MIN_CIRCULARITY"])
        params.maxCircularity = kwargs.get('max_circularity', s.BLOB_DETECTOR["MAX_CIRCULARITY"])
        params.filterByInertia = kwargs.get('filter_by_inertia', s.BLOB_DETECTOR["FILTER_BY_INERTIA"])
        params.minInertiaRatio = kwargs.get('min_inertia', s.BLOB_DETECTOR["MIN_INERTIA"])
        params.maxInertiaRatio = kwargs.get('max_inertia', s.BLOB_DETECTOR["MAX_INERTIA"])
        params.filterByArea = kwargs.get('filter_by_area', s.BLOB_DETECTOR["FILTER_BY_AREA"])
        params.minArea = kwargs.get('min_area', s.BLOB_DETECTOR["MIN_AREA"])
        params.maxArea = kwargs.get('max_area', s.BLOB_DETECTOR["MAX_AREA"])
        params.filterByColor = kwargs.get('filter_by_colour', s.BLOB_DETECTOR["FILTER_BY_COLOUR"])
        params.blobColor = kwargs.get('blob_color', s.BLOB_DETECTOR["BLOB_COLOUR"])
        params.minDistBetweenBlobs = kwargs.get('min_dest_between_blobs', s.BLOB_DETECTOR["MIN_DIST_BETWEEN_BLOBS"])
        self.__blob_detector = cv2.SimpleBlobDetector_create(params)

    def get_snapshot_report(self) -> str:
        """Creates a report of  snapshots to show the difference between them

        :return: table comparision between `last_shot_snapshot` 
                 and `cur_shot_snapshot` in a string format
        :rtype: str
        """
        report = '--------------------------------------\n'
        report += 'PREVIOUS SNAPSHOT | CURRENT SNAPSHOT \n'
        report += '------------------|-------------------\n'
        for colour in self.__last_shot_snapshot.colours:
            prev_ball_status = f'{colour.lower()}s: {self.__last_shot_snapshot.colours[colour].count}'
            while len(prev_ball_status) < 17:
                prev_ball_status += ' '
            cur_ball_status = f'{colour.lower()}s: {self.__cur_shot_snapshot.colours[colour].count}'
            report += prev_ball_status + ' | ' + cur_ball_status + '\n'
        report += '--------------------------------------\n'
        return report

    def draw_balls(self, frame: np.ndarray, balls: Keypoints):
        """Draws each ball from `balls` onto `frame`

        :param frame: frame to process
        :type frame: np.ndarray
        :param balls: list of balls to draw onto `frame`
        :type balls: Keypoints
        """
        for ball_colour, ball_list in balls.items():
            for ball in ball_list:
                cv2.putText(
                    frame, ball_colour, (int(
                        ball.pt[0] + 10), int(ball.pt[1])),
                    0, 0.6, (0, 255, 0), thickness=2
                )
                cv2.circle(frame, (int(ball.pt[0]), int(ball.pt[1])),
                           int(ball.size / 2), (0, 255, 0))

    def update_balls(self, balls: Keypoints, cur_balls: Keypoints) -> Keypoints:
        """Updates `balls` with previously detected `cur_balls`
        If a ball from `cur_balls` is close enough to a ball in `balls`,
        it is deemed to be the same ball and the ball in `balls` is updated
        with the ball colour info from `cur_balls`

        :param balls: list of detected balls
        :param cur_ball: list of current balls that are were already detected

        :param balls: list of newly detected balls
        :type balls: Keypoints
        :param cur_balls: list of balls that are were detected previously
        :type cur_balls: Keypoints
        :return: list of newly detected balls mapped to their appropriate colours
        :rtype: Keypoints
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

    def process_image(self, image: typing.Tuple[np.ndarray, np.ndarray, np.ndarray], 
                      show_threshold: bool=False) -> tuple:
        """Process `image` to detect/track balls, determine if a shot has started/finished
        and determine if a ball was potted

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

        :param image: image to process, contains 3 frames (RGB, HSV and binary versions of image)
        :type image: typing.Tuple[np.ndarray, np.ndarray, np.ndarray]
        :param show_threshold: if True return a binary version of `image`, defaults to False
        :type show_threshold: bool, optional
        :return: processed image, ball potted if any were and the number of balls potted
        :rtype: tuple
        """
        ball_potted = None
        pot_count = 0

        # Unpack image tuple
        output_frame, binary_frame, hsv_frame = image

        # Every 5 images run the colour detection phase, otherwise just update ball positions
        if self.__image_counter == 0 or self.__image_counter % 5 == 0:
            self.__keypoints = self.perform_colour_detection(binary_frame, hsv_frame)
        else:
            cur_keypoints = self.__blob_detector.detect(binary_frame)
            self.update_balls(self.__keypoints, cur_keypoints)

        if self.__image_counter == 0:
            self.__cur_shot_snapshot.assign_balls_from_dict(self.__keypoints)
            self.__last_shot_snapshot.assign_balls_from_dict(self.__keypoints)

        if show_threshold:
            output_frame = binary_frame

        self.draw_balls(output_frame, self.__keypoints)

        # Every 5 images run the snapshot comparision/generation phase
        if self.__image_counter == 0 or self.__image_counter % 5 == 0:
            ball_status = None

            self.__temp_snapshot.assign_balls_from_dict(self.__keypoints)

            if not self.__shot_in_progess:
                self.__shot_in_progess = self.has_shot_started(self.__temp_snapshot, self.__cur_shot_snapshot)

            if self.__shot_in_progess:
                if self.has_shot_finished(self.__temp_snapshot, self.__cur_shot_snapshot):
                    for ball_colour in self.__last_shot_snapshot.colours:
                        count = self.__last_shot_snapshot.compare_ball_diff(
                            ball_colour, self.__temp_snapshot
                        )
                        if ball_colour != 'WHITE' and count > 0:
                            ball_potted = ball_colour
                            pot_count = count
                            ball_status = 'Potted {} {}/s'.format(
                                pot_count, ball_potted.lower())

                    if ball_status is not None:
                        print(ball_status)
                    print('===========================================\n')
                    self.__last_shot_snapshot.assign_balls_from_snapshot(self.__cur_shot_snapshot)
                    self.__shot_in_progess = False
        
                if self.__cur_shot_snapshot.white and self.__temp_snapshot.white:
                    self.__cur_shot_snapshot.white.is_moving = self.__temp_snapshot.white.is_moving
            self.__cur_shot_snapshot.assign_balls_from_snapshot(self.__temp_snapshot)

        self.__image_counter += 1

        return output_frame, ball_potted, pot_count

    def perform_colour_detection(self, binary_frame: np.ndarray, hsv_frame: np.ndarray) -> Keypoints:
        """Performs the colour detection process

        This method handles the colour detection phase and returns a list of
        detected balls in the image and maps the appropriate colour to each ball

        :param binary_frame: binary frame where detected balls are white on a black background
        :type binary_frame: np.ndarray
        :param hsv_frame: HSV frame to detect colours with
        :type hsv_frame: np.ndarray
        :return: list of keypoints mapped to an appropriate colour found in `binary_frame`
        :rtype: Keypoints
        """

        balls: Keypoints = {
            'WHITE': [],
            'RED': [],
            'YELLOW': [],
            'GREEN': [],
            'BROWN': [],
            'BLUE': [],
            'PINK': [],
            'BLACK': []
        }

        # Detect balls in the binary image (White circles on a black background)
        keypoints = self.__blob_detector.detect(binary_frame)

        # Obtain 8 contours for each ball colour from the HSV colour space of the image
        if s.DETECT_COLOURS['WHITE']:
            _, whites = self.get_mask_contours_for_colour(hsv_frame, 'WHITE')
        if s.DETECT_COLOURS['RED']:
            _, reds = self.get_mask_contours_for_colour(hsv_frame, 'RED')
        if s.DETECT_COLOURS['YELLOW']:
            _, yellows = self.get_mask_contours_for_colour(hsv_frame, 'YELLOW')
        if s.DETECT_COLOURS['GREEN']:
            _, greens = self.get_mask_contours_for_colour(hsv_frame, 'GREEN')
        if s.DETECT_COLOURS['BROWN']:
            _, browns = self.get_mask_contours_for_colour(hsv_frame, 'BROWN')
        if s.DETECT_COLOURS['BLUE']:
            _, blues = self.get_mask_contours_for_colour(hsv_frame, 'BLUE')
        if s.DETECT_COLOURS['PINK']:
            _, pinks = self.get_mask_contours_for_colour(hsv_frame, 'PINK')
        if s.DETECT_COLOURS['BLACK']:
            _, blacks = self.get_mask_contours_for_colour(hsv_frame, 'BLACK')

        # For each ball found, determine what colour it is and add it to the list of balls
        # If a ball is not mapped to an appropriate colour, it is discarded
        for keypoint in keypoints:
            is_ball = False

            if not is_ball and s.DETECT_COLOURS['RED']:
                is_ball = self.__keypoint_is_ball('RED', reds, keypoint, balls)

            if not is_ball and s.DETECT_COLOURS['WHITE']:
                is_ball = self.__keypoint_is_ball(
                    'WHITE', whites, keypoint, balls)

            if not is_ball and s.DETECT_COLOURS['YELLOW']:
                is_ball = self.__keypoint_is_ball(
                    'YELLOW', yellows, keypoint, balls, biggest_contour=True)

            if not is_ball and s.DETECT_COLOURS['GREEN']:
                is_ball = self.__keypoint_is_ball(
                    'GREEN', greens, keypoint, balls, biggest_contour=False)

            if not is_ball and s.DETECT_COLOURS['BLUE']:
                is_ball = self.__keypoint_is_ball(
                    'BLUE', blues, keypoint, balls, biggest_contour=True)

            if not is_ball and s.DETECT_COLOURS['PINK']:
                is_ball = self.__keypoint_is_ball(
                    'PINK', pinks, keypoint, balls, biggest_contour=True)

            if not is_ball and s.DETECT_COLOURS['BLACK']:
                is_ball = self.__keypoint_is_ball(
                    'BLACK', blacks, keypoint, balls)

            if not is_ball and s.DETECT_COLOURS['BROWN']:
                self.__keypoint_is_ball('BROWN', browns, keypoint, balls)
        return balls

    def __keypoint_is_ball(self, colour: str, colour_contours: typing.List[np.ndarray], 
                           keypoint: cv2.KeyPoint, balls: Keypoints, 
                           biggest_contour: bool=False) -> bool:
        """Determine if `keypoint` is a ball of `colour`

        :param colour: colour to check `keypoint` against
        :type colour: str
        :param colour_contours: contours of `colour`
        :type colour_contours: typing.List[np.ndarray]
        :param keypoint: keypoint to check
        :type keypoint: cv2.KeyPoint
        :param balls: list of balls already detected
        :type balls: Keypoints
        :param biggest_contour: use only the biggest contour in `colour_contours` 
                                to determine if `keypoint` is a ball of `colour`, defaults to False
        :type biggest_contour: bool, optional
        :return: True if `keypoint` is within `contour`, False otherwise
        :rtype: bool
        """
        if len(colour_contours) > 1 and biggest_contour:
            colour_contour = max(
                colour_contours, key=lambda el: cv2.contourArea(el))
            if self.__keypoint_in_contour(keypoint, colour_contour):
                balls[colour].append(keypoint)
                return True
        else:
            for contour in colour_contours:
                if self.__keypoint_in_contour(keypoint, contour):
                    balls[colour].append(keypoint)
                    return True
        return False

    def __keypoint_in_contour(self, keypoint: cv2.KeyPoint, contour: np.ndarray) -> bool:
        """Determine if `keypoint` is contained within `contour`

        :param keypoint: keypoint to check
        :type keypoint: cv2.KeyPoint
        :param contour: contour to check
        :type contour: np.ndarray
        :return: True if `keypoint` is within `contour`, False otherwise
        :rtype: bool
        """
        dist = cv2.pointPolygonTest(contour, keypoint.pt, False)
        return True if dist == 1 else False

    def get_mask_contours_for_colour(self, frame: np.ndarray, colour: str) -> tuple:
        """Obtains the colour mask of `colour` from `frame`

        :param frame: frame to process
        :type frame: np.ndarray
        :param colour: colour to extract contours from `frame`
        :type colour: str
        :return: colour mask of `colour` and a list of contours
        :rtype: tuple
        """
        colour_mask = None
        contours = None
        if colour in self.__colour_settings:
            colour_mask = cv2.inRange(frame, self.__colour_settings[colour]['LOWER'],
                                      self.__colour_settings[colour]['UPPER'])
            contours, _ = cv2.findContours(
                colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return colour_mask, contours

    def detect_colour(self, frame: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> tuple:
        """Detects a colour in `frame` based on the `lower` and `upper` HSV values

        :param frame: frame to process
        :type frame: np.ndarray
        :param lower: lower range of colour HSV values
        :type lower: np.ndarray
        :param upper: upper range of colour HSV values
        :type upper: np.ndarray
        :return: colour mask of `lower` and `upper` HSV values and a list of contours
        :rtype: tuple
        """
        colour_mask = cv2.inRange(frame, lower, upper)
        contours, _ = cv2.findContours(
            colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return colour_mask, contours

    def get_threshold(self, frame: np.ndarray, color_space: int=cv2.COLOR_BGR2GRAY, 
                      threshold_type: int=cv2.THRESH_BINARY_INV) -> np.ndarray:
        """Converts `frame` into a binary frame

        :param frame: frame to process
        :type frame: np.ndarray
        :param color_space: colour space to convert `frame` into, defaults to cv2.COLOR_BGR2GRAY
        :type color_space: int, optional
        :param threshold_type: threshold type to use in conversion, defaults to cv2.THRESH_BINARY_INV
        :type threshold_type: int, optional
        :return: binary version of `frame`
        :rtype: np.ndarray
        """
        gray = cv2.cvtColor(frame, color_space)
        retval, binary_frame = cv2.threshold(
            gray, s.MIN_THRESHOLD, s.MAX_THRESHOLD, threshold_type)
        return binary_frame

    def has_shot_started(self, first_snapshot: SnapShot, second_snapshot: SnapShot) -> bool:
        """Determine if the shot has started by comparing `first_snapshot` white ball
        with `second_snapshot` white ball

        :param first_snapshot: first snapshot
        :type first_snapshot: SnapShot
        :param second_snapshot: second snapshot
        :type second_snapshot: SnapShot
        :return: True if the shot has started, otherwise False
        :rtype: bool
        """
        if first_snapshot.colours["WHITE"].count > 0:
            if first_snapshot.colours["WHITE"].count == second_snapshot.colours["WHITE"].count:
                if first_snapshot.white and second_snapshot.white:
                    if self.has_ball_moved(first_snapshot.white.keypoint, second_snapshot.white.keypoint):
                        print('===========================================')
                        print('WHITE STATUS: moving...')
                        self.__white_status_setter(True)
                        return True
                return False
        return False

    def has_shot_finished(self, first_snapshot: SnapShot, second_snapshot: SnapShot) -> bool:
        """Determine if the shot has finished by comparing `first_snapshot` white ball
        with `second_snapshot` white ball

        :param first_snapshot: first snapshot
        :type first_snapshot: SnapShot
        :param second_snapshot: second snapshot
        :type second_snapshot: SnapShot
        :return: True if the shot has finished, otherwise False
        :rtype: bool
        """
        if first_snapshot.colours["WHITE"].count > 0:
            if first_snapshot.colours["WHITE"].count == second_snapshot.colours["WHITE"].count:
                if first_snapshot.white and second_snapshot.white:
                    if self.has_ball_stopped(first_snapshot.white.keypoint, second_snapshot.white.keypoint):
                        print('WHITE STATUS: stopped...\n')
                        self.__white_status_setter(False)
                        return True
                else:
                    return True
        return False

    def has_ball_stopped(self, first_ball: cv2.KeyPoint, second_ball: cv2.KeyPoint) -> bool:
        """Determine if a specific ball has stopped

        :param first_ball: first ball
        :type first_ball: cv2.KeyPoint
        :param second_ball: second ball
        :type second_ball: cv2.KeyPoint
        :return: True if the ball has stopped, otherwise False
        :rtype: bool
        """
        dist = dist_between_two_balls(first_ball, second_ball)
        return True if dist <= 0.1 else False

    def has_ball_moved(self, first_ball: cv2.KeyPoint, second_ball: cv2.KeyPoint) -> bool:
        """Determine if a specific ball has moved

        :param first_ball: first ball
        :type first_ball: cv2.KeyPoint
        :param second_ball: second ball
        :type second_ball: cv2.KeyPoint
        :return: True if the ball has moved, otherwise False
        :rtype: bool
        """
        dist = dist_between_two_balls(first_ball, second_ball)
        return True if dist > 0.1 else False
