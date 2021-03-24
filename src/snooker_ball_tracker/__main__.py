import argparse
import sys
from snooker_ball_tracker.views import MainWindow
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import test
# from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
#     QRect, QSize, QUrl, Qt)
# from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
#     QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
#     QRadialGradient)
# from PySide2.QtWidgets import *

class ExampleApp(QMainWindow, test.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", dest="settings_file", default=None, 
                        help="Use settings from JSON file")
    parser.add_argument("--no-splash", dest="splash", action="store_false", default=True, 
                        help="Lanuch GUI without splash screen")

    args = parser.parse_args()
    app = QApplication([])
    window = ExampleApp()
    window.show()
    # window.show()

    sys.exit(app.exec())
