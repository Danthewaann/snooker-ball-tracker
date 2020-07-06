import tkinter as tk
import tkinter.ttk as ttk
# from tkinter import *
# from tkinter.ttk import *
from collections import OrderedDict
import time
import snooker_ball_tracker.settings as s

class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="gray")
        self.left = tk.Frame(master=self, width=800, padx=20, pady=20)
        self.middle = tk.Frame(master=self)
        self.right = tk.Frame(master=self)
        self.file_output = tk.Canvas(master=self.middle, width=800, height=400, bg="gray")

        self.data = {
            "threshold": tk.BooleanVar(self, False),
            "detect-colour": tk.StringVar(self, "None"),
            "detect-colours": ["None"] + (list(s.COLOURS.keys())),
            "mask-colour": tk.BooleanVar(self, False),
            "crop-frames": tk.BooleanVar(self, False)
        }

        self.ball_detection_settings = {
            'filter_by_convexity': tk.BooleanVar(value=s.FILTER_BY_CONVEXITY),
            'min_convexity': tk.DoubleVar(value=s.MIN_CONVEXITY),
            'max_convexity': tk.DoubleVar(value=s.MAX_CONVEXITY),
            'filter_by_circularity': tk.BooleanVar(value=s.FILTER_BY_CIRCULARITY),
            'min_circularity': tk.DoubleVar(value=s.MIN_CIRCULARITY),
            'max_circularity': tk.DoubleVar(value=s.MAX_CIRCULARITY),
            'filter_by_inertia': tk.BooleanVar(value=s.FILTER_BY_INERTIA),
            'min_inertia': tk.DoubleVar(value=s.MIN_INERTIA_RATIO),
            'max_inertia': tk.DoubleVar(value=s.MAX_INERTIA_RATIO),
            'filter_by_area': tk.BooleanVar(value=s.FILTER_BY_AREA),
            'min_area': tk.DoubleVar(value=s.MIN_AREA),
            'max_area': tk.DoubleVar(value=s.MAX_AREA),
            'min_dist_between_blobs': tk.DoubleVar(value=s.MIN_DIST_BETWEEN_BLOBS),
            'min_threshold': tk.IntVar(value=s.MIN_THRESHOLD),
            'max_threshold': tk.IntVar(value=s.MAX_THRESHOLD)
        }

        self.btns_frame = tk.Frame(master=self.middle)

        self.video_player_label = tk.Label(master=self.btns_frame, text="Video Player Options", font=("Helvetica", 18))
        self.separator_hori = ttk.Separator(master=self.btns_frame, orient="horizontal")
        self.separator_vert = ttk.Separator(master=self.btns_frame, orient="vertical")
        self.threshold_label = tk.Label(master=self.btns_frame, text="Show Threshold", height=2)
        self.detect_colour_label = tk.Label(master=self.btns_frame, text="Detect Colour", height=2)
        self.detect_colour_options = tk.OptionMenu(self.btns_frame, self.data["detect-colour"], *self.data["detect-colours"], command=self._detect_colour)
        self.detect_colour_options.configure(state="disabled")
        self.mask_colour_label = tk.Label(master=self.btns_frame, text="Mask Colour", height=2)

        self.crop_frames = tk.Label(master=self.btns_frame, text="Crop Frames", height=2)

        self.btns = OrderedDict([
            ("toggle", tk.Button(
                self.btns_frame, text="Play", command=self._toogle_output, height=1, width=10,
                font=self.master.fonts["h4"], state="disabled"
            )),
            ("restart", tk.Button(
                self.btns_frame, text="Restart", command=self._restart_output, height=1, width=10,
                font=self.master.fonts["h4"], state="disabled"
            )),
            ("update-bounds", tk.Button(
                self.btns_frame, text="Detect Table", command=self._update_bounds, height=1, width=20,
                font=self.master.fonts["h4"], state="disabled"
            )),
            ("threshold-yes", tk.Radiobutton(
                self.btns_frame, text="Yes", height=1, command=self._update_threshold, 
                variable=self.data["threshold"], value=True, relief="raised", indicatoron=0, state="disabled"
            )),
            ("threshold-no", tk.Radiobutton(
                self.btns_frame, text="No", height=1, command=self._update_threshold, 
                variable=self.data["threshold"], value=False, relief="raised", indicatoron=0, state="disabled"
            )),
            ("mask-colour-yes", tk.Radiobutton(
                self.btns_frame, text="Yes", height=1, command=self._mask_colour, 
                variable=self.data["mask-colour"], value=True, relief="raised", indicatoron=0, state="disabled"
            )),
            ("mask-colour-no", tk.Radiobutton(
                self.btns_frame, text="No", height=1, command=self._mask_colour, 
                variable=self.data["mask-colour"], value=False, relief="raised", indicatoron=0, state="disabled"
            )),
            ("crop-frames-yes", tk.Radiobutton(
                self.btns_frame, text="Yes", height=1, command=self._crop_frames, 
                variable=self.data["crop-frames"], value=True, relief="raised", indicatoron=0, state="disabled"
            )),
            ("crop-frames-no", tk.Radiobutton(
                self.btns_frame, text="No", height=1, command=self._crop_frames, 
                variable=self.data["crop-frames"], value=False, relief="raised", indicatoron=0, state="disabled"
            )),
            ("reset-options", tk.Button(
                self.btns_frame, text="Reset", command=self._reset_video_options, height=1, width=10,
                font=self.master.fonts["h4"], state="disabled"
            )),
        ])

        self.video_player_label.grid(column=3, row=0, columnspan=3, sticky="e")
        self.separator_hori.grid(column=0, row=1, columnspan=7, sticky="ew", pady=(10, 0))

        self.btns["toggle"].grid(column=0, row=2, sticky="ensw", pady=(20, 0))
        self.btns["restart"].grid(column=1, row=2, columnspan=2, sticky="ensw", pady=(20, 0), padx=(0, 10))
        self.separator_vert.grid(column=3, row=2, rowspan=4, sticky="ns", padx=(20, 20))
        self.threshold_label.grid(column=4, row=2, sticky="w", padx=(0, 10), pady=(20, 0))
        self.btns["threshold-yes"].grid(column=5, row=2, sticky="ensw", pady=(20, 0))
        self.btns["threshold-no"].grid(column=6, row=2, sticky="ensw", pady=(20, 0))

        self.btns["update-bounds"].grid(column=0, row=3, columnspan=3, sticky="ensw", padx=(0, 10))
        self.crop_frames.grid(column=0, row=4, sticky="w", padx=(0, 10), pady=(20, 0))
        self.btns["crop-frames-yes"].grid(column=1, row=4, sticky="ensw", pady=(20, 0))
        self.btns["crop-frames-no"].grid(column=2, row=4, sticky="ensw", pady=(20, 0), padx=(0, 10))
        self.detect_colour_label.grid(column=4, row=3, sticky="w", padx=(0, 10), pady=(20, 0))
        self.detect_colour_options.grid(column=5, row=3, columnspan=2, sticky="ensw", pady=(20, 0))

        self.mask_colour_label.grid(column=4, row=4, sticky="w", padx=(0, 10), pady=(20, 0))
        self.btns["mask-colour-yes"].grid(column=5, row=4, sticky="ensw", pady=(20, 0))
        self.btns["mask-colour-no"].grid(column=6, row=4, sticky="ensw", pady=(20, 0))

        self.btns["reset-options"].grid(column=5, row=5, columnspan=2, sticky="ensw", pady=(20, 0))

        self.convexity_frame = tk.Frame(master=self.left)
        self.circularity_frame = tk.Frame(master=self.left)
        self.inertia_frame = tk.Frame(master=self.left)
        self.area_frame = tk.Frame(master=self.left)
        self.threshold_frame = tk.Frame(master=self.left)
        self.dist_frame = tk.Frame(master=self.left)

        self.separator_hori = ttk.Separator(master=self.left, orient="horizontal")
        self.separator_hori_1 = ttk.Separator(master=self.left, orient="horizontal")
        self.separator_vert = ttk.Separator(master=self.left, orient="vertical")

        # self.convexity_widgets = OrderedDict()
        # self.circularity_widgets = OrderedDict()
        # self.inertia_widgets = OrderedDict()
        # self.area_widgets = OrderedDict()
        # self.threshold_widgets = OrderedDict()
        # self.dist_widgets = OrderedDict()

        self.ball_tracker_options = tk.Label(master=self.left, text="Ball Tracker Options", font=("Helvetica", 18))
        self.ball_tracker_reset = tk.Button(master=self.left, text="Reset", command=self._reset_tracker_options, height=1, width=10,
                font=self.master.fonts["h4"], state="normal", cursor="hand2"
            )

        self.convexity_widgets = OrderedDict([
            ('radio_label', tk.Label(self.convexity_frame, text="Filter by Convexity", anchor="w", width=20)),
            ('radio_true', tk.Radiobutton(self.convexity_frame, text="Yes", value=True,
                                          variable=self.ball_detection_settings['filter_by_convexity'])),
            ('radio_false', tk.Radiobutton(self.convexity_frame, text="No", value=False,
                                           variable=self.ball_detection_settings['filter_by_convexity'])),
            ('min_label', tk.Label(self.convexity_frame, text="Minimum Convexity", anchor="w", width=20)),
            ('min', tk.Scale(self.convexity_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['min_convexity'])),
            ('max_label', tk.Label(self.convexity_frame, text="Maximum Convexity", anchor="w", width=20)),
            ('max', tk.Scale(self.convexity_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['max_convexity']))
        ])

        self.circularity_widgets = OrderedDict([
            ('radio_label', tk.Label(self.circularity_frame, text="Filter by Circularity", anchor="w", width=20)),
            ('radio_true', tk.Radiobutton(self.circularity_frame, text="Yes", value=True,
                                          variable=self.ball_detection_settings['filter_by_circularity'])),
            ('radio_false', tk.Radiobutton(self.circularity_frame, text="No", value=False,
                                           variable=self.ball_detection_settings['filter_by_circularity'])),
            ('min_label', tk.Label(self.circularity_frame, text="Minimum Circularity", anchor="w", width=20)),
            ('min', tk.Scale(self.circularity_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['min_circularity'])),
            ('max_label', tk.Label(self.circularity_frame, text="Maximum Circularity", anchor="w", width=20)),
            ('max', tk.Scale(self.circularity_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['max_circularity']))
        ])

        self.inertia_widgets = OrderedDict([
            ('radio_label', tk.Label(self.inertia_frame, text="Filter by Inertia", anchor="w", width=20)),
            ('radio_true',
             tk.Radiobutton(self.inertia_frame, text="Yes", value=True,
                            variable=self.ball_detection_settings['filter_by_inertia'])),
            ('radio_false',
             tk.Radiobutton(self.inertia_frame, text="No", value=False,
                            variable=self.ball_detection_settings['filter_by_inertia'])),
            ('min_label', tk.Label(self.inertia_frame, text="Minimum Inertia", anchor="w", width=20)),
            ('min', tk.Scale(self.inertia_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['min_inertia'])),
            ('max_label', tk.Label(self.inertia_frame, text="Maximum Inertia", anchor="w", width=20)),
            ('max', tk.Scale(self.inertia_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=-1,
                             variable=self.ball_detection_settings['max_inertia']))
        ])

        self.area_widgets = OrderedDict([
            ('radio_label', tk.Label(self.area_frame, text="Filter by Area", anchor="w", width=20)),
            ('radio_true',
             tk.Radiobutton(self.area_frame, text="Yes", variable=self.ball_detection_settings['filter_by_area'],
                            value=True)),
            ('radio_false',
             tk.Radiobutton(self.area_frame, text="No", variable=self.ball_detection_settings['filter_by_area'],
                            value=False)),
            ('min_label', tk.Label(self.area_frame, text="Minimum Area", anchor="w", width=20)),
            ('min', tk.Scale(self.area_frame, from_=1, to=2000, orient=tk.HORIZONTAL, length=300,
                             variable=self.ball_detection_settings['min_area'])),
            ('max_label', tk.Label(self.area_frame, text="Maximum Area", anchor="w", width=20)),
            ('max', tk.Scale(self.area_frame, from_=1, to=2000, orient=tk.HORIZONTAL, length=300,
                             variable=self.ball_detection_settings['max_area']))
        ])

        self.threshold_widgets = OrderedDict([
            ('min_label', tk.Label(self.threshold_frame, text="Minimum Threshold", anchor="w", width=20)),
            ('min', tk.Scale(self.threshold_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                             variable=self.ball_detection_settings['min_threshold'])),
            ('max_label', tk.Label(self.threshold_frame, text="Maximum Threshold", anchor="w", width=20)),
            ('max', tk.Scale(self.threshold_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                             variable=self.ball_detection_settings['max_threshold']))
        ])

        self.dist_widgets = OrderedDict([
            ('min_label', tk.Label(self.dist_frame, text="Minimum distance between balls", anchor="w", width=20,
                                   wraplength=150)),
            ('min', tk.Scale(self.dist_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                             variable=self.ball_detection_settings['min_dist_between_blobs'])),
        ])

        self.convexity_widgets['radio_label'].grid(column=0, row=0)
        self.convexity_widgets['radio_true'].grid(column=1, row=0)
        self.convexity_widgets['radio_false'].grid(column=2, row=0)
        self.convexity_widgets['min_label'].grid(column=0, row=1)
        self.convexity_widgets['min'].grid(column=1, row=1, columnspan=2)
        self.convexity_widgets['max_label'].grid(column=0, row=2)
        self.convexity_widgets['max'].grid(column=1, row=2, columnspan=2)

        self.circularity_widgets['radio_label'].grid(column=0, row=0)
        self.circularity_widgets['radio_true'].grid(column=1, row=0)
        self.circularity_widgets['radio_false'].grid(column=2, row=0)
        self.circularity_widgets['min_label'].grid(column=0, row=1)
        self.circularity_widgets['min'].grid(column=1, row=1, columnspan=2)
        self.circularity_widgets['max_label'].grid(column=0, row=2)
        self.circularity_widgets['max'].grid(column=1, row=2, columnspan=2)

        self.inertia_widgets['radio_label'].grid(column=0, row=0)
        self.inertia_widgets['radio_true'].grid(column=1, row=0)
        self.inertia_widgets['radio_false'].grid(column=2, row=0)
        self.inertia_widgets['min_label'].grid(column=0, row=1)
        self.inertia_widgets['min'].grid(column=1, row=1, columnspan=2)
        self.inertia_widgets['max_label'].grid(column=0, row=2)
        self.inertia_widgets['max'].grid(column=1, row=2, columnspan=2)

        self.area_widgets['radio_label'].grid(column=0, row=0)
        self.area_widgets['radio_true'].grid(column=1, row=0)
        self.area_widgets['radio_false'].grid(column=2, row=0)
        self.area_widgets['min_label'].grid(column=0, row=1)
        self.area_widgets['min'].grid(column=1, row=1, columnspan=10)
        self.area_widgets['max_label'].grid(column=0, row=2)
        self.area_widgets['max'].grid(column=1, row=2, columnspan=10)

        self.threshold_widgets['min_label'].grid(column=0, row=0)
        self.threshold_widgets['min'].grid(column=1, row=0)
        self.threshold_widgets['max_label'].grid(column=0, row=1)
        self.threshold_widgets['max'].grid(column=1, row=1)

        self.dist_widgets['min_label'].grid(column=0, row=0)
        self.dist_widgets['min'].grid(column=1, row=0)

        self.ball_tracker_options.grid(column=0, row=0, sticky="w")
        self.separator_hori_1.grid(column=0, row=1, columnspan=6, sticky="ew", pady=(10, 10))
        self.ball_tracker_reset.grid(column=0, row=2, sticky="w", padx=(20, 0))
        self.separator_hori.grid(column=0, row=3, columnspan=6, sticky="ew", pady=(10, 20))
        self.separator_vert.grid(column=1, row=3, rowspan=4, sticky="ns", pady=(10, 0))
        self.convexity_frame.grid(column=0, row=4, sticky="ew", padx=20)
        self.circularity_frame.grid(column=0, row=5, sticky="ew", padx=20, pady=(20, 0))
        self.threshold_frame.grid(column=0, row=6, sticky="ew", padx=20, pady=(20, 0))
        self.inertia_frame.grid(column=2, row=4, sticky="ew", padx=(20, 0))
        self.area_frame.grid(column=2, row=5, columnspan=4, sticky="ew", padx=(20, 0), pady=(20, 0))
        self.dist_frame.grid(column=2, row=6, sticky="ew", padx=(20, 0), pady=(20, 0))
        
        
        # self.colour_detection_frame = tk.Frame(self, padx=30)
        # self.red_colour_frame = tk.Frame(self.colour_detection_frame)
        # self.yellow_colour_frame = tk.Frame(self.colour_detection_frame)
        # self.green_colour_frame = tk.Frame(self.colour_detection_frame)
        # self.brown_colour_frame = tk.Frame(self.colour_detection_frame)
        # self.blue_colour_frame = tk.Frame(self.colour_detection_frame)
        # self.pink_colour_frame = tk.Frame(self.colour_detection_frame)
        # self.black_colour_frame = tk.Frame(self.colour_detection_frame)
        # self.white_colour_frame = tk.Frame(self.colour_detection_frame)
        # self.table_colour_frame = tk.Frame(self.colour_detection_frame)

        # self.red_colour_widgets = OrderedDict()
        # self.yellow_colour_widgets = OrderedDict()
        # self.green_colour_widgets = OrderedDict()
        # self.brown_colour_widgets = OrderedDict()
        # self.blue_colour_widgets = OrderedDict()
        # self.pink_colour_widgets = OrderedDict()
        # self.black_colour_widgets = OrderedDict()
        # self.white_colour_widgets = OrderedDict()
        # self.table_colour_widgets = OrderedDict()





        self.left.pack(side="left", fill="both", expand=1, anchor="w")
        self.middle.pack(side="left", fill="both", expand=1, anchor="w")
        # self.right.pack(side="right", fill="both", expand=1, anchor="w")

        self.file_output.pack(side="top", anchor="ne", padx=50, pady=(50, 0))
        self.btns_frame.pack(side="top", anchor="ne", padx=50, pady=20)
        self.pack(side="top", fill="both", expand=1, anchor="n")


    def enable_btns(self):
        for btn in self.btns:
            self.btns[btn].configure(state="normal", cursor="hand2")
        self.btns["mask-colour-yes"].configure(state="disable", cursor="")
        self.btns["mask-colour-no"].configure(state="disable", cursor="")
        self.btns["crop-frames-yes"].configure(state="disable", cursor="")
        self.btns["crop-frames-no"].configure(state="disable", cursor="")
        self.detect_colour_options.configure(state="normal", cursor="hand2")


    def _reset_video_options(self):
        self.data["threshold"].set(False)
        self._update_threshold()
        self.data["detect-colour"].set("None")
        self._detect_colour(self.data["detect-colour"].get())
        self.data["mask-colour"].set(False)
        self._mask_colour()


    def _reset_tracker_options(self):
        self.ball_detection_settings['filter_by_convexity'].set(s.FILTER_BY_CONVEXITY)
        self.ball_detection_settings['min_convexity'].set(s.MIN_CONVEXITY)
        self.ball_detection_settings['max_convexity'].set(s.MAX_CONVEXITY)

        self.ball_detection_settings['filter_by_circularity'].set(s.FILTER_BY_CIRCULARITY)
        self.ball_detection_settings['min_circularity'].set(s.MIN_CIRCULARITY)
        self.ball_detection_settings['max_circularity'].set(s.MAX_CIRCULARITY)

        self.ball_detection_settings['filter_by_inertia'].set(s.FILTER_BY_INERTIA)
        self.ball_detection_settings['min_inertia'].set(s.MIN_INERTIA_RATIO)
        self.ball_detection_settings['max_inertia'].set(s.MAX_INERTIA_RATIO)

        self.ball_detection_settings['filter_by_area'].set(s.FILTER_BY_AREA)
        self.ball_detection_settings['min_area'].set(s.MIN_AREA)
        self.ball_detection_settings['max_area'].set(s.MAX_AREA)

        self.ball_detection_settings['min_dist_between_blobs'].set(s.MIN_DIST_BETWEEN_BLOBS)

        self.ball_detection_settings['min_threshold'].set(s.MIN_THRESHOLD)
        self.ball_detection_settings['max_threshold'].set(s.MAX_THRESHOLD)


    def _update_threshold(self):
        self.data["mask-colour"].set(False)
        self.master.thread.mask_colour = self.data["mask-colour"].get()
        self.master.thread.show_threshold = self.data["threshold"].get()

    
    def _mask_colour(self):
        self.data["threshold"].set(False)
        self.master.thread.show_threshold = self.data["threshold"].get()
        self.master.thread.mask_colour = self.data["mask-colour"].get()

    
    def _crop_frames(self):
        self.master.thread.crop_frames = self.data["crop-frames"].get()


    def _detect_colour(self, value):
        if value != "None":
            self.btns["mask-colour-yes"].configure(state="normal", cursor="hand2")
            self.btns["mask-colour-no"].configure(state="normal", cursor="hand2")
        else:
            self.data["mask-colour"].set(False)
            self.btns["mask-colour-yes"].configure(state="disable", cursor="")
            self.btns["mask-colour-no"].configure(state="disable", cursor="")
        self.master.thread.detect_colour = value


    def _toogle_output(self):
        if self.master.thread.play_stream:
            self.master.thread.play_stream = False
            self.btns['toggle'].configure(text="Play")
        else:
            self.master.thread.play_stream = True
            self.btns['toggle'].configure(text="Pause")


    def _restart_output(self):
        self.master.thread.restart_stream()


    def _update_bounds(self):
        self.master.thread.update_bounds()
        time.sleep(0.1)
        if self.master.thread.ball_tracker.detected_table():
            self.btns["crop-frames-yes"].configure(state="normal", cursor="hand2")
            self.btns["crop-frames-no"].configure(state="normal", cursor="hand2")
