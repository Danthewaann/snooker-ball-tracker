from collections import OrderedDict
from copy import deepcopy

import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s

from .hsv_colour_model import HSVColourModel


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
