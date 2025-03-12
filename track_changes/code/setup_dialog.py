from PyQt5.QtWidgets import QDialog
from qgis.core import QgsMessageLog, Qgis

from ..ui.main_dialog import Ui_Dialog

class SetupDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect the button to a function
        self.pbHelloWorld.clicked.connect(self.say_hello)

    def say_hello(self):
        QgsMessageLog.logMessage("Hello World!", "Track Changes", level=Qgis.Info)
