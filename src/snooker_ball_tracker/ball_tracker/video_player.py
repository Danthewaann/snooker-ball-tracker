from __future__ import annotations

import threading
from typing import TYPE_CHECKING

import magic
import numpy as np
import PyQt5.QtCore as QtCore
from imutils.video import FPS

from . import BallTracker
from .video_file_stream import VideoFileStream
from .video_processor import VideoProcessor

if TYPE_CHECKING:
    from .types import Frame


class VideoPlayer(QtCore.QObject):
    def __init__(self, ball_tracker: BallTracker) -> None:
        """Creates an instance of this class that contains properties used by the
        video player to display frames processed by the ball tracker"""
        super().__init__()
        self.ball_tracker = ball_tracker or BallTracker()
        self.video_processor_lock = threading.Lock()
        self.video_processor_stop_event = threading.Event()
        self.video_processor: VideoProcessor | None = None
        self.video_file_stream: VideoFileStream | None = None
        self.video_file: str | None = None

        self._width = 1100
        self._height = 600
        self._play = False
        self._crop_frames = False
        self._show_threshold = False
        self._perform_morph = False
        self._detect_table = False
        self._queue_size = 0
        self._fps = FPS()
        self._output_frame: Frame = np.array([])
        self._hsv_frame: Frame = np.array([])

    widthChanged = QtCore.pyqtSignal(int)

    @property
    def width(self) -> int:
        """Width property

        :return: player width
        """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """Width setter

        :param value: value to set
        """
        self._width = value
        self.widthChanged.emit(self._width)

    heightChanged = QtCore.pyqtSignal(int)

    @property
    def height(self) -> int:
        """Height property

        :return: player height
        """
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        """Height setter

        :param value: value to set
        """
        self._height = value
        self.heightChanged.emit(self._height)

    playChanged = QtCore.pyqtSignal(bool)

    @property
    def play(self) -> bool:
        """Play property

        :return: play video
        """
        return self._play

    @play.setter
    def play(self, value: bool) -> None:
        """Play setter

        :param value: value to set
        """
        self._play = value
        self.playChanged.emit(self._play)

    crop_framesChanged = QtCore.pyqtSignal(bool)

    @property
    def crop_frames(self) -> bool:
        """Crop frames property

        :return: crop frames
        """
        return self._crop_frames

    @crop_frames.setter
    def crop_frames(self, value: bool) -> None:
        """Crop frames setter

        :param value: value to set
        """
        self._crop_frames = value
        self.crop_framesChanged.emit(self._crop_frames)

    show_thresholdChanged = QtCore.pyqtSignal(bool)

    @property
    def show_threshold(self) -> bool:
        """Show threshold property

        :return: show threshold
        """
        return self._show_threshold

    @show_threshold.setter
    def show_threshold(self, value: bool) -> None:
        """Show threshold setter

        :param value: value to set
        """
        self._show_threshold = value
        self.show_thresholdChanged.emit(self._show_threshold)

    perform_morphChanged = QtCore.pyqtSignal(bool)

    @property
    def perform_morph(self) -> bool:
        """Perform morph property

        :return: perform morph
        """
        return self._perform_morph

    @perform_morph.setter
    def perform_morph(self, value: bool) -> None:
        """Perform morph setter

        :param value: value to set
        """
        self._perform_morph = value
        self.perform_morphChanged.emit(self._perform_morph)

    detect_tableChanged = QtCore.pyqtSignal(bool)

    @property
    def detect_table(self) -> bool:
        """Detect table property

        :return: detect table
        """
        return self._detect_table

    @detect_table.setter
    def detect_table(self, value: bool) -> None:
        """Detect table setter

        :param value: value to set
        """
        self._detect_table = value
        self.detect_tableChanged.emit(self._detect_table)

    queue_sizeChanged = QtCore.pyqtSignal(int)

    @property
    def queue_size(self) -> int:
        """Queue size property

        :return: queue size
        """
        return self._queue_size

    @queue_size.setter
    def queue_size(self, value: int) -> None:
        """Queue size setter

        :param value: value to set
        """
        self._queue_size = value
        self.queue_sizeChanged.emit(self._queue_size)

    fpsChanged = QtCore.pyqtSignal(int)

    def start_fps(self) -> None:
        """Start FPS timer"""
        self._fps = FPS()
        self._fps.start()

    def update_fps(self) -> None:
        """Update FPS timer"""
        self._fps.update()

    def stop_fps(self) -> None:
        """Stop FPS timer"""
        self._fps.stop()
        self.fpsChanged.emit(self._fps.fps())

    output_frameChanged = QtCore.pyqtSignal(np.ndarray)

    @property
    def output_frame(self) -> Frame:
        """Frame property

        :return: output frame
        """
        return self._output_frame

    @output_frame.setter
    def output_frame(self, value: Frame) -> None:
        """Output frame setter

        :param value: value to set
        """
        self._output_frame = value
        self.output_frameChanged.emit(self._output_frame)

    hsv_frameChanged = QtCore.pyqtSignal(np.ndarray)

    @property
    def hsv_frame(self) -> Frame:
        """HSV frame property

        :return: hsv frame
        """
        return self._hsv_frame

    @hsv_frame.setter
    def hsv_frame(self, value: Frame) -> None:
        """HSV frame setter

        :param value: value to set
        """
        self._hsv_frame = value
        self.hsv_frameChanged.emit(self._hsv_frame)

    def start(self, video_file: str | None = None) -> None:
        """Creates VideoProcessor and VideoFileStream instances to handle
        the selected video file.

        The VideoFileStream is the producer thread and the VideoProcessor
        is the consumer thread, where the VideoFileStream instance reads
        frames from the video file and puts them into a queue for the
        VideoProcessor to obtain frames to process from.

        The VideoProcessor then passes processed frames to the VideoPlayer
        to display to the user.

        :param video_file: video file to read from, defaults to None
        :raises TypeError: if `video_file` isn't an actual video file
        """
        if video_file and "video" not in magic.from_file(
            video_file, mime=True
        ):  # type: ignore[no-untyped-call]
            raise TypeError(f"{video_file} is not a video file")

        self.play = False
        self.video_file = video_file or self.video_file

        if self.video_file is None:
            raise ValueError("video_file is not set")

        self.destroy_video_threads()
        self.video_processor_stop_event.clear()

        self.video_file_stream = VideoFileStream(
            self.video_file,
            video_player=self,
            colour_settings=self.ball_tracker.colour_settings,
            queue_size=1,
        )

        self.video_processor = VideoProcessor(
            video_stream=self.video_file_stream,
            video_player=self,
            ball_tracker=self.ball_tracker,
            lock=self.video_processor_lock,
            stop_event=self.video_processor_stop_event,
        )

        self.video_processor.start()

    def restart(self) -> None:
        """Restart the video player by destroying the VideoProcessor
        and VideoFileStream instances and creating new ones before
        starting the video player again."""
        self.start()

    def destroy_video_threads(self) -> None:
        """Destroy the VideoProcessor and VideoFileStream thread instances"""
        if self.video_processor is not None:
            if self.video_file_stream is not None:
                with self.video_processor_lock:
                    self.video_file_stream.stop()
            self.video_processor_stop_event.set()
            self.video_processor.join()
