from tkinter import *
from tkinter.ttk import *
# from tkinter.ttk import Style, Separator, Progressbar
import cv2
import os
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

        self.a = Toplevel()
        self.a.wm_protocol("WM_DELETE_WINDOW", self.on_close)
        self.a.title("Launching...")
        self.a.geometry("+{}+{}".format(positionRight, positionDown))
        self.dots = 5
        Label(self.a, text="=== Snooker Ball Tracker - Demo Application ===").pack(padx=20, pady=(20, 5))
        Label(self.a, text="Version: 0.1.dev0").pack(padx=20)
        Separator(self.a, orient="horizontal").pack(pady=(20, 0), fill="x", expand=True)
        self.load = Label(self.a, text="Loading{}".format("."*5), font=("Helvetica", 18))
        self.progress_bar = Progressbar(self.a, orient="horizontal", length=200, mode="determinate")
        self.load.pack(padx=20, pady=(20, 0))
        self.progress_bar.pack(padx=20, pady=(0, 20))
        self.load_bar()

    def load_bar(self):
        self.dots += 1
        self.progress_bar["value"] += 3
        self.root.update_idletasks()
        if self.dots > 5:
            self.dots = 1
        self.load.config(text="Loading{}{}".format("."*self.dots, " "*(5-self.dots)))
        if self.progress_bar["value"] >= 100:
            self.a.destroy()
            self.root.deiconify()
            # try:
            #     self.root.attributes('-zoomed', True)
            # except TclError:
            #     self.root.state("zoomed")
            # return
        else:
            self.root.after(100,self.load_bar)
    
    def on_close(self):
        self.a.destroy()
        self.root.destroy()


class GUI(Tk):
    def __init__(self):
        super().__init__() 
        self.iconphoto(True, PhotoImage(file=os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "icon.png")))
        self.iconname("Snooker Ball Tracker")
        self.title("Snooker Ball Tracker - Demo Application")
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)
        try:
            self.attributes('-zoomed', True)
        except TclError:
            self.state("zoomed")
        self.withdraw()

        try:
            Style().theme_use("vista")
        except TclError:
            Style().theme_use("default")
        SplashScreen(self)

        # threading.Thread(target=self.__load_splashscreen, daemon=True).start()

        font.nametofont("TkDefaultFont").configure(size=10)
        font.nametofont("TkTextFont").configure(size=10)

        s.settings_module_name = "pre_recorded_footage"
        s.load()

        self.fonts = {
            "h1": font.Font(size=24, weight="bold"),
            "h2-bold": font.Font(size=22, weight="bold"),
            "h2": font.Font(size=22),
            "h3-bold": font.Font(size=20, weight="bold"),
            "h3": font.Font(size=16),
            "h4": font.Font(size=14),
            "h5": font.Font(size=12),
            "logs": font.Font(size=10)
        }

        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.thread = None
        self.stream = None
        self.selected_file = None
        self.ball_tracker = None

        print(Style().lookup("TButton", "background"))
        self.styles = [
            Style().configure("Canvas", background="NavajoWhite3"),
            Style().configure("Left.TFrame", background="red"),
            Style().configure("Middle.TFrame", background="blue"),
            Style().configure("Right.TFrame", background="green"),
            Style().configure("DB.TFrame", background="light gray"),
            Style().configure("TButton", padding=6, cursor="hand2"),
            Style().configure("TMenubutton", padding=6, background="light gray"),
            Style().configure("TRadiobutton", relief="raised")
        ]

        self.scrollable_canvas = Canvas(master=self, highlightthickness = 0, background="#dcdad5")
        self.vert_scrollbar = Scrollbar(master=self, orient="vertical", command=self.scrollable_canvas.yview)
        self.hori_scrollbar = Scrollbar(master=self, orient="horizontal", command=self.scrollable_canvas.xview)
        # self.main_frame = Frame(master=self)

        # self.main_frame.fonts = self.fonts
        # self.main_frame.styles = self.styles
        # self.main_frame.lock = threading.Lock()
        # self.main_frame.stop_event = threading.Event()
        # self.main_frame.thread = None
        # self.main_frame.stream = None
        # self.main_frame.selected_file = None
        # self.main_frame.ball_tracker = None

        # self.left = Frame(master=self, style="Left.TFrame")
        # self.middle = Frame(master=self, style="Middle.TFrame")
        # self.right = Frame(master=self, style="Right.TFrame")
        self.left = Frame(master=self)
        self.middle = Frame(master=self)
        self.right = Frame(master=self)
        self.bottom = Frame(master=self)
        self.separator_vert_1 = Separator(master=self, orient="vertical")
        self.separator_vert_2 = Separator(master=self, orient="vertical")

        # self.main_frame.bind(
        #     "<Configure>",
        #     lambda e: self.scrollable_canvas.configure(
        #         scrollregion=self.scrollable_canvas.bbox("all")
        #     )
        # )

        # self.scrollable_canvas.configure(yscrollcommand=self.vert_scrollbar.set)
        # self.scrollable_canvas.configure(xscrollcommand=self.hori_scrollbar.set)

        self.program_output = ProgramOutput(master=self.middle)
        self.ball_tracker_options = BallTrackerOptions(master=self.left, logger=self.program_output)
        self.colour_detection_options = ColourDetectionOptions(master=self.left, logger=self.program_output)
        self.video_player = VideoPlayer(master=self.right, logger=self.program_output)

        self.nav_bar = Navbar(master=self.bottom)
        self.nav_bar.pack(side="bottom", fill="x", anchor="s")

        self.bottom.pack(side="bottom", fill="x", anchor="s")
        # self.main_frame.pack(side="left", fill="both", expand=True)
        # self.hori_scrollbar.pack(side="bottom", fill="x")
        # self.scrollable_canvas.pack(side="left", fill="both", expand=True)
        # self.vert_scrollbar.pack(side="right", fill="y")
        # self.scrollable_canvas.create_window((0, 0), window=self.main_frame, anchor="center")

        self.__setup_left_column()
        self.__setup_middle_column()
        self.__setup_right_column()
        self.__setup_window()

    def __load_splashscreen(self):
        SplashScreen(self)

    def __setup_window(self):
        self.left.pack(side="left", fill="y", expand=True, anchor="w", ipadx=10, ipady=10)
        self.separator_vert_1.pack(side="left", fill="y", expand=True, padx=20)
        self.middle.pack(side="left", fill="y", expand=True, anchor="center", ipady=20)
        self.separator_vert_2.pack(side="left", fill="y", expand=True, padx=20)
        self.right.pack(side="left", fill="y", expand=True, anchor="e", ipadx=10, ipady=10)

    def __setup_left_column(self):
        self.ball_tracker_options.pack(side="top", fill="both", expand=1, anchor="nw", padx=(20, 0), pady=(20, 10))
        self.ball_tracker_options.grid_children()
        self.colour_detection_options.pack(side="top", fill="both", expand=1, anchor="w", padx=(20, 0), pady=(0, 20))
        self.colour_detection_options.grid_children()

    def __setup_middle_column(self):
        self.program_output.pack(side="left", fill="both", expand=True, pady=(20, 10))
        self.program_output.grid_children()

    def __setup_right_column(self):
        self.video_player.pack(side="top", fill="both", expand=1, anchor="sw", padx=(0, 20), pady=(20, 10))
        self.video_player.grid_children()

    def on_close(self):
        if self.stream is not None:
            self.stream.release()
        self.quit()
        
    def select_file_onclick(self):
        self.selected_file = filedialog.askopenfilename()

        if self.selected_file == "":
            return

        if self.thread is not None:
            self.thread.stop_event.set()

        try:
            self.stream = cv2.VideoCapture(self.selected_file)
            if not self.stream.isOpened():
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
        self.stream = cv2.VideoCapture(self.selected_file)
        self.ball_tracker = BallTracker()
        self.stop_event = threading.Event()
        self.thread = VideoProcessor(master=self, stream=self.stream, 
                                                video_file=self.selected_file, ball_tracker=self.ball_tracker, 
                                                lock=self.lock, stop_event=self.stop_event)
        self.thread.start()