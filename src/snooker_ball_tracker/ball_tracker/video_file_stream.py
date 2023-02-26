from __future__ import annotations

from typing import TYPE_CHECKING

import cv2
from imutils.video import FileVideoStream

from .video_stream import VideoStream

if TYPE_CHECKING:
    from . import ColourDetectionSettings, VideoPlayer


class VideoFileStream(FileVideoStream, VideoStream):  # type: ignore[misc]
    def __init__(
        self,
        path: str,
        video_player: VideoPlayer,
        colour_settings: ColourDetectionSettings,
        queue_size: int = 128,
    ):
        """Create instance of VideoFileStream that loads frames from a video file in a
        separate thread and performs some basic transformations

        :param path: file path to video file to process
        :param video_player: video player to obtain transformation settings from
        :param colour_settings: colour settings to obtain colours from
        :param queue_size: max number of frames to process and store at a time,
                           defaults to 128
        """
        try:
            video_file_stream = cv2.VideoCapture(path)
            if not video_file_stream.isOpened():
                raise TypeError
        except Exception as error:
            raise error
        finally:
            video_file_stream.release()

        self._video_player = video_player
        self._colour_settings = colour_settings

        super().__init__(path, queue_size=queue_size)
        self.transform = self.transform_frame
        self.thread.name = self.__class__.__name__
