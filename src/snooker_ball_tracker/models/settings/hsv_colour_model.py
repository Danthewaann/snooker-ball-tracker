import PyQt5.QtCore as QtCore


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