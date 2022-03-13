import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class Ui_RadioButton(QtWidgets.QRadioButton):
    def __init__(
        self,
        name,
        value,
        checked=False,
        parent=None,
        objectName=None,
        width=None,
        height=None,
        sizePolicy=(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred),
    ):
        super().__init__(name, parent)
        if width:
            self.setMinimumWidth(width[0])
            self.setMaximumWidth(width[1])
        if height:
            self.setMinimumHeight(height[0])
            self.setMaximumHeight(height[1])
        if objectName:
            self.setObjectName(objectName)

        self._value = value

        self.setStyleSheet("padding; .3em")
        self.setSizePolicy(QtWidgets.QSizePolicy(sizePolicy[0], sizePolicy[1]))
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setChecked(checked)
        self.toggled.connect(self.onToggle)

    @property
    def state(self):
        return self.isChecked()

    stateChanged = QtCore.pyqtSignal(bool)

    @state.setter
    def state(self, value):
        if value == self._value:
            self.setChecked(True)
            self.stateChanged.emit(value)

    @QtCore.pyqtSlot(bool)
    def onToggle(self, selected):
        if selected:
            self.setChecked(selected)
            self.stateChanged.emit(self._value)
