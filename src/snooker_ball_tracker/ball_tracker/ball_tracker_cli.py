import argparse
import json
import os
from pprint import pprint

import cv2
import numpy as np
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import BallTracker
from snooker_ball_tracker.ball_tracker.util import transform_frame
from snooker_ball_tracker.colours import SnookerColour


# dummy callback method for trackbar
def nothing(x):
    pass


def pick_color(event, x_pos, y_pos, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = image.hsv_frame
        pixel = hsv[y_pos, x_pos]
        upper = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

        colour['LOWER'] = lower
        colour['UPPER'] = upper

        ball_tracker.colour_settings.colour_model.update(colour)

        cv2.setTrackbarPos('H (lower)', window_title, colour['LOWER'][0])
        cv2.setTrackbarPos('H (upper)', window_title, colour['UPPER'][0])
        cv2.setTrackbarPos('S (lower)', window_title, colour['LOWER'][1])
        cv2.setTrackbarPos('S (upper)', window_title, colour['UPPER'][1])
        cv2.setTrackbarPos('V (lower)', window_title, colour['LOWER'][2])
        cv2.setTrackbarPos('V (upper)', window_title, colour['UPPER'][2])


if __name__ == '__main__':
    global image, ball_tracker

    parser = argparse.ArgumentParser(
        description='Ball Tracker CLI (Only works with images)')
    parser.add_argument(
        'image', help='Image file to detect and track balls from')
    parser.add_argument('--width', dest='width', default=800, type=int,
                        help='Set width of image for processing, defaults to "%(default)s" pixels')
    parser.add_argument('--show-threshold', dest='show_threshold', action='store_true', default=False,
                        help='Show thresholded frames')
    parser.add_argument('--detect-colour', dest='detect_colour', default=None,
                        type=str.upper, choices=[
                            colour.value for colour in SnookerColour],
                        help='Detect contours matching provided colour')
    parser.add_argument('--mask-colour', dest='mask_colour', action='store_true', default=False,
                        help='Mask contours of provided colour')
    parser.add_argument('--morph', dest='morph', action='store_true', default=False,
                        help='Perform morph closing morphology on processed frames')
    parser.add_argument('--settings', dest='settings', default=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))), "resources/config/default_settings.json"),
        help='Settings file to use, defaults to "%(default)s"')
    args = parser.parse_args()

    args.image = os.path.abspath(args.image)
    args.settings = os.path.abspath(args.settings)

    # load settings from json file
    success, error = s.load(args.settings)
    if not success:
        parser.exit(1, message=f"No such settings file: {args.settings}")

    if os.path.exists(args.image):
        print("=================================")
        print("CLI Arguments:")
        print("=================================")
        pprint(vars(args), sort_dicts=True)
        print("=================================")
        print('USER CONTROLS:')
        print("=================================")
        print('s -> save processed frame to a jpg file')
        print('q -> exit the program')
        print('waiting for user input...\n')

        ball_tracker = BallTracker()
        colour = {
            'LOWER': np.array([0, 0, 0]),
            'UPPER': np.array([0, 0, 0])
        }

        # create main ball tracker window
        window_title = 'Snooker Ball Tracker Image CLI'
        cv2.namedWindow(window_title)

        # setup trackbars if --detect-colours in set
        if args.detect_colour is not None:
            ball_tracker.colour_settings.selected_colour = args.detect_colour
            colour = {
                'LOWER': s.COLOUR_DETECTION_SETTINGS["COLOURS"][args.detect_colour]['LOWER'],
                'UPPER': s.COLOUR_DETECTION_SETTINGS["COLOURS"][args.detect_colour]['UPPER']
            }

            # create trackbars for lower and upper HSV values
            cv2.createTrackbar('H (lower)', window_title, 0, 180, nothing)
            cv2.createTrackbar('H (upper)', window_title, 0, 180, nothing)
            cv2.createTrackbar('S (lower)', window_title, 0, 255, nothing)
            cv2.createTrackbar('S (upper)', window_title, 0, 255, nothing)
            cv2.createTrackbar('V (lower)', window_title, 0, 255, nothing)
            cv2.createTrackbar('V (upper)', window_title, 0, 255, nothing)
            cv2.setTrackbarPos('H (lower)', window_title, colour['LOWER'][0])
            cv2.setTrackbarPos('H (upper)', window_title, colour['UPPER'][0])
            cv2.setTrackbarPos('S (lower)', window_title, colour['LOWER'][1])
            cv2.setTrackbarPos('S (upper)', window_title, colour['UPPER'][1])
            cv2.setTrackbarPos('V (lower)', window_title, colour['LOWER'][2])
            cv2.setTrackbarPos('V (upper)', window_title, colour['UPPER'][2])
            cv2.setMouseCallback(window_title, pick_color)

            cv2.setTrackbarPos('H (lower)', window_title, colour['LOWER'][0])
            cv2.setTrackbarPos('H (upper)', window_title, colour['UPPER'][0])
            cv2.setTrackbarPos('S (lower)', window_title, colour['LOWER'][1])
            cv2.setTrackbarPos('S (upper)', window_title, colour['UPPER'][1])
            cv2.setTrackbarPos('V (lower)', window_title, colour['LOWER'][2])
            cv2.setTrackbarPos('V (upper)', window_title, colour['UPPER'][2])

        # read in image provided
        in_frame = cv2.imread(args.image)

        # frame display loop
        while True:
            image = transform_frame(
                in_frame, width=args.width, morph=args.morph)
            out_frame, _, _ = ball_tracker.process_image(
                image, show_threshold=args.show_threshold, detect_colour=args.detect_colour, mask_colour=args.mask_colour)
            cv2.imshow(window_title, out_frame)

            # obtain key value if a key was pressed
            key = cv2.waitKey(1) & 0xFF

            # if window is closed, exit program
            if cv2.getWindowProperty(window_title, cv2.WND_PROP_VISIBLE) == 0:
                break

            # if the 'q' key is pressed, exit program
            if key == ord('q'):
                break

            # if the 's' key is pressed, save processed frame to file
            if key == ord('s'):
                counter = 1
                file_name = os.path.join(os.path.dirname(args.image),
                                         os.path.splitext(os.path.basename(args.image))[0])
                while True:
                    frame_name = file_name + \
                        '-frame-' + str(counter) + '.jpg'
                    if not os.path.exists(frame_name):
                        print('saving frame to ' + frame_name)
                        cv2.imwrite(frame_name, out_frame)
                        break
                    counter += 1

            # obtain trackbar values and use them for --detect-colour
            if args.detect_colour is not None:
                h_lower = cv2.getTrackbarPos('H (lower)', window_title)
                h_upper = cv2.getTrackbarPos('H (upper)', window_title)
                s_lower = cv2.getTrackbarPos('S (lower)', window_title)
                s_upper = cv2.getTrackbarPos('S (upper)', window_title)
                v_lower = cv2.getTrackbarPos('V (lower)', window_title)
                v_upper = cv2.getTrackbarPos('V (upper)', window_title)

                colour['LOWER'] = np.array([h_lower, s_lower, v_lower])
                colour['UPPER'] = np.array([h_upper, s_upper, v_upper])

                ball_tracker.colour_settings.colour_model.update(colour)

    else:
        parser.exit(1, message=f"No such image file: {args.image}")

    cv2.destroyAllWindows()
