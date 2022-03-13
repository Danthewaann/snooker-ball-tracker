from collections import OrderedDict

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker import (
    BallDetectionSettingGroup,
    BallDetectionSettings,
)
from snooker_ball_tracker.observer import Observer

from ..components import Ui_Label, Ui_PushButton, Ui_RadioButton, Ui_Slider


class BallDetectionTab(QtWidgets.QWidget):
    def __init__(self, ball_settings: BallDetectionSettings):
        super().__init__()
        self.ball_settings = ball_settings

        self.layout = QtWidgets.QGridLayout(self)

        self.setting_group_widgets = OrderedDict(
            [
                (
                    "convexity",
                    BallDetectionSettingView(
                        "Convexity", self.ball_settings.groups["convexity"]
                    ),
                ),
                (
                    "inertia",
                    BallDetectionSettingView(
                        "Inertia", self.ball_settings.groups["inertia"]
                    ),
                ),
                (
                    "circularity",
                    BallDetectionSettingView(
                        "Circularity", self.ball_settings.groups["circularity"]
                    ),
                ),
                (
                    "area",
                    BallDetectionSettingView(
                        "Area", self.ball_settings.groups["area"], max_range=2000
                    ),
                ),
            ]
        )

        self.layout.addWidget(self.setting_group_widgets["convexity"], 0, 0)
        self.layout.addWidget(self.setting_group_widgets["inertia"], 0, 1)
        self.layout.addWidget(self.setting_group_widgets["circularity"], 1, 0)
        self.layout.addWidget(self.setting_group_widgets["area"], 1, 1)


class BallDetectionSettingView(QtWidgets.QGroupBox):
    def __init__(self, name, settings: BallDetectionSettingGroup, max_range=100):
        super().__init__(name)
        self.settings = settings

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(20)

        self.widgets = {
            "filterBy_label": Ui_Label(
                "Filter By", self, alignment=QtCore.Qt.AlignCenter
            ),
            "filterBy_yradio": Ui_RadioButton("Yes", value=True, parent=self),
            "filterBy_nradio": Ui_RadioButton(
                "No", value=False, checked=True, parent=self
            ),
            "minVal_label": Ui_Label(
                "Min Value",
                self,
                alignment=QtCore.Qt.AlignCenter,
                sizePolicy=(
                    QtWidgets.QSizePolicy.Fixed,
                    QtWidgets.QSizePolicy.Preferred,
                ),
            ),
            "minVal_value": Ui_Label(
                "0",
                self,
                alignment=QtCore.Qt.AlignCenter,
                sizePolicy=(
                    QtWidgets.QSizePolicy.Expanding,
                    QtWidgets.QSizePolicy.Expanding,
                ),
            ),
            "minVal_slider": Ui_Slider(
                max_range=max_range, parent=self, objectName="minVal_slider"
            ),
            "maxVal_label": Ui_Label(
                "Max Value",
                self,
                alignment=QtCore.Qt.AlignCenter,
                sizePolicy=(
                    QtWidgets.QSizePolicy.Fixed,
                    QtWidgets.QSizePolicy.Preferred,
                ),
            ),
            "maxVal_value": Ui_Label(
                "0",
                self,
                alignment=QtCore.Qt.AlignCenter,
                sizePolicy=(
                    QtWidgets.QSizePolicy.Expanding,
                    QtWidgets.QSizePolicy.Expanding,
                ),
            ),
            "maxVal_slider": Ui_Slider(
                max_range=max_range, parent=self, objectName="maxVal_slider"
            ),
            "reset_btn": Ui_PushButton("Reset", self, objectName="reset_btn"),
        }

        self.layout.addWidget(self.widgets["filterBy_label"], 0, 0, 1, 1)
        self.layout.addWidget(self.widgets["filterBy_yradio"], 0, 2, 1, 1)
        self.layout.addWidget(self.widgets["filterBy_nradio"], 0, 3, 1, 1)
        self.layout.addWidget(self.widgets["minVal_label"], 1, 0, 1, 1)
        self.layout.addWidget(self.widgets["minVal_value"], 1, 1, 1, 1)
        self.layout.addWidget(self.widgets["minVal_slider"], 1, 2, 1, 2)
        self.layout.addWidget(self.widgets["maxVal_label"], 2, 0, 1, 1)
        self.layout.addWidget(self.widgets["maxVal_value"], 2, 1, 1, 1)
        self.layout.addWidget(self.widgets["maxVal_slider"], 2, 2, 1, 2)
        self.layout.addWidget(
            self.widgets["reset_btn"], 3, 3, 1, 1, alignment=QtCore.Qt.AlignRight
        )

        self.observers = [
            Observer(
                [
                    (self.widgets["filterBy_yradio"], "state", bool),
                    (self.widgets["filterBy_nradio"], "state", bool),
                    (self.settings, "filter_by", bool),
                ]
            ),
            Observer(
                [
                    (self.widgets["minVal_value"], "text", str),
                    (self.widgets["minVal_slider"], "value", int),
                    (self.settings, "min_value", int),
                ]
            ),
            Observer(
                [
                    (self.widgets["maxVal_value"], "text", str),
                    (self.widgets["maxVal_slider"], "value", int),
                    (self.settings, "max_value", int),
                ]
            ),
        ]

        QtCore.QMetaObject.connectSlotsByName(self)
        self.settings.reset()

    @QtCore.pyqtSlot()
    def on_reset_btn_pressed(self):
        self.settings.reset()
