import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets


class Ui_Label(QtWidgets.QLabel):

    textChanged = QtCore.pyqtSignal(str)

    def __init__(
        self,
        name,
        parent=None,
        objectName=None,
        width=None,
        height=None,
        alignment=None,
        styleSheet=None,
        sizePolicy=(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred),
    ):
        super().__init__(name, parent)
        if width:
            self.setMinimumWidth(width[0])
            self.setMaximumWidth(width[1])
        if height:
            self.setMinimumHeight(height[0])
            self.setMaximumHeight(height[1])
        if alignment:
            self.setAlignment(alignment)
        if objectName:
            self.setObjectName(objectName)
        if styleSheet:
            self.setStyleSheet(styleSheet)

        self.setSizePolicy(QtWidgets.QSizePolicy(sizePolicy[0], sizePolicy[1]))

    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        super().setText(text)
        self.textChanged.emit(text)
