import cv2
import threading
import snooker_ball_tracker.settings as s
from PIL import Image, ImageTk

class VideoProcessor(threading.Thread):
    def __init__(self, master, stream, video_file, ball_tracker, lock):
        super().__init__(args=(lock,), name="video_processor", daemon=True)
        self.master = master
        self.play_stream = True
        self.stream = stream
        self.video_file = video_file
        self.ball_tracker = ball_tracker
        self.show_threshold = False
        self.detect_colour = "None"
        self.__frame = None

    def run(self):
        while True:
            detect_colour = self.detect_colour
            show_threshold = self.show_threshold
            ball_tracker = self.ball_tracker
            if self.play_stream:
                success, frame = self.stream.read()
                if success:
                    if detect_colour != "None":
                        self.__frame, threshold, hsv = ball_tracker.perform_init_ops(frame, width=800, crop=True)
                        colour_mask, contours = ball_tracker.detect_colour(
                            hsv, s.COLOURS[detect_colour]['LOWER'], s.COLOURS[detect_colour]['UPPER']
                        )
                        if show_threshold:
                            self.__frame = threshold
                        else:
                            self.__frame = cv2.bitwise_and(self.__frame, self.__frame, mask=colour_mask)
                        cv2.drawContours(self.__frame, contours, -1, (0, 255, 0), 2)
                    else:
                        self.__frame, _, _ = ball_tracker.run(frame, width=800, crop=True, show_threshold=show_threshold)
                    
                    self.__frame = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.__frame, cv2.COLOR_BGR2RGB)))
                else:
                    print("exiting...")
                    break


                self.master.main_view.file_output.configure(image=self.__frame)
                self.master.main_view.file_output.image = self.__frame
                if ball_tracker.update_boundary:
                    ball_tracker.update_boundary = False

    def restart_stream(self):
        self.stream = cv2.VideoCapture(self.video_file)
        success, frame = self.stream.read()
        if success and frame is not None:
            frame, _, _ = self.ball_tracker.run(frame, width=800, crop=True, show_threshold=self.show_threshold)
            frame = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

            self.master.main_view.file_output.configure(image=frame)
            self.master.main_view.file_output.image = frame
            if self.ball_tracker.update_boundary:
                self.ball_tracker.update_boundary = False

    def update_bounds(self):
        self.ball_tracker.update_boundary = True
