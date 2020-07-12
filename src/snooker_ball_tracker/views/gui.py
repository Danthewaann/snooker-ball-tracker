import tkinter as tk
from tkinter.ttk import Style, Separator, Progressbar
import cv2
import imutils
import numpy as np
import time
import threading
from snooker_ball_tracker.views.components.navbar import Navbar
from snooker_ball_tracker.views.components.ball_tracker_options import BallTrackerOptions
from snooker_ball_tracker.views.components.colour_detection_options import ColourDetectionOptions
from snooker_ball_tracker.views.components.program_output import ProgramOutput
from snooker_ball_tracker.views.components.video_player import VideoPlayer
from snooker_ball_tracker.ball_tracker import BallTracker
from snooker_ball_tracker.video_processor import VideoProcessor
import snooker_ball_tracker.settings as s
from collections import OrderedDict
from tkinter import font
from tkinter import filedialog
from PIL import Image, ImageTk

# class Splash(tk.Toplevel):
#     def __init__(self, master):
#         tk.Toplevel.__init__(self, master)
#         self.title("Splash")

#         ## required to make window show before the program gets to the mainloop
#         self.update()

class SplashScreen:
    def __init__(self, root):
        self.root = root
        # Gets the requested values of the height and width.
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        print("Width",windowWidth,"Height",windowHeight)

        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

        self.a = tk.Toplevel()
        self.a.title("Launching...")
        self.a.geometry("+{}+{}".format(positionRight, positionDown))
        self.dots = 5
        tk.Label(self.a,text="Snooker Ball Tracker - Demo Application").pack(padx=20, pady=20)
        self.load = tk.Label(self.a, text="Loading{}".format("."*5), font=("Helvetica", 18))
        self.progress_bar = Progressbar(self.a, orient="horizontal", length=200, mode="determinate")
        self.load.pack(padx=20, pady=(20, 0))
        self.progress_bar.pack(padx=20, pady=(0, 20))
        self.load_bar()

    def load_bar(self):
        self.dots += 1
        self.progress_bar["value"] += 5
        self.root.update_idletasks()
        # self.percentage +=5
        if self.dots > 5:
            self.dots = 1
        self.load.config(text="Loading{}{}".format("."*self.dots, " "*(5-self.dots)))
        if self.progress_bar["value"] == 100:
            self.a.destroy()
            self.root.deiconify()
            return
        else:
            self.root.after(100,self.load_bar)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-zoomed', True)
        self.withdraw()
        SplashScreen(self)
        # threading.Thread(target=self.__load_splashscreen, daemon=True).start()
        self.title("Snooker Ball Tracker - Demo Application")
        s.settings_module_name = "pre_recorded_footage"
        s.load()
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        font.nametofont("TkDefaultFont").configure(size=11, family="Helvetica")
        font.nametofont("TkTextFont").configure(size=11, family="Helvetica")

        self.fonts = {
            "h1": font.Font(size=24, family="Helvetica", weight="bold"),
            "h2-bold": font.Font(size=22, family="Helvetica", weight="bold"),
            "h2": font.Font(size=22, family="Helvetica"),
            "h3-bold": font.Font(size=18, family="Helvetica", weight="bold"),
            "h3": font.Font(size=18, family="Helvetica"),
            "h4": font.Font(size=14, family="Helvetica"),
            "h5": font.Font(size=12, family="Helvetica")
        }

        self.styles = {
            "DB.TFrame": Style().configure("DB.TFrame", background="light gray")
        }

        self.scrollable_canvas = tk.Canvas(master=self)
        self.vert_scrollbar = tk.Scrollbar(master=self, orient="vertical", width=20, command= self.scrollable_canvas.yview)
        self.main_frame = tk.Frame(master=self.scrollable_canvas)

        self.main_frame.fonts = self.fonts
        self.main_frame.lock = threading.Lock()
        self.main_frame.stop_event = threading.Event()
        self.main_frame.thread = None
        self.main_frame.stream = None
        self.main_frame.selected_file = None
        self.main_frame.ball_tracker = None

        self.left = tk.Frame(master=self.main_frame)
        self.middle = tk.Frame(master=self.main_frame)
        self.right = tk.Frame(master=self.main_frame)
        self.bottom = tk.Frame(master=self)
        self.separator_vert_1 = Separator(master=self.main_frame, orient="vertical")
        self.separator_vert_2 = Separator(master=self.main_frame, orient="vertical")

        self.main_frame.bind(
            "<Configure>",
            lambda e: self.scrollable_canvas.configure(
                scrollregion=self.scrollable_canvas.bbox("all")
            )
        )

        self.scrollable_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.scrollable_canvas.configure(yscrollcommand=self.vert_scrollbar.set)

        self.nav_bar = Navbar(master=self.bottom)
        self.nav_bar.pack(side="bottom", fill="x", anchor="s")
        self.bottom.pack(side="bottom", fill="x", anchor="s")
        self.scrollable_canvas.pack(side="left", fill="both", expand=True)
        self.vert_scrollbar.pack(side="right", fill="y")

        self.program_output = ProgramOutput(master=self.middle)
        self.ball_tracker_options = BallTrackerOptions(master=self.left, logger=self.program_output)
        self.colour_detection_options = ColourDetectionOptions(master=self.left, logger=self.program_output)
        self.video_player = VideoPlayer(master=self.right, logger=self.program_output)

        self.__setup_left_column()
        self.__setup_middle_column()
        self.__setup_right_column()
        self.__setup_window()

    def __load_splashscreen(self):
        SplashScreen(self)

    def __setup_window(self):
        self.left.pack(side="left", fill="both", expand=1, anchor="w", padx=(20, 0), pady=(20, 20))
        self.separator_vert_1.pack(side="left", fill="y", expand=1, padx=20)
        self.middle.pack(side="left", fill="both", expand=1, anchor="center", pady=(20, 20))
        self.separator_vert_2.pack(side="left", fill="y", expand=1, padx=20)
        self.right.pack(side="right", fill="both", expand=1, anchor="e", padx=(0, 20), pady=(20, 20))

    def __setup_left_column(self):
        self.ball_tracker_options.grid_children()
        self.ball_tracker_options.pack(side="top", fill="both", expand=1, anchor="nw")
        self.colour_detection_options.pack(side="top", fill="both", expand=1, anchor="w")

    def __setup_middle_column(self):
        self.program_output.pack(side="top", fill="both", anchor="n")

    def __setup_right_column(self):
        self.video_player.pack(side="top", fill="both", expand=1, anchor="sw")

    def on_close(self):
        if self.main_frame.stream is not None:
            self.main_frame.stream.release()
        self.quit()
        
    def select_file_onclick(self):
        self.selected_file = filedialog.askopenfilename()

        if self.selected_file == "":
            return

        if self.main_frame.thread is not None:
            self.main_frame.thread.stop_event.set()

        try:
            self.main_frame.stream = cv2.VideoCapture(self.selected_file)
            if not self.main_frame.stream.isOpened():
                self.program_output.error('Invalid file, please select a video file!')
                return
        except TypeError:
            self.program_output.error('Invalid file, please select a video file!')
            return

        self.video_player.load_video_player()
        self.video_player.reset_video_options()
        self.video_player.btns['toggle'].configure(text="Play")
        self.start_video_processor()

    def start_video_processor(self):
        self.program_output.info("Starting video processor...")
        self.main_frame.stream = cv2.VideoCapture(self.selected_file)
        self.main_frame.ball_tracker = BallTracker()
        self.main_frame.stop_event = threading.Event()
        self.main_frame.thread = VideoProcessor(master=self, stream=self.main_frame.stream, 
                                                video_file=self.selected_file, ball_tracker=self.main_frame.ball_tracker, 
                                                lock=self.main_frame.lock, stop_event=self.main_frame.stop_event)
        self.main_frame.thread.start()