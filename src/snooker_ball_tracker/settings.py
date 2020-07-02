from snooker_ball_tracker.config import default_settings
import importlib

settings_module_name = 'default_settings'
try:
    settings_module = importlib.import_module('config.' + settings_module_name, package=__package__)
except ImportError:
    settings_module = None


def get_setting(name):
    try:
        return getattr(settings_module, name)
    except AttributeError:
        return getattr(default_settings, name)


###################
#  BASE SETTINGS  #
###################
DETECT_COLOURS = get_setting('DETECT_COLOURS')

#############################
#  BLOB DETECTION SETTINGS  #
#############################
FILTER_BY_CONVEXITY = get_setting('FILTER_BY_CONVEXITY')
MIN_CONVEXITY = get_setting('MIN_CONVEXITY')
MAX_CONVEXITY = get_setting('MAX_CONVEXITY')

FILTER_BY_CIRCULARITY = get_setting('FILTER_BY_CIRCULARITY')
MIN_CIRCULARITY = get_setting('MIN_CIRCULARITY')
MAX_CIRCULARITY = get_setting('MAX_CIRCULARITY')

FILTER_BY_INERTIA = get_setting('FILTER_BY_INERTIA')
MIN_INERTIA_RATIO = get_setting('MIN_INERTIA_RATIO')
MAX_INERTIA_RATIO = get_setting('MAX_INERTIA_RATIO')

FILTER_BY_AREA = get_setting('FILTER_BY_AREA')
MIN_AREA = get_setting('MIN_AREA')
MAX_AREA = get_setting('MAX_AREA')

FILTER_BY_COLOUR = get_setting('FILTER_BY_COLOUR')
BLOB_COLOUR = get_setting('BLOB_COLOUR')

MIN_DIST_BETWEEN_BLOBS = get_setting('MIN_DIST_BETWEEN_BLOBS')

MIN_THRESHOLD = get_setting('MIN_THRESHOLD')
MAX_THRESHOLD = get_setting('MAX_THRESHOLD')

###############################
#  HSV COLOUR RANGE SETTINGS  #
###############################
COLOURS = get_setting('COLOURS')


def load():
    global settings_module, DETECT_COLOURS, FILTER_BY_CONVEXITY, MIN_CONVEXITY, \
        MAX_CONVEXITY, FILTER_BY_CIRCULARITY, MIN_CIRCULARITY, \
        MAX_CIRCULARITY, FILTER_BY_INERTIA, MIN_INERTIA_RATIO, MAX_INERTIA_RATIO, FILTER_BY_AREA, \
        MIN_AREA, MAX_AREA, FILTER_BY_COLOUR, BLOB_COLOUR, MIN_DIST_BETWEEN_BLOBS, MIN_THRESHOLD, MAX_THRESHOLD, \
        COLOURS

    try:
        settings_module = importlib.import_module('snooker_ball_tracker.config.' + settings_module_name, package=__package__)
    except ImportError as e:
        print(e)
        settings_module = None

    ###################
    #  BASE SETTINGS  #
    ###################
    DETECT_COLOURS = get_setting('DETECT_COLOURS')

    #############################
    #  BLOB DETECTION SETTINGS  #
    #############################
    FILTER_BY_CONVEXITY = get_setting('FILTER_BY_CONVEXITY')
    MIN_CONVEXITY = get_setting('MIN_CONVEXITY')
    MAX_CONVEXITY = get_setting('MAX_CONVEXITY')

    FILTER_BY_CIRCULARITY = get_setting('FILTER_BY_CIRCULARITY')
    MIN_CIRCULARITY = get_setting('MIN_CIRCULARITY')
    MAX_CIRCULARITY = get_setting('MAX_CIRCULARITY')

    FILTER_BY_INERTIA = get_setting('FILTER_BY_INERTIA')
    MIN_INERTIA_RATIO = get_setting('MIN_INERTIA_RATIO')
    MAX_INERTIA_RATIO = get_setting('MAX_INERTIA_RATIO')

    FILTER_BY_AREA = get_setting('FILTER_BY_AREA')
    MIN_AREA = get_setting('MIN_AREA')
    MAX_AREA = get_setting('MAX_AREA')

    FILTER_BY_COLOUR = get_setting('FILTER_BY_COLOUR')
    BLOB_COLOUR = get_setting('BLOB_COLOUR')

    MIN_DIST_BETWEEN_BLOBS = get_setting('MIN_DIST_BETWEEN_BLOBS')

    MIN_THRESHOLD = get_setting('MIN_THRESHOLD')
    MAX_THRESHOLD = get_setting('MAX_THRESHOLD')

    ###############################
    #  HSV COLOUR RANGE SETTINGS  #
    ###############################
    COLOURS = get_setting('COLOURS')
