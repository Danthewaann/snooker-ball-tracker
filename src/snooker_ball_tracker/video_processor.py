import threading
from copy import deepcopy
from queue import Queue

import cv2
from imutils.video import FPS

import settings as s

from .ball_tracker import BallTracker, Logger, VideoPlayer
from .ball_tracker.settings import ColourDetectionSettings
from .video_file_stream import VideoFileStream


class VideoProcessor(threading.Thread):
    def __init__(self, video_stream: VideoFileStream, logger: Logger, 
                 video_player: VideoPlayer, colour_settings: ColourDetectionSettings,
                 ball_tracker: BallTracker, lock: threading.Lock, stop_event: threading.Event):
        """Creates instance of VideoProcessor that processes frames from a 
        VideoFileStream and passes them to the ball tracker for processing before
        passing them to the video player to display

        :param video_stream: video stream that produces images to process
        :type video_stream: VideoFileStream
        :param logger: logger instance that we pass ball potted info to
        :type logger: Logger
        :param video_player: video player instance that we pass processed frames to
        :type video_player: VideoPlayer
        :param colour_settings: colour settings that we obtain colour detection info from
        :type colour_settings: ColourDetectionSettings
        :param ball_tracker: ball tracker that we pass frames obtained from VideoFileStream to
        :type ball_tracker: BallTracker
        :param lock: lock used to manage access to VideoFileStream
        :type lock: threading.Lock
        :param stop_event: stop event used to shut down the VideoProcessor
        :type stop_event: threading.Event
        """
        super().__init__(name=self.__class__.__name__, daemon=True)
        self.__logger = logger
        self.__video_player = video_player
        self.__colour_settings = colour_settings
        self.__ball_tracker = ball_tracker
        self.__producer_lock = lock
        self.__stop_event = stop_event
        self.__image_producer = video_stream
        self.__image = None
        self.__fps = FPS()

    def run(self):
        """Run the main video processor process"""
        self.__video_player.play_video = True
        self.__image_producer.start()
        self.__fps.start()
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
        """Process the next image obtained from the VideoFileStream

        :return: True if VideoFileStream still has frames to read, False otherwise
        :rtype: bool
        """
        with self.__producer_lock:
            image = self.__image_producer.read()

        if image:
            self.__image = image
            self._process_image()

        if self.__image_producer.running():
            return True

        return False

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

        if self.__video_player.play_video:
            self.__fps.update()
            self.__fps.stop()

        cv2.putText(output_frame, "Queue Size: {}".format(self.__image_producer.Q.qsize()),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(output_frame, "FPS: {:.2f}".format(self.__fps.fps()),
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        with self.__producer_lock:
            self.__video_player.frame = output_frame

        if ball_potted:
            self.__logger.balls_potted.addPottedBall(f'Potted {count} {ball_potted.lower()}/s...')
