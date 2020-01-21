import cv2
import argparse
import requests
import numpy as np
import time
import os
import settings as s
from config import get_setting_modules
from ball_tracker import BallTracker


# dummy callback method for trackbar
def nothing(x):
    pass


def pick_color(event, x_pos, y_pos, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        pixel = hsv[y_pos, x_pos]
        upper = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

        colour['LOWER'] = lower
        colour['UPPER'] = upper

        cv2.setTrackbarPos('H (lower)', window_title, colour['LOWER'][0])
        cv2.setTrackbarPos('H (upper)', window_title, colour['UPPER'][0])
        cv2.setTrackbarPos('S (lower)', window_title, colour['LOWER'][1])
        cv2.setTrackbarPos('S (upper)', window_title, colour['UPPER'][1])
        cv2.setTrackbarPos('V (lower)', window_title, colour['LOWER'][2])
        cv2.setTrackbarPos('V (upper)', window_title, colour['UPPER'][2])


if __name__ == '__main__':
    global hsv, frame

    parser = argparse.ArgumentParser(description='Ball detection and tracking process')
    parser.add_argument('-l', '--live', metavar='live', dest='live', default=None,
                        help='IP address of live video stream to detect and track balls from')
    parser.add_argument('-v', '--video', metavar='video', dest='video', default=None,
                        help='Pre-recorded video file to detect and track balls from')
    parser.add_argument('-i', '--image', metavar='img', dest='image', default=None,
                        help='Image file to detect and track balls from')
    parser.add_argument('--width', dest='width', default=800, type=int,
                        help='Set width of image for processing, defaults to "%(default)s" pixels')
    parser.add_argument('--show-threshold', dest='show_threshold', action='store_true', default=False,
                        help='Show thresholded frames')
    parser.add_argument('--detect-colour', dest='detect_colour', default=None, 
                        type=str.upper, choices=s.COLOURS.keys(),
                        help='Detect contours matching provided colour')
    parser.add_argument('--crop', dest='crop', action='store_true', default=False,
                        help='Crop video/image around detected table boundaries')
    parser.add_argument('--morph', dest='morph', action='store_true', default=False,
                        help='Perform morph closing morphology on processed frames')
    parser.add_argument('--settings', dest='settings', default='default_settings',
                        type=str.lower, choices=get_setting_modules(),
                        help='Settings file to use, defaults to "%(default)s"')
    args = parser.parse_args()

    print('==============')
    print('USER CONTROLS:')
    print('s -> save current frame to a jpg file')
    print('q -> exit the program')
    print('p -> pause/resume video/live footage')
    print('waiting for user input...\n')

    if args.live or args.video or args.image:
        s.settings_module_name = args.settings
        s.load()
        is_playing = True
        ball_tracker = BallTracker()
        colour = {
            'LOWER': np.array([0, 0, 0]),
            'UPPER': np.array([0, 0, 0])
        }

        # create main ball tracker window
        window_title = 'Snooker Ball Tracker'
        cv2.namedWindow(window_title)

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

        if args.detect_colour is not None:
            colour = {
                'LOWER': s.COLOURS[args.detect_colour]['LOWER'],
                'UPPER': s.COLOURS[args.detect_colour]['UPPER']
            }

            cv2.setTrackbarPos('H (lower)', window_title, colour['LOWER'][0])
            cv2.setTrackbarPos('H (upper)', window_title, colour['UPPER'][0])
            cv2.setTrackbarPos('S (lower)', window_title, colour['LOWER'][1])
            cv2.setTrackbarPos('S (upper)', window_title, colour['UPPER'][1])
            cv2.setTrackbarPos('V (lower)', window_title, colour['LOWER'][2])
            cv2.setTrackbarPos('V (upper)', window_title, colour['UPPER'][2])

        if args.live is not None:
            # main video capture loop
            ball_tracker.update_boundary = True
            while True:
                if is_playing:
                    try:
                        im_resp = requests.get('http://{}/shot.jpg'.format(args.live))
                        im_arr = np.array(bytearray(im_resp.content), dtype=np.uint8)
                        frame = cv2.imdecode(im_arr, -1)

                        if args.detect_colour is None:
                            frame, _, _ = ball_tracker.run(frame, width=args.width, crop=args.crop,
                                                           morph=args.morph, show_threshold=args.show_threshold)

                            cv2.imshow(window_title, frame)
                    except requests.ConnectionError:
                        print('Cannot connect to {}'.format(ip))
                        break

                # obtain trackbar values and use them for --detect-colour
                if args.detect_colour is not None:
                    frame, _, hsv = ball_tracker.perform_init_ops(frame, width=args.width,
                                                                  morph=args.morph, crop=args.crop)
                    colour_mask, contours = ball_tracker.detect_colour(
                        hsv, colour['LOWER'], colour['UPPER']
                    )
                    res = cv2.bitwise_and(frame, frame, mask=colour_mask)
                    cv2.drawContours(res, contours, -1, (0, 255, 0), 2)
                    cv2.imshow(window_title, res)

                key = cv2.waitKey(1) & 0xFF

                # if the 'q' key is pressed, stop the loop
                if key == ord('q'):
                    print('exiting...')
                    break

                # if the 's' key is pressed, save current frame to file
                if key == ord('s'):
                    file_name = os.path.join(os.path.dirname(args.video), 
                                             os.path.splitext(os.path.basename(args.video))[0])
                    frame_name = file_name + '-frame-' + str(ball_tracker.get_frame_counter()) + '.jpg'
                    print('saving frame to ' + frame_name)
                    cv2.imwrite(frame_name, frame)

                # if the 'p' key is pressed, pause/play the recording
                if key == ord('p'):
                    if is_playing:
                        print('video paused...')
                        is_playing = False
                    else:
                        print('video resumed...')
                        is_playing = True

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

        elif args.video is not None:
            ball_tracker.update_boundary = True
            cap = cv2.VideoCapture(args.video)

            # make sure provided video stream or file is loaded
            if not cap.isOpened():
                print('Error opening video stream or file')

            # main video capture loop
            while cap.isOpened():
                if is_playing:
                    ret, frame = cap.read()
                    # if we successfully read a frame, process it
                    if ret:
                        if args.detect_colour is None:
                            frame, _, _ = ball_tracker.run(frame, width=args.width, crop=args.crop,
                                                           morph=args.morph, show_threshold=args.show_threshold)
                            cv2.imshow(window_title, frame)

                # obtain trackbar values and use them for --detect-colour
                if args.detect_colour is not None:
                    frame, _, hsv = ball_tracker.perform_init_ops(frame, width=args.width,
                                                                  morph=args.morph, crop=args.crop)
                    colour_mask, contours = ball_tracker.detect_colour(
                        hsv, colour['LOWER'], colour['UPPER']
                    )
                    res = cv2.bitwise_and(frame, frame, mask=colour_mask)
                    cv2.drawContours(res, contours, -1, (0, 255, 0), 2)
                    cv2.imshow(window_title, res)

                key = cv2.waitKey(1) & 0xFF

                # if the 'q' key is pressed, stop the loop
                if key == ord('q'):
                    print('exiting...')
                    break

                # if the 's' key is pressed, save current frame to file
                if key == ord('s'):
                    file_name = os.path.join(os.path.dirname(args.video), 
                                             os.path.splitext(os.path.basename(args.video))[0])
                    frame_name = file_name + '-frame-' + str(ball_tracker.get_frame_counter()) + '.jpg'
                    print('saving frame to ' + frame_name)
                    cv2.imwrite(frame_name, frame)

                # if the 'p' key is pressed, pause/play the recording
                if key == ord('p'):
                    if is_playing:
                        print('video paused...')
                        is_playing = False
                    else:
                        print('video resumed...')
                        is_playing = True

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

            cap.release()

        elif args.image is not None:
            # read in image provided from -i/--image
            ball_tracker.update_boundary = True
            frame = cv2.imread(args.image)

            if args.detect_colour is None:
                # detect balls in provided image
                _, _, hsv = ball_tracker.perform_init_ops(frame, width=args.width, morph=args.morph, crop=args.crop)
                frame, _, _ = ball_tracker.run(frame, width=args.width, crop=args.crop,
                                               morph=args.morph, show_threshold=args.show_threshold,
                                               show_fps=False)

            # frame display loop
            while True:
                # extract colours from HSV frame if --detect-colour is provided
                if args.detect_colour:
                    frame, _, hsv = ball_tracker.perform_init_ops(frame, width=args.width, morph=args.morph, crop=args.crop)
                    colour_mask, contours = ball_tracker.detect_colour(
                        hsv, colour['LOWER'], colour['UPPER']
                    )

                    res = cv2.bitwise_and(frame, frame, mask=colour_mask)
                    cv2.drawContours(res, contours, -1, (255, 0, 0), 2)
                    cv2.imshow(window_title, res)
                else:
                    cv2.imshow(window_title, frame)

                # obtain key value if a key was pressed
                key = cv2.waitKey(1) & 0xFF

                # if the 'q' key is pressed, stop the loop
                if key == ord('q'):
                    print('exiting...')
                    break

                # if the 's' key is pressed, save processed frame to file
                if key == ord('s'):
                    counter = 1
                    file_name = os.path.join(os.path.dirname(args.image), 
                                             os.path.splitext(os.path.basename(args.image))[0])
                    while True:
                        frame_name = file_name + '-frame-' + str(counter) + '.jpg'
                        if not os.path.exists(frame_name):
                            print('saving frame to ' + frame_name)
                            cv2.imwrite(frame_name, frame)
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

    else:
        parser.print_help()
        exit(1)

    cv2.destroyAllWindows()
