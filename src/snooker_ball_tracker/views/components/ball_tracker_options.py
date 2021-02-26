import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from collections import OrderedDict
import time
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import BallTracker
from copy import copy, deepcopy


class BallTrackerOptions(Frame):
    def __init__(self, master=None, logger=None):
        super().__init__(master)
        self.logger = logger
        self.ball_detection_settings = {
            'filter_by_convexity': BooleanVar(value=s.FILTER_BY_CONVEXITY),
            'min_convexity': DoubleVar(value=s.MIN_CONVEXITY),
            'max_convexity': DoubleVar(value=s.MAX_CONVEXITY),
            'filter_by_circularity': BooleanVar(value=s.FILTER_BY_CIRCULARITY),
            'min_circularity': DoubleVar(value=s.MIN_CIRCULARITY),
            'max_circularity': DoubleVar(value=s.MAX_CIRCULARITY),
            'filter_by_inertia': BooleanVar(value=s.FILTER_BY_INERTIA),
            'min_inertia_ratio': DoubleVar(value=s.MIN_INERTIA_RATIO),
            'max_inertia_ratio': DoubleVar(value=s.MAX_INERTIA_RATIO),
            'filter_by_area': BooleanVar(value=s.FILTER_BY_AREA),
            'min_area': DoubleVar(value=s.MIN_AREA),
            'max_area': DoubleVar(value=s.MAX_AREA),
            'min_dist_between_blobs': DoubleVar(value=s.MIN_DIST_BETWEEN_BLOBS),
            'min_threshold': IntVar(value=s.MIN_THRESHOLD),
            'max_threshold': IntVar(value=s.MAX_THRESHOLD)
        }

        self.convexity_frame = Frame(master=self)
        self.circularity_frame = Frame(master=self)
        self.inertia_frame = Frame(master=self)
        self.area_frame = Frame(master=self)
        self.threshold_frame = Frame(master=self)
        self.dist_frame = Frame(master=self)

        self.separator_hori = Separator(master=self, orient="horizontal")
        self.separator_hori_1 = Separator(master=self, orient="horizontal")
        self.separator_hori_2 = Separator(master=self, orient="horizontal")
        self.separator_hori_3 = Separator(master=self, orient="horizontal")
        self.separator_vert = Separator(master=self, orient="vertical")

        self.ball_tracker_options = Label(
            master=self, text="Ball Tracker Options", font=self.master.master.fonts["h3-bold"])
        self.ball_tracker_reset = Button(
            master=self, text="Reset", command=self._reset_tracker_options, cursor="hand2")

        self.convexity_widgets = OrderedDict([
            ('radio_label', Label(self.convexity_frame,
                                  text="Filter by Convexity", anchor="w")),
            ('radio_true', Radiobutton(self.convexity_frame, text="Yes", value=True, command=self._update_ball_tracker,
                                       variable=self.ball_detection_settings['filter_by_convexity'], cursor="hand2")),
            ('radio_false', Radiobutton(self.convexity_frame, text="No", value=False, command=self._update_ball_tracker,
                                        variable=self.ball_detection_settings['filter_by_convexity'], cursor="hand2")),
            ('min_label', Label(self.convexity_frame,
                                text="Minimum Convexity", anchor="w")),
            ('min', tk.Scale(self.convexity_frame, from_=0, to=1, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['min_convexity'], cursor="hand2")),
            ('max_label', Label(self.convexity_frame,
                                text="Maximum Convexity", anchor="w")),
            ('max', tk.Scale(self.convexity_frame, from_=0, to=1, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['max_convexity'], cursor="hand2"))
        ])

        self.circularity_widgets = OrderedDict([
            ('radio_label', Label(self.circularity_frame,
                                  text="Filter by Circularity", anchor="w")),
            ('radio_true', Radiobutton(self.circularity_frame, text="Yes", value=True, command=self._update_ball_tracker,
                                       variable=self.ball_detection_settings['filter_by_circularity'], cursor="hand2")),
            ('radio_false', Radiobutton(self.circularity_frame, text="No", value=False, command=self._update_ball_tracker,
                                        variable=self.ball_detection_settings['filter_by_circularity'], cursor="hand2")),
            ('min_label', Label(self.circularity_frame,
                                text="Minimum Circularity", anchor="w")),
            ('min', tk.Scale(self.circularity_frame, from_=0, to=1, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['min_circularity'], cursor="hand2")),
            ('max_label', Label(self.circularity_frame,
                                text="Maximum Circularity", anchor="w")),
            ('max', tk.Scale(self.circularity_frame, from_=0, to=1, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['max_circularity'], cursor="hand2"))
        ])

        self.inertia_widgets = OrderedDict([
            ('radio_label', Label(self.inertia_frame,
                                  text="Filter by Inertia", anchor="w")),
            ('radio_true',
             Radiobutton(self.inertia_frame, text="Yes", value=True, command=self._update_ball_tracker,
                         variable=self.ball_detection_settings['filter_by_inertia'], cursor="hand2")),
            ('radio_false',
             Radiobutton(self.inertia_frame, text="No", value=False, command=self._update_ball_tracker,
                         variable=self.ball_detection_settings['filter_by_inertia'], cursor="hand2")),
            ('min_label', Label(self.inertia_frame,
                                text="Minimum Inertia", anchor="w")),
            ('min', tk.Scale(self.inertia_frame, from_=0, to=1, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['min_inertia_ratio'], cursor="hand2")),
            ('max_label', Label(self.inertia_frame,
                                text="Maximum Inertia", anchor="w")),
            ('max', tk.Scale(self.inertia_frame, from_=0, to=1, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['max_inertia_ratio'], cursor="hand2"))
        ])

        self.area_widgets = OrderedDict([
            ('radio_label', Label(self.area_frame, text="Filter by Area", anchor="w")),
            ('radio_true',
             Radiobutton(self.area_frame, text="Yes", variable=self.ball_detection_settings['filter_by_area'],
                         value=True, command=self._update_ball_tracker, cursor="hand2")),
            ('radio_false',
             Radiobutton(self.area_frame, text="No", variable=self.ball_detection_settings['filter_by_area'],
                         value=False, command=self._update_ball_tracker, cursor="hand2")),
            ('min_label', Label(self.area_frame, text="Minimum Area", anchor="w")),
            ('min', tk.Scale(self.area_frame, from_=1, to=2000, orient=HORIZONTAL, length=400, resolution=-1,
                             variable=self.ball_detection_settings['min_area'], cursor="hand2")),
            ('max_label', Label(self.area_frame, text="Maximum Area", anchor="w")),
            ('max', tk.Scale(self.area_frame, from_=1, to=2000, orient=HORIZONTAL, length=400, resolution=-1,
                             variable=self.ball_detection_settings['max_area'], cursor="hand2"))
        ])

        self.threshold_widgets = OrderedDict([
            ('min_label', Label(self.threshold_frame,
                                text="Minimum Threshold", anchor="w", width=20)),
            ('min', tk.Scale(self.threshold_frame, from_=0, to=255, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['min_threshold'], cursor="hand2")),
            ('max_label', Label(self.threshold_frame,
                                text="Maximum Threshold", anchor="w", width=20)),
            ('max', tk.Scale(self.threshold_frame, from_=0, to=255, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['max_threshold'], cursor="hand2"))
        ])

        self.dist_widgets = OrderedDict([
            ('min_label', Label(self.dist_frame, text="Minimum distance between balls", anchor="w",
                                wraplength=150)),
            ('min', tk.Scale(self.dist_frame, from_=0, to=100, orient=HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['min_dist_between_blobs'], cursor="hand2")),
        ])

        self.convexity_widgets['min'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.convexity_widgets['max'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.circularity_widgets['min'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.circularity_widgets['max'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.inertia_widgets['min'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.inertia_widgets['max'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.area_widgets['min'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.area_widgets['max'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.threshold_widgets['min'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.threshold_widgets['max'].bind("<ButtonRelease-1>", self._update_ball_tracker)
        self.dist_widgets['min'].bind("<ButtonRelease-1>", self._update_ball_tracker)

    def grid_children(self):
        self.convexity_widgets['radio_label'].grid(column=0, row=0, sticky="w", padx=(0, 20), pady=(0, 10))
        self.convexity_widgets['radio_true'].grid(column=1, row=0, padx=(0, 10), pady=(0, 10))
        self.convexity_widgets['radio_false'].grid(column=2, row=0, padx=(0, 10), pady=(0, 10))
        self.convexity_widgets['min_label'].grid(column=0, row=1, sticky="w", padx=(0, 20), pady=(0, 10))
        self.convexity_widgets['min'].grid(column=1, row=1, columnspan=2, pady=(0, 10))
        self.convexity_widgets['max_label'].grid(column=0, row=2, sticky="w", padx=(0, 20), pady=(0, 10))
        self.convexity_widgets['max'].grid(column=1, row=2, columnspan=2, pady=(0, 10))

        self.circularity_widgets['radio_label'].grid(column=0, row=0, sticky="w", padx=(0, 20), pady=(0, 10))
        self.circularity_widgets['radio_true'].grid(column=1, row=0, padx=(0, 10), pady=(0, 10))
        self.circularity_widgets['radio_false'].grid(column=2, row=0, padx=(0, 10), pady=(0, 10))
        self.circularity_widgets['min_label'].grid(column=0, row=1, sticky="w", padx=(0, 20), pady=(0, 10))
        self.circularity_widgets['min'].grid(column=1, row=1, columnspan=2, pady=(0, 10))
        self.circularity_widgets['max_label'].grid(column=0, row=2, sticky="w", padx=(0, 20))
        self.circularity_widgets['max'].grid(column=1, row=2, columnspan=2, pady=(0, 10))

        self.inertia_widgets['radio_label'].grid(column=0, row=0, sticky="w", padx=(0, 20), pady=(0, 10))
        self.inertia_widgets['radio_true'].grid(column=1, row=0, padx=(0, 10), pady=(0, 10))
        self.inertia_widgets['radio_false'].grid(column=2, row=0, padx=(0, 10), pady=(0, 10))
        self.inertia_widgets['min_label'].grid(column=0, row=1, sticky="w", padx=(0, 20), pady=(0, 10))
        self.inertia_widgets['min'].grid(column=1, row=1, columnspan=2, pady=(0, 10))
        self.inertia_widgets['max_label'].grid(column=0, row=2, sticky="w", padx=(0, 20), pady=(0, 10))
        self.inertia_widgets['max'].grid(column=1, row=2, columnspan=2, pady=(0, 10))

        self.area_widgets['radio_label'].grid(column=0, row=0, sticky="w", padx=(0, 20), pady=(0, 10))
        self.area_widgets['radio_true'].grid(column=1, row=0, padx=(0, 10), pady=(0, 10))
        self.area_widgets['radio_false'].grid(column=2, row=0, padx=(0, 10), pady=(0, 10))
        self.area_widgets['min_label'].grid(column=0, row=1, sticky="w", padx=(0, 20), pady=(0, 10))
        self.area_widgets['min'].grid(column=1, row=1, columnspan=10, pady=(0, 10))
        self.area_widgets['max_label'].grid(column=0, row=2, sticky="w", padx=(0, 20), pady=(0, 10))
        self.area_widgets['max'].grid(column=1, row=2, columnspan=10, pady=(0, 10))

        self.dist_widgets['min_label'].grid(column=0, row=0, padx=(0, 20), pady=(0, 10))
        self.dist_widgets['min'].grid(column=1, row=0)

        self.ball_tracker_options.grid(column=0, row=0, sticky="w")
        self.separator_hori_1.grid(column=0, row=1, columnspan=6, sticky="ew", pady=(10, 10))
        self.ball_tracker_reset.grid(column=0, row=2, sticky="w")
        self.separator_hori.grid(column=0, row=3, columnspan=6, sticky="ew", pady=(10, 20))
        self.separator_vert.grid(column=1, row=3, rowspan=3, sticky="ns", pady=(10, 0))
        self.convexity_frame.grid(column=0, row=4, sticky="ew", padx=(0, 10))
        self.inertia_frame.grid(column=2, row=4, sticky="ew", padx=(10, 0))
        self.circularity_frame.grid(column=0, row=5, sticky="ew", padx=(0, 10), pady=(20, 20))
        # self.threshold_frame.grid(column=0, row=6, sticky="ew", pady=(20, 0))
        self.dist_frame.grid(column=2, row=5, sticky="ew", padx=(10, 0), pady=(20, 0))
        self.separator_hori_2.grid(column=0, row=6, columnspan=6, sticky="ew", pady=(0, 20))
        self.area_frame.grid(column=0, row=7, columnspan=6, sticky="ew", pady=(0, 0))
        self.separator_hori_3.grid(column=0, row=8, columnspan=6, sticky="ew", pady=(20, 0))

    def update(self):
        for key in self.ball_detection_settings:
            self.ball_detection_settings[key].set(s.__getattr__(key.upper()))
        
        self._update_ball_tracker()

    def _update_ball_tracker(self, event=None):
        if self.master.master.thread is not None:
            ball_detection_settings = {
                'filter_by_convexity': self.ball_detection_settings['filter_by_convexity'].get(),
                'min_convexity': self.ball_detection_settings['min_convexity'].get(),
                'max_convexity': self.ball_detection_settings['max_convexity'].get(),
                'filter_by_circularity': self.ball_detection_settings['filter_by_circularity'].get(),
                'min_circularity': self.ball_detection_settings['min_circularity'].get(),
                'max_circularity': self.ball_detection_settings['max_circularity'].get(),
                'filter_by_inertia': self.ball_detection_settings['filter_by_inertia'].get(),
                'min_inertia_ratio': self.ball_detection_settings['min_inertia_ratio'].get(),
                'max_inertia_ratio': self.ball_detection_settings['max_inertia_ratio'].get(),
                'filter_by_area': self.ball_detection_settings['filter_by_area'].get(),
                'min_area': self.ball_detection_settings['min_area'].get(),
                'max_area': self.ball_detection_settings['max_area'].get(),
                'min_dist_between_blobs': self.ball_detection_settings['min_dist_between_blobs'].get(),
                'min_threshold': self.ball_detection_settings['min_threshold'].get(),
                'max_threshold': self.ball_detection_settings['max_threshold'].get()
            }
            self.master.master.thread.ball_tracker.setup_blob_detector(**ball_detection_settings)


    def _reset_tracker_options(self):
        self.update()
        self._update_ball_tracker()
        self.logger.info("Ball tracker options reset")
