import cv2
import imutils
import snooker_ball_tracker.settings as s
import numpy as np
import time


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


def get_snapshot_report(prev_snapshot, cur_snapshot):
    """
    Creates a report of two snapshots to show the difference between them

    :param prev_snapshot: previous snapshot
    :param cur_snapshot: current snapshot
    :returns: table of comparision between `prev_snapshot`, `cur_snapshot` and `temp_snapshot`
    """
    report = '--------------------------------------\n'
    report += 'PREVIOUS SNAPSHOT | CURRENT SNAPSHOT \n'
    report += '------------------|-------------------\n'
    for ball in prev_snapshot.balls:
        prev_ball_status = '{}s: {}'.format(ball.lower(), len(prev_snapshot.balls[ball]))
        while len(prev_ball_status) < 17:
            prev_ball_status += ' '
        cur_ball_status = '{}s: {}'.format(ball.lower(), len(cur_snapshot.balls[ball]))
        report += prev_ball_status + ' | ' + cur_ball_status + '\n'
    report += '--------------------------------------\n'
    return report


class BallTracker:
    def __init__(self, **kwargs):
        """
        Creates an instance of BallTracker

        :param **kwargs: dictionary of options to use to configure
                         the underlying blob detector to detect balls with
        """
        params = cv2.SimpleBlobDetector_Params()
        params.filterByConvexity = kwargs.get('filter_by_convexity', s.FILTER_BY_CONVEXITY)
        params.minConvexity = kwargs.get('min_convexity', s.MIN_CONVEXITY)
        params.maxConvexity = kwargs.get('max_convexity', s.MAX_CONVEXITY)
        params.filterByCircularity = kwargs.get('filter_by_circularity', s.FILTER_BY_CIRCULARITY)
        params.minCircularity = kwargs.get('min_circularity', s.MIN_CIRCULARITY)
        params.maxCircularity = kwargs.get('max_circularity', s.MAX_CIRCULARITY)
        params.filterByInertia = kwargs.get('filter_by_inertia', s.FILTER_BY_INERTIA)
        params.minInertiaRatio = kwargs.get('min_inertia_ratio', s.MIN_INERTIA_RATIO)
        params.maxInertiaRatio = kwargs.get('max_inertia_ratio', s.MAX_INERTIA_RATIO)
        params.filterByArea = kwargs.get('filter_by_area', s.FILTER_BY_AREA)
        params.minArea = kwargs.get('min_area', s.MIN_AREA)
        params.maxArea = kwargs.get('max_area', s.MAX_AREA)
        params.filterByColor = kwargs.get('filter_by_colour', s.FILTER_BY_COLOUR)
        params.blobColor = kwargs.get('blob_color', s.BLOB_COLOUR)
        params.minDistBetweenBlobs = kwargs.get('min_dest_between_blobs', s.MIN_DIST_BETWEEN_BLOBS)
        self.__blob_detector = cv2.SimpleBlobDetector_create(params)
        self.__table_bounds = None
        self.__table_bounds_mask = None
        self.__balls = []
        self.__frame_counter = 0
        self.__temp_snapshot = None
        self.__prev_snapshot = None
        self.__cur_snapshot = None
        self.update_boundary = False

    def perform_init_ops(self, frame, width=None, crop=True, morph=False):
        """
        Performs initial operations on `frame` before it is properly processed

        :param frame: image to process
        :param width: width to resize `frame` to
        :param crop: if True crop `frame` around the detected table boundary
        :param morph: if True perform morph closing morphology to `frame`
        :returns: processed `frame`, binary version of `frame` and HSV version of `frame`
        """
        # resize the frame if width is provided
        if width:
            frame = imutils.resize(frame, width=width)

        # convert frame into HSV colour space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # get mask of table cloth colour
        threshold, contours = self.get_mask_contours_for_colour(hsv, 'TABLE')
        threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
        threshold = cv2.bitwise_not(threshold)

        # Perform closing morphology if `morph` is True
        if morph:
            threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

        if self.update_boundary:
            self.create_table_boundary(frame, contours)

        # crop frame, hsv and threshold
        if crop and self.__table_bounds is not None:
            frame = self.crop(frame)
            hsv = self.crop(hsv)
            threshold = self.crop(threshold)

        return frame, threshold, hsv

    def create_table_boundary(self, frame, contours=None):
        """
        Creates the table boundary mask from `frame`

        :param frame: image to process
        :param contours: list of contours to possibly use for the table boundary
        """
        # Create mask where white is what we want, black otherwise
        self.__table_bounds_mask = np.zeros_like(frame)
        if len(contours) > 1:
            self.__table_bounds = max(contours, key=lambda el: cv2.contourArea(el))
        elif len(contours) == 1:
            self.__table_bounds = contours[0]
        else:
            self.__table_bounds = None
        if self.__table_bounds is not None:
            cv2.drawContours(self.__table_bounds_mask, [self.__table_bounds], -1, (255, 255, 255), -1)

    def crop(self, frame):
        """
        Crops `frame` using the detected table boundary

        :param frame: image to process
        :returns: cropped `frame`
        """
        # Extract out the object and place into output image
        out = np.zeros_like(frame)
        out[self.__table_bounds_mask == 255] = frame[self.__table_bounds_mask == 255]
        (x, y, _) = np.where(self.__table_bounds_mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        frame = out[topx:bottomx + 1, topy:bottomy + 1]
        return frame

    def draw_balls(self, frame, balls):
        """
        Draws each ball from `balls` onto `frame`

        :param frame: image to process
        :param balls: list of balls to draw onto `frame`
        """
        for ball_colour in balls:
            for ball in balls[ball_colour]:
                cv2.putText(
                    frame, ball_colour, (int(ball.pt[0] + 10), int(ball.pt[1])),
                    0, 0.6, (0, 255, 0), thickness=2
                )
                cv2.circle(frame, (int(ball.pt[0]), int(ball.pt[1])),
                           int(ball.size / 2), (0, 255, 0))

    def update_balls(self, balls, cur_balls):
        """
        Updates `balls` with previously detected `cur_balls`
        If a ball from `cur_balls` is close enough to a ball in `balls`,
        it is deemed to be the same ball and the ball in `balls` is updated
        with the ball colour info from `cur_balls`

        :param balls: list of detected balls
        :param cur_ball: list of current balls that are were already detected
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

    def get_white_ball_status(self):
        """
        Obtain the status of the white ball, either `moving` or `stopped`

        :returns: status of white ball
        """
        if self.__prev_snapshot.white_is_moving:
            return 'moving...'
        else:
            return 'stopped...'

    def get_snapshot_status(self, current=True):
        """
        Obtain the status of either the previous or temporary SnapShot

        :param current: if True return the previous SnapShot info,
                        otherwise return the temporary SnapShot info
        :returns: previous or temporary SnapShot info
        """
        if current:
            return self.__prev_snapshot.__str__()
        else:
            return self.__temp_snapshot.__str__()

    def run(self, frame, width=None, crop=True, morph=False, show_threshold=False, show_fps=True):
        """
        Process `frame` to detect/track balls, determine if a shot has started/finished
        and determine if a ball was potted

        :param frame: image to process
        :param width: width to resize `frame` to
        :param crop: if True crop `frame` around the detected table boundary
        :param morph: if True perform morph closing morphology to `frame`
        :param show_threshold: if True return a binary version of `frame`
        :param show_fps: if True draw the FPS and frame counter onto `frame`
        :returns: processed image, ball potted if any were and the number of balls potted
        """
        # We store 3 different Snapshots:
        #  - Previous shot SnapShot
        #  - Current shot SnapShot
        #  - Temporary shot SnapShot
        #  
        # The previous shot SnapShot stores info about the state of the table 
        # of the last shot taken
        #
        # The Current shot SnapShot stores info about the state of the table
        # currently in play before the shot is taken
        #
        # The Temporary shot SnapShot is used to determine when a shot has 
        # started and finished, which is determined by comparing the 
        # Temporary SnapShot with the Current SnapShot

        ball_potted = None
        pot_count = 0
        start = time.time()

        # Perform initial operations on provided frame (resize and crop)
        frame, threshold, hsv = self.perform_init_ops(frame, width=width, crop=crop, morph=morph)

        # Every 5 frames run the colour detection phase, otherwise just update ball positions
        if self.__frame_counter == 0 or self.__frame_counter % 5 == 0:
            self.__balls = self.__run(threshold, hsv)
        else:
            cur_balls = self.__blob_detector.detect(threshold)
            self.update_balls(self.__balls, cur_balls)

        # Every 5 frames run the snapshot comparision/generation phase
        if self.__frame_counter == 0 or self.__frame_counter % 5 == 0:
            ball_status = None
            if not self.__prev_snapshot:
                self.__prev_snapshot = SnapShot(self.__balls)
                self.__temp_snapshot = self.__prev_snapshot
                print(self.__temp_snapshot.get_snapshot_info('INITIAL SNAPSHOT'))

            self.__cur_snapshot = SnapShot(self.__balls)

            if self.__prev_snapshot.has_shot_started(self.__cur_snapshot):
                if self.__cur_snapshot != self.__temp_snapshot:
                    for ball_colour in self.__temp_snapshot.balls:
                        potted, count = self.__temp_snapshot.compare_ball_diff(ball_colour, self.__cur_snapshot)
                        if potted != 'WHITE' and count > 0:
                            ball_potted = potted
                            pot_count = count
                            ball_status = 'Potted {} {}/s'.format(pot_count, ball_potted.lower())

                    print(get_snapshot_report(self.__temp_snapshot, self.__cur_snapshot))
                    if ball_status is not None:
                        print(ball_status)
                    print('===========================================\n')
                    self.__temp_snapshot = self.__cur_snapshot

            if self.__prev_snapshot.has_shot_finished(self.__cur_snapshot):
                for ball_colour in self.__temp_snapshot.balls:
                    potted, count = self.__temp_snapshot.compare_ball_diff(ball_colour, self.__cur_snapshot)
                    if potted != 'WHITE' and count > 0:
                        ball_potted = potted
                        pot_count = count
                        ball_status = 'Potted {} {}/s'.format(pot_count, ball_potted.lower())

                print(get_snapshot_report(self.__temp_snapshot, self.__cur_snapshot))
                if ball_status is not None:
                    print(ball_status)
                print('===========================================\n')
                self.__temp_snapshot = self.__cur_snapshot

            self.__cur_snapshot.white_is_moving = self.__prev_snapshot.white_is_moving
            self.__prev_snapshot = self.__cur_snapshot

        self.__frame_counter += 1

        if show_threshold:
            frame = threshold

        self.draw_balls(frame, self.__balls)
        if show_fps:
            fps = int(1.0 / (time.time() - start))
            cv2.putText(frame, str(fps) + ' fps', (20, 20), 0, 0.8, (0, 255, 0))
            cv2.putText(frame, 'frame ' + str(self.__frame_counter), (120, 20), 0, 0.8, (0, 255, 0))

        return frame, ball_potted, pot_count

    def __run(self, threshold, hsv):
        """
        Performs the underlying colour detection process

        :param threshold: binary image where detected balls are white on a black background
        :param hsv: HSV colour space image to detect colours with
        :returns: list of balls mapped to an appropriate colour found in `threshold`
        """
        # This function handles the colour detection phase and returns a list of 
        # detected balls in the frame and maps the appropriate colour to each ball
        balls = {
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
        keypoints = self.__blob_detector.detect(threshold)

        # Obtain 8 contours for each ball colour from the HSV colour space of the frame
        if s.DETECT_COLOURS['WHITE']:
            _, whites = self.get_mask_contours_for_colour(hsv, 'WHITE')
        if s.DETECT_COLOURS['RED']:
            _, reds = self.get_mask_contours_for_colour(hsv, 'RED')
        if s.DETECT_COLOURS['YELLOW']:
            _, yellows = self.get_mask_contours_for_colour(hsv, 'YELLOW')
        if s.DETECT_COLOURS['GREEN']:
            _, greens = self.get_mask_contours_for_colour(hsv, 'GREEN')
        if s.DETECT_COLOURS['BROWN']:
            _, browns = self.get_mask_contours_for_colour(hsv, 'BROWN')
        if s.DETECT_COLOURS['BLUE']:
            _, blues = self.get_mask_contours_for_colour(hsv, 'BLUE')
        if s.DETECT_COLOURS['PINK']:
            _, pinks = self.get_mask_contours_for_colour(hsv, 'PINK')
        if s.DETECT_COLOURS['BLACK']:
            _, blacks = self.get_mask_contours_for_colour(hsv, 'BLACK')

        # For each ball found, determine what colour it is and add it to the list of balls
        # If a ball is not mapped to an appropriate colour, it is discarded
        for keypoint in keypoints:
            is_ball = False

            if not is_ball and s.DETECT_COLOURS['RED']:
                is_ball = self.__keypoint_is_ball('RED', reds, keypoint, balls)

            if not is_ball and s.DETECT_COLOURS['WHITE']:
                is_ball = self.__keypoint_is_ball('WHITE', whites, keypoint, balls)

            if not is_ball and s.DETECT_COLOURS['YELLOW']:
                is_ball = self.__keypoint_is_ball('YELLOW', yellows, keypoint, balls, biggest_contour=True)

            if not is_ball and s.DETECT_COLOURS['GREEN']:
                is_ball = self.__keypoint_is_ball('GREEN', greens, keypoint, balls, biggest_contour=False)

            if not is_ball and s.DETECT_COLOURS['BLUE']:
                is_ball = self.__keypoint_is_ball('BLUE', blues, keypoint, balls, biggest_contour=True)

            if not is_ball and s.DETECT_COLOURS['PINK']:
                is_ball = self.__keypoint_is_ball('PINK', pinks, keypoint, balls, biggest_contour=True)

            if not is_ball and s.DETECT_COLOURS['BLACK']:
                is_ball = self.__keypoint_is_ball('BLACK', blacks, keypoint, balls)

            if not is_ball and s.DETECT_COLOURS['BROWN']:
                self.__keypoint_is_ball('BROWN', browns, keypoint, balls)
        return balls

    def __keypoint_is_ball(self, colour, colour_contours, keypoint, balls, biggest_contour=False):
        """
        Determine if `keypoint` is a ball of `colour`

        :param colour: colour to check `keypoint` against
        :param colour_contours: contours of `colour`
        :param keypoint: keypoint to check
        :param balls: list of balls already detected
        :param biggest_contour: use only the biggest contour in `colour_contours` 
                                to determine if `keypoint` is a ball of `colour`
        :returns: True if `keypoint` is within `contour`, False otherwise
        """
        if len(colour_contours) > 1 and biggest_contour:
            colour_contour = max(colour_contours, key=lambda el: cv2.contourArea(el))
            if self.__keypoint_in_contour(keypoint, colour_contour):
                balls[colour].append(keypoint)
                return True
        else:
            for contour in colour_contours:
                if self.__keypoint_in_contour(keypoint, contour):
                    balls[colour].append(keypoint)
                    return True
        return False

    def __keypoint_in_contour(self, keypoint, contour):
        """
        Determine if `keypoint` is contained within `contour`

        :param keypoint: keypoint to check
        :param contour: contour to check
        :returns: True if `keypoint` is within `contour`, False otherwise
        """
        dist = cv2.pointPolygonTest(contour, keypoint.pt, False)
        if dist == 1:
            return True
        return False

    def get_mask_contours_for_colour(self, frame, colour):
        """
        Obtains the colour mask of `colour` from `frame`

        :param frame: image to process
        :param colour: colour to extract contours from `frame`
        :returns: colour mask of `colour` and a list of contours
        """
        colour_mask = None
        contours = None
        if colour in s.COLOURS:
            colour_mask = cv2.inRange(frame, s.COLOURS[colour]['LOWER'],
                                      s.COLOURS[colour]['UPPER'])
            contours, _ = cv2.findContours(colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return colour_mask, contours

    def detect_colour(self, frame, lower, upper):
        """
        Detects a colour in `frame` based on the `lower` and `upper` HSV values

        :param frame: image to process
        :param lower: lower range of colour HSV values
        :param upper: upper range of colour HSV values
        :returns: colour mask of `lower` and `upper` HSV values and a list of contours
        """
        colour_mask = cv2.inRange(frame, lower, upper)
        contours, _ = cv2.findContours(colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return colour_mask, contours

    def get_threshold(self, frame, color_space=cv2.COLOR_BGR2GRAY, threshold_type=cv2.THRESH_BINARY_INV):
        """
        Converts `frame` into a binary image

        :param frame: image to process
        :param color_space: colour space to convert `frame` into
        :param threshold_type: threshold type to use in conversion
        """
        gray = cv2.cvtColor(frame, color_space)
        retval, threshold = cv2.threshold(gray, s.MIN_THRESHOLD, s.MAX_THRESHOLD, threshold_type)
        return threshold

    def get_frame_counter(self):
        """
        Obtain the current frame counter

        :returns: current frame counter
        """
        return self.__frame_counter


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
        snapshot_info = '=================\n'
        snapshot_info += title + '\n'
        snapshot_info += '=================\n'
        for ball_colour in s.DETECT_COLOURS:
            if s.DETECT_COLOURS[ball_colour]:
                snapshot_info += '{}s: {}\n'.format(ball_colour.lower(), len(self.balls[ball_colour]))
        snapshot_info += '=================\n'
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
