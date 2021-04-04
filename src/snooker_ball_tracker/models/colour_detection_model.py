from collections import OrderedDict
from copy import deepcopy

import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s


class HSVColourModel(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self._l_Hue = 0
        self._u_Hue = 0 
        self._l_Saturation = 0 
        self._u_Saturation = 0 
        self._l_Value = 0 
        self._u_Value = 0

    @property
    def l_Hue(self):
        return self._l_Hue

    l_HueChanged = QtCore.pyqtSignal(int, name="l_HueChanged")

    @l_Hue.setter
    def l_Hue(self, value):
        self._l_Hue = value
        self.l_HueChanged.emit(self._l_Hue)

    @property
    def u_Hue(self):
        return self._u_Hue

    u_HueChanged = QtCore.pyqtSignal(int, name="u_HueChanged")

    @u_Hue.setter
    def u_Hue(self, value):
        self._u_Hue = value
        self.u_HueChanged.emit(self._u_Hue)

    @property
    def l_Saturation(self):
        return self._l_Saturation

    l_SaturationChanged = QtCore.pyqtSignal(int, name="l_SaturationChanged")

    @l_Saturation.setter
    def l_Saturation(self, value):
        self._l_Saturation = value
        self.l_SaturationChanged.emit(self._l_Saturation)

    @property
    def u_Saturation(self):
        return self._u_Saturation

    u_SaturationChanged = QtCore.pyqtSignal(int, name="u_SaturationChanged")

    @u_Saturation.setter
    def u_Saturation(self, value):
        self._u_Saturation = value
        self.u_SaturationChanged.emit(self._u_Saturation)

    @property
    def l_Value(self):
        return self._l_Value

    l_ValueChanged = QtCore.pyqtSignal(int, name="l_ValueChanged")

    @l_Value.setter
    def l_Value(self, value):
        self._l_Value = value
        self.l_ValueChanged.emit(self._l_Value)

    @property
    def u_Value(self):
        return self._u_Value

    u_ValueChanged = QtCore.pyqtSignal(int, name="u_ValueChanged")

    @u_Value.setter
    def u_Value(self, value):
        self._u_Value = value
        self.u_ValueChanged.emit(self._u_Value)

    def update(self, colour):
        self.l_Hue = colour["LOWER"][0]
        self.l_Saturation = colour["LOWER"][1]
        self.l_Value = colour["LOWER"][2]
        self.u_Hue = colour["UPPER"][0]
        self.u_Saturation = colour["UPPER"][1]
        self.u_Value = colour["UPPER"][2]

    def clear(self):
        self.l_Hue = 0
        self.u_Hue = 0
        self.l_Saturation = 0
        self.u_Saturation = 0
        self.l_Value = 0
        self.u_Value = 0


class ColourDetectionTabModel(QtCore.QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._colours = deepcopy(s.COLOURS)
        self._colour_model = HSVColourModel()
        self._colour_mask = False
        self._selected_colour = "NONE"

    @property
    def colours(self):
        return self._colours

    @property
    def colour_model(self):
        return self._colour_model

    @property
    def colour_mask(self):
        return self._colour_mask

    colour_maskChanged = QtCore.pyqtSignal(bool)

    @colour_mask.setter
    def colour_mask(self, value):
        self._colour_mask = value
        self.colour_maskChanged.emit(self._colour_mask)

    @property
    def selected_colour(self):
        return self._selected_colour

    selected_colourChanged = QtCore.pyqtSignal(str)

    @selected_colour.setter
    def selected_colour(self, value):
        value = value.upper()
        if self._selected_colour != "NONE":
            self.update_colour()

        if value != "NONE":
            self._colour_model.update(self._colours[value])
        else:
            self._colour_model.clear()

        self._selected_colour = value
        self.selected_colourChanged.emit(self._selected_colour)

    def update_colour(self):
        self._colours[self._selected_colour]["LOWER"][0] = self._colour_model.l_Hue
        self._colours[self._selected_colour]["LOWER"][1] = self._colour_model.l_Saturation
        self._colours[self._selected_colour]["LOWER"][2] = self._colour_model.l_Value
        self._colours[self._selected_colour]["UPPER"][0] = self._colour_model.u_Hue
        self._colours[self._selected_colour]["UPPER"][1] = self._colour_model.u_Saturation
        self._colours[self._selected_colour]["UPPER"][2] = self._colour_model.u_Value

    def reset(self):
        if self._selected_colour != "NONE":
            self._colours[self._selected_colour]["LOWER"][0] = s.COLOURS[self._selected_colour]["LOWER"][0]
            self._colours[self._selected_colour]["LOWER"][1] = s.COLOURS[self._selected_colour]["LOWER"][1]
            self._colours[self._selected_colour]["LOWER"][2] = s.COLOURS[self._selected_colour]["LOWER"][2]
            self._colours[self._selected_colour]["UPPER"][0] = s.COLOURS[self._selected_colour]["UPPER"][0]
            self._colours[self._selected_colour]["UPPER"][1] = s.COLOURS[self._selected_colour]["UPPER"][1]
            self._colours[self._selected_colour]["UPPER"][2] = s.COLOURS[self._selected_colour]["UPPER"][2]
            self._colour_model.update(self._colours[self._selected_colour])
