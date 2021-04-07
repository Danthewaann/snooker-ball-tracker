from collections import OrderedDict
from copy import deepcopy

import PyQt5.QtCore as QtCore
import snooker_ball_tracker.settings as s

from .hsv_colour import HSVColourModel


class ColourDetectionTabModel(QtCore.QObject):
    def __init__(self):
        """Creates and instance of this class that contains colour detection
        properties used by the ball tracker"""
        super().__init__()
        self._colours = deepcopy(s.COLOURS)
        self._colour_model = HSVColourModel()
        self._colour_mask = False
        self._selected_colour = "NONE"

    @property
    def colours(self) -> dict:
        """Copy of colour values loaded from settings

        :return: colours
        :rtype: dict
        """
        return self._colours

    @colours.setter
    def colours(self, value: dict):
        """Colours setter

        :param value: value to set
        :type value: dict
        """
        self._colours = value
        if self._selected_colour != "NONE":
            self.colour_model.update(self._colours[self._selected_colour])

    @property
    def colour_model(self) -> HSVColourModel:
        """Colour model used to store temporary values in sliders

        :return: colour model
        :rtype: HSVColourModel
        """
        return self._colour_model

    @property
    def colour_mask(self) -> bool:
        """Mask selected colour in frames if True

        :return: colour mask
        :rtype: bool
        """
        return self._colour_mask

    colour_maskChanged = QtCore.pyqtSignal(bool)

    @colour_mask.setter
    def colour_mask(self, value: bool):
        """Colour mask setter

        :param value: value to set
        :type value: bool
        """
        self._colour_mask = value
        self.colour_maskChanged.emit(self._colour_mask)

    @property
    def selected_colour(self) -> str:
        """Selected colour that we are currently detecting in frames

        :return: selected colour
        :rtype: str
        """
        return self._selected_colour

    selected_colourChanged = QtCore.pyqtSignal(str)

    @selected_colour.setter
    def selected_colour(self, value: str):
        """Selected colour setter

        :param value: value to set
        :type value: str
        """
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
        """Update selected colour in `colours` with values in `colour_model`"""
        self._colours[self._selected_colour]["LOWER"][0] = self._colour_model.l_Hue
        self._colours[self._selected_colour]["LOWER"][1] = self._colour_model.l_Saturation
        self._colours[self._selected_colour]["LOWER"][2] = self._colour_model.l_Value
        self._colours[self._selected_colour]["UPPER"][0] = self._colour_model.u_Hue
        self._colours[self._selected_colour]["UPPER"][1] = self._colour_model.u_Saturation
        self._colours[self._selected_colour]["UPPER"][2] = self._colour_model.u_Value

    def reset(self):
        """Reset selected colour in `colours` and `colour_model` with original values from settings"""
        if self._selected_colour != "NONE":
            self._colours[self._selected_colour]["LOWER"][0] = s.COLOURS[self._selected_colour]["LOWER"][0]
            self._colours[self._selected_colour]["LOWER"][1] = s.COLOURS[self._selected_colour]["LOWER"][1]
            self._colours[self._selected_colour]["LOWER"][2] = s.COLOURS[self._selected_colour]["LOWER"][2]
            self._colours[self._selected_colour]["UPPER"][0] = s.COLOURS[self._selected_colour]["UPPER"][0]
            self._colours[self._selected_colour]["UPPER"][1] = s.COLOURS[self._selected_colour]["UPPER"][1]
            self._colours[self._selected_colour]["UPPER"][2] = s.COLOURS[self._selected_colour]["UPPER"][2]
            self._colour_model.update(self._colours[self._selected_colour])
