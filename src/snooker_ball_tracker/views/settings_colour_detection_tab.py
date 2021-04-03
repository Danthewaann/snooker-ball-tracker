import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import snooker_ball_tracker.settings as s

from collections import OrderedDict
from snooker_ball_tracker.models.settings.colour_detection import ColourDetectionTabModel
from snooker_ball_tracker.models.observer import Observer
from .components.slider import Ui_Slider
from .components.line import Ui_Line
from .components.label import Ui_Label
from .components.combobox import Ui_Combobox
from .components.radiobutton import Ui_RadioButton
from .components.pushbutton import Ui_PushButton


class Ui_ColourDetectionTab(QtWidgets.QWidget):
    def __init__(self, model: ColourDetectionTabModel):
        super().__init__()
        self.model = model

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        self._label_policy = (QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

        self.option_bar = {
            "detectColour_label": Ui_Label("Detect Colour", self, width=(50, 100), objectName="detectColour_label"),
            "detectColour_combobox": Ui_Combobox(self, items=["None"] + [key.lower() for key in s.COLOURS.keys()], objectName="detectColour_combobox"),
            "showMask_label": Ui_Label("Show Mask", self, width=(50, 100), objectName="showMask_label", alignment=QtCore.Qt.AlignCenter),
            "showMask_yradio": Ui_RadioButton("Yes", value=True, parent=self, objectName="showMask_yradio"),
            "showMask_nradio": Ui_RadioButton("No", value=False, parent=self, checked=True, objectName="showMask_nradio"),
            "reset_btn": Ui_PushButton("Reset", parent=self, objectName="reset_btn")
        }

        self.slider_names = ["Hue", "Saturation", "Value"]

        self.range_labels = {
            "lower": Ui_Label("Lower Range", self, alignment=QtCore.Qt.AlignCenter, sizePolicy=self._label_policy),
            "upper": Ui_Label("Upper Range", self, alignment=QtCore.Qt.AlignCenter, sizePolicy=self._label_policy)
        }

        self.range_sliders = {
            name: self._create_range_slider(name) for name in self.slider_names
        }

        self.range_slider_obeservers = {
            name: { 
                "l_slider": Observer([
                    (self.range_sliders[name]["l_value"], "text"), 
                    (self.range_sliders[name]["l_slider"], "value"), 
                    (self.model.colour_model, "l_"+name)
                ]), 
                "u_slider": Observer([
                    (self.range_sliders[name]["u_value"], "text"), 
                    (self.range_sliders[name]["u_slider"], "value"), 
                    (self.model.colour_model, "u_"+name)
                ]) 
            } for name in self.slider_names
        }

        self.colour_combobox_observer = Observer([(self.option_bar["detectColour_combobox"], "currentText"), (self.model, "selected_colour")])

        self.layout.addWidget(Ui_Line(self),                            0, 0, 1, 9)
        self.layout.addWidget(self.option_bar["detectColour_label"],    1, 0, 1, 1)
        self.layout.addWidget(self.option_bar["detectColour_combobox"], 1, 1, 1, 3)
        self.layout.addWidget(self.option_bar["showMask_label"],        1, 4, 1, 1)
        self.layout.addWidget(self.option_bar["showMask_yradio"],       1, 5, 1, 1)
        self.layout.addWidget(self.option_bar["showMask_nradio"],       1, 6, 1, 1)
        self.layout.addWidget(self.option_bar["reset_btn"],             1, 8, 1, 1)
        self.layout.addWidget(Ui_Line(self),                            2, 0, 1, 9)
        
        self.layout.addWidget(self.range_labels["lower"], 3, 2, 1, 3)
        self.layout.addWidget(self.range_labels["upper"], 3, 6, 1, 3)

        _row_index = 4
        for range_slider in self.range_sliders.values():
            self.toggle_range_slider(range_slider, False)

            self.layout.addWidget(range_slider["label"],    _row_index, 0, 1, 1, alignment=QtCore.Qt.AlignRight)
            self.layout.addWidget(range_slider["l_value"],  _row_index, 1, 1, 1)
            self.layout.addWidget(range_slider["l_slider"], _row_index, 2, 1, 3)
            self.layout.addWidget(range_slider["u_value"],  _row_index, 5, 1, 1)
            self.layout.addWidget(range_slider["u_slider"], _row_index, 6, 1, 3)
            _row_index += 1

        QtCore.QMetaObject.connectSlotsByName(self)

    def _create_range_slider(self, name):
        return {
            "label": Ui_Label(name, parent=self, sizePolicy=self._label_policy),
            "l_value": Ui_Label("0", parent=self, width=(50, 100), objectName=name+"_l_value", sizePolicy=self._label_policy, alignment=QtCore.Qt.AlignCenter),
            "l_slider": Ui_Slider(255, parent=self, name=name, objectName=name+"_l_slider", sizePolicy=self._label_policy),
            "u_value": Ui_Label("0", parent=self, width=(50, 100), objectName=name+"_u_value", sizePolicy=self._label_policy, alignment=QtCore.Qt.AlignCenter),
            "u_slider": Ui_Slider(255, parent=self, name=name, objectName=name+"_u_slider", sizePolicy=self._label_policy)
        }

    def toggle_range_sliders(self, enable=True):
        for range_slider in self.range_sliders.values(): self.toggle_range_slider(range_slider, enable)

    def toggle_range_slider(self, range_slider, enable=True):
        for key in range_slider: range_slider[key].setEnabled(enable)

    @QtCore.pyqtSlot("QString")
    def on_detectColour_combobox_currentTextChanged(self, colour):
        self.toggle_range_sliders(True if colour != "None" else False)
            
    @QtCore.pyqtSlot()
    def on_reset_btn_pressed(self):
        self.model.reset()
