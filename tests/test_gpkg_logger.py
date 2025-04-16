import pytest
from unittest.mock import MagicMock, patch

# Mock QGIS classes
class MockQWidget:
    def __init__(self):
        self.cbVectorLayers = MockQComboBox()
        self.pbActivate = MockQPushButton()
        self.pbDeactivate = MockQPushButton()
        self.fwGpkgFile = MockQgsFileWidget()

class MockQComboBox:
    def __init__(self):
        self._enabled = False
        self._items = []
        self._current_index = -1

    def setEnabled(self, enabled):
        self._enabled = enabled

    def isEnabled(self):
        return self._enabled

    def addItem(self, item):
        self._items.append(item)

    def clear(self):
        self._items = []

    def count(self):
        return len(self._items)

    def setCurrentIndex(self, index):
        self._current_index = index

    def currentIndex(self):
        return self._current_index

class MockQPushButton:
    def __init__(self):
        self._enabled = False

    def setEnabled(self, enabled):
        self._enabled = enabled

    def isEnabled(self):
        return self._enabled

class MockQgsFileWidget:
    def __init__(self):
        self._file_path = ""

    def filePath(self):
        return self._file_path

    def setFilePath(self, path):
        self._file_path = path

class MockQgsVectorLayer:
    def __init__(self, path, name, provider):
        self.path = path
        self.name = name
        self.provider = provider

class MockQgsProject:
    def __init__(self):
        self._layers = []

    def addMapLayer(self, layer):
        self._layers.append(layer)

    def mapLayers(self):
        return {layer.name: layer for layer in self._layers}

class GpkgLogger:
    def __init__(self):
        self.ui = MockQWidget()
        self.layer = None
        self.layer_name = None
        self.file_path = None

    def on_file_selected(self):
        self.file_path = self.ui.fwGpkgFile.filePath()
        if self.file_path:
            self.ui.cbVectorLayers.setEnabled(True)
            self.refresh_layers()

    def refresh_layers(self):
        self.ui.cbVectorLayers.clear()
        if self.file_path:
            # Mock adding layers
            layer1 = MockQgsVectorLayer(self.file_path, "layer1", "ogr")
            layer2 = MockQgsVectorLayer(self.file_path, "layer2", "ogr")
            self.ui.cbVectorLayers.addItem(layer1.name)
            self.ui.cbVectorLayers.addItem(layer2.name)

    def on_layer_selected(self):
        if self.ui.cbVectorLayers.currentIndex() >= 0:
            self.layer_name = self.ui.cbVectorLayers._items[self.ui.cbVectorLayers.currentIndex()]
            self.ui.pbActivate.setEnabled(True)

    def activate_tracking(self):
        if self.layer_name:
            self.ui.pbActivate.setEnabled(False)
            self.ui.pbDeactivate.setEnabled(True)

    def deactivate_tracking(self):
        self.ui.pbActivate.setEnabled(True)
        self.ui.pbDeactivate.setEnabled(False)

@pytest.fixture
def logger():
    return GpkgLogger()

def test_initialization(logger):
    assert not logger.ui.cbVectorLayers.isEnabled()
    assert not logger.ui.pbActivate.isEnabled()
    assert not logger.ui.pbDeactivate.isEnabled()

def test_file_selection(logger):
    logger.ui.fwGpkgFile.setFilePath("/path/to/file.gpkg")
    logger.on_file_selected()
    assert logger.ui.cbVectorLayers.isEnabled()
    assert logger.file_path == "/path/to/file.gpkg"

def test_refresh_layers(logger):
    logger.ui.fwGpkgFile.setFilePath("/path/to/file.gpkg")
    logger.on_file_selected()
    assert logger.ui.cbVectorLayers.count() == 2
    assert logger.ui.cbVectorLayers._items == ["layer1", "layer2"]

def test_activate_tracking(logger):
    logger.ui.fwGpkgFile.setFilePath("/path/to/file.gpkg")
    logger.on_file_selected()
    logger.ui.cbVectorLayers.setCurrentIndex(0)
    logger.on_layer_selected()
    logger.activate_tracking()
    assert not logger.ui.pbActivate.isEnabled()
    assert logger.ui.pbDeactivate.isEnabled()

def test_deactivate_tracking(logger):
    logger.ui.fwGpkgFile.setFilePath("/path/to/file.gpkg")
    logger.on_file_selected()
    logger.ui.cbVectorLayers.setCurrentIndex(0)
    logger.on_layer_selected()
    logger.activate_tracking()
    logger.deactivate_tracking()
    assert logger.ui.pbActivate.isEnabled()
    assert not logger.ui.pbDeactivate.isEnabled() 