import tkinter as tk
import tkinter.ttk as ttk
from collections import OrderedDict
import time
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import BallTracker
from snooker_ball_tracker.ball_tracker import SnapShot
from copy import copy, deepcopy

class ProgramOutput(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.separator_hori = ttk.Separator(master=self, orient="horizontal")
        self.separator_hori_1 = ttk.Separator(master=self, orient="horizontal")
        self.separator_hori_2 = ttk.Separator(master=self, orient="horizontal")
        self.separator_hori_3 = ttk.Separator(master=self, orient="horizontal")
        self.separator_hori_4 = ttk.Separator(master=self, orient="horizontal")
        self.separator_vert = ttk.Separator(master=self, orient="vertical")
        self.current_ball_count_label = tk.Label(self, text='Ball count', font=self.master.master.fonts["h3"])
        self.current_ball_count = tk.Label(self, text=SnapShot().get_snapshot_info(), font=self.master.master.fonts["h5"])
        self.last_ball_count_label = tk.Label(self, text='Last ball count', font=self.master.master.fonts["h3"])
        self.last_ball_count = tk.Label(self, text=SnapShot().get_snapshot_info(), font=self.master.master.fonts["h5"])

        self.balls_potted_label = tk.Label(master=self, text='Balls potted', font=self.master.master.fonts["h3"])
        self.balls_potted_frame = tk.Frame(master=self)
        self.balls_potted_scrollbar = tk.Scrollbar(self.balls_potted_frame, orient="vertical")
        self.balls_potted_list = tk.Listbox(self.balls_potted_frame, font=self.master.master.fonts["h4"], 
                                            width=13, height=7, yscrollcommand=self.balls_potted_scrollbar.set)
        self.balls_potted_scrollbar.config(command=self.balls_potted_list.yview)

        self.white_ball_status_label = tk.Label(self, text='White status', font=self.master.master.fonts["h3"])
        self.white_ball_status = tk.Label(self, text=BallTracker().get_white_ball_status() ,font=self.master.master.fonts["h4"])

        self.output_log_label = tk.Label(master=self, text="Program logs", font=self.master.master.fonts["h3"])
        self.output_log_frame = tk.Frame(master=self)
        self.output_log_scrollbar = tk.Scrollbar(master=self.output_log_frame, orient="vertical")
        self.output_log = tk.Text(master=self.output_log_frame, font=self.master.master.fonts["h5"], height=10, wrap="word", width=40, yscrollcommand=self.output_log_scrollbar.set)
        self.output_log_scrollbar.config(command=self.output_log.yview)

        self.output_log_label.grid(column=0, row=0, columnspan=4, sticky="ew")
        self.separator_hori.grid(column=0, row=1, columnspan=4, sticky="ew", pady=(10, 0))
        self.output_log_frame.grid(column=0, row=2, columnspan=4, sticky="ewns", pady=20)
        self.output_log.pack(side="left", fill="y")
        self.output_log_scrollbar.pack(side="left", fill="y")

        self.last_ball_count_label.grid(column=0, row=4, columnspan=2, sticky="ew")
        self.current_ball_count_label.grid(column=3, row=4, sticky="ew")
        self.separator_hori_1.grid(column=0, row=3, columnspan=4, sticky="ew", pady=(0, 10))
        self.separator_hori_2.grid(column=0, row=5, columnspan=4, sticky="ew", pady=(10, 0))
        self.separator_vert.grid(column=2, row=3, rowspan=8, sticky="ns", padx=10, pady=(0, 10))
        self.last_ball_count.grid(column=0, row=6, columnspan=2, sticky="ewns", pady=10)
        self.current_ball_count.grid(column=3, row=6, sticky="ewns", pady=10)

        self.balls_potted_label.grid(column=0, row=8, columnspan=2, sticky="ew")
        self.white_ball_status_label.grid(column=3, row=8, sticky="ew")
        self.separator_hori_3.grid(column=0, row=7, columnspan=4, sticky="ew", pady=(0, 10))
        self.separator_hori_4.grid(column=0, row=9, columnspan=4, sticky="ew", pady=(10, 0))
        self.balls_potted_frame.grid(column=0, row=10, columnspan=2, sticky="ew", pady=20)
        self.balls_potted_list.pack(side="left", fill="y")
        self.balls_potted_scrollbar.pack(side="left", fill="y")
        self.white_ball_status.grid(column=3, row=10, sticky="n", padx=(10, 0), pady=20)

    def info(self, value):
        self.output_log.insert(tk.END, "[Info] {}\n".format(value))
        self.output_log.see(tk.END)

    def error(self, value):
        self.output_log.insert(tk.END, "[Error] {}\n".format(value))
        self.output_log.see(tk.END)
