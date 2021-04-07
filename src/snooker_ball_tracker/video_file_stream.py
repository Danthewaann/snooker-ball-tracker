from threading import Thread

import cv2
import imutils
import numpy as np
from imutils.video import FileVideoStream

import snooker_ball_tracker.settings as s
from .ball_tracker import video_player


class VideoFileStream(FileVideoStream):
    def __init__(self, path: str, video_player: video_player, queue_size: int=128):
        """Create instance of VideoFileStream that loads frames from a file in a
        separate thread and performs some basic transformations

        :param path: file path to video file to process
        :type path: str
        :param crop: crop frames around detected table boundary, defaults to False
        :type crop: bool, optional
        :param morph: perform morphology to clear up noise in frames, defaults to False
        :type morph: bool, optional
        :param queue_size: max number of frames to process and store at a time, defaults to 128
        :type queue_size: int, optional
        """
        super().__init__(path, transform=self.transform_frame, queue_size=queue_size)
        self.video_player = video_player
        self.__table_bounds = None
        self.__table_bounds_mask = None
        self.thread = Thread(
            target=self.update, name=self.__class__.__name__, args=())
        self.thread.daemon = True

    def transform_frame(self, frame) -> tuple:
        """Performs initial operations on `frame` before it is properly processed

        :param frame: image to process
        :returns: processed `frame`, binary version of `frame` and HSV version of `frame`
        

        :param frame: image to process
        :type frame: [type]
        :return: processed `frame`, binary version of `frame` and HSV version of `frame`
        :rtype: tuple
        """
        if frame is not None:
            # resize the frame if width is provided
            frame = imutils.resize(frame, width=self.video_player.player_width)

            # convert frame into HSV colour space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # get mask of table cloth colour
            threshold, contours = self.get_mask_contours_for_colour(
                hsv, 'TABLE')
            threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
            threshold = cv2.bitwise_not(threshold)

            # perform closing morphology if `morph` is True
            if self.video_player.perform_morph:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
                threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

            # get the bounds of the table
            if self.video_player.detect_table:
                print("Drawing table boundary...")
                self.create_table_boundary(frame, contours)
                self.video_player.detect_table = False

            # draw the bounds of the table if we have it
            if self.__table_bounds is not None and not self.video_player.crop_frames:
                cv2.drawContours(
                    frame, [self.__table_bounds], -1, (255, 255, 255), 3)

            # crop frame, hsv and threshold
            if self.video_player.crop_frames and self.__table_bounds is not None:
                frame = self.crop(frame)
                hsv = self.crop(hsv)
                threshold = self.crop(threshold)

            return (frame, threshold, hsv)

        return (None, None, None)

    def create_table_boundary(self, frame, contours=None):
        """
        Creates the table boundary mask from `frame`

        :param frame: image to process
        :param contours: list of contours to possibly use for the table boundary
        """
        # Create mask where white is what we want, black otherwise
        self.__table_bounds_mask = np.zeros_like(frame)
        if len(contours) > 1:
            self.__table_bounds = max(
                contours, key=lambda el: cv2.contourArea(el))
        elif len(contours) == 1:
            self.__table_bounds = contours[0]
        else:
            self.__table_bounds = None
        if self.__table_bounds is not None:
            cv2.drawContours(self.__table_bounds_mask, [
                             self.__table_bounds], -1, (255, 255, 255), -1)

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
            contours, _ = cv2.findContours(
                colour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return colour_mask, contours

    def crop(self, frame):
        """
        Crops `frame` using the detected table boundary

        :param frame: image to process
        :returns: cropped `frame`
        """
        # Extract out the object and place into output image
        out = np.zeros_like(frame)
        out[self.__table_bounds_mask ==
            255] = frame[self.__table_bounds_mask == 255]
        (x, y, _) = np.where(self.__table_bounds_mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        frame = out[topx:bottomx + 1, topy:bottomy + 1]
        return frame
