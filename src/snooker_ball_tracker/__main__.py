import argparse
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from snooker_ball_tracker.views import Ui_MainWindow

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", dest="settings_file", default=None, 
                        help="Use settings from JSON file")
    parser.add_argument("--no-splash", dest="splash", action="store_false", default=True, 
                        help="Lanuch GUI without splash screen")

    args = parser.parse_args()
    app = QApplication([])
    window = Ui_MainWindow(args)
    window.show()

    sys.exit(app.exec())
