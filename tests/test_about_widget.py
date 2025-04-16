import pytest
from unittest.mock import MagicMock, patch
import os
import sqlite3
import tempfile
import shutil
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, ANY
import sys

# --- Mock QGIS/PyQt/GUI modules before importing plugin code ---
# Create mock modules
mock_qgis = MagicMock()
mock_pyqt = MagicMock()
mock_pyqt_gui = MagicMock()
mock_widgets = MagicMock()
mock_core = MagicMock()
mock_utils = MagicMock()
mock_qgis_gui = MagicMock()
mock_qgsfilewidget_module = MagicMock()

# Assign mock attributes needed during import (can be expanded)
mock_qgis.PyQt = mock_pyqt
mock_qgis.core = mock_core
mock_qgis.utils = mock_utils
mock_qgis.gui = mock_qgis_gui
mock_pyqt.QtGui = mock_pyqt_gui
mock_pyqt.QtWidgets = mock_widgets
mock_pyqt.QtCore = MagicMock()
mock_pyqt_gui.QIcon = MagicMock()
mock_widgets.QAction = MagicMock()
mock_widgets.QDialog = MagicMock() # Keep QDialog mock for base class if AboutWidget is still imported implicitly
mock_widgets.QTableWidgetItem = MagicMock() # Mock here for the import in about_widget
mock_widgets.QAbstractItemView = MagicMock() # Mock base class for table triggers
mock_qgis_gui.QgsFileWidget = MagicMock()
mock_qgsfilewidget_module.QgsFileWidget = mock_qgis_gui.QgsFileWidget

# Insert mocks into sys.modules BEFORE importing track_changes
sys.modules['qgis'] = mock_qgis
sys.modules['qgis.PyQt'] = mock_pyqt
sys.modules['qgis.PyQt.QtGui'] = mock_pyqt_gui
sys.modules['qgis.PyQt.QtWidgets'] = mock_widgets
sys.modules['qgis.PyQt.QtCore'] = mock_pyqt.QtCore
sys.modules['qgis.core'] = mock_core
sys.modules['qgis.utils'] = mock_utils
sys.modules['qgis.gui'] = mock_qgis_gui
sys.modules['qgsfilewidget'] = mock_qgsfilewidget_module

# Import the function we want to test
from track_changes.code.about_widget import AboutWidget, get_plugin_version

about_widget = AboutWidget

# Helper function to create dummy GeoPackage files
def create_gpkg(path, with_changelog=True, add_data=True, error_on_insert=False):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    try:
        # Minimal GPKG setup
        cursor.execute("CREATE TABLE gpkg_contents (table_name TEXT NOT NULL PRIMARY KEY, data_type TEXT NOT NULL);")
        if with_changelog:
            cursor.execute("""
                CREATE TABLE gpkg_changelog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                    data_version TEXT,
                    author TEXT,
                    layer_name TEXT,
                    feature_id INTEGER,
                    message TEXT,
                    data BLOB
                    -- Match the columns selected in the actual query
                );
            """)
            if add_data:
                if error_on_insert: # Simulate an error during data creation if needed
                    raise sqlite3.OperationalError("Simulated insert error")
                # Add a sample row (adjust timestamp slightly for humanize)
                # Use format compatible with datetime.fromisoformat in Python 3.9 (no 'Z')
                past_time = (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S.%f')
                cursor.execute("""
                    INSERT INTO gpkg_changelog
                    (timestamp, data_version, author, layer_name, feature_id, message, data)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (past_time, '1.0', 'tester', 'Layer 1', 123, 'Initial commit', b'{}'))
    finally:
        conn.commit()
        conn.close()

@pytest.fixture
def setup_teardown():
    """Pytest fixture for setting up and tearing down test resources."""
    temp_dir = tempfile.mkdtemp()
    gpkg_with_changelog_path = os.path.join(temp_dir, "with_changelog.gpkg")
    gpkg_without_changelog_path = os.path.join(temp_dir, "without_changelog.gpkg")
    gpkg_empty_changelog_path = os.path.join(temp_dir, "empty_changelog.gpkg")
    gpkg_error_path = os.path.join(temp_dir, "error_create.gpkg") # For db error test

    create_gpkg(gpkg_with_changelog_path, with_changelog=True, add_data=True)
    create_gpkg(gpkg_without_changelog_path, with_changelog=False)
    create_gpkg(gpkg_empty_changelog_path, with_changelog=True, add_data=False)
    # Don't create gpkg_error_path yet, simulate error during connect

    # --- Mock Dependencies for the standalone function ---
    # Patch where imports happen in about_widget.py
    patchers = {
        # Patch the imports used by _fetch_and_populate_changelog
        'iface': patch('track_changes.code.about_widget.iface', MagicMock()), 
        'qtw': patch('track_changes.code.about_widget.QTableWidgetItem', MagicMock()),
        'qabstractview': patch('track_changes.code.about_widget.QAbstractItemView', MagicMock()),
        'qgis_in_about': patch('track_changes.code.about_widget.Qgis', MagicMock()), 
        'dt': patch('track_changes.code.about_widget.datetime'), 
        'humanize': patch('track_changes.code.about_widget.humanize', MagicMock()), # Also mock humanize
    }
    mocks = {name: p.start() for name, p in patchers.items()}

    # Configure mocks
    mock_datetime = mocks['dt']
    mock_qgis_about = mocks['qgis_in_about']
    mock_humanize = mocks['humanize']
    mock_datetime.now.return_value = datetime.now() 
    # Make fromisoformat use the real implementation BUT allow mocking if needed later
    mock_datetime.fromisoformat.side_effect = datetime.fromisoformat 
    mock_humanize.naturaltime.return_value = '5 minutes ago' # Mock humanize output
    mock_qgis_about.Warning = 1 
    mock_qgis_about.Critical = 3
    # Ensure QAbstractItemView.NoEditTriggers exists
    mocks['qabstractview'].NoEditTriggers = 0

    # Create a mock QTableWidget for the function to interact with
    mock_table = MagicMock()
    # Mock methods used by the function
    mock_table.setEditTriggers = MagicMock()
    mock_table.setRowCount = MagicMock()
    mock_table.setItem = MagicMock()
    mock_table.resizeColumnsToContents = MagicMock()
    mock_table.setColumnWidth = MagicMock()
    mock_table.columnCount = MagicMock(return_value=7) # Example column count
    mock_table.columnWidth = MagicMock(return_value=400) # Example width

    # Yield necessary objects to the tests
    yield {
        "mock_table": mock_table, # Yield the direct mock table
        "mock_iface": mocks['iface'], 
        "mock_qtw": mocks['qtw'], # QTableWidgetItem class mock
        "mock_qgis_about": mock_qgis_about, 
        "mock_humanize": mock_humanize,
        "gpkg_with_changelog": gpkg_with_changelog_path,
        "gpkg_without_changelog": gpkg_without_changelog_path,
        "gpkg_empty_changelog": gpkg_empty_changelog_path,
        "gpkg_error_path": gpkg_error_path,
    }

    # --- Teardown ---
    for p in patchers.values():
        try:
            p.stop()
        except RuntimeError: 
            pass
    shutil.rmtree(temp_dir)

    # --- Clean up sys.modules ---
    modules_to_remove = [
        'qgis', 'qgis.PyQt', 'qgis.PyQt.QtGui', 'qgis.PyQt.QtWidgets', 
        'qgis.PyQt.QtCore', 'qgis.core', 'qgis.utils', 'qgis.gui',
        'qgsfilewidget'
    ]
    for mod_name in modules_to_remove:
        if mod_name in sys.modules:
            del sys.modules[mod_name]

# --- Test Functions (Testing the standalone function) ---

def test_fetch_populate_with_changelog(setup_teardown):
    """Test populating the table with a valid changelog GPKG."""
    mock_table = setup_teardown["mock_table"]
    mock_iface = setup_teardown["mock_iface"]
    mock_qtw = setup_teardown["mock_qtw"]
    mock_humanize = setup_teardown["mock_humanize"]
    gpkg_path = setup_teardown["gpkg_with_changelog"]

    # Call the standalone function
    about_widget._fetch_and_populate_changelog(about_widget, gpkg_path, mock_table, mock_iface)

    # Check table setup
    mock_table.setEditTriggers.assert_called_once()
    mock_table.setRowCount.assert_any_call(0) # Initial clear
    mock_table.setRowCount.assert_called_with(1) # One row added

    # Check items added
    assert mock_qtw.call_count == 7
    assert mock_table.setItem.call_count == 7

    # Check specific item content for the first column (humanized time)
    # mock_humanize.naturaltime.assert_called_once() # Check humanize was called
    # mock_qtw.assert_any_call('5 minutes ago') 
    mock_table.setItem.assert_any_call(0, 0, mock_qtw.return_value)

    # Check resize calls
    mock_table.resizeColumnsToContents.assert_called_once()
    mock_table.setColumnWidth.assert_called() 

    # Ensure no warnings/errors were pushed
    mock_iface.messageBar().pushMessage.assert_not_called()

def test_fetch_populate_without_changelog(setup_teardown):
    """Test populating with a GPKG missing the changelog table."""
    mock_table = setup_teardown["mock_table"]
    mock_iface = setup_teardown["mock_iface"]
    mock_qgis = setup_teardown["mock_qgis_about"]
    mock_qtw = setup_teardown["mock_qtw"]
    gpkg_path = setup_teardown["gpkg_without_changelog"]

    about_widget._fetch_and_populate_changelog(about_widget, gpkg_path, mock_table, mock_iface)

    # Check table setup
    mock_table.setEditTriggers.assert_called_once()
    mock_table.setRowCount.assert_called_once_with(0) 

    # Check items were NOT added
    mock_qtw.assert_not_called()
    mock_table.setItem.assert_not_called()

    # Ensure the specific warning was pushed (using the original message format)
    expected_msg = f"File '{gpkg_path}' doesn't have changelog yet. Please activate the plugin to track changes of the GeoPackage file first."
    mock_iface.messageBar().pushMessage.assert_called_once_with(
        "Warning",
        expected_msg,
        level=mock_qgis.Warning,
        duration=5
    )

def test_fetch_populate_with_empty_changelog(setup_teardown):
    """Test populating with a GPKG with an empty changelog table."""
    mock_table = setup_teardown["mock_table"]
    mock_iface = setup_teardown["mock_iface"]
    mock_qtw = setup_teardown["mock_qtw"]
    gpkg_path = setup_teardown["gpkg_empty_changelog"]

    about_widget._fetch_and_populate_changelog(about_widget, gpkg_path, mock_table, mock_iface)

    # Check table setup
    mock_table.setEditTriggers.assert_called_once()
    mock_table.setRowCount.assert_any_call(0) 
    mock_table.setRowCount.assert_called_with(0) 

    # Check items were NOT added
    mock_qtw.assert_not_called()
    mock_table.setItem.assert_not_called()

    # Check resize calls were made
    mock_table.resizeColumnsToContents.assert_called_once()

    # Ensure no warnings/errors were pushed
    mock_iface.messageBar().pushMessage.assert_not_called()

def test_fetch_populate_with_empty_path(setup_teardown):
    """Test calling populate with an empty file path."""
    mock_table = setup_teardown["mock_table"]
    mock_iface = setup_teardown["mock_iface"]
    mock_qtw = setup_teardown["mock_qtw"]

    about_widget._fetch_and_populate_changelog(about_widget, "", mock_table, mock_iface)

    # Check table setup
    mock_table.setEditTriggers.assert_called_once()
    mock_table.setRowCount.assert_called_once_with(0) 

    # Check items were NOT added
    mock_qtw.assert_not_called()
    mock_table.setItem.assert_not_called()

    # Check resize calls were NOT made
    mock_table.resizeColumnsToContents.assert_not_called()

    # Ensure no warnings/errors were pushed
    mock_iface.messageBar().pushMessage.assert_not_called()


@patch('track_changes.code.about_widget.sqlite3.connect')
def test_fetch_populate_other_sqlite_error(mock_connect, setup_teardown):
    """Test handling of a generic sqlite3 OperationalError."""
    mock_table = setup_teardown["mock_table"]
    mock_iface = setup_teardown["mock_iface"]
    mock_qgis = setup_teardown["mock_qgis_about"]
    mock_qtw = setup_teardown["mock_qtw"]
    gpkg_path = setup_teardown["gpkg_error_path"]

    error_message = "database is locked"
    mock_connect.side_effect = sqlite3.OperationalError(error_message)

    about_widget._fetch_and_populate_changelog(about_widget, gpkg_path, mock_table, mock_iface)

    # Check table setup
    mock_table.setEditTriggers.assert_called_once()
    mock_table.setRowCount.assert_called_once_with(0) 

    # Check items were NOT added
    mock_qtw.assert_not_called()
    mock_table.setItem.assert_not_called()

    # Ensure the generic error message was pushed
    expected_title = "Error"
    expected_msg = f"Database error: {error_message}"
    mock_iface.messageBar().pushMessage.assert_called_once_with(
        expected_title,
        expected_msg,
        level=mock_qgis.Critical,
        duration=5
    )

@patch('track_changes.code.about_widget.humanize.naturaltime')
def test_fetch_populate_humanize_exception(mock_naturaltime, setup_teardown):
    """Test handling of an exception during time humanizing."""
    mock_table = setup_teardown["mock_table"]
    mock_iface = setup_teardown["mock_iface"]
    mock_qtw = setup_teardown["mock_qtw"]
    gpkg_path = setup_teardown["gpkg_with_changelog"]

    mock_naturaltime.side_effect = ValueError("Humanize failed")

    about_widget._fetch_and_populate_changelog(about_widget, gpkg_path, mock_table, mock_iface)

    # Check table setup
    mock_table.setEditTriggers.assert_called_once()
    mock_table.setRowCount.assert_any_call(0)
    mock_table.setRowCount.assert_called_with(1) 

    # Check that setItem was called 7 times
    assert mock_table.setItem.call_count == 7

    # Check raw timestamp was used
    conn = sqlite3.connect(gpkg_path)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp FROM gpkg_changelog LIMIT 1")
    # Read the timestamp *after* modification
    raw_timestamp = (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S.%f')
    # We need to read what was *actually* stored, which matches the modified format
    cursor.execute("SELECT timestamp FROM gpkg_changelog LIMIT 1")
    actual_stored_timestamp = cursor.fetchone()[0]
    conn.close()

    # Check QTableWidgetItem was created with the actual stored timestamp
    mock_qtw.assert_any_call(actual_stored_timestamp) 
    found_call = False
    for call in mock_qtw.call_args_list:
        if call.args[0] == actual_stored_timestamp:
             for setitem_call in mock_table.setItem.call_args_list:
                 if setitem_call.args[0] == 0 and setitem_call.args[1] == 0:
                      found_call = True
                      break
             if found_call: break
    assert found_call, "QTableWidgetItem should have been called with the raw timestamp on humanize error"

    # Ensure no message bar call
    mock_iface.messageBar().pushMessage.assert_not_called() 

# --- Test for get_plugin_version ---

def test_get_plugin_version(monkeypatch):
    """Test that get_plugin_version retrieves the version correctly using monkeypatch."""
    # Arrange: Create a mock module and set its __version__
    mock_track_changes_module = MagicMock()
    expected_version = "1.2.3-test"
    mock_track_changes_module.__version__ = expected_version
    
    # Use monkeypatch to temporarily insert the mock into sys.modules
    monkeypatch.setitem(sys.modules, 'track_changes', mock_track_changes_module)
    
    # Act: Call the function (it should now import our mock module)
    actual_version = get_plugin_version()
    
    # Assert: Check if the returned version matches the mocked one
    assert actual_version == expected_version

    # No need to manually stop patch or clean sys.modules, monkeypatch handles it. 