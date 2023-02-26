from __future__ import annotations

import threading
from copy import deepcopy
from queue import Queue
from time import sleep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import BallTracker, VideoPlayer
    from .types import Frame
    from .video_stream import VideoStream


class VideoProcessor(threading.Thread):
    def __init__(
        self,
        video_stream: VideoStream,
        video_player: VideoPlayer,
        ball_tracker: BallTracker,
        lock: threading.Lock,
        stop_event: threading.Event,
    ) -> None:
        """Creates instance of VideoProcessor that processes frames from a
        VideoStream and passes them to the ball tracker for processing before
        passing them to the video player to display

        :param video_stream: video stream that produces images to process
        :param video_player: video player instance that we pass processed frames to
        :param ball_tracker: ball tracker that we pass frames obtained from
                             VideoStream to
        :param lock: lock used to manage access to VideoStream
        :param stop_event: stop event used to shut down the VideoProcessor
        """
        super().__init__(name=self.__class__.__name__, daemon=True)
        self.__logger = ball_tracker.logger
        self.__video_player = video_player
        self.__colour_settings = ball_tracker.colour_settings
        self.__ball_tracker = ball_tracker
        self.__producer_lock = lock
        self.__stop_event = stop_event
        self.__frame_producer = video_stream
        self.__frame: Frame | None = None

    def run(self) -> None:
        """Run the main video processor process"""
        self.__video_player.play = True
        self.__frame_producer.start()
        self.__video_player.start_fps()
        self._process_next_image()
        self.__video_player.play = False
        self.__frame_producer.Q = Queue(maxsize=16)

        while not self.__stop_event.is_set():
            if self.__video_player.play and self.__frame_producer.running():
                self._process_next_image()
            else:
                self._process_image()
        with self.__producer_lock:
            self.__frame_producer.stop()

    def _process_next_image(self) -> None:
        """Process the next image obtained from the VideoStream"""
        with self.__producer_lock:
            frame = self.__frame_producer.read()
            self.__video_player.update_fps()

        if frame is not None:
            self.__frame = frame
            self._process_image()
            self.__video_player.stop_fps()
            # Limit frame processing speed
            sleep(0.01)

    def _process_image(self) -> None:
        """Process the currently loaded image"""
        if self.__frame is None:
            raise ValueError("frame is not set")

        show_threshold = self.__video_player.show_threshold
        detect_table = self.__video_player.detect_table
        crop_frames = self.__video_player.crop_frames
        perform_morph = self.__video_player.perform_morph
        selected_colour = self.__colour_settings.selected_colour
        mask_colour = self.__colour_settings.colour_mask

        image, ball_potted, count = self.__ball_tracker.process_frame(
            deepcopy(self.__frame),
            show_threshold=show_threshold,
            detect_table=detect_table,
            crop_frames=crop_frames,
            perform_morph=perform_morph,
            detect_colour=selected_colour if selected_colour != "NONE" else None,
            mask_colour=mask_colour,
        )

        self.__video_player.detect_table = False

        self.__video_player.queue_size = self.__frame_producer.Q.qsize()

        with self.__producer_lock:
            self.__video_player.output_frame = image.frame
            self.__video_player.hsv_frame = image.hsv_frame

        if ball_potted:
            self.__logger.balls_potted.addPottedBall(
                f"Potted {count} {ball_potted.lower()}/s..."
            )
