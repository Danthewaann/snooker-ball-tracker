from threading import Thread

from imutils.video import FileVideoStream

import snooker_ball_tracker.settings as s

from .ball_tracker import VideoPlayer, ColourDetectionSettings
from .video_stream import VideoStream
import typing


class VideoFileStream(VideoStream, FileVideoStream):
    def __init__(self, path: str, video_player: VideoPlayer, 
                 colour_settings: typing.Union[dict, ColourDetectionSettings]=s.COLOUR_DETECTION_SETTINGS, 
                 queue_size: int=128):
        """Create instance of VideoFileStream that loads frames from a video file in a
        separate thread and performs some basic transformations

        :param path: file path to video file to process
        :type path: str
        :param video_player: video player to obtain transformation settings from
        :type video_player: VideoPlayer
        :param colour_settings: colour settings to obtain colours from, defaults to s.COLOUR_DETECTION_SETTINGS,
        :type colour_settings: typing.Union[dict, ColourDetectionSettings], optional
        :param queue_size: max number of frames to process and store at a time, defaults to 128
        :type queue_size: int, optional
        """
        super().__init__(video=path, video_player=video_player, colours_settings=colour_settings, queue_size=queue_size)
        self.thread.name = self.__class__.__name__
