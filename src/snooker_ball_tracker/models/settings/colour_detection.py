import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import snooker_ball_tracker.settings as s

from collections import OrderedDict
from copy import deepcopy


class RangeSliderModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._l_value = 0
        self._u_value = 0

    l_valueChanged = QtCore.pyqtSignal(int, name="l_valueChanged")
    u_valueChanged = QtCore.pyqtSignal(int, name="u_valueChanged")

    @QtCore.pyqtProperty(int, notify=l_valueChanged)
    def l_value(self):
        return self._l_value

    @QtCore.pyqtProperty(int, notify=u_valueChanged)
    def u_value(self):
        return self._u_value

    def setLValue(self, value):
        self._l_value = value
        self.l_valueChanged.emit(self._l_value)

    def setUValue(self, value):
        self._u_value = value
        self.u_valueChanged.emit(self._u_value)

    def reset(self, colour, index):
        self.setLValue(s.COLOURS[colour.upper()]['LOWER'][index])
        self.setUValue(s.COLOURS[colour.upper()]['UPPER'][index])


class ColourModel(QtCore.QObject):
    def __init__(self, colour, parent=None):
        super().__init__(parent)
        self._colour = colour
        self.lower = s.COLOURS[colour]["LOWER"]
        self.upper = s.COLOURS[colour]["UPPER"]


# class ColourDetectionTabModel(QtCore.QObject):

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._selected_colour = "None"
#         self._colours = deepcopy(s.COLOURS)
        
#         self.models = OrderedDict([
#             ("hue", RangeSliderModel()),
#             ("sat", RangeSliderModel()),
#             ("val", RangeSliderModel())
#         ])

#         # self.colour_models = {
#         #     colour: { ColourModel(colour) } for colour in s.COLOURS
#         # }

#     @QtCore.pyqtProperty("QString")
#     def colour(self):
#         return self._colour

#     def setColour(self, colour):
#         if self._selected_colour != "None":


#         if colour != "None":
#             for i, model in enumerate(self.models.values()):
#                 self._colours[self._selected_colour.upper()]["LOWER"][i] = model.l_value
#                 self._colours[self._selected_colour.upper()]["UPPER"][i] = model.u_value
#                 model.setLValue(self._colours[colour.upper()]["LOWER"][i])
#                 model.setUValue(self._colours[colour.upper()]["UPPER"][i])
#         else:
#             self.reset(colour)

#         self._selected_colour = colour

#     # def setColour   

#     def reset(self, colour):
#         for i, model in enumerate(self.models.values()):
#             model.setLValue(s.COLOURS[colour.upper()]["LOWER"][i])
#             model.setUValue(s.COLOURS[colour.upper()]["UPPER"][i])


class ColourDetectionTabModel(QtCore.QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._selected_colour = "None"
        self._colours = deepcopy(s.COLOURS)
        
        self.models = OrderedDict([
            ("hue", RangeSliderModel()),
            ("sat", RangeSliderModel()),
            ("val", RangeSliderModel())
        ])

        # self.colour_models = {
        #     colour: { ColourModel(colour) } for colour in s.COLOURS
        # }

    @QtCore.pyqtProperty("QString")
    def colour(self):
        return self._colour

    def setColour(self, colour):
        # if self._selected_colour == "None":


        if colour != "None":
            for i, model in enumerate(self.models.values()):
                self._colours[self._selected_colour.upper()]["LOWER"][i] = model.l_value
                self._colours[self._selected_colour.upper()]["UPPER"][i] = model.u_value
                model.setLValue(self._colours[colour.upper()]["LOWER"][i])
                model.setUValue(self._colours[colour.upper()]["UPPER"][i])
        else:
            self.reset(colour)

        self._selected_colour = colour

    # def setColour   

    def reset(self, colour):
        for i, model in enumerate(self.models.values()):
            model.setLValue(s.COLOURS[colour.upper()]["LOWER"][i])
            model.setUValue(s.COLOURS[colour.upper()]["UPPER"][i])
