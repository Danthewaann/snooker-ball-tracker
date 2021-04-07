import threading
from copy import copy
from queue import Queue

import cv2
from imutils.video import FPS

import settings as s

from .ball_tracker import BallTracker
from .models import LoggingModel, SettingsModel, VideoPlayerModel
from .video_file_stream import VideoFileStream


class VideoProcessor(threading.Thread):
    def __init__(self, video_stream: VideoFileStream, 
                 logger: LoggingModel, video_player: VideoPlayerModel, settings: SettingsModel,
                 ball_tracker: BallTracker, lock: threading.Lock, stop_event: threading.Event):
        super().__init__(name=self.__class__.__name__, daemon=True)
        self.logger = logger
        self.video_player = video_player
        self.settings = settings
        self.ball_tracker = ball_tracker

        self.stream_lock = lock
        self.stop_event = stop_event
        self.video_stream = video_stream
        self.__input_frame = None
        self.__input_hsv = None
        self.__input_threshold = None
        self.__fps = FPS()

        for model in self.settings.models["ball_detection"].models.values():
            model.filter_byChanged.connect(self.update_ball_tracker)
            model.min_valueChanged.connect(self.update_ball_tracker)
            model.max_valueChanged.connect(self.update_ball_tracker)

    def update_ball_tracker(self):
        kwargs = {}
        for model in self.settings.models["ball_detection"].models.values():
            kwargs["filter_by_" + model.name.lower()] = model.filter_by
            kwargs["min_" + model.name.lower()] = model.min_value / model.multiplier
            kwargs["max_" + model.name.lower()] = model.max_value / model.multiplier

        self.ball_tracker.setup_blob_detector(**kwargs)

    def get_hsv(self):
        return self.__input_hsv

    def run(self):
        self.video_player.play_video = True
        self.video_stream.start()
        self.__fps.start()
        self._process_next_frame()
        self.video_player.play_video = False
        self.video_stream.Q = Queue(maxsize=16)

        while not self.stop_event.is_set():
            if self.video_player.play_video and self.video_stream.running():
                if not self._process_next_frame():
                    continue
            else:
                self._process_frame()
        with self.stream_lock:
            self.video_stream.stop()

    def _process_next_frame(self):
        with self.stream_lock:
            input_frame, input_threshold, input_hsv = self.video_stream.read()

        if input_frame is not None:
            self.__input_frame, self.__input_threshold, self.__input_hsv = input_frame, input_threshold, input_hsv
            self._process_frame()

        if self.video_stream.running():
            return True

        return False

    def _process_frame(self):
        self.video_stream.detect_colour = self.settings.models["colour_detection"].selected_colour
        self.video_stream.crop_frames = self.video_player.crop_frames

        output_frame, ball_potted, count = self.ball_tracker.run(
            (copy(self.__input_frame), copy(self.__input_threshold), copy(self.__input_hsv)), width=800, 
            crop=self.video_stream.crop_frames, show_threshold=self.video_player.show_threshold
        )

        if self.video_stream.detect_colour != "NONE":
            colour_mask, contours = self.ball_tracker.detect_colour(
                self.__input_hsv, self.settings.models["colour_detection"].colour_model.lower_range(), 
                self.settings.models["colour_detection"].colour_model.upper_range()
            )
            if self.video_player.show_threshold:
                output_frame = copy(self.__input_threshold)
            else:
                if self.settings.models["colour_detection"].colour_mask:
                    output_frame = cv2.bitwise_and(
                        output_frame, output_frame, mask=colour_mask)

            cv2.drawContours(output_frame, contours, -1, (0, 255, 0), 2)

        if self.video_player.play_video:
            self.__fps.update()
            self.__fps.stop()

        cv2.putText(output_frame, "Queue Size: {}".format(self.video_stream.Q.qsize()),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(output_frame, "FPS: {:.2f}".format(self.__fps.fps()),
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        self.video_player.frame = output_frame

        if ball_potted is not None:
            self.logger.balls_potted.addPottedBall(f'Potted {count} {ball_potted.lower()}/s...')
