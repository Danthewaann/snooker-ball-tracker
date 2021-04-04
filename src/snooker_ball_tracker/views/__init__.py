import os
import threading
from collections import OrderedDict

import cv2
import numpy as np
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import BallTracker
from snooker_ball_tracker.video_file_stream import VideoFileStream
from snooker_ball_tracker.video_processor import VideoProcessor

from snooker_ball_tracker.models.settings_model import SettingsModel
from snooker_ball_tracker.models.logging_model import LoggingModel
from snooker_ball_tracker.models.video_player_model import VideoPlayerModel

from .logging_view import LoggingView
from .settings_view import SettingsView
from .video_player_view import VideoPlayerView


class SplashScreen:
    def __init__(self, root):
        self.root = root

        # Gets the requested values of the height and width.
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()

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
        Separator(self.a, orient="horizontal").pack(
            pady=(20, 0), fill="x", expand=True)
        self.load = Label(self.a, text="Loading{}".format(
            "."*5), font=("Helvetica", 18))
        self.progress_bar = Progressbar(
            self.a, orient="horizontal", length=200, mode="determinate")
        self.load.pack(padx=20, pady=(20, 0))
        self.progress_bar.pack(padx=20, pady=(0, 20))
        self.load_bar()

    def load_bar(self):
        self.dots += 1
        self.progress_bar["value"] += 3
        if self.dots > 5:
            self.dots = 1
        self.load.config(text="Loading{}{}".format(
            "."*self.dots, " "*(5-self.dots)))
        if self.progress_bar["value"] >= 100:
            self.a.destroy()
            self.root.deiconify()
        else:
            self.root.update()
            self.root.after(100, self.load_bar)

    def on_close(self):
        self.a.destroy()
        self.root.destroy()


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, args):
        super().__init__()

        self.settings_file = args.settings_file

        if self.settings_file:
            s.load(self.settings_file)

        self.setWindowTitle("Snooker Ball Tracker Demo")

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget_layout = QtWidgets.QGridLayout(self.central_widget)
        self.central_widget_layout.setContentsMargins(30, 30, 30, 30)
        self.central_widget_layout.setSpacing(30)

        self.settings_model = SettingsModel()
        self.settings_view = SettingsView(self.settings_model)

        self.logging_model = LoggingModel()
        self.logging_view = LoggingView(self.logging_model)

        self.video_player_model = VideoPlayerModel()
        self.video_player_view = VideoPlayerView(self.video_player_model)

        self.central_widget_layout.addWidget(self.settings_view, 0, 0, 1, 1)
        self.central_widget_layout.addWidget(self.logging_view, 1, 0, 1, 1)
        self.central_widget_layout.addWidget(self.video_player_view, 0, 1, 2, 1)
        self.central_widget_layout.setColumnStretch(1, 2)

        self.setCentralWidget(self.central_widget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1269, 22))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuExit = QtWidgets.QMenu(self.menubar)
        self.menuExit.setObjectName("menuExit")
        self.menuExit_2 = QtWidgets.QMenu(self.menubar)
        self.menuExit_2.setObjectName("menuExit_2")
        self.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setEnabled(True)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)
        self.actionLoad = QtWidgets.QAction(self)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionSelect_Video_File = QtWidgets.QAction(self)
        self.actionSelect_Video_File.setObjectName("actionSelect_Video_File")
        self.menuSettings.addAction(self.actionLoad)
        self.menuSettings.addAction(self.actionSave)
        self.menuExit.addAction(self.actionSelect_Video_File)
        self.menubar.addAction(self.menuExit.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuExit_2.menuAction())

    #     try:
    #         self.iconphoto(True, PhotoImage(file="icon.png"))
    #     except TclError:
    #         pass

    #     self.iconname("Snooker Ball Tracker")
    #     self.title("Snooker Ball Tracker - Demo Application")
    #     self.wm_protocol("WM_DELETE_WINDOW", self.on_close)

    #     try:
    #         self.attributes('-zoomed', True)
    #     except TclError:
    #         self.state("zoomed")

    #     if args.splash:
    #         self.withdraw()

    #     try:
    #         Style().theme_use("vista")
    #     except TclError:
    #         Style().theme_use("default")

    #     font.nametofont("TkDefaultFont").configure(size=10)
    #     font.nametofont("TkTextFont").configure(size=10)

    #     self.fonts = {
    #         "h1": font.Font(size=24, weight="bold"),
    #         "h2-bold": font.Font(size=22, weight="bold"),
    #         "h2": font.Font(size=22),
    #         "h3-bold": font.Font(size=20, weight="bold"),
    #         "h3": font.Font(size=16),
    #         "h4": font.Font(size=14),
    #         "h5": font.Font(size=12),
    #         "logs": font.Font(size=10)
    #     }

    #     self.lock = threading.Lock()
    #     self.stop_event = threading.Event()
    #     self.thread = None
    #     self.stream = None
    #     self.selected_file = None
    #     self.ball_tracker = BallTracker()

    #     self.styles = [
    #         Style().configure("Left.TFrame", background="red"),
    #         Style().configure("Middle.TFrame", background="blue"),
    #         Style().configure("Right.TFrame", background="green"),
    #         Style().configure("NavBar.TFrame", background="light gray"),
    #         Style().configure("TButton", padding=6, cursor="hand2"),
    #         Style().configure("TMenubutton", padding=6, relief="raised"),
    #         Style().configure("TRadiobutton", relief="raised")
    #     ]

    #     threading.Thread(target=self.__setup_widgets).start()
    #     if args.splash:
    #         SplashScreen(self)

    # def __setup_widgets(self):
    #     self.left = Frame(master=self)
    #     self.middle = Frame(master=self)
    #     self.right = Frame(master=self)
    #     self.bottom = Frame(master=self)
    #     self.separator_vert_1 = Separator(master=self, orient="vertical")
    #     self.separator_vert_2 = Separator(master=self, orient="vertical")

    #     self.program_output = ProgramOutput(master=self.middle)
    #     self.ball_tracker_options = BallTrackerOptions(master=self.left, logger=self.program_output)
    #     self.colour_detection_options = ColourDetectionOptions(master=self.left, logger=self.program_output)
    #     self.video_player = VideoPlayer(master=self.right, logger=self.program_output)

    #     self.nav_bar = Navbar(master=self.bottom)
    #     self.nav_bar.pack(side="bottom", fill="x", anchor="s")

    #     self.bottom.pack(side="bottom", fill="x", anchor="s")

    #     self.__setup_left_column()
    #     self.__setup_middle_column()
    #     self.__setup_right_column()
    #     self.__setup_window()

    # def __setup_window(self):
    #     self.left.pack(side="left", fill="both", expand=True,
    #                    anchor="w", ipadx=10, ipady=10)
    #     self.separator_vert_1.pack(side="left", fill="both")
    #     self.middle.pack(side="left", fill="both",
    #                      expand=True, anchor="center", ipady=20)
    #     self.separator_vert_2.pack(side="left", fill="both")
    #     self.right.pack(side="left", fill="both", expand=True,
    #                     anchor="e", ipadx=10, ipady=10)

    # def __setup_left_column(self):
    #     self.ball_tracker_options.pack(
    #         side="top", fill="both", expand=True, padx=(20, 0), pady=(20, 10))
    #     self.ball_tracker_options.grid_children()
    #     self.colour_detection_options.pack(
    #         side="top", fill="both", expand=True, padx=(20, 0), pady=(0, 20))
    #     self.colour_detection_options.grid_children()

    # def __setup_middle_column(self):
    #     self.program_output.pack(
    #         side="top", fill="both", expand=True, padx=20, pady=(20, 10))
    #     self.program_output.grid_children()

    # def __setup_right_column(self):
    #     self.video_player.pack(side="top", fill="both",
    #                            expand=True, padx=(0, 20), pady=(20, 10))
    #     self.video_player.grid_children()

    # def on_close(self):
    #     if self.stream is not None:
    #         self.stream.stop()
    #     self.quit()

    # def select_file_onclick(self):
    #     self.selected_file = filedialog.askopenfilename(title="Select Video File",
    #         initialdir="resources/videos")

    #     if not self.selected_file:
    #         return

    #     if self.thread is not None:
    #         self.thread.stop_event.set()

    #     try:
    #         self.stream = cv2.VideoCapture(self.selected_file)
    #         if not self.stream.isOpened():
    #             self.program_output.error(
    #                 'Invalid file, please select a video file!')
    #             return
    #     except TypeError:
    #         self.program_output.error(
    #             'Invalid file, please select a video file!')
    #         return

    #     self.video_player.load_video_player()
    #     self.video_player.reset_video_options()
    #     self.video_player.btns['toggle'].configure(text="Play")
    #     self.start_video_processor()

    # def start_video_processor(self):
    #     self.program_output.info("Starting video processor...")
    #     self.stream = VideoFileStream(self.selected_file, queue_size=1)

    #     self.stop_event = threading.Event()
    #     self.thread = VideoProcessor(master=self, stream=self.stream,
    #                                  video_file=self.selected_file, ball_tracker=self.ball_tracker,
    #                                  lock=self.lock, stop_event=self.stop_event)
    #     self.thread.start()

    # def restart_video_processor(self):
    #     if self.thread is not None:
    #         self.thread.stop_event.set()

    #     self.start_video_processor()

    # def load_settings(self):
    #     settings_file = filedialog.askopenfilename(title="Load Settings",
    #         filetypes=[("Json Files", ".json")], initialdir="resources/config")

    #     if not settings_file:
    #         return

    #     self.settings_file = settings_file
    #     threading.Thread(target=self.__load_settings, args=(settings_file,), daemon=True).start()

    # def __load_settings(self, settings_file):
    #     success, error = s.load(settings_file)
    #     if success:
    #         self.colour_detection_options.update()
    #         self.ball_tracker_options.update()
    #         self.program_output.info(f"Loaded \"{os.path.basename(settings_file)}\"")
    #     else:
    #         self.program_output.error(f"Failed to load \"{os.path.basename(settings_file)}\"\n{str(error)}")

    # def save_settings(self):
    #     data = [("Json Files", ".json")]
    #     name, ext = os.path.splitext(os.path.basename(self.settings_file))
    #     settings_file = filedialog.asksaveasfilename(title="Save Settings", initialfile=f"{name} copy{ext}",
    #         filetypes=data, defaultextension=data, initialdir="resources/config")

    #     if not settings_file:
    #         return

    #     self.settings_file = settings_file
    #     threading.Thread(target=self.__save_settings, args=(settings_file,), daemon=True).start()

    # def __save_settings(self, settings_file):
    #     success, error = s.save(settings_file)
    #     if success:
    #         self.colour_detection_options.update()
    #         self.ball_tracker_options.update()
    #         self.program_output.info(f"Saved \"{os.path.basename(settings_file)}\"")
    #     else:
    #         self.program_output.error(f"Failed to save \"{os.path.basename(settings_file)}\"\n{str(error)}")
