import cv2
import threading
import snooker_ball_tracker.settings as s
from PIL import Image, ImageTk
from tkinter import END

class VideoProcessor(threading.Thread):
    def __init__(self, master, stream, video_file, ball_tracker, lock, stop_event):
        super().__init__(name="video_processor", daemon=True)
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
        self.__output_frame = None

    def run(self):
        self._process_next_frame()
        self.play_stream = False
        while not self.stop_event.is_set():
            if self.play_stream:
                if not self._process_next_frame():
                    print("exiting...")
                    break
            else:
                self._process_frame()
        with self.stream_lock:
            self.stream.release()

    def _process_next_frame(self):
        if self.play_stream:
            with self.stream_lock:
                success, self.__input_frame = self.stream.read()
                if success:
                    self._process_frame()
                return success
        return True

    def _process_frame(self):
        detect_colour = self.detect_colour
        crop_frames = self.crop_frames
        ball_potted = None
        count = None
        if detect_colour != "None":
            self.__output_frame, threshold, hsv = self.ball_tracker.perform_init_ops(self.__input_frame, width=800, crop=crop_frames)
            colour_mask, contours = self.ball_tracker.detect_colour(
                hsv, s.COLOURS[detect_colour]['LOWER'], s.COLOURS[detect_colour]['UPPER']
            )
            if self.show_threshold:
                self.__output_frame = threshold
            else:
                if self.mask_colour:
                    self.__output_frame = cv2.bitwise_and(self.__output_frame, self.__output_frame, mask=colour_mask)
            cv2.drawContours(self.__output_frame, contours, -1, (0, 255, 0), 2)
        else:
            self.__output_frame, ball_potted, count = self.ball_tracker.run(self.__input_frame, width=800, crop=crop_frames, show_threshold=self.show_threshold)
        
        self.__output_frame = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.__output_frame, cv2.COLOR_BGR2RGB)))
        self.master.video_player.file_output.configure(image=self.__output_frame)
        self.master.video_player.file_output.image = self.__output_frame

        self.master.program_output.current_ball_count['text'] = self.ball_tracker.get_snapshot_status()
        self.master.program_output.last_ball_count['text'] = self.ball_tracker.get_snapshot_status(False)
        self.master.program_output.white_ball_status['text'] = self.ball_tracker.get_white_ball_status()

        if ball_potted is not None:
            self.master.program_output.balls_potted_list.insert(END, 'Potted {} {}/s...'.format(count, ball_potted.lower()))
            self.master.program_output.balls_potted_list.see(END)

    def restart_stream(self):
        self.ball_tracker.reset()
        self.stream = cv2.VideoCapture(self.video_file)

    def update_bounds(self):
        self.ball_tracker.update_boundary = True

    def crop_frames_around_boundary(self, crop):
        self.ball_tracker.reset_snapshots()
        self.crop_frames = crop
