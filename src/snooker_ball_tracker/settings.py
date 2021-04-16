import json
import numpy as np
from json import JSONEncoder


class __SettingsJSONEncoder(JSONEncoder):
    def default(self, obj):
        # Convert numpy array to a list before outputing to json file
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def __decode_colour_to_np_array(dct):
    # Decode colour dicts loaded from json into numpy arrays
    if "LOWER" in dct:
        dct["LOWER"] = np.array(dct["LOWER"])
    if "UPPER" in dct:
        dct["UPPER"] = np.array(dct["UPPER"])
    return dct


def load(settings_file: str) -> tuple:
    """Load settings from provided json file.

    :param settings_file: path to json file to read from  
    :type settings_file: str  
    :return: True/False if load operation succeeded/failed and error message  
    :rtype: tuple  
    """
    global __SETTINGS
    try:
        with open(settings_file, "r") as fp:
            __SETTINGS = json.load(fp, object_hook=__decode_colour_to_np_array)
    except Exception as error:
        return False, error
    else:
        return True, None


def save(settings_file: str, settings: dict=None) -> tuple:
    """Save settings to provided json file. 

    :param settings_file: path to json to write to  
    :type settings_file: str  
    :param settings: settings to save, defaults to None  
    :type settings: dict, optional  
    :return: True/False if save operation succeeded/failed and error message  
    :rtype: tuple  
    """
    global __SETTINGS
    settings_to_save = __SETTINGS
    if settings:
        settings_to_save = settings

    try:
        with open(settings_file, "w") as fp:
            json.dump(settings_to_save, fp, indent=4, sort_keys=True, cls=__SettingsJSONEncoder)
    except Exception as error:
        return False, error
    else:
        return True, None


def __getattr__(key):
    try:
        return __SETTINGS[key]
    except KeyError:
        try:
            default_value = __DEFAULT_SETTINGS[key]
            print(f"Error: could not find key '{key}' in loaded settings, using default")
            return default_value
        except KeyError:
            return getattr(__file__, key)
            # raise KeyError(f"Error: could not find key '{key}' in {__DEFAULT_SETTINGS}")


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
            "WHITE": True,
            "RED": True,
            "YELLOW": True,
            "GREEN": True,
            "BROWN": True,
            "BLUE": True,
            "PINK": True,
            "BLACK": True
        },
        "COLOURS": {
            "RED": {
                "LOWER": np.array([25, 190, 150]),
                "UPPER": np.array([180, 255, 255])
            },
            "YELLOW": {
                "LOWER": np.array([10, 100, 100]),
                "UPPER": np.array([35, 255, 255])
            },
            "GREEN": {
                "LOWER": np.array([55, 50, 50]),
                "UPPER": np.array([100, 255, 255])
            },
            "BROWN": {
                "LOWER": np.array([0, 136, 150]),
                "UPPER": np.array([10, 225, 255])
            },
            "BLUE": {
                "LOWER": np.array([115, 60, 60]),
                "UPPER": np.array([135, 255, 255])
            },
            "PINK": {
                "LOWER": np.array([160, 60, 240]),
                "UPPER": np.array([180, 120, 255])
            },
            "BLACK": {
                "LOWER": np.array([0, 0, 0]),
                "UPPER": np.array([180, 255, 40])
            },
            "WHITE": {
                "LOWER": np.array([0, 0, 240]),
                "UPPER": np.array([30, 80, 255])
            },
            "TABLE": {
                "LOWER": np.array([0, 18, 0]),
                "UPPER": np.array([66, 125, 230])
            }
        }
    }
}

#####################
#  LOADED SETTINGS  #
#####################
__SETTINGS = __DEFAULT_SETTINGS
