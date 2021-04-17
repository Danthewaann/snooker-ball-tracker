from __future__ import annotations

import threading
import typing
from copy import deepcopy
from queue import Queue

import cv2

import snooker_ball_tracker.settings as s

if typing.TYPE_CHECKING:
    from .ball_tracker import BallTracker, Logger, VideoPlayer, ColourDetectionSettings

from .video_stream import VideoStream


class VideoProcessor(threading.Thread):
    def __init__(self, video_stream: VideoStream, video_player: VideoPlayer, 
                 ball_tracker: BallTracker, lock: threading.Lock, stop_event: threading.Event):
        """Creates instance of VideoProcessor that processes frames from a 
        VideoStream and passes them to the ball tracker for processing before
        passing them to the video player to display

        :param video_stream: video stream that produces images to process
        :type video_stream: VideoStream
        :param video_player: video player instance that we pass processed frames to
        :type video_player: VideoPlayer
        :param ball_tracker: ball tracker that we pass frames obtained from VideoStream to
        :type ball_tracker: BallTracker
        :param lock: lock used to manage access to VideoStream
        :type lock: threading.Lock
        :param stop_event: stop event used to shut down the VideoProcessor
        :type stop_event: threading.Event
        """
        super().__init__(name=self.__class__.__name__, daemon=True)
        self.__logger = ball_tracker.logger
        self.__video_player = video_player
        self.__colour_settings = ball_tracker.colour_settings
        self.__ball_tracker = ball_tracker
        self.__producer_lock = lock
        self.__stop_event = stop_event
        self.__image_producer = video_stream
        self.__image = None

    def run(self):
        """Run the main video processor process"""
        self.__video_player.play_video = True
        self.__image_producer.start()
        self.__video_player.start_fps()
        self._process_next_image()
        self.__video_player.play_video = False
        self.__image_producer.Q = Queue(maxsize=16)

        while not self.__stop_event.is_set():
            if self.__video_player.play_video and self.__image_producer.running():
                if not self._process_next_image():
                    continue
            else:
                self._process_image()
        with self.__producer_lock:
            self.__image_producer.stop()

    def _process_next_image(self) -> bool:
        """Process the next image obtained from the VideoStream

        :return: True if VideoStream still has frames to read, False otherwise
        :rtype: bool
        """
        with self.__producer_lock:
            image = self.__image_producer.read()
            self.__video_player.update_fps()

        if image:
            self.__image = image
            self._process_image()
            self.__video_player.stop_fps()

        return self.__image_producer.running()

    def _process_image(self):
        """Process the currently loaded image"""
        show_threshold = self.__video_player.show_threshold
        selected_colour = self.__colour_settings.selected_colour
        mask_colour = self.__colour_settings.colour_mask

        output_frame, ball_potted, count = self.__ball_tracker.process_image(
            deepcopy(self.__image), 
            show_threshold=show_threshold,
            detect_colour=selected_colour if selected_colour != "NONE" else None,
            mask_colour=mask_colour
        )

        self.__video_player.queue_size = self.__image_producer.Q.qsize()

        with self.__producer_lock:
            self.__video_player.output_frame = output_frame
            self.__video_player.hsv_frame = self.__image.hsv_frame

        if ball_potted:
            self.__logger.balls_potted.addPottedBall(f'Potted {count} {ball_potted.lower()}/s...')
