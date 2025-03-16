from PyQt5.QtWidgets import QDialog
from ..ui.about_dialog import Ui_About

class AboutWidget(QDialog):
    """A dialog window for the About section."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_About()
        self.ui.setupUi(self)
