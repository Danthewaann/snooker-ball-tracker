import typing
from abc import ABC

import cv2
import imutils
import numpy as np

import snooker_ball_tracker.settings as s

from .ball_tracker import VideoPlayer
from .ball_tracker.util import Image, get_mask_contours_for_colour


class VideoStream(ABC):
    def __init__(self, video: typing.Any, video_player: VideoPlayer, 
                 colours: dict=s.COLOURS, queue_size: int=128):
        """VideoStream abstract base class that contains base functionality to
        process video streams

        :param video: video representation
        :type video: typing.Any
        :param video_player: video player to obtain transformation settings from
        :type video_player: VideoPlayer
        :param colours: settings to obtain colours from, defaults to s.COLOURS
        :type colours: dict, optional
        :param queue_size: max number of frames to process and store at a time, defaults to 128
        :type queue_size: int, optional
        """
        self._video_player = video_player
        self._colours = colours
        self._table_bounds: typing.Union[np.ndarray, None] = None
        self._table_bounds_mask: typing.Union[np.ndarray, None] = None
        super().__init__(video, transform=self.transform_frame, queue_size=queue_size)

    def transform_frame(self, frame: np.ndarray) -> Image:
        """Performs initial operations on `frame` before it is properly processed

        :param frame: frame to process
        :type frame: np.ndarray
        :return: processed `frame`, binary version of `frame` and HSV version of `frame`
        :rtype: Image
        """
        if frame is not None:
            # resize the frame if width is provided
            frame = imutils.resize(frame, width=self._video_player.width)

            # set video player height to height of resized frame
            self._video_player.height = frame.shape[0]

            # convert frame into HSV colour space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # get mask of table cloth colour
            threshold, contours = get_mask_contours_for_colour(
                hsv, 'TABLE', self._colours)
            threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
            threshold = cv2.bitwise_not(threshold)

            # perform closing morphology if `morph` is True
            if self._video_player.perform_morph:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
                threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

            # get the bounds of the table
            if self._video_player.detect_table:
                print("Drawing table boundary...")
                self.create_table_boundary(frame, contours)
                self._video_player.detect_table = False

            # draw the bounds of the table if we have it
            if self._table_bounds is not None and not self._video_player.crop_frames:
                cv2.drawContours(
                    frame, [self._table_bounds], -1, (255, 255, 255), 3)

            # crop frame, hsv and threshold
            if self._video_player.crop_frames and self._table_bounds is not None:
                frame = self.crop(frame)
                hsv = self.crop(hsv)
                threshold = self.crop(threshold)

            return Image(frame, threshold, hsv)

        return None

    def create_table_boundary(self, frame: np.ndarray, contours: typing.List[np.ndarray]=None):
        """Creates the table boundary mask from `frame`

        :param frame: frame to process
        :type frame: np.ndarray
        :param contours: list of contours to possibly use for the table boundary, defaults to None
        :type contours: typing.List[np.ndarray], optional
        """
        # Create mask where white is what we want, black otherwise
        self._table_bounds_mask = np.zeros_like(frame)
        if contours:
            if len(contours) > 1:
                self._table_bounds = max(contours, key=lambda el: cv2.contourArea(el))
            elif len(contours) == 1:
                self._table_bounds = contours[0]
        else:
            self._table_bounds = None
        if self._table_bounds is not None:
            cv2.drawContours(self._table_bounds_mask, [
                             self._table_bounds], -1, (255, 255, 255), -1)

    def crop(self, frame: np.ndarray) -> np.ndarray:
        """Crops `frame` using the detected table boundary

        :param frame: frame to process
        :type frame: np.ndarray
        :return: frame cropped around table boundary
        :rtype: np.ndarray
        """
        # Extract out the object and place into output image
        out = np.zeros_like(frame)
        out[self._table_bounds_mask ==
            255] = frame[self._table_bounds_mask == 255]
        (x, y, _) = np.where(self._table_bounds_mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        frame = out[topx:bottomx + 1, topy:bottomy + 1]
        return frame
