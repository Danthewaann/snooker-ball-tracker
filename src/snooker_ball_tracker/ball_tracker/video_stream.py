from __future__ import annotations

import typing
from abc import ABC

import cv2
import imutils
import numpy as np

if typing.TYPE_CHECKING:
    from . import VideoPlayer, ColourDetectionSettings

from .util import Image, get_mask_contours_for_colour


class VideoStream(ABC):
    def __init__(self, video: typing.Any, video_player: VideoPlayer, 
                 colours_settings: ColourDetectionSettings, queue_size: int=128):
        """VideoStream abstract base class that contains base functionality to
        process video streams

        :param video: video representation
        :type video: typing.Any
        :param video_player: video player to obtain transformation settings from
        :type video_player: VideoPlayer
        :param colours_settings: settings to obtain colours from
        :type colours_settings: ColourDetectionSettings
        :param queue_size: max number of frames to process and store at a time, defaults to 128
        :type queue_size: int, optional
        """
        self._video_player = video_player
        self._colour_settings = colours_settings
        super().__init__(video, transform=self.transform_frame, queue_size=queue_size)

    def transform_frame(self, frame: np.ndarray) -> np.ndarray:
        """Performs initial operations on `frame` before it is properly processed

        :param frame: frame to process
        :type frame: np.ndarray
        :return: processed frame
        :rtype: np.ndarray
        """
        if frame is not None:
            # resize the frame if width is provided
            frame = imutils.resize(frame, width=self._video_player.width)

            # set video player height to height of resized frame
            self._video_player.height = frame.shape[0]
            return frame

        return None
