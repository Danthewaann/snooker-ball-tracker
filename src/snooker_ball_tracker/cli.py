from __future__ import annotations

import argparse
import os
from copy import deepcopy
from typing import TYPE_CHECKING, Any

import cv2
import numpy as np

from snooker_ball_tracker.ball_tracker import BallTracker
from snooker_ball_tracker.ball_tracker.util import transform_frame
from snooker_ball_tracker.enums import SnookerColour
from snooker_ball_tracker.settings import settings as s

if TYPE_CHECKING:
    from snooker_ball_tracker.ball_tracker.types import Frame, Image


class CLI:

    image: Image | None = None
    ball_tracker: BallTracker | None = None
    window_title = "Snooker Ball Tracker Image CLI"
    colour: dict[str, Frame] = {
        "LOWER": np.array([0, 0, 0]),
        "UPPER": np.array([0, 0, 0]),
    }

    def create_parser(self) -> argparse.ArgumentParser:
        """Create CLI argument parser

        :return: CLI argument parser
        """
        parser = argparse.ArgumentParser(
            description="Ball Tracker Image CLI (Only works with images)"
        )
        parser.add_argument("image", help="Image file to detect and track balls from")
        parser.add_argument(
            "-s",
            "--settings",
            dest="settings",
            default=os.path.join(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                ),
                "resources",
                "config",
                "default_settings.json",
            ),
            help='Settings file to use, defaults to "%(default)s"',
        )
        parser.add_argument(
            "-w",
            "--width",
            dest="width",
            default=800,
            type=int,
            help='Set width of image for processing, defaults to "%(default)s" pixels',
        )
        parser.add_argument(
            "-d",
            "--detect-colour",
            dest="detect_colour",
            default=None,
            type=str.upper,
            choices=[colour.value for colour in SnookerColour],
            help="Detect contours matching provided colour",
        )
        parser.add_argument(
            "--mask-colour",
            dest="mask_colour",
            action="store_true",
            default=False,
            help="Mask contours of provided colour",
        )
        parser.add_argument(
            "--show-threshold",
            dest="show_threshold",
            action="store_true",
            default=False,
            help="Show thresholded frames",
        )
        parser.add_argument(
            "--morph",
            dest="morph",
            action="store_true",
            default=False,
            help="Perform morph closing morphology on processed frames",
        )
        return parser

    def __pick_color(self, event: int, x_pos: int, y_pos: int, *ignore: Any) -> None:
        """Listens to a left click event on the processed frame to
        extract colour values from pixel located using `x_pos` and `y_pos`

        :param event: event type
        :param x_pos: x position in frame
        :param y_pos: y position in frame
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.image:
                return
            if not self.ball_tracker:
                return

            hsv = self.image.hsv_frame
            pixel = hsv[y_pos, x_pos]
            upper: Frame = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
            lower: Frame = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

            self.colour["LOWER"] = lower
            self.colour["UPPER"] = upper

            self.ball_tracker.colour_settings.colour_model.update(self.colour)

            cv2.setTrackbarPos("H (lower)", self.window_title, self.colour["LOWER"][0])
            cv2.setTrackbarPos("H (upper)", self.window_title, self.colour["UPPER"][0])
            cv2.setTrackbarPos("S (lower)", self.window_title, self.colour["LOWER"][1])
            cv2.setTrackbarPos("S (upper)", self.window_title, self.colour["UPPER"][1])
            cv2.setTrackbarPos("V (lower)", self.window_title, self.colour["LOWER"][2])
            cv2.setTrackbarPos("V (upper)", self.window_title, self.colour["UPPER"][2])

    def run(self, args: argparse.Namespace) -> None:
        """Run the CLI app

        :param args: args parsed from CLI parser
        :raises OSError: if `settings` arg failed to load
        :raises OSError: if `image` arg failed to load
        """
        # load settings from json file
        success, _ = s.load(args.settings)
        if not success:
            raise OSError(f"Failed to load settings file: {args.settings}")

        if os.path.exists(args.image):
            print("=================================")
            print("CLI Arguments:")
            print("=================================")
            for key, value in vars(args).items():
                print(f"{key}: {value}")
            print("=================================")
            print("USER CONTROLS:")
            print("=================================")
            print("s -> save processed frame to a jpg file")
            print("q -> exit the program")
            print("=================================")
            if args.detect_colour is not None:
                print("Click on image to obtain HSV values from selected pixel")
                print(
                    f"This will be used to update colour values for: "
                    f"{args.detect_colour}"
                )
                print("=================================")
            print("waiting for user input...\n")

            # create ball tracker with loaded settings
            self.ball_tracker = BallTracker()

            # create main ball tracker window
            cv2.namedWindow(self.window_title)

            # setup trackbars if --detect-colours in set
            if args.detect_colour is not None:
                self.ball_tracker.colour_settings.selected_colour = args.detect_colour
                colour = {
                    "LOWER": s.COLOUR_DETECTION_SETTINGS["COLOURS"][args.detect_colour][
                        "LOWER"
                    ],
                    "UPPER": s.COLOUR_DETECTION_SETTINGS["COLOURS"][args.detect_colour][
                        "UPPER"
                    ],
                }

                # create trackbars for lower and upper HSV values
                cv2.createTrackbar("H (lower)", self.window_title, 0, 180, lambda x: x)
                cv2.createTrackbar("H (upper)", self.window_title, 0, 180, lambda x: x)
                cv2.createTrackbar("S (lower)", self.window_title, 0, 255, lambda x: x)
                cv2.createTrackbar("S (upper)", self.window_title, 0, 255, lambda x: x)
                cv2.createTrackbar("V (lower)", self.window_title, 0, 255, lambda x: x)
                cv2.createTrackbar("V (upper)", self.window_title, 0, 255, lambda x: x)
                cv2.setTrackbarPos("H (lower)", self.window_title, colour["LOWER"][0])
                cv2.setTrackbarPos("H (upper)", self.window_title, colour["UPPER"][0])
                cv2.setTrackbarPos("S (lower)", self.window_title, colour["LOWER"][1])
                cv2.setTrackbarPos("S (upper)", self.window_title, colour["UPPER"][1])
                cv2.setTrackbarPos("V (lower)", self.window_title, colour["LOWER"][2])
                cv2.setTrackbarPos("V (upper)", self.window_title, colour["UPPER"][2])
                cv2.setMouseCallback(self.window_title, self.__pick_color)

                cv2.setTrackbarPos("H (lower)", self.window_title, colour["LOWER"][0])
                cv2.setTrackbarPos("H (upper)", self.window_title, colour["UPPER"][0])
                cv2.setTrackbarPos("S (lower)", self.window_title, colour["LOWER"][1])
                cv2.setTrackbarPos("S (upper)", self.window_title, colour["UPPER"][1])
                cv2.setTrackbarPos("V (lower)", self.window_title, colour["LOWER"][2])
                cv2.setTrackbarPos("V (upper)", self.window_title, colour["UPPER"][2])

            # read in image provided
            in_frame = cv2.imread(args.image)
            in_frame = transform_frame(in_frame, width=args.width)

            # frame display loop
            while True:
                self.image, _, _ = self.ball_tracker.process_frame(
                    deepcopy(in_frame),
                    show_threshold=args.show_threshold,
                    detect_colour=args.detect_colour,
                    mask_colour=args.mask_colour,
                    perform_morph=args.morph,
                )
                cv2.imshow(self.window_title, self.image.frame)

                # obtain key value if a key was pressed
                pressed_key: int = cv2.waitKey(1) & 0xFF

                # if window is closed, exit program
                if cv2.getWindowProperty(self.window_title, cv2.WND_PROP_VISIBLE) == 0:
                    break

                # if the "q" key is pressed, exit program
                if pressed_key == ord("q"):
                    break

                # if the "s" key is pressed, save processed frame to file
                if pressed_key == ord("s"):
                    counter = 1
                    file_name = os.path.join(
                        os.path.dirname(args.image),
                        os.path.splitext(os.path.basename(args.image))[0],
                    )
                    while True:
                        frame_name = file_name + "-frame-" + str(counter) + ".jpg"
                        if not os.path.exists(frame_name):
                            print("saving frame to " + frame_name)
                            cv2.imwrite(frame_name, self.image.frame)
                            break
                        counter += 1

                # obtain trackbar values and use them for --detect-colour
                if args.detect_colour is not None:
                    h_lower = cv2.getTrackbarPos("H (lower)", self.window_title)
                    h_upper = cv2.getTrackbarPos("H (upper)", self.window_title)
                    s_lower = cv2.getTrackbarPos("S (lower)", self.window_title)
                    s_upper = cv2.getTrackbarPos("S (upper)", self.window_title)
                    v_lower = cv2.getTrackbarPos("V (lower)", self.window_title)
                    v_upper = cv2.getTrackbarPos("V (upper)", self.window_title)

                    colour["LOWER"] = np.array([h_lower, s_lower, v_lower])
                    colour["UPPER"] = np.array([h_upper, s_upper, v_upper])

                    self.ball_tracker.colour_settings.colour_model.update(colour)

        else:
            raise OSError(f"Failed to load image file: {args.image}")


def main() -> None:
    cli = CLI()
    parser = cli.create_parser()
    args = parser.parse_args()
    args.image = os.path.abspath(args.image)
    args.settings = os.path.abspath(args.settings)

    try:
        cli.run(args)
    except OSError as ex:
        parser.exit(1, message=str(ex))
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
