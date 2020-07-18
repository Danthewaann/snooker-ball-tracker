# import tkinter as tk
# import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
from collections import OrderedDict
import time
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import BallTracker
from copy import copy, deepcopy

class ColourDetectionOptions(Frame):
    def __init__(self, master=None, logger=None):
        super().__init__(master)
        self.logger = logger
        self.orig_colour_settings = deepcopy(s.COLOURS)

        self.colour_detection_settings = {
            "select-colour": StringVar(self, "RED"),
            "select-colours": list(s.COLOURS.keys()),
            "colour": {
                'lower_h': IntVar(value=s.COLOURS["RED"]['LOWER'][0]),
                'lower_s': IntVar(value=s.COLOURS["RED"]['LOWER'][1]),
                'lower_v': IntVar(value=s.COLOURS["RED"]['LOWER'][2]),
                'upper_h': IntVar(value=s.COLOURS["RED"]['UPPER'][0]),
                'upper_s': IntVar(value=s.COLOURS["RED"]['UPPER'][1]),
                'upper_v': IntVar(value=s.COLOURS["RED"]['UPPER'][2])
            }
        }

        self.colour_detection_label = Label(master=self, text="Colour Detection Options", font=self.master.master.fonts["h3-bold"])
        self.separator_hori_2 = Separator(master=self, orient="horizontal")
        self.separator_hori_3 = Separator(master=self, orient="horizontal")
        self.colour_detection = Frame(master=self)
        self.reset_colour_btn = Button(master=self, text="Reset", command=self._reset_colour, cursor="hand2")
        self.select_colour_label = Label(master=self, text="Select Colour")
        self.select_colour_options = OptionMenu(self, self.colour_detection_settings["select-colour"], "RED", *self.colour_detection_settings["select-colours"], command=self._select_colour)
        self.select_colour_options.configure(cursor="hand2", width=10)
        self.colour_detection_widgets = {
            'lower_label': Label(self.colour_detection, text="Lower", anchor="w"),
            'lower_h_label': Label(self.colour_detection, text="H", anchor="w"),
            'lower_h': Scale(self.colour_detection, from_=0, to=255, orient=HORIZONTAL,
                                       variable=self.colour_detection_settings["colour"]['lower_h'], cursor="hand2"),
            'lower_s_label': Label(self.colour_detection, text="S", anchor="w"),
            'lower_s': Scale(self.colour_detection, from_=0, to=255, orient=HORIZONTAL,
                                       variable=self.colour_detection_settings["colour"]['lower_s'], cursor="hand2"),
            'lower_v_label': Label(self.colour_detection, text="V", anchor="w"),
            'lower_v': Scale(self.colour_detection, from_=0, to=255, orient=HORIZONTAL,
                                       variable=self.colour_detection_settings["colour"]['lower_v'], cursor="hand2"),

            'upper_label': Label(self.colour_detection, text="Upper", anchor="w"),
            'upper_h_label': Label(self.colour_detection, text="H", anchor="w"),
            'upper_h': Scale(self.colour_detection, from_=0, to=255, orient=HORIZONTAL,
                                       variable=self.colour_detection_settings["colour"]['upper_h'], cursor="hand2"),
            'upper_s_label': Label(self.colour_detection, text="S", anchor="w"),
            'upper_s': Scale(self.colour_detection, from_=0, to=255, orient=HORIZONTAL,
                                       variable=self.colour_detection_settings["colour"]['upper_s'], cursor="hand2"),
            'upper_v_label': Label(self.colour_detection, text="V", anchor="w"),
            'upper_v': Scale(self.colour_detection, from_=0, to=255, orient=HORIZONTAL,
                                       variable=self.colour_detection_settings["colour"]['upper_v'], cursor="hand2")
        }

        self.colour_detection_widgets['lower_h'].bind("<ButtonRelease-1>", self._update_colour)
        self.colour_detection_widgets['lower_s'].bind("<ButtonRelease-1>", self._update_colour)
        self.colour_detection_widgets['lower_v'].bind("<ButtonRelease-1>", self._update_colour)
        self.colour_detection_widgets['upper_h'].bind("<ButtonRelease-1>", self._update_colour)
        self.colour_detection_widgets['upper_s'].bind("<ButtonRelease-1>", self._update_colour)
        self.colour_detection_widgets['upper_v'].bind("<ButtonRelease-1>", self._update_colour)


    def grid_children(self):
        self.colour_detection_widgets['lower_label'].grid(column=0, row=0, sticky="ew", padx=(0, 20), pady=(0, 10))
        self.colour_detection_widgets['lower_h_label'].grid(column=1, row=0, sticky="ew", padx=(0, 5), pady=(0, 10))
        self.colour_detection_widgets['lower_h'].grid(column=2, row=0, padx=(0, 10), pady=(0, 10))
        self.colour_detection_widgets['lower_s_label'].grid(column=3, row=0, padx=(0, 5), pady=(0, 10))
        self.colour_detection_widgets['lower_s'].grid(column=4, row=0, padx=(0, 10), pady=(0, 10))
        self.colour_detection_widgets['lower_v_label'].grid(column=5, row=0, padx=(0, 5), pady=(0, 10))
        self.colour_detection_widgets['lower_v'].grid(column=6, row=0, padx=(0, 5), pady=(0, 10))
        self.colour_detection_widgets['upper_label'].grid(column=0, row=1, sticky="ew", padx=(0, 20), pady=(0, 10))
        self.colour_detection_widgets['upper_h_label'].grid(column=1, row=1, padx=(0, 5), pady=(0, 10))
        self.colour_detection_widgets['upper_h'].grid(column=2, row=1, padx=(0, 10), pady=(0, 10))
        self.colour_detection_widgets['upper_s_label'].grid(column=3, row=1, padx=(0, 5), pady=(0, 10))
        self.colour_detection_widgets['upper_s'].grid(column=4, row=1, padx=(0, 10), pady=(0, 10))
        self.colour_detection_widgets['upper_v_label'].grid(column=5, row=1, padx=(0, 5), pady=(0, 10))
        self.colour_detection_widgets['upper_v'].grid(column=6, row=1, padx=(0, 10), pady=(0, 10))

        self.colour_detection_label.grid(column=0, row=7, columnspan=3, sticky="w")
        self.separator_hori_2.grid(column=0, row=8, columnspan=4, sticky="ew", pady=(10, 10))
        self.select_colour_label.grid(column=0, row=9, sticky="w")
        self.select_colour_options.grid(column=1, row=9, sticky="w")
        self.reset_colour_btn.grid(column=2, row=9, sticky="w")
        self.separator_hori_3.grid(column=0, row=10, columnspan=4, sticky="ew", pady=(10, 10))
        self.colour_detection.grid(column=0, row=11, columnspan=4, sticky="w", pady=(10, 0))

    def _select_colour(self, colour):
        self.colour_detection_settings["colour"]["lower_h"].set(s.COLOURS[colour]["LOWER"][0])
        self.colour_detection_settings["colour"]["lower_s"].set(s.COLOURS[colour]["LOWER"][1])
        self.colour_detection_settings["colour"]["lower_v"].set(s.COLOURS[colour]["LOWER"][2])
        self.colour_detection_settings["colour"]["upper_h"].set(s.COLOURS[colour]["UPPER"][0])
        self.colour_detection_settings["colour"]["upper_s"].set(s.COLOURS[colour]["UPPER"][1])
        self.colour_detection_settings["colour"]["upper_v"].set(s.COLOURS[colour]["UPPER"][2])
        self.logger.info(f"Selected colour {colour}")

    
    def _update_colour(self, event=None):
        colour = self.colour_detection_settings["select-colour"].get()
        s.COLOURS[colour]['LOWER'][0] = self.colour_detection_settings['colour']['lower_h'].get()
        s.COLOURS[colour]['LOWER'][1] = self.colour_detection_settings['colour']['lower_s'].get()
        s.COLOURS[colour]['LOWER'][2] = self.colour_detection_settings['colour']['lower_v'].get()
        s.COLOURS[colour]['UPPER'][0] = self.colour_detection_settings['colour']['upper_h'].get()
        s.COLOURS[colour]['UPPER'][1] = self.colour_detection_settings['colour']['upper_s'].get()
        s.COLOURS[colour]['UPPER'][2] = self.colour_detection_settings['colour']['upper_v'].get()

    
    def _reset_colour(self):
        colour = self.colour_detection_settings["select-colour"].get()
        s.COLOURS[colour] = deepcopy(self.orig_colour_settings[colour])
        self.colour_detection_settings['colour']['lower_h'].set(s.COLOURS[colour]['LOWER'][0])
        self.colour_detection_settings['colour']['lower_s'].set(s.COLOURS[colour]['LOWER'][1])
        self.colour_detection_settings['colour']['lower_v'].set(s.COLOURS[colour]['LOWER'][2])
        self.colour_detection_settings['colour']['upper_h'].set(s.COLOURS[colour]['UPPER'][0])
        self.colour_detection_settings['colour']['upper_s'].set(s.COLOURS[colour]['UPPER'][1])
        self.colour_detection_settings['colour']['upper_v'].set(s.COLOURS[colour]['UPPER'][2])
        self.logger.info(f"{colour} HSV values reset")
