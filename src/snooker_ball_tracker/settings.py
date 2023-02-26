from __future__ import annotations

import json
from json import JSONEncoder
from typing import Any

import numpy as np

from .enums import SnookerColour


class Settings:

    ######################
    #  DEFAULT SETTINGS  #
    ######################
    __DEFAULT_SETTINGS = {
        #############################
        #  BALL DETECTION SETTINGS  #
        #############################
        "BALL_DETECTION_SETTINGS": {
            "FILTER_BY_CONVEXITY": False,
            "MIN_CONVEXITY": 0.5,
            "MAX_CONVEXITY": 1,
            "FILTER_BY_CIRCULARITY": True,
            "MIN_CIRCULARITY": 0.3,
            "MAX_CIRCULARITY": 1,
            "FILTER_BY_INERTIA": False,
            "MIN_INERTIA": 0.2,
            "MAX_INERTIA": 1,
            "FILTER_BY_AREA": True,
            "MIN_AREA": 200,
            "MAX_AREA": 2000,
            "FILTER_BY_COLOUR": True,
            "BLOB_COLOUR": 255,
            "MIN_DIST_BETWEEN_BLOBS": 10,
            "MIN_THRESHOLD": 0,
            "MAX_THRESHOLD": 255,
        },
        #####################
        #  COLOUR SETTINGS  #
        #####################
        "COLOUR_DETECTION_SETTINGS": {
            "BALL_COLOURS": {
                SnookerColour.RED: {"DETECT": True, "ORDER": 1},
                SnookerColour.YELLOW: {"DETECT": True, "ORDER": 3},
                SnookerColour.GREEN: {"DETECT": True, "ORDER": 4},
                SnookerColour.BROWN: {"DETECT": True, "ORDER": 8},
                SnookerColour.BLUE: {"DETECT": True, "ORDER": 5},
                SnookerColour.PINK: {"DETECT": True, "ORDER": 6},
                SnookerColour.BLACK: {"DETECT": True, "ORDER": 7},
                SnookerColour.WHITE: {"DETECT": True, "ORDER": 2},
            },
            "COLOURS": {
                SnookerColour.RED: {
                    "LOWER": np.array([25, 190, 150]),
                    "UPPER": np.array([180, 255, 255]),
                },
                SnookerColour.YELLOW: {
                    "LOWER": np.array([10, 100, 100]),
                    "UPPER": np.array([35, 255, 255]),
                },
                SnookerColour.GREEN: {
                    "LOWER": np.array([55, 50, 50]),
                    "UPPER": np.array([100, 255, 255]),
                },
                SnookerColour.BROWN: {
                    "LOWER": np.array([0, 136, 150]),
                    "UPPER": np.array([10, 225, 255]),
                },
                SnookerColour.BLUE: {
                    "LOWER": np.array([115, 60, 60]),
                    "UPPER": np.array([135, 255, 255]),
                },
                SnookerColour.PINK: {
                    "LOWER": np.array([160, 60, 240]),
                    "UPPER": np.array([180, 120, 255]),
                },
                SnookerColour.BLACK: {
                    "LOWER": np.array([0, 0, 0]),
                    "UPPER": np.array([180, 255, 40]),
                },
                SnookerColour.WHITE: {
                    "LOWER": np.array([0, 0, 240]),
                    "UPPER": np.array([30, 80, 255]),
                },
                SnookerColour.TABLE: {
                    "LOWER": np.array([0, 18, 0]),
                    "UPPER": np.array([66, 125, 230]),
                },
            },
        },
    }

    #####################
    #  LOADED SETTINGS  #
    #####################
    __SETTINGS = __DEFAULT_SETTINGS

    class __SettingsJSONEncoder(JSONEncoder):
        def default(self, obj: Any) -> Any:
            # Convert numpy array to a list before outputing to json file
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)

    def __settings_object_hook(self, dct: dict[str, Any]) -> dict[str, Any]:
        # Decode colour keys into Enums
        if SnookerColour.WHITE in dct:
            for colour in SnookerColour:
                if colour.value in dct:
                    dct[colour] = dct.pop(colour.value)
        # Decode colour range dicts loaded from json into numpy arrays
        if "LOWER" in dct:
            dct["LOWER"] = np.array(dct["LOWER"])
        if "UPPER" in dct:
            dct["UPPER"] = np.array(dct["UPPER"])
        return dct

    def load(self, settings_file: str) -> tuple[bool, Exception | None]:
        """Load settings from provided json file.

        :param settings_file: path to json file to read from
        :return: True/False if load operation succeeded/failed and error message
        """
        try:
            with open(settings_file, "r") as fp:
                self.__SETTINGS = json.load(fp, object_hook=self.__settings_object_hook)
        except Exception as error:
            return False, error
        else:
            return True, None

    def save(
        self, settings_file: str, settings: dict[str, Any] | None = None
    ) -> tuple[bool, Exception | None]:
        """Save settings to provided json file.

        :param settings_file: path to json to write to
        :param settings: settings to save, defaults to None
        :return: True/False if save operation succeeded/failed and error message
        """
        settings_to_save = self.__SETTINGS
        if settings:
            settings_to_save = settings

        try:
            with open(settings_file, "w") as fp:
                json.dump(
                    settings_to_save,
                    fp,
                    indent=4,
                    sort_keys=True,
                    cls=self.__SettingsJSONEncoder,
                )
        except Exception as error:
            return False, error
        else:
            return True, None

    def __getattr__(self, key: str) -> Any:
        """Obtain attribute from loaded settings if found, otherwise
        get base attribute

        :param key: setting key to get
        :return: value of setting
        """
        try:
            return self.__SETTINGS[key]
        except KeyError:
            try:
                default_value = self.__DEFAULT_SETTINGS[key]
            except KeyError:
                return super().__getattribute__(key)
            else:
                print(
                    f"Error: could not find key '{key}' "
                    "in loaded settings, using default"
                )
                return default_value


settings = Settings()
