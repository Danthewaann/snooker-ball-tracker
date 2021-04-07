import numpy as np
import PyQt5.QtCore as QtCore


class HSVColour(QtCore.QObject):
    def __init__(self):
        """Creates instance of this class that contains 
        hue, saturation and value properties that make up a specific colour"""
        super().__init__()
        self._l_Hue = 0
        self._u_Hue = 0 
        self._l_Saturation = 0 
        self._u_Saturation = 0 
        self._l_Value = 0 
        self._u_Value = 0

    def lower_range(self) -> np.ndarray:
        """Get lower colour values concated into an array

        :return: lower colour values
        :rtype: np.ndarray
        """
        return np.array([self._l_Hue, self._l_Saturation, self._l_Value])

    def upper_range(self) -> np.ndarray:
        """Get upper colour values concated into an array

        :return: upper colour values
        :rtype: np.ndarray
        """
        return np.array([self._u_Hue, self._u_Saturation, self._u_Value])

    @property
    def l_Hue(self) -> int:
        """Lower hue property

        :return: lower hue
        :rtype: int
        """
        return self._l_Hue

    l_HueChanged = QtCore.pyqtSignal(int, name="l_HueChanged")

    @l_Hue.setter
    def l_Hue(self, value: int):
        """Lower hue setter

        :param value: value to set
        :type value: int
        """
        self._l_Hue = value
        self.l_HueChanged.emit(self._l_Hue)

    @property
    def u_Hue(self) -> int:
        """Upper hue property

        :return: upper hue
        :rtype: int
        """
        return self._u_Hue

    u_HueChanged = QtCore.pyqtSignal(int, name="u_HueChanged")

    @u_Hue.setter
    def u_Hue(self, value: int):
        """Upper hue setter

        :param value: value to set
        :type value: int
        """
        self._u_Hue = value
        self.u_HueChanged.emit(self._u_Hue)

    @property
    def l_Saturation(self) -> int:
        """Lower saturation property

        :return: lower saturation
        :rtype: int
        """
        return self._l_Saturation

    l_SaturationChanged = QtCore.pyqtSignal(int, name="l_SaturationChanged")

    @l_Saturation.setter
    def l_Saturation(self, value: int):
        """Lower saturation setter

        :param value: value to set
        :type value: int
        """
        self._l_Saturation = value
        self.l_SaturationChanged.emit(self._l_Saturation)

    @property
    def u_Saturation(self) -> int:
        """Upper saturation property

        :return: upper saturation
        :rtype: int
        """
        return self._u_Saturation

    u_SaturationChanged = QtCore.pyqtSignal(int, name="u_SaturationChanged")

    @u_Saturation.setter
    def u_Saturation(self, value: int):
        """Upper saturation setter

        :param value: value to set
        :type value: int
        """
        self._u_Saturation = value
        self.u_SaturationChanged.emit(self._u_Saturation)

    @property
    def l_Value(self) -> int:
        """Lower value property

        :return: lower value
        :rtype: int
        """
        return self._l_Value

    l_ValueChanged = QtCore.pyqtSignal(int, name="l_ValueChanged")

    @l_Value.setter
    def l_Value(self, value: int):
        """Lower value setter

        :param value: value to set
        :type value: int
        """
        self._l_Value = value
        self.l_ValueChanged.emit(self._l_Value)

    @property
    def u_Value(self) -> int:
        """Upper value property

        :return: upper value
        :rtype: int
        """
        return self._u_Value

    u_ValueChanged = QtCore.pyqtSignal(int, name="u_ValueChanged")

    @u_Value.setter
    def u_Value(self, value: int):
        """Upper value setter

        :param value: value to set
        :type value: int
        """
        self._u_Value = value
        self.u_ValueChanged.emit(self._u_Value)

    def update(self, colour: dict):
        """Update colour properties with provided colour values

        :param colour: colour dict with lower and upper range values
        :type colour: dict
        """
        self.l_Hue = colour["LOWER"][0]
        self.l_Saturation = colour["LOWER"][1]
        self.l_Value = colour["LOWER"][2]
        self.u_Hue = colour["UPPER"][0]
        self.u_Saturation = colour["UPPER"][1]
        self.u_Value = colour["UPPER"][2]

    def clear(self):
        """Clear all colour property values"""
        self.l_Hue = 0
        self.u_Hue = 0
        self.l_Saturation = 0
        self.u_Saturation = 0
        self.l_Value = 0
        self.u_Value = 0
