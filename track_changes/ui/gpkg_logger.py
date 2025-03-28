# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'track_changes/ui/gpkg_logger.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SetupTrackingChanges(object):
    def setupUi(self, SetupTrackingChanges):
        SetupTrackingChanges.setObjectName("SetupTrackingChanges")
        SetupTrackingChanges.resize(370, 245)
        self.dockWidgetContents = QtWidgets.QWidget(SetupTrackingChanges)
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.mQgsFileWidget = gui.QgsFileWidget(self.dockWidgetContents)
        self.mQgsFileWidget.setObjectName("mQgsFileWidget")
        self.verticalLayout_2.addWidget(self.mQgsFileWidget)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.cbVectorLayers = QtWidgets.QComboBox(self.dockWidgetContents)
        self.cbVectorLayers.setObjectName("cbVectorLayers")
        self.verticalLayout.addWidget(self.cbVectorLayers)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbActivate = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pbActivate.setObjectName("pbActivate")
        self.horizontalLayout.addWidget(self.pbActivate)
        self.pbDeactivate = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pbDeactivate.setObjectName("pbDeactivate")
        self.horizontalLayout.addWidget(self.pbDeactivate)
        self.pbRefreshLayers = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pbRefreshLayers.setObjectName("pbRefreshLayers")
        self.horizontalLayout.addWidget(self.pbRefreshLayers)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.labelActive = QtWidgets.QLabel(self.dockWidgetContents)
        self.labelActive.setObjectName("labelActive")
        self.horizontalLayout_2.addWidget(self.labelActive)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(SetupTrackingChanges)
        QtCore.QMetaObject.connectSlotsByName(SetupTrackingChanges)

    def retranslateUi(self, SetupTrackingChanges):
        _translate = QtCore.QCoreApplication.translate
        SetupTrackingChanges.setWindowTitle(_translate("SetupTrackingChanges", "GeoPackage tracking changes"))
        self.label.setText(_translate("SetupTrackingChanges", "GeoPackage file path"))
        self.label_2.setText(_translate("SetupTrackingChanges", "Start/stop tracking changes"))
        self.pbActivate.setText(_translate("SetupTrackingChanges", "Activate"))
        self.pbDeactivate.setText(_translate("SetupTrackingChanges", "Deactivate"))
        self.pbRefreshLayers.setText(_translate("SetupTrackingChanges", "Refresh Layers"))
        self.label_3.setText(_translate("SetupTrackingChanges", "Active Layer:"))
        self.labelActive.setText(_translate("SetupTrackingChanges", "None"))
from qgis import gui
