import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add track_changes to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock Qt classes and modules
class MockQDockWidget:
    def __init__(self):
        self.setVisible = MagicMock()
        self.isVisible = MagicMock(return_value=True)
        self.setWidget = MagicMock()
        self.widget = MagicMock()

class MockQt:
    RightDockWidgetArea = 2

class MockQAction:
    def __init__(self, icon=None, text=None, parent=None):
        self.icon = icon
        self.text = text
        self.parent = parent
        self.triggered = MagicMock()
        self.setEnabled = MagicMock()
        self.setIcon = MagicMock()
        self.setToolTip = MagicMock()

class MockQIcon:
    def __init__(self, path=None):
        self.path = path

class MockQgsFileWidget:
    def __init__(self):
        self.setStorageMode = MagicMock()
        self.setFilePath = MagicMock()
        self.filePath = MagicMock(return_value="")

class MockQgsVectorLayer:
    def __init__(self):
        self.id = MagicMock(return_value="layer_id")
        self.name = MagicMock(return_value="layer_name")

class MockQgsProject:
    def __init__(self):
        self.mapLayers = MagicMock(return_value={})
        self.instance = MagicMock(return_value=self)

class TestTrackChangesPlugin(unittest.TestCase):
    def setUp(self):
        # Create mock modules
        self.mock_modules = {
            'PyQt5.QtCore': MagicMock(Qt=MockQt),
            'PyQt5.QtWidgets': MagicMock(QAction=MockQAction, QDockWidget=MockQDockWidget),
            'PyQt5.QtGui': MagicMock(QIcon=MockQIcon),
            'qgis.PyQt.QtWidgets': MagicMock(QAction=MockQAction),
            'qgis.PyQt.QtGui': MagicMock(QIcon=MockQIcon),
            'qgis.core': MagicMock(QgsVectorLayer=MockQgsVectorLayer, QgsProject=MockQgsProject),
            'qgis.gui': MagicMock(QgsFileWidget=MockQgsFileWidget),
            'qgsfilewidget': MagicMock(QgsFileWidget=MockQgsFileWidget)
        }

        # Create patches for all Qt/QGIS imports
        self.patches = [
            patch.dict('sys.modules', self.mock_modules)
        ]

        # Start all patches
        for p in self.patches:
            p.start()

        # Create a mock iface
        self.iface = MagicMock()
        self.iface.messageBar.return_value = MagicMock()
        self.iface.addDockWidget = MagicMock()
        self.iface.mainWindow.return_value = MagicMock()
        self.toolbar = MagicMock()
        self.iface.addToolBar.return_value = self.toolbar

        # Import the plugin class after patching
        from track_changes.code.main_plugin import TrackChangesPlugin
        self.plugin = TrackChangesPlugin(self.iface)

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def test_init(self):
        self.assertEqual(self.plugin.iface, self.iface)
        self.assertIsNone(self.plugin.default_log_dialog)
        self.assertIsNone(self.plugin.gpkg_log_dialog)
        self.assertIsNone(self.plugin.about_action)
        self.assertIsNone(self.plugin.default_log_action)
        self.assertIsNone(self.plugin.gpkg_log_action)

    def test_initGui(self):
        self.plugin.initGui()
        
        self.assertIsNotNone(self.plugin.about_action)
        self.assertIsNotNone(self.plugin.default_log_action)
        self.assertIsNotNone(self.plugin.gpkg_log_action)
        
        self.iface.addPluginToMenu.assert_called()
        self.toolbar.addAction.assert_called()

    def test_unload(self):
        self.plugin.about_action = MagicMock()
        self.plugin.default_log_action = MagicMock()
        self.plugin.gpkg_log_action = MagicMock()
        
        self.plugin.unload()
        
        self.iface.removePluginMenu.assert_called()
        self.iface.removeToolBarIcon.assert_called()
        
        self.assertIsNone(self.plugin.about_action)
        self.assertIsNone(self.plugin.default_log_action)
        self.assertIsNone(self.plugin.gpkg_log_action)

    @patch('track_changes.code.main_plugin.DefaultFeatureLogger')
    def test_run_default_new_dialog(self, mock_default_logger):
        mock_dialog = MockQDockWidget()
        mock_default_logger.return_value = mock_dialog
        
        self.plugin.run_default()
        
        mock_default_logger.assert_called_once()
        self.iface.addDockWidget.assert_called_once_with(MockQt.RightDockWidgetArea, mock_dialog)
        self.assertEqual(self.plugin.default_log_dialog, mock_dialog)

    def test_run_default_existing_dialog(self):
        mock_dialog = MockQDockWidget()
        self.plugin.default_log_dialog = mock_dialog
        
        self.plugin.run_default()
        
        mock_dialog.setVisible.assert_called_once()

    @patch('track_changes.code.main_plugin.GpkgFeatureLogger')
    def test_run_gpkg_new_dialog(self, mock_gpkg_logger):
        mock_dialog = MockQDockWidget()
        mock_gpkg_logger.return_value = mock_dialog
        
        self.plugin.run_gpkg()
        
        mock_gpkg_logger.assert_called_once_with(self.iface)
        self.iface.addDockWidget.assert_called_once_with(MockQt.RightDockWidgetArea, mock_dialog)
        self.assertEqual(self.plugin.gpkg_log_dialog, mock_dialog)

    def test_run_gpkg_existing_dialog(self):
        mock_dialog = MockQDockWidget()
        self.plugin.gpkg_log_dialog = mock_dialog
        
        self.plugin.run_gpkg()
        
        mock_dialog.setVisible.assert_called_once()

    @patch('track_changes.code.main_plugin.AboutWidget')
    def test_about(self, mock_about_widget):
        mock_dialog = MagicMock()
        mock_about_widget.return_value = mock_dialog
        
        self.plugin.about()
        
        mock_about_widget.assert_called_once_with(self.iface.mainWindow())
        mock_dialog.exec_.assert_called_once()

    def test_get_icon_path(self):
        path = "../icon.png"
        plugin_dir = os.path.dirname(os.path.dirname(__file__))
        expected = os.path.join(plugin_dir, "track_changes/code", path)
        result = self.plugin.get_icon_path(path)
        self.assertEqual(os.path.normpath(result), os.path.normpath(expected))

if __name__ == '__main__':
    unittest.main() 