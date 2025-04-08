import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock QGIS components
class MockQgsMessageLog:
    @staticmethod
    def logMessage(message, tag="Track Changes", level=0):
        pass

class MockQgis:
    Info = 0
    Warning = 1
    Critical = 2

class MockQgsProject:
    @staticmethod
    def instance():
        return MockQgsProject()
    
    def mapLayers(self):
        return {}

class MockQgsVectorLayer:
    def __init__(self, source, name, provider):
        self.source = source
        self.name = name
        self.provider = provider
        self.id = f"mock_layer_{name}"

# Mock PyQt5 components
class MockQApplication:
    @staticmethod
    def instance():
        return MockQApplication()

class MockQWidget:
    def __init__(self):
        self._enabled = True
    
    def isEnabled(self):
        return self._enabled
    
    def setEnabled(self, enabled):
        self._enabled = enabled

class MockQComboBox(MockQWidget):
    def __init__(self):
        super().__init__()
        self._items = []
        self._current_index = -1
    
    def addItem(self, item):
        self._items.append(item)
    
    def currentText(self):
        if 0 <= self._current_index < len(self._items):
            return self._items[self._current_index]
        return ""
    
    def setCurrentText(self, text):
        if text in self._items:
            self._current_index = self._items.index(text)
    
    def clear(self):
        self._items = []
        self._current_index = -1

class MockQPushButton(MockQWidget):
    def __init__(self):
        super().__init__()
        self._text = ""
    
    def setText(self, text):
        self._text = text
    
    def text(self):
        return self._text

class MockQLineEdit(MockQWidget):
    def __init__(self):
        super().__init__()
        self._text = ""
    
    def setText(self, text):
        self._text = text
    
    def text(self):
        return self._text

class MockQAction:
    def __init__(self, text, parent=None):
        self._text = text
        self._parent = parent
        self._enabled = True
    
    def setText(self, text):
        self._text = text
    
    def text(self):
        return self._text
    
    def isEnabled(self):
        return self._enabled
    
    def setEnabled(self, enabled):
        self._enabled = enabled

class MockQDockWidget(MockQWidget):
    def __init__(self, title, parent=None):
        super().__init__()
        self._title = title
        self._parent = parent
        self._widget = None
    
    def setWidget(self, widget):
        self._widget = widget
    
    def widget(self):
        return self._widget

class MockQgsFileWidget(MockQWidget):
    def __init__(self):
        super().__init__()
        self._file_path = ""
    
    def filePath(self):
        return self._file_path
    
    def setFilePath(self, path):
        self._file_path = path

# Add mocks to sys.modules
sys.modules['qgis.core'] = type('MockQgisCore', (), {
    'QgsMessageLog': MockQgsMessageLog,
    'Qgis': MockQgis,
    'QgsProject': MockQgsProject,
    'QgsVectorLayer': MockQgsVectorLayer
})

sys.modules['qgis.PyQt.QtWidgets'] = type('MockQtWidgets', (), {
    'QApplication': MockQApplication,
    'QWidget': MockQWidget,
    'QComboBox': MockQComboBox,
    'QPushButton': MockQPushButton,
    'QLineEdit': MockQLineEdit,
    'QAction': MockQAction,
    'QDockWidget': MockQDockWidget
})

sys.modules['qgis.PyQt.QtCore'] = type('MockQtCore', (), {})
sys.modules['qgis.PyQt.QtGui'] = type('MockQtGui', (), {})
sys.modules['qgis'] = type('MockQgis', (), {}) 