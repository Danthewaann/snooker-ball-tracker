from __future__ import annotations

import argparse
import pathlib
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from snooker_ball_tracker.utils import IS_FROZEN
from snooker_ball_tracker.views import MainView


class GUI:
    def __init__(self) -> None:
        if IS_FROZEN:
            self.icon_path = str(
                pathlib.Path(pathlib.Path(sys.executable).parent / "icon.ico").resolve()
            )
            self.default_settings_path = str(
                pathlib.Path(
                    pathlib.Path(sys.executable).parent / "default_settings.json"
                ).resolve()
            )
        else:
            self.icon_path = str(
                pathlib.Path(
                    pathlib.Path(__file__).parent / "resources" / "icon.ico"
                ).resolve()
            )
            self.default_settings_path = str(
                pathlib.Path(
                    pathlib.Path(__file__).parent
                    / "resources"
                    / "default_settings.json"
                ).resolve()
            )

    def create_parser(self) -> argparse.ArgumentParser:
        """Create GUI argument parser

        :return: GUI argument parser
        """
        parser = argparse.ArgumentParser(
            description="Ball Tracker Video GUI (Only works with videos)"
        )
        parser.add_argument(
            "-s",
            "--settings",
            dest="settings_file",
            default=self.default_settings_path,
            help="Load settings from JSON file, defaults to %(default)s",
        )
        parser.add_argument(
            "-v", "--video", dest="video", default=None, help="Video file to process"
        )
        return parser

    def run(self, args: argparse.Namespace) -> None:
        """Run the GUI app

        :param args: args parsed from GUI parser
        """
        app = QApplication([])
        icon = QtGui.QIcon(self.icon_path)
        window = MainView(args, icon)
        window.show()
        sys.exit(app.exec())


def main() -> None:
    gui = GUI()
    parser = gui.create_parser()
    args = parser.parse_args()
    gui.run(args)


if __name__ == "__main__":
    main()
