# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'track_changes/ui/about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


def get_plugin_version():
    from track_changes import __version__
    return __version__


class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(461, 321)
        self.gridLayout = QtWidgets.QGridLayout(About)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(About)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(About)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(About)
        self.buttonBox.accepted.connect(About.accept)
        self.buttonBox.rejected.connect(About.reject)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About QGIS Tracking Changes"))
        self.label.setText(_translate("About", f"<html><head/><body><p><span style=\" font-weight:600;\">QGIS Track Changes</span><br/>Version: {get_plugin_version()}<br/><br/>This plugin helps track changes in vector layer data, including:<br/>- Feature modifications<br/>- Geometry updates<br/>- Attribute changes<br/><br/>It ensures data integrity by logging changes efficiently within QGIS.<br/><br/><span style=\" font-weight:600;\">Developer:</span> Ahmad Zaenun Faiz<br/><span style=\" font-weight:600;\">License:</span> GPL-3.0<br/><br/>For documentation, visit:<br/><a href=\"https://qgis-track-changes.readthedocs.io/en/latest/\"><span style=\" text-decoration: underline; color:#419cff;\">QGIS Track Changes Documentation</span></a></p></body></html>"))
