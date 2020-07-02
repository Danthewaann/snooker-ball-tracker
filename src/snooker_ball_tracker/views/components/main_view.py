import tkinter as tk
import tkinter.ttk as ttk
# from tkinter import *
# from tkinter.ttk import *
from collections import OrderedDict
import snooker_ball_tracker.settings as s

class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="gray")
        self.left = tk.Frame(master=self)
        self.middle = tk.Frame(master=self)
        self.right = tk.Frame(master=self)
        self.file_output = tk.Canvas(master=self.middle, width=800, height=400, bg="gray")

        self.data = {
            "threshold": tk.BooleanVar(self, False),
            "detect-colour": tk.StringVar(self, "None"),
            "detect-colours": ["None"] + (list(s.COLOURS.keys())) 
        }

        self.btns_frame = tk.Frame(master=self.middle)

        self.video_player_label = tk.Label(master=self.btns_frame, text="Video Player Options", font=("Helvetica", 18))
        self.separator1 = ttk.Separator(master=self.btns_frame, orient="horizontal")
        self.separator = ttk.Separator(master=self.btns_frame, orient="vertical")
        self.threshold_label = tk.Label(master=self.btns_frame, text="Enable Threshold", height=2)
        self.detect_colour_label = tk.Label(master=self.btns_frame, text="Detect Colour", height=2)
        self.detect_colour_options = tk.OptionMenu(self.btns_frame, self.data["detect-colour"], *self.data["detect-colours"], command=self._detect_colour)
        self.detect_colour_options.configure(state="disabled", cursor="hand2")

        self.btns = OrderedDict([
            ("toggle", tk.Button(
                self.btns_frame, text="Pause", command=self._toogle_output, height=1, width=10,
                font=self.master.fonts["h4"], state="disabled", cursor="hand2"
            )),
            ("restart", tk.Button(
                self.btns_frame, text="Restart", command=self._restart_output, height=1, width=10,
                font=self.master.fonts["h4"], state="disabled", cursor="hand2"
            )),
            ("update-bounds", tk.Button(
                self.btns_frame, text="Update Bounds", command=self._update_bounds, height=1, width=20,
                font=self.master.fonts["h4"], state="disabled", cursor="hand2"
            )),
            ("threshold-yes", tk.Radiobutton(
                self.btns_frame, text="Enable", height=1, command=self._update_threshold, 
                variable=self.data["threshold"], value=True, relief="raised", indicatoron=0, state="disabled", cursor="hand2"
            )),
            ("threshold-no", tk.Radiobutton(
                self.btns_frame, text="Disable", height=1, command=self._update_threshold, 
                variable=self.data["threshold"], value=False, relief="raised", indicatoron=0, state="disabled", cursor="hand2"
            )),
        ])

        self.video_player_label.grid(column=3, row=0, columnspan=3, sticky="e")
        self.separator1.grid(column=0, row=1, columnspan=6, sticky="ew", pady=(10, 0))

        self.btns["toggle"].grid(column=0, row=2, pady=(20, 0))
        self.btns["restart"].grid(column=1, row=2, pady=(20, 0))
        self.separator.grid(column=2, row=2, rowspan=3, sticky="ns", padx=(20, 20))
        self.threshold_label.grid(column=3, row=2, sticky="w", padx=(0, 10), pady=(20, 0))
        self.btns["threshold-yes"].grid(column=4, row=2, sticky="ensw", pady=(20, 0))
        self.btns["threshold-no"].grid(column=5, row=2, sticky="ensw", pady=(20, 0))

        self.btns["update-bounds"].grid(column=0, row=3, columnspan=2, sticky="ew")
        self.detect_colour_label.grid(column=3, row=3, sticky="w", padx=(0, 10))
        self.detect_colour_options.grid(column=4, row=3, columnspan=2, sticky="ew")

        self.left.pack(side="left", fill="both", expand=1, anchor="w")
        self.middle.pack(side="left", fill="both", expand=1, anchor="w")
        # self.right.pack(side="right", fill="both", expand=1, anchor="w")

        self.file_output.pack(side="top", anchor="ne", padx=50, pady=(50, 0))
        self.btns_frame.pack(side="top", anchor="ne", padx=50, pady=20)
        self.pack(side="top", fill="both", expand=1, anchor="n")

    def enable_btns(self):
        self.btns["toggle"].configure(state="normal")
        self.btns["restart"].configure(state="normal")
        self.btns["threshold-yes"].configure(state="normal")
        self.btns["threshold-no"].configure(state="normal")
        self.btns["update-bounds"].configure(state="normal")
        self.detect_colour_options.configure(state="normal")

    def _update_threshold(self):
        self.master.thread.show_threshold = self.data["threshold"].get()

    def _detect_colour(self, value):
        self.master.thread.detect_colour = value

    def _toogle_output(self):
        if self.master.thread.play_stream:
            self.master.thread.play_stream = False
            self.btns['toggle']['text'] = 'Play'
        else:
            self.master.thread.play_stream = True
            self.btns['toggle']['text'] = 'Pause'

    def _restart_output(self):
        self.master.thread.restart_stream()

    def _update_bounds(self):
        self.master.thread.update_bounds()
