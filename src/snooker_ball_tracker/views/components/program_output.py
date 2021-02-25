from tkinter import *
from tkinter.ttk import *
from collections import OrderedDict
import time
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import BallTracker
from snooker_ball_tracker.ball_tracker import SnapShot
from copy import copy, deepcopy
from tkinter import font


class ProgramOutput(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.separator_hori = Separator(master=self, orient="horizontal")
        self.separator_hori_1 = Separator(master=self, orient="horizontal")
        self.separator_hori_2 = Separator(master=self, orient="horizontal")
        self.separator_hori_3 = Separator(master=self, orient="horizontal")
        self.separator_hori_4 = Separator(master=self, orient="horizontal")
        self.separator_vert = Separator(master=self, orient="vertical")
        self.current_ball_count_label = Label(
            master=self, text='Current ball count', font=self.master.master.fonts["h4"])
        self.current_ball_count = Label(master=self, text=SnapShot(
        ).get_snapshot_info(), font=self.master.master.fonts["h5"])
        self.last_ball_count_label = Label(
            master=self, text='Last ball count', font=self.master.master.fonts["h4"])
        self.last_ball_count = Label(master=self, text=SnapShot(
        ).get_snapshot_info(), font=self.master.master.fonts["h5"])

        self.balls_potted_label = Label(
            master=self, text='Balls potted', font=self.master.master.fonts["h4"])
        self.balls_potted_frame = Frame(master=self)
        self.balls_potted_scrollbar = Scrollbar(
            self.balls_potted_frame, orient="vertical")
        self.balls_potted_list = Listbox(master=self.balls_potted_frame, font=self.master.master.fonts["logs"],
                                         width=25, height=7, yscrollcommand=self.balls_potted_scrollbar.set)
        self.balls_potted_scrollbar.config(
            command=self.balls_potted_list.yview)
        self.balls_potted_clear_btn = Button(
            master=self, text="Clear List", command=self.clear_balls_potted_list, cursor="hand2")

        self.white_ball_status_label = Label(
            master=self, text='White status', font=self.master.master.fonts["h4"])
        self.white_ball_status = Label(master=self, text=BallTracker(
        ).get_white_ball_status(), font=self.master.master.fonts["h4"])

        self.output_log_label = Label(
            master=self, text="Program Output", font=self.master.master.fonts["h3-bold"])
        self.output_log_frame = Frame(master=self)
        self.output_log_scrollbar = Scrollbar(
            master=self.output_log_frame, orient="vertical")
        self.output_log = Text(master=self.output_log_frame, font=self.master.master.fonts[
                               "logs"], height=10, width=50, wrap="word", yscrollcommand=self.output_log_scrollbar.set)
        self.output_log.configure(state="disabled")
        self.output_log.tag_config(
            "info-loglevel", foreground="blue", underline=1, font=font.Font(size=10, weight="bold"))
        self.output_log.tag_config(
            "error-loglevel", foreground="red", underline=1, font=font.Font(size=10, weight="bold"))
        self.output_log_scrollbar.config(command=self.output_log.yview)

    def grid_children(self):
        self.output_log_label.grid(column=0, row=0, columnspan=3, sticky="ew")
        self.separator_hori.grid(
            column=0, row=1, columnspan=3, sticky="ew", pady=(10, 0))
        self.output_log_frame.grid(
            column=0, row=2, columnspan=3, sticky="ew", pady=20)
        self.output_log.pack(side="left", fill="y")
        self.output_log_scrollbar.pack(side="left", fill="y")

        self.last_ball_count_label.grid(column=0, row=4, sticky="ew")
        self.current_ball_count_label.grid(column=2, row=4, sticky="ew")
        self.separator_hori_1.grid(
            column=0, row=3, columnspan=3, sticky="nsew", pady=(0, 10))
        self.separator_hori_2.grid(
            column=0, row=5, columnspan=3, sticky="nsew", pady=(10, 0))
        self.separator_vert.grid(
            column=1, row=3, rowspan=9, sticky="ns", padx=10)
        self.last_ball_count.grid(column=0, row=6, pady=10, sticky="w")
        self.current_ball_count.grid(column=2, row=6, pady=10, sticky="w")

        self.balls_potted_label.grid(column=2, row=8, sticky="ew")
        self.white_ball_status_label.grid(column=0, row=8, sticky="ew")
        self.separator_hori_3.grid(
            column=0, row=7, columnspan=3, sticky="ew", pady=(0, 10))
        self.separator_hori_4.grid(
            column=0, row=9, columnspan=3, sticky="ew", pady=(10, 0))
        self.balls_potted_frame.grid(column=2, row=10, sticky="nsew", pady=20)
        self.balls_potted_list.pack(side="left", fill="y")
        self.balls_potted_scrollbar.pack(side="left", fill="y")
        self.balls_potted_clear_btn.grid(column=2, row=11, sticky="nsw")
        self.white_ball_status.grid(column=0, row=10, sticky="nw", pady=20)

    def info(self, value):
        self.output_log.configure(state="normal")
        self.output_log.insert(END, "[INFO]", "info-loglevel")
        self.output_log.insert(END, " {}\n".format(value))
        self.output_log.see(END)
        self.output_log.configure(state="disabled")

    def error(self, value):
        self.output_log.configure(state="normal")
        self.output_log.insert(END, "[ERROR]", "error-loglevel")
        self.output_log.insert(END, " {}\n".format(value))
        self.output_log.see(END)
        self.output_log.configure(state="disabled")

    def clear_balls_potted_list(self):
        self.balls_potted_list.delete(0, END)
