import cv2
import threading
import snooker_ball_tracker.settings as s
import time
from PIL import Image, ImageTk
from tkinter import END
from imutils.video import FPS
from snooker_ball_tracker.video_file_stream import VideoFileStream
from queue import Queue
from random import randint
from copy import copy


class VideoProcessor(threading.Thread):
    def __init__(self, master, stream, video_file, ball_tracker, lock, stop_event):
        super().__init__(name="VideoProcessor{}".format(randint(0, 100)), daemon=True)
        self.master = master
        self.stream_lock = lock
        self.stop_event = stop_event
        self.play_stream = True
        self.stream = stream
        self.video_file = video_file
        self.ball_tracker = ball_tracker
        self.show_threshold = False
        self.mask_colour = False
        self.detect_colour = "None"
        self.crop_frames = False
        self.__input_frame = None
        self.__input_hsv = None
        self.__input_threshold = None
        self.__output_frame = None
        self.__fps = FPS()

    def get_hsv(self):
        return self.__input_hsv

    def run(self):
        self.stream.start()
        self.__fps.start()
        self._process_next_frame()
        self.play_stream = False
        self.stream.Q = Queue(maxsize=8)

        while not self.stop_event.is_set():
            if self.play_stream and self.stream.running():
                if not self._process_next_frame():
                    continue
            else:
                self._process_frame()
        with self.stream_lock:
            self.stream.stop()

    def _process_next_frame(self):
        with self.stream_lock:
            input_frame, input_threshold, input_hsv = self.stream.read()

        if input_frame is not None:
            self.__input_frame, self.__input_threshold, self.__input_hsv = input_frame, input_threshold, input_hsv
            self._process_frame()

        if self.stream.running():
            return True

        return False

    def _process_frame(self):
        self.stream.detect_colour = self.detect_colour
        self.stream.crop_frames = self.crop_frames
        ball_potted = None
        count = None

        self.__output_frame, ball_potted, count = self.ball_tracker.run(
            (copy(self.__input_frame), copy(self.__input_threshold), copy(self.__input_hsv)), width=800, crop=self.stream.crop_frames, show_threshold=self.show_threshold)

        if self.stream.detect_colour != "None":
            colour_mask, contours = self.ball_tracker.detect_colour(
                self.__input_hsv, s.COLOURS[self.stream.detect_colour]['LOWER'], s.COLOURS[self.stream.detect_colour]['UPPER']
            )
            if self.show_threshold:
                self.__output_frame = copy(self.__input_threshold)
            else:
                if self.mask_colour:
                    self.__output_frame = cv2.bitwise_and(
                        self.__output_frame, self.__output_frame, mask=colour_mask)

            cv2.drawContours(self.__output_frame, contours, -1, (0, 255, 0), 2)

        if self.play_stream:
            self.__fps.update()
            self.__fps.stop()

        cv2.putText(self.__output_frame, "Queue Size: {}".format(self.stream.Q.qsize()),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.putText(self.__output_frame, "FPS: {:.2f}".format(self.__fps.fps()),
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        self.__output_frame = ImageTk.PhotoImage(image=Image.fromarray(
            cv2.cvtColor(self.__output_frame, cv2.COLOR_BGR2RGB)))

        self.display_frame()

        if ball_potted is not None:
            self.master.program_output.balls_potted_list.insert(
                END, 'Potted {} {}/s...'.format(count, ball_potted.lower()))
            self.master.program_output.balls_potted_list.see(END)

    def display_frame(self):
        self.master.video_player.file_output.configure(
            image=self.__output_frame)
        self.master.video_player.file_output.image = self.__output_frame

        self.master.program_output.current_ball_count['text'] = self.ball_tracker.get_snapshot_status(
        )
        self.master.program_output.last_ball_count['text'] = self.ball_tracker.get_snapshot_status(
            False)
        self.master.program_output.white_ball_status['text'] = self.ball_tracker.get_white_ball_status(
        )

    def update_bounds(self):
        self.stream.update_boundary = True

    def crop_frames_around_boundary(self, crop):
        self.ball_tracker.reset_snapshots()
        self.crop_frames = crop
