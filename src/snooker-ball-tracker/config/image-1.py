import numpy as np

###################
#  BASE SETTINGS  #
###################
DETECT_COLOURS = {
    'WHITE': True,
    'RED': True,
    'YELLOW': True,
    'GREEN': True,
    'BROWN': True,
    'BLUE': True,
    'PINK': True,
    'BLACK': True,
}

#############################
#  BLOB DETECTION SETTINGS  #
#############################
FILTER_BY_CONVEXITY = False
MIN_CONVEXITY = 0.5
MAX_CONVEXITY = 1

FILTER_BY_CIRCULARITY = False
MIN_CIRCULARITY = 0.3
MAX_CIRCULARITY = 1

FILTER_BY_INERTIA = True
MIN_INERTIA_RATIO = 0.2
MAX_INERTIA_RATIO = 1

FILTER_BY_AREA = True
MIN_AREA = 200
MAX_AREA = 2000

FILTER_BY_COLOUR = False
BLOB_COLOUR = 255

MIN_DIST_BETWEEN_BLOBS = 10
MIN_THRESHOLD = 170
MAX_THRESHOLD = 255

###############################
#  HSV COLOUR RANGE SETTINGS  #
###############################
COLOURS = {
    'RED': {
        'LOWER': np.array([25, 190, 150]),
        'UPPER': np.array([180, 255, 255])
    },
    'YELLOW': {
        'LOWER': np.array([10, 100, 100]),
        'UPPER': np.array([35, 255, 255])
    },
    'GREEN': {
        'LOWER': np.array([55, 0, 0]),
        'UPPER': np.array([100, 255, 255])
    },
    'BROWN': {
        'LOWER': np.array([0, 136, 150]),
        'UPPER': np.array([10, 225, 255])
    },
    'BLUE': {
        'LOWER': np.array([115, 60, 60]),
        'UPPER': np.array([135, 255, 255])
    },
    'PINK': {
        'LOWER': np.array([160, 60, 240]),
        'UPPER': np.array([180, 120, 255])
    },
    'BLACK': {
        'LOWER': np.array([0, 0, 0]),
        'UPPER': np.array([180, 255, 40])
    },
    'WHITE': {
        'LOWER': np.array([0, 0, 240]),
        'UPPER': np.array([30, 80, 255])
    },
    'TABLE': {
        'LOWER': np.array([0, 0, 0]),
        'UPPER': np.array([66, 67, 166])
    }
}

if __name__ == '__main__':
    from shutil import copy
    import argparse

    parser = argparse.ArgumentParser(description='Create configurable settings file')
    parser.add_argument('settings_file', help='Name of new settings file')

    args = parser.parse_args()
    if args:
        copy(__file__, args.settings_file + '.py')
    else:
        parser.print_help()
