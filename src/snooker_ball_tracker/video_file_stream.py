from __future__ import annotations

import typing
from threading import Thread

import cv2
from imutils.video import FileVideoStream

import snooker_ball_tracker.settings as s

if typing.TYPE_CHECKING:
    from .ball_tracker import ColourDetectionSettings, VideoPlayer

from .video_stream import VideoStream


class VideoFileStream(VideoStream, FileVideoStream):
    def __init__(self, path: str, video_player: VideoPlayer, 
                 colour_settings: ColourDetectionSettings, queue_size: int=128):
        """Create instance of VideoFileStream that loads frames from a video file in a
        separate thread and performs some basic transformations

        :param path: file path to video file to process
        :type path: str
        :param video_player: video player to obtain transformation settings from
        :type video_player: VideoPlayer
        :param colour_settings: colour settings to obtain colours from
        :type colour_settings: ColourDetectionSettings
        :param queue_size: max number of frames to process and store at a time, defaults to 128
        :type queue_size: int, optional
        """
        try:
            video_file_stream = cv2.VideoCapture(path)
            if not video_file_stream.isOpened():
                raise TypeError
        except Exception as error:
           raise error
        finally:
            video_file_stream.release()
        super().__init__(video=path, video_player=video_player, colours_settings=colour_settings, queue_size=queue_size)
        self.thread.name = self.__class__.__name__
