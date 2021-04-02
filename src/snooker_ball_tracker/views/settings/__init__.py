import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import snooker_ball_tracker.settings as s

from .colour_detection import Ui_ColourDetectionTab
from .ball_detection import Ui_BallDetectionTab
from snooker_ball_tracker.models.settings.ball_detection import BallDetectionTabModel
from snooker_ball_tracker.models.settings.colour_detection import ColourDetectionTabModel

def wrap_pyqtSlot(func, name):
    
    # @QtCore.pyqtSlot(int, name=f"on_{name}_l_slider_valueChanged")
    @QtCore.pyqtSlot(int, name=f"on_{name}_u_slider_valueChanged")
    def wrapper(*args, **kw):
        func(*args, **kw)
    # for name in names:
    #     wrapper = QtCore.pyqtSlot(wrapper, int, name=f"on_{name}_u_slider_valueChanged")
    return wrapper

class Ui_Settings(QtWidgets.QGroupBox):
    def __init__(self):
        super().__init__("Settings")
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.settings_tabs = QtWidgets.QTabWidget(self)
        self.settings_tabs.setMaximumWidth(700)

        self.colour_detection_tab = Ui_ColourDetectionTab(ColourDetectionTabModel())
        self.settings_tabs.addTab(self.colour_detection_tab, "Colour Detection")
        self.settings_tabs.addTab(Ui_BallDetectionTab(BallDetectionTabModel()), "Ball Detection")
        self.layout.addWidget(self.settings_tabs)