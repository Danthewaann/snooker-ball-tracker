from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
from collections import OrderedDict
import time
import numpy as np
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import BallTracker


class VideoPlayer(Frame):
    def __init__(self, master=None, logger=None):
        super().__init__(master)
        self.logger = logger
        self.file_output = Canvas(
            master=self, width=800, height=400, bg="light gray")

        self.data = {
            "threshold": BooleanVar(self, False),
            "detect-colour": StringVar(self, "None"),
            "detect-colours": ["None"] + (list(s.COLOURS.keys())),
            "mask-colour": BooleanVar(self, False),
            "crop-frames": BooleanVar(self, False)
        }

        self.btns_frame = Frame(master=self)

        self.cursor_x_y = Label(master=self.btns_frame, text="X: 0, Y: 0")
        self.video_player_label = Label(
            master=self.btns_frame, text="Video Player Options", font=self.master.master.fonts["h3-bold"])
        self.separator_hori = Separator(
            master=self.btns_frame, orient="horizontal")
        self.separator_vert = Separator(
            master=self.btns_frame, orient="vertical")
        self.threshold_label = Label(
            master=self.btns_frame, text="Show Threshold")
        self.detect_colour_label = Label(
            master=self.btns_frame, text="Detect Colour")
        self.detect_colour_options = OptionMenu(
            self.btns_frame, self.data["detect-colour"], "None", *self.data["detect-colours"], command=self._detect_colour)
        self.detect_colour_options.configure(state="disabled")
        self.mask_colour_label = Label(
            master=self.btns_frame, text="Mask Colour")

        self.crop_frames = Label(master=self.btns_frame, text="Crop Frames")

        self.btns = OrderedDict([
            ("toggle", Button(
                self.btns_frame, text="Play", command=self._toogle_output, state="disable"
            )),
            ("restart", Button(
                self.btns_frame, text="Restart", command=self._restart_output, state="disable"
            )),
            ("update-bounds", Button(
                self.btns_frame, text="Detect Table", command=self._update_bounds, state="disable"
            )),
            ("threshold-yes", Radiobutton(
                self.btns_frame, text="Yes", command=self._update_threshold, state="disable",
                variable=self.data["threshold"], value=True
            )),
            ("threshold-no", Radiobutton(
                self.btns_frame, text="No", command=self._update_threshold, state="disable",
                variable=self.data["threshold"], value=False
            )),
            ("mask-colour-yes", Radiobutton(
                self.btns_frame, text="Yes", command=self._mask_colour, state="disable",
                variable=self.data["mask-colour"], value=True
            )),
            ("mask-colour-no", Radiobutton(
                self.btns_frame, text="No", command=self._mask_colour, state="disable",
                variable=self.data["mask-colour"], value=False
            )),
            ("crop-frames-yes", Radiobutton(
                self.btns_frame, text="Yes", command=self._crop_frames, state="disable",
                variable=self.data["crop-frames"], value=True
            )),
            ("crop-frames-no", Radiobutton(
                self.btns_frame, text="No", command=self._crop_frames, state="disable",
                variable=self.data["crop-frames"], value=False
            )),
            ("reset-options", Button(
                self.btns_frame, text="Reset", command=self.reset_video_options, state="disable"
            )),
        ])

    def grid_children(self):
        self.cursor_x_y.grid(column=0, row=0)
        self.video_player_label.grid(column=3, row=0, columnspan=4, sticky="e")
        self.separator_hori.grid(
            column=0, row=1, columnspan=7, sticky="ew", pady=(10, 0))

        self.btns["toggle"].grid(column=0, row=2, sticky="ensw", pady=(20, 0))
        self.btns["restart"].grid(
            column=1, row=2, columnspan=2, sticky="ensw", pady=(20, 0), padx=(0, 10))
        self.separator_vert.grid(
            column=3, row=2, rowspan=4, sticky="ns", padx=(20, 20))
        self.threshold_label.grid(
            column=4, row=2, sticky="w", padx=(0, 10), pady=(20, 0))
        self.btns["threshold-yes"].grid(column=5,
                                        row=2, sticky="ensw", pady=(20, 0))
        self.btns["threshold-no"].grid(column=6,
                                       row=2, sticky="ensw", pady=(20, 0))

        self.btns["update-bounds"].grid(column=0, row=3,
                                        columnspan=3, sticky="ensw", padx=(0, 10))
        self.crop_frames.grid(column=0, row=4, sticky="w",
                              padx=(0, 10), pady=(20, 0))
        self.btns["crop-frames-yes"].grid(column=1,
                                          row=4, sticky="ensw", pady=(20, 0))
        self.btns["crop-frames-no"].grid(column=2, row=4,
                                         sticky="ensw", pady=(20, 0), padx=(0, 10))
        self.detect_colour_label.grid(
            column=4, row=3, sticky="w", padx=(0, 10), pady=(20, 0))
        self.detect_colour_options.grid(
            column=5, row=3, columnspan=2, sticky="ensw", pady=(20, 0))

        self.mask_colour_label.grid(
            column=4, row=4, sticky="w", padx=(0, 10), pady=(20, 0))
        self.btns["mask-colour-yes"].grid(column=5,
                                          row=4, sticky="ensw", pady=(20, 0))
        self.btns["mask-colour-no"].grid(column=6,
                                         row=4, sticky="ensw", pady=(20, 0))

        self.btns["reset-options"].grid(column=5, row=5,
                                        columnspan=2, sticky="ensw", pady=(20, 0))

        self.file_output.pack(side="top", anchor="ne")
        self.btns_frame.pack(side="top", anchor="ne", pady=(20, 0))

    def load_video_player(self):
        self.logger.info("Loading video player...")
        self.enable_btns()
        self.file_output.destroy()
        self.btns_frame.pack_forget()
        self.file_output = Label(master=self)
        self.file_output.bind("<Button 1>", self._update_selected_colour)
        self.file_output.bind("<Motion>", lambda event: self.cursor_x_y.configure(text=f"X: {event.x}, Y: {event.y}"))
        self.file_output.bind("<Leave>", lambda event: self.cursor_x_y.configure(text="X: 0, Y: 0"))
        self.file_output.pack(side="top", anchor="ne")
        self.btns_frame.pack(side="top", anchor="ne", pady=(20, 0))

    def enable_btns(self):
        for btn in self.btns:
            self.btns[btn].configure(state="normal", cursor="hand2")
        self.btns["mask-colour-yes"].configure(state="disable", cursor="")
        self.btns["mask-colour-no"].configure(state="disable", cursor="")
        # self.btns["crop-frames-yes"].configure(state="disable", cursor="")
        # self.btns["crop-frames-no"].configure(state="disable", cursor="")
        self.detect_colour_options.configure(state="normal", cursor="hand2")

    def reset_video_options(self):
        self.data["threshold"].set(False)
        self._update_threshold()
        self.data["detect-colour"].set("None")
        self._detect_colour(self.data["detect-colour"].get())
        self.data["mask-colour"].set(False)
        self._mask_colour()
        self.data["crop-frames"].set(False)
        self._crop_frames()
        self.logger.info("Video player options reset")

    def _update_threshold(self):
        self.data["mask-colour"].set(False)
        if self.data["threshold"].get():
            self.logger.info("Showing binary frames...")
        else:
            self.logger.info("Hiding binary frames...")
        if self.master.master.thread is not None:
            self.master.master.thread.mask_colour = self.data["mask-colour"].get(
            )
            self.master.master.thread.show_threshold = self.data["threshold"].get(
            )

    def _mask_colour(self):
        self.data["threshold"].set(False)
        if self.data["mask-colour"].get():
            self.logger.info("Showing selected colour mask...")
        else:
            self.logger.info("Hiding selected colour mask...")
        if self.master.master.thread is not None:
            self.master.master.thread.show_threshold = self.data["threshold"].get(
            )
            self.master.master.thread.mask_colour = self.data["mask-colour"].get(
            )

    def _crop_frames(self):
        crop = self.data["crop-frames"].get()
        if crop:
            self.logger.info(
                "Enabling cropped frames around table boundary...")
        else:
            self.logger.info(
                "Disabling cropped frames around table boundary...")
        if self.master.master.thread is not None:
            self.master.master.thread.crop_frames_around_boundary(crop)

    def _detect_colour(self, value):
        if value != "None":
            self.logger.info(f"Detecting {value} in frames...")
            self.data["mask-colour"].set(False)
            self.btns["mask-colour-yes"].configure(
                state="normal", cursor="hand2")
            self.btns["mask-colour-no"].configure(
                state="normal", cursor="hand2")
        else:
            self.logger.info("Detecting all colours in frames...")
            self.btns["mask-colour-yes"].configure(state="disable", cursor="")
            self.btns["mask-colour-no"].configure(state="disable", cursor="")
        if self.master.master.thread is not None:
            self.master.master.thread.detect_colour = value

    def _toogle_output(self):
        if self.master.master.thread.play_stream:
            self.logger.info("Pausing video...")
            self.master.master.thread.play_stream = False
            self.btns['toggle'].configure(text="Play")
        else:
            self.logger.info("Playing video...")
            self.master.master.thread.play_stream = True
            self.btns['toggle'].configure(text="Pause")

    def _restart_output(self):
        self.logger.info("Restarting video...")
        if self.master.master.thread is not None:
            self.btns['toggle'].configure(text="Play")

            if self.master.master.thread.is_alive():
                self.master.master.restart_video_processor()
            else:
                self.master.master.start_video_processor()

    def _update_bounds(self):
        self.logger.info("Detecting table boundary...")
        self.master.master.thread.update_bounds()

    def _update_selected_colour(self, event):
        hsv = self.master.master.thread.get_hsv()
        pixels = hsv[event.y-5:event.y+5, event.x-5:event.x+5]
        min_pixel = np.min(pixels, axis=0)[0]
        max_pixel = np.max(pixels, axis=0)[0]

        colour = {}
        colour['LOWER'] = min_pixel
        colour['UPPER'] = max_pixel

        self.master.master.colour_detection_options.colour_detection_settings["colour"]["lower_h"].set(
            colour["LOWER"][0])
        self.master.master.colour_detection_options.colour_detection_settings["colour"]["lower_s"].set(
            colour["LOWER"][1])
        self.master.master.colour_detection_options.colour_detection_settings["colour"]["lower_v"].set(
            colour["LOWER"][2])

        self.master.master.colour_detection_options.colour_detection_settings["colour"]["upper_h"].set(
            colour["UPPER"][0])
        self.master.master.colour_detection_options.colour_detection_settings["colour"]["upper_s"].set(
            colour["UPPER"][1])
        self.master.master.colour_detection_options.colour_detection_settings["colour"]["upper_v"].set(
            colour["UPPER"][2])

        s.COLOURS[self.master.master.colour_detection_options.colour_detection_settings["select-colour"].get()]['LOWER'][0] = self.master.master.colour_detection_options.colour_detection_settings['colour']['lower_h'].get()
        s.COLOURS[self.master.master.colour_detection_options.colour_detection_settings["select-colour"].get()]['LOWER'][1] = self.master.master.colour_detection_options.colour_detection_settings['colour']['lower_s'].get()
        s.COLOURS[self.master.master.colour_detection_options.colour_detection_settings["select-colour"].get()]['LOWER'][2] = self.master.master.colour_detection_options.colour_detection_settings['colour']['lower_v'].get()
        s.COLOURS[self.master.master.colour_detection_options.colour_detection_settings["select-colour"].get()]['UPPER'][0] = self.master.master.colour_detection_options.colour_detection_settings['colour']['upper_h'].get()
        s.COLOURS[self.master.master.colour_detection_options.colour_detection_settings["select-colour"].get()]['UPPER'][1] = self.master.master.colour_detection_options.colour_detection_settings['colour']['upper_s'].get()
        s.COLOURS[self.master.master.colour_detection_options.colour_detection_settings["select-colour"].get()]['UPPER'][2] = self.master.master.colour_detection_options.colour_detection_settings['colour']['upper_v'].get()
