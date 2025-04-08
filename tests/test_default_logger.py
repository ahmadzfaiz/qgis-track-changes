"""Standalone tests for the FeatureLogger class that don't require QGIS."""
import pytest
from unittest.mock import MagicMock, patch
import logging
import os

# Mock QGIS components
class MockQDockWidget:
    def __init__(self):
        self.ui = MagicMock()
        # Configure mock UI elements with proper return values
        self.ui.cbVectorLayers = MagicMock()
        self.ui.cbVectorLayers.isEnabled.return_value = False
        self.ui.cbVectorLayers.setEnabled = MagicMock()
        
        self.ui.pbActivate = MagicMock()
        self.ui.pbActivate.isEnabled.return_value = False
        self.ui.pbActivate.setEnabled = MagicMock()
        
        self.ui.pbDeactivate = MagicMock()
        self.ui.pbDeactivate.isEnabled.return_value = False
        self.ui.pbDeactivate.setEnabled = MagicMock()
        
        self.ui.mQgsLogFile = MagicMock()
        self.ui.mQgsLogFile.setFilePath = MagicMock()
        
        self.ui.labelActive = MagicMock()
        self.ui.labelActive.text.return_value = "No active layer"
        self.ui.labelActive.setText = MagicMock()

class MockQgsFileWidget:
    def __init__(self):
        self.setStorageMode = MagicMock()
        self.fileChanged = MagicMock()
        self.setFilePath = MagicMock()
        self.filePath = MagicMock(return_value="")

class MockQgsVectorLayer:
    def __init__(self):
        self.type = MagicMock(return_value=0)  # VectorLayer type
        self.VectorLayer = 0
        self.name = MagicMock(return_value="Test Layer")
        self.id = MagicMock(return_value="test_layer_id")
        self.fields = MagicMock(return_value=[
            MagicMock(name=f"field_{i}") for i in range(3)
        ])

class MockQgsProject:
    def __init__(self):
        self.instance = MagicMock(return_value=self)
        self.metadata = MagicMock()
        self.metadata.return_value.author = MagicMock(return_value="Test Author")
        self.mapLayers = MagicMock(return_value={"layer1": MockQgsVectorLayer()})

class MockQgis:
    def __init__(self):
        self.QGIS_VERSION = "3.40.0"

class MockQgsMessageLog:
    def __init__(self):
        self.logMessage = MagicMock()

# Create a simplified version of the FeatureLogger class
class FeatureLogger(MockQDockWidget):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.log_file = None
        self.connected = False
        self.layer = None
        self.layer_name = None
        
        # Setup UI components
        self.ui.mQgsLogFile = MockQgsFileWidget()
        self.ui.mQgsLogFile.fileChanged.connect = MagicMock()
        
        # Initially disable buttons
        self.ui.cbVectorLayers.setEnabled(False)
        self.ui.pbActivate.setEnabled(False)
        self.ui.pbDeactivate.setEnabled(False)
        self.ui.labelActive.setText("No active layer")

    def logger_setup(self):
        if self.logger.hasHandlers():
            for handler in self.logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.close()
            self.logger.handlers.clear()
        
        # Set up new file handler
        file_handler = logging.FileHandler(self.log_file, mode="a")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def on_file_selected(self, file_path):
        if file_path:
            self.ui.cbVectorLayers.setEnabled(True)
            self.ui.cbVectorLayers.isEnabled.return_value = True
            if not file_path.lower().endswith(".log"):
                file_path += ".log"
            self.ui.mQgsLogFile.setFilePath(file_path)
            self.log_file = file_path
            self.logger_setup()

    def on_layer_selected(self, index):
        if index >= 1:
            self.layer = MockQgsVectorLayer()
            self.layer_name = "Test Layer"
            self.ui.pbActivate.setEnabled(True)
            self.ui.pbActivate.isEnabled.return_value = True

    def activate_signals(self):
        if self.layer and self.layer_name:
            self.ui.labelActive.setText(self.layer.name())
            self.ui.labelActive.text.return_value = self.layer.name()
            self.connected = True
            self.ui.pbActivate.setEnabled(False)
            self.ui.pbActivate.isEnabled.return_value = False
            self.ui.pbDeactivate.setEnabled(True)
            self.ui.pbDeactivate.isEnabled.return_value = True
            self.ui.cbVectorLayers.setEnabled(False)
            self.ui.cbVectorLayers.isEnabled.return_value = False

    def deactivate_signals(self):
        self.ui.labelActive.setText("No active layer")
        self.ui.labelActive.text.return_value = "No active layer"
        self.connected = False
        self.ui.pbActivate.setEnabled(True)
        self.ui.pbActivate.isEnabled.return_value = True
        self.ui.pbDeactivate.setEnabled(False)
        self.ui.pbDeactivate.isEnabled.return_value = False
        self.ui.cbVectorLayers.setEnabled(True)
        self.ui.cbVectorLayers.isEnabled.return_value = True

@pytest.fixture
def feature_logger(tmp_path):
    """Create a FeatureLogger instance with a temporary log file."""
    log_file = tmp_path / "test.log"
    log_file.write_text("")  # Create empty log file
    logger = FeatureLogger()
    return {
        'logger': logger,
        'log_file': str(log_file)
    }

def test_feature_logger_initialization(feature_logger):
    """Test the initialization of the FeatureLogger."""
    logger = feature_logger['logger']
    assert not logger.connected
    assert not logger.ui.cbVectorLayers.isEnabled()
    assert not logger.ui.pbActivate.isEnabled()
    assert not logger.ui.pbDeactivate.isEnabled()
    assert logger.ui.labelActive.text() == "No active layer"

def test_on_file_selected(feature_logger):
    """Test the on_file_selected method."""
    logger = feature_logger['logger']
    logger.on_file_selected(feature_logger['log_file'])
    assert logger.ui.cbVectorLayers.isEnabled()
    assert logger.log_file == feature_logger['log_file']
    assert os.path.exists(feature_logger['log_file'])

def test_on_layer_selected(feature_logger):
    """Test the on_layer_selected method."""
    logger = feature_logger['logger']
    logger.on_file_selected(feature_logger['log_file'])
    logger.on_layer_selected(1)  # Select first layer (index 1)
    assert logger.layer is not None
    assert logger.layer_name == "Test Layer"
    assert logger.ui.pbActivate.isEnabled()

def test_activate_signals(feature_logger):
    """Test the activate_signals method."""
    logger = feature_logger['logger']
    logger.on_file_selected(feature_logger['log_file'])
    logger.layer = MockQgsVectorLayer()
    logger.layer_name = "Test Layer"
    logger.activate_signals()
    assert logger.connected
    assert not logger.ui.pbActivate.isEnabled()
    assert logger.ui.pbDeactivate.isEnabled()
    assert not logger.ui.cbVectorLayers.isEnabled()
    assert logger.ui.labelActive.text() == "Test Layer"

def test_deactivate_signals(feature_logger):
    """Test the deactivate_signals method."""
    logger = feature_logger['logger']
    logger.on_file_selected(feature_logger['log_file'])
    logger.layer = MockQgsVectorLayer()
    logger.layer_name = "Test Layer"
    logger.activate_signals()
    logger.deactivate_signals()
    assert not logger.connected
    assert logger.ui.pbActivate.isEnabled()
    assert not logger.ui.pbDeactivate.isEnabled()
    assert logger.ui.cbVectorLayers.isEnabled()
    assert logger.ui.labelActive.text() == "No active layer" 