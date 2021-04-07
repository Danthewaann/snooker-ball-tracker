from collections import OrderedDict

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import snooker_ball_tracker.settings as s
from snooker_ball_tracker.ball_tracker import Observer
from snooker_ball_tracker.ball_tracker.settings import (
    BallDetectionSettingGroup, BallDetectionSettings)

from ..components import Ui_Label, Ui_PushButton, Ui_RadioButton, Ui_Slider


class BallDetectionTab(QtWidgets.QWidget):
    def __init__(self, model: BallDetectionSettings):
        super().__init__()
        self.model = model

        self.layout = QtWidgets.QGridLayout(self)

        self.setting_group_widgets = OrderedDict([
            ("convexity", BallDetectionSettingView("Convexity", self.model.models["convexity"])),
            ("inertia", BallDetectionSettingView("Inertia", self.model.models["inertia"])),
            ("circularity", BallDetectionSettingView("Circularity", self.model.models["circularity"])),
            ("area", BallDetectionSettingView("Area", self.model.models["area"], max_range=2000)),
        ])

        self.layout.addWidget(self.setting_group_widgets["convexity"], 0, 0)
        self.layout.addWidget(self.setting_group_widgets["inertia"], 0, 1)
        self.layout.addWidget(self.setting_group_widgets["circularity"], 1, 0)
        self.layout.addWidget(self.setting_group_widgets["area"], 1, 1)


class BallDetectionSettingView(QtWidgets.QGroupBox):
    def __init__(self, name, model: BallDetectionSettingGroup, max_range=100):
        super().__init__(name)
        self.model = model

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.widgets = {
            "filterBy_label": Ui_Label("Filter By", self, width=(120, 120), alignment=QtCore.Qt.AlignCenter),
            "filterBy_yradio": Ui_RadioButton("Yes", value=True, parent=self, width=(50, 50)),
            "filterBy_nradio": Ui_RadioButton("No", value=False, checked=True, parent=self, width=(50, 50)),
            "minVal_label": Ui_Label("Minimum Value", self, width=(120, 120), alignment=QtCore.Qt.AlignCenter, 
                                     sizePolicy=(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)),
            "minVal_value": Ui_Label("0", self, alignment=QtCore.Qt.AlignCenter, width=(50, 50),
                              sizePolicy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)),
            "minVal_slider": Ui_Slider(max_range=max_range, parent=self, objectName="minVal_slider"),
            "maxVal_label": Ui_Label("Maximum Value", self, width=(120, 120), alignment=QtCore.Qt.AlignCenter, 
                                   sizePolicy=(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)),
            "maxVal_value": Ui_Label("0", self, alignment=QtCore.Qt.AlignCenter, width=(50, 50),
                            sizePolicy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)),
            "maxVal_slider": Ui_Slider(max_range=max_range, parent=self, objectName="maxVal_slider"),
            "reset_btn": Ui_PushButton("Reset", self, width=(0, 100), objectName="reset_btn")
        }

        self.layout.addWidget(self.widgets["filterBy_label"],  0, 0, 1, 1)
        self.layout.addWidget(self.widgets["filterBy_yradio"], 0, 2, 1, 1)
        self.layout.addWidget(self.widgets["filterBy_nradio"], 0, 3, 1, 1)
        self.layout.addWidget(self.widgets["minVal_label"],    1, 0, 1, 1)
        self.layout.addWidget(self.widgets["minVal_value"],    1, 1, 1, 1)
        self.layout.addWidget(self.widgets["minVal_slider"],   1, 2, 1, 2)
        self.layout.addWidget(self.widgets["maxVal_label"],    2, 0, 1, 1)
        self.layout.addWidget(self.widgets["maxVal_value"],    2, 1, 1, 1)
        self.layout.addWidget(self.widgets["maxVal_slider"],   2, 2, 1, 2)
        self.layout.addWidget(self.widgets["reset_btn"],       3, 3, 1, 1, alignment=QtCore.Qt.AlignRight)

        self.observers = [
            Observer([
                (self.widgets["filterBy_yradio"], "state"), 
                (self.widgets["filterBy_nradio"], "state"),
                (self.model, "filter_by")
            ]),
            Observer([
                (self.widgets["minVal_value"], "text"),
                (self.widgets["minVal_slider"], "value"),
                (self.model, "min_value")
            ]),
            Observer([
                (self.widgets["maxVal_value"], "text"),
                (self.widgets["maxVal_slider"], "value"),
                (self.model, "max_value")
            ])
        ]
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.model.reset()

    @QtCore.pyqtSlot()
    def on_reset_btn_pressed(self):
        self.model.reset()
