import argparse
import sys

from PyQt5.QtWidgets import QApplication

from snooker_ball_tracker.views import MainView


class GUI():

    def create_parser(self) -> argparse.ArgumentParser:
        """Create GUI argument parser

        :return: GUI argument parser
        :rtype: argparse.ArgumentParser
        """
        parser = argparse.ArgumentParser(description="Ball Tracker Video GUI (Only works with videos)")
        parser.add_argument("-s", "--settings", dest="settings_file", default=None,
                            help="Load settings from JSON file")
        parser.add_argument("-v", "--video", dest="video", default=None,
                            help="Video file to process")
        return parser

    def run(self, args: argparse.Namespace):
        """Run the GUI app

        :param args: args parsed from GUI parser
        :type args: argparse.Namespace
        """
        app = QApplication([])
        window = MainView(args)
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":

    gui = GUI()
    parser = gui.create_parser()
    args = parser.parse_args()
    gui.run(args)
