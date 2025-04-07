import sqlite3
import humanize
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from ..ui.about_dialog import Ui_About

def get_plugin_version():
    from track_changes import __version__
    return __version__

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
            Version: <span style="color:#007acc;">{get_plugin_version()}</span><br/><br/>
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
        """Fill the change history table with changelog data."""
        if file_path:
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
            table = self.ui.changeHistoryTable
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            table.setRowCount(len(data))

            for row_idx, row in enumerate(data):
                timestamp = row[0]
                try:
                    dt = datetime.fromisoformat(timestamp)
                    pretty_time = humanize.naturaltime(datetime.now() - dt)
                except Exception:
                    pretty_time = timestamp

                row = (pretty_time,) + row[1:]
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    table.setItem(row_idx, col_idx, item)

            table.resizeColumnsToContents()
            max_width = 300
            for col in range(table.columnCount()):
                current_width = table.columnWidth(col)
                if current_width > max_width:
                    table.setColumnWidth(col, max_width)