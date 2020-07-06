# import tkinter as tk
# import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
import cv2
import imutils
import numpy as np
import time
import threading
from snooker_ball_tracker.views.components.navbar import Navbar
from snooker_ball_tracker.views.components.main_view import MainView
from snooker_ball_tracker.ball_tracker import BallTracker
from snooker_ball_tracker.video_processor import VideoProcessor
import snooker_ball_tracker.settings as s
from collections import OrderedDict
from tkinter import font
from tkinter import filedialog
from PIL import Image, ImageTk


class Application(Tk):
    def __init__(self,):
        super().__init__()
        self.title("Snooker Ball Tracker - Demo Application")
        s.settings_module_name = "pre_recorded_footage"
        s.load()
        self.state('zoomed')
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.thread = None
        self.stream = None
        self.ball_tracker = None
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        font.nametofont("TkDefaultFont").configure(size=11, family="Helvetica")
        font.nametofont("TkTextFont").configure(size=11, family="Helvetica")

        self.fonts = {
            "h1": font.Font(size=24, family="Helvetica", weight="bold"),
            "h2-bold": font.Font(size=22, family="Helvetica", weight="bold"),
            "h2": font.Font(size=22, family="Helvetica"),
            "h3-bold": font.Font(size=18, family="Helvetica", weight="bold"),
            "h3": font.Font(size=18, family="Helvetica"),
            "h4": font.Font(size=14, family="Helvetica")
        }

        self.styles = {
            "DB.TFrame": Style().configure("DB.TFrame", background="light gray")
        }

        # menu = Menu(master=self)
        # self.config(menu=menu)
        # filemenu = Menu(master=menu)
        # menu.add_cascade(label="File", menu=filemenu)
        # filemenu.add_command(label="Open...", command=self.select_file_onclick)

        self.main_view = MainView(master=self)
        self.nav_bar = Navbar(master=self)
    
    def on_close(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        # if self.stream is not None:
        #     self.stream.release()
        self.quit()
        
    def select_file_onclick(self):
        selected_file = filedialog.askopenfilename()

        if selected_file == "":
            return

        if self.thread is not None:
            # if self.thread.stream is not None:
            #     self.thread.stream.release()
            self.thread.stop_event.set()

        self.stream = cv2.VideoCapture(selected_file)
        if not self.stream.isOpened():
            print('File is invalid')
            return

        self.main_view.enable_btns()
        self.main_view.file_output.destroy()
        self.main_view.btns_frame.pack_forget()
        self.main_view.file_output = Label(master=self.main_view.middle)
        self.main_view.file_output.pack(side="top", anchor="ne", padx=50, pady=(50, 0))
        self.main_view.btns_frame.pack(side="top", anchor="ne", padx=50, pady=20)
        self.main_view.btns['toggle'].configure(text="Play")
        self.ball_tracker = BallTracker()
        self.stop_event = threading.Event()
        self.thread = VideoProcessor(master=self, stream=self.stream, video_file=selected_file, ball_tracker=self.ball_tracker, lock=self.lock, stop_event=self.stop_event)
        self.thread.start()
