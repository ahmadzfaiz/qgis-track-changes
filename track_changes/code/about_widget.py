import sqlite3
import humanize
from datetime import datetime, timezone
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from qgis.core import Qgis
from qgis.utils import iface
from ..ui.about_dialog import Ui_About

def get_plugin_version():
    from track_changes import __version__
    return __version__


def _fetch_and_populate_changelog(file_path, table, iface_ref):
    """Connects to GPKG, fetches changelog, and populates the table.
    
    Handles database errors and missing table, reporting via iface message bar.
    """
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setRowCount(0)  # Clear table before populating

    if not file_path:
        return

    conn = None
    try:
        conn = sqlite3.connect(file_path, timeout=30)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                timestamp,
                data_version,
                author,
                layer_name,
                feature_id,
                message,
                data
            FROM gpkg_changelog
        """)

        data = cursor.fetchall()
        table.setRowCount(len(data))

        for row_idx, row in enumerate(data):
            timestamp = row[0]
            try:
                dt = datetime.fromisoformat(timestamp)
                pretty_time = humanize.naturaltime(datetime.now(timezone.utc) - dt)
            except Exception:
                pretty_time = timestamp

            row_data = (pretty_time,) + row[1:] # Create tuple for table row
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        max_width = 300
        for col in range(table.columnCount()):
            current_width = table.columnWidth(col)
            if current_width > max_width:
                table.setColumnWidth(col, max_width)

    except sqlite3.OperationalError as e:
        if "no such table: gpkg_changelog" in str(e):
            iface_ref.messageBar().pushMessage(
                "Warning",
                f"File '{file_path}' doesn't have changelog yet. Please activate the plugin to track changes of the GeoPackage file first.",
                level=Qgis.Warning,
                duration=5
            )
        else:
            iface_ref.messageBar().pushMessage(
                "Error",
                f"Database error: {e}",
                level=Qgis.Critical,
                duration=5
            )
    except Exception as e:
        iface_ref.messageBar().pushMessage(
            "Error",
            f"An unexpected error occurred: {e}",
            level=Qgis.Critical,
            duration=5
        )
        print(f"An unexpected error occurred: {e}") 
    finally:
        if conn:
            conn.close()


class AboutWidget(QDialog):
    """A dialog window for the About section."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_About()
        self.ui.setupUi(self)

        about_html = f"""
        <html><head/><body>
        <p>
            <span style=" font-weight:600;">QGIS Track Changes</span><br/>
            Version: <i>{get_plugin_version()}</i><br/><br/>
            This plugin helps track changes in vector layer data, including:<br/>
            - Feature modifications<br/>
            - Geometry updates<br/>
            - Attribute changes<br/><br/>
            It ensures data integrity by logging changes efficiently within QGIS.<br/><br/>
            <span style=" font-weight:600;">Developer:</span> Ahmad Zaenun Faiz<br/>
            <span style=" font-weight:600;">License:</span> GPL-3.0<br/><br/>
            For documentation, visit:<br/>
            <a href="https://qgis-track-changes.readthedocs.io/en/latest/">
                <span style=" text-decoration: underline; color:#419cff;">QGIS Track Changes Documentation</span>
            </a>
        </p>
        </body></html>
        """

        self.ui.label.setText(about_html)

        self.ui.inputGpkgFile.setFilter("GeoPackage (*.gpkg)")
        self.ui.inputGpkgFile.fileChanged.connect(self.populate_change_history)

    def populate_change_history(self, file_path):
        """Fill the change history table with changelog data by calling the helper function."""
        # Pass the actual table widget and the global iface reference
        _fetch_and_populate_changelog(file_path, self.ui.changeHistoryTable, iface)