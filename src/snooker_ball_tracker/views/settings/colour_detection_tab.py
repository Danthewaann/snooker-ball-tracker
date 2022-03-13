import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

from snooker_ball_tracker.ball_tracker import ColourDetectionSettings
from snooker_ball_tracker.enums import SnookerColour
from snooker_ball_tracker.observer import Observer

from ..components import (
    Ui_Combobox,
    Ui_Label,
    Ui_Line,
    Ui_PushButton,
    Ui_RadioButton,
    Ui_Slider,
)


class ColourDetectionTab(QtWidgets.QWidget):
    def __init__(self, colour_settings: ColourDetectionSettings):
        super().__init__()
        self.colour_settings = colour_settings
        self.slider_names = ["Hue", "Saturation", "Value"]

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(20)

        self._label_policy = (
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed,
        )

        self.option_bar_widgets = {
            "detectColour_label": Ui_Label(
                "Detect Colour", self, objectName="detectColour_label"
            ),
            "detectColour_combobox": Ui_Combobox(
                self,
                items=["None"]
                + [colour[0].upper() + colour[1:].lower() for colour in SnookerColour],
                objectName="detectColour_combobox",
            ),
            "showMask_label": Ui_Label(
                "Show Mask",
                self,
                objectName="showMask_label",
                alignment=QtCore.Qt.AlignCenter,
            ),
            "showMask_yradio": Ui_RadioButton(
                "Yes", value=True, parent=self, objectName="showMask_yradio"
            ),
            "showMask_nradio": Ui_RadioButton(
                "No",
                value=False,
                parent=self,
                checked=True,
                objectName="showMask_nradio",
            ),
            "reset_btn": Ui_PushButton("Reset", parent=self, objectName="reset_btn"),
        }

        self.range_label_widgets = {
            "lower": Ui_Label(
                "Lower Range",
                self,
                alignment=QtCore.Qt.AlignCenter,
                sizePolicy=self._label_policy,
            ),
            "upper": Ui_Label(
                "Upper Range",
                self,
                alignment=QtCore.Qt.AlignCenter,
                sizePolicy=self._label_policy,
            ),
        }

        self.range_slider_widgets = {
            name: self._create_range_slider_widget(name) for name in self.slider_names
        }

        self.observers = [
            Observer(
                [
                    (self.option_bar_widgets["detectColour_combobox"], "currentText"),
                    (self.colour_settings, "selected_colour"),
                ]
            ),
            Observer(
                [
                    (self.option_bar_widgets["showMask_yradio"], "state"),
                    (self.option_bar_widgets["showMask_nradio"], "state"),
                    (self.colour_settings, "colour_mask"),
                ]
            ),
            [
                (
                    Observer(
                        [
                            (self.range_slider_widgets[name]["l_value"], "text"),
                            (self.range_slider_widgets[name]["l_slider"], "value"),
                            (self.colour_settings.colour_model, "l_" + name),
                        ]
                    ),
                    Observer(
                        [
                            (self.range_slider_widgets[name]["u_value"], "text"),
                            (self.range_slider_widgets[name]["u_slider"], "value"),
                            (self.colour_settings.colour_model, "u_" + name),
                        ]
                    ),
                )
                for name in self.slider_names
            ],
        ]

        self.layout.addWidget(Ui_Line(self), 0, 0, 1, 9)
        self.layout.addWidget(self.option_bar_widgets["detectColour_label"], 1, 0, 1, 1)
        self.layout.addWidget(
            self.option_bar_widgets["detectColour_combobox"], 1, 1, 1, 3
        )
        self.layout.addWidget(
            self.option_bar_widgets["showMask_label"],
            1,
            4,
            1,
            1,
        )
        self.layout.addWidget(self.option_bar_widgets["showMask_yradio"], 1, 5, 1, 1)
        self.layout.addWidget(self.option_bar_widgets["showMask_nradio"], 1, 6, 1, 1)
        self.layout.addWidget(self.option_bar_widgets["reset_btn"], 1, 8, 1, 1)
        self.layout.addWidget(Ui_Line(self), 2, 0, 1, 9)

        self.layout.addWidget(self.range_label_widgets["lower"], 3, 2, 1, 3)
        self.layout.addWidget(self.range_label_widgets["upper"], 3, 6, 1, 3)

        _row_index = 4
        for range_slider in self.range_slider_widgets.values():
            self.layout.addWidget(
                range_slider["label"],
                _row_index,
                0,
                1,
                1,
                alignment=QtCore.Qt.AlignRight,
            )
            self.layout.addWidget(range_slider["l_value"], _row_index, 1, 1, 1)
            self.layout.addWidget(range_slider["l_slider"], _row_index, 2, 1, 3)
            self.layout.addWidget(range_slider["u_value"], _row_index, 5, 1, 1)
            self.layout.addWidget(range_slider["u_slider"], _row_index, 6, 1, 3)
            _row_index += 1

        self.toggle_colour_widgets()

        QtCore.QMetaObject.connectSlotsByName(self)

    def _create_range_slider_widget(self, name):
        return {
            "label": Ui_Label(name, parent=self, sizePolicy=self._label_policy),
            "l_value": Ui_Label(
                "0",
                parent=self,
                objectName=name + "_l_value",
                sizePolicy=self._label_policy,
                width=(50, 50),
                alignment=QtCore.Qt.AlignCenter,
            ),
            "l_slider": Ui_Slider(
                255,
                parent=self,
                name=name,
                objectName=name + "_l_slider",
                sizePolicy=self._label_policy,
            ),
            "u_value": Ui_Label(
                "0",
                parent=self,
                objectName=name + "_u_value",
                sizePolicy=self._label_policy,
                alignment=QtCore.Qt.AlignCenter,
            ),
            "u_slider": Ui_Slider(
                255,
                parent=self,
                name=name,
                objectName=name + "_u_slider",
                sizePolicy=self._label_policy,
            ),
        }

    @QtCore.pyqtSlot("QString", name="on_detectColour_combobox_currentTextChanged")
    def toggle_colour_widgets(self, colour="None"):
        enable_widgets = True if colour != "None" else False

        for range_slider_widget in self.range_slider_widgets.values():
            for widget in range_slider_widget.values():
                widget.setEnabled(enable_widgets)

        self.option_bar_widgets["showMask_yradio"].setEnabled(enable_widgets)
        self.option_bar_widgets["showMask_nradio"].setEnabled(enable_widgets)

    @QtCore.pyqtSlot()
    def on_reset_btn_pressed(self):
        self.colour_settings.reset()
