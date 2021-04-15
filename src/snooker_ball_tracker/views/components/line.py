import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui


class Ui_Line(QtWidgets.QFrame):
    def __init__(self, parent=None, shape=QtWidgets.QFrame.HLine):
        super().__init__(parent)
        self.setFrameShape(shape)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
