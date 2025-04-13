import json
import sqlite3
import humanize
from datetime import datetime, timezone
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from qgis.core import Qgis
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPalette
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        mpl.rcParams['font.size'] = 8

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
        self._fetch_and_populate_changelog(file_path, self.ui.changeHistoryTable, iface)
        self._fetch_and_populate_dashboard(file_path)

    def _fetch_and_populate_changelog(self, file_path, table, iface_ref):
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
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
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

    def _fetch_and_populate_dashboard(self, file_path):
        self.ui.version_picker.clear()
        self.file_path = file_path

        try:
            self.ui.version_picker.currentTextChanged.disconnect(self.change_dashboard)
        except:
            pass

        try:
            conn = sqlite3.connect(self.file_path, timeout=30)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT data_version
                FROM gpkg_changelog
                ORDER BY id DESC 
                LIMIT 1;
            """)
            current_version = cursor.fetchone()[0]

            cursor.execute("""
                SELECT 
                    json_extract(data, '$.old_version') AS previous_version
                FROM gpkg_changelog
                WHERE change_code = 50 
                    AND data_version = ?
                    AND json_extract(data, '$.message') != "No version update"
            """, (current_version,))
            last_version = cursor.fetchone()[0]

            cursor.execute("""
                SELECT change_code, COUNT(*)
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY change_code
            """, (last_version,))
            data_counts = {}
            for item in cursor.fetchall():
                data_counts[item[0]] = item[1]

            cursor.execute("""
                SELECT
                    (strftime('%s', timestamp) / 1800) * 1800 AS interval_start,
                    COUNT(*)
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY interval_start
                ORDER BY interval_start;
            """, (last_version,))
            timeframe_counts = {}
            for item in cursor.fetchall():
                formatted = datetime.fromtimestamp(item[0], tz=timezone.utc).strftime('%d %b %y\n%H:%M')
                timeframe_counts[formatted] = item[1]

            cursor.execute("""
                SELECT DISTINCT data_version
                FROM gpkg_changelog
                ORDER BY id DESC
            """)
            version_list = [item[0] for item in cursor.fetchall()]

            conn.close()
        except Exception:
            last_version = "0.0.0"
            data_counts = {}
            timeframe_counts = {}
            version_list = []

        self.ui.version_picker.addItems(version_list)
        
        self.populate_version_detail(current_version, data_counts)
        self.populate_version_chart(data_counts, timeframe_counts)

        self.ui.version_picker.currentTextChanged.connect(self.change_dashboard)

    def change_dashboard(self, version):
        try:
            conn = sqlite3.connect(self.file_path, timeout=30)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    json_extract(data, '$.old_version') AS previous_version
                FROM gpkg_changelog
                WHERE change_code = 50 
                    AND data_version = ?
                    AND json_extract(data, '$.message') != "No version update"
            """, (version,))
            last_version = cursor.fetchone()[0]

            cursor.execute("""
                SELECT change_code, COUNT(*)
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY change_code
            """, (last_version,))
            data_counts = {}
            for item in cursor.fetchall():
                data_counts[item[0]] = item[1]

            cursor.execute("""
                SELECT
                    (strftime('%s', timestamp) / 1800) * 1800 AS interval_start,
                    COUNT(*)
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY interval_start
                ORDER BY interval_start;
            """, (last_version,))
            timeframe_counts = {}
            for item in cursor.fetchall():
                formatted = datetime.fromtimestamp(item[0], tz=timezone.utc).strftime('%d %b %y\n%H:%M')
                timeframe_counts[formatted] = item[1]

            conn.close()
        except Exception:
            last_version = "0.0.0"
            data_counts = {}
            timeframe_counts = {}
        
        self.populate_version_detail(version, data_counts)
        self.populate_version_chart(data_counts, timeframe_counts)

    def populate_version_detail(self, last_version, data_counts):
        code10 = data_counts.get(10, 0)
        code11 = data_counts.get(11, 0)
        code20 = data_counts.get(20, 0)
        code21 = data_counts.get(21, 0)
        code22 = data_counts.get(22, 0)
        code23 = data_counts.get(23, 0)
        code24 = data_counts.get(24, 0)
        code25 = data_counts.get(25, 0)
        code26 = data_counts.get(26, 0)
        code30 = data_counts.get(30, 0)
        code31 = data_counts.get(31, 0)
        code32 = data_counts.get(32, 0)
        code33 = data_counts.get(33, 0)
        code34 = data_counts.get(34, 0)
        code35 = data_counts.get(35, 0)
        code50 = data_counts.get(50, 0)

        data_version_html = f"""
        <html><head/><body>
        <p><span style=" font-size:14pt;">Committed data version:</span></p>
        <p><span style=" font-size:48pt; font-weight:600;">{last_version}</span></p>
        <p><span style=" font-size:12pt;">Data changes:</span></p>
        <table border="1" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;" cellspacing="0" cellpadding="2">
            <thead>
                <tr>
                    <td><p align="center"><span style=" font-size:10px; font-weight:600;">Code</span></p></td>
                    <td><p align="center"><span style=" font-size:10px; font-weight:600;">Data Changes</span></p></td>
                    <td><p align="center"><span style=" font-size:10px; font-weight:600;">Count</span></p></td>
                </tr>
            </thead>
            <tr>
                <td><p><span style=" font-size:10px;">10</span></p></td>
                <td><p><span style=" font-size:10px;">start editing</span></p></td>
                <td><p><span style=" font-size:10px;">{code10}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">11</span></p></td>
                <td><p><span style=" font-size:10px;">stop editing</span></p></td>
                <td><p><span style=" font-size:10px;">{code11}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">20</span></p></td>
                <td><p><span style=" font-size:10px;">features selection</span></p></td>
                <td><p><span style=" font-size:10px;">{code20}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">21</span></p></td>
                <td><p><span style=" font-size:10px;">feature add</span></p></td>
                <td><p><span style=" font-size:10px;">{code21}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">22</span></p></td>
                <td><p><span style=" font-size:10px;">feature delete</span></p></td>
                <td><p><span style=" font-size:10px;">{code22}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">23</span></p></td>
                <td><p><span style=" font-size:10px;">feature geometry change</span></p></td>
                <td><p><span style=" font-size:10px;">{code23}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">24</span></p></td>
                <td><p><span style=" font-size:10px;">feature add committed</span></p></td>
                <td><p><span style=" font-size:10px;">{code24}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">25</span></p></td>
                <td><p><span style=" font-size:10px;">feature delete committed</span></p></td>
                <td><p><span style=" font-size:10px;">{code25}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">26</span></p></td>
                <td><p><span style=" font-size:10px;">features geometry change committed</span></p></td>
                <td><p><span style=" font-size:10px;">{code26}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">30</span></p></td>
                <td><p><span style=" font-size:10px;">attribute add</span></p></td>
                <td><p><span style=" font-size:10px;">{code30}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">31</span></p></td>
                <td><p><span style=" font-size:10px;">attribute delete</span></p></td>
                <td><p><span style=" font-size:10px;">{code31}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">32</span></p></td>
                <td><p><span style=" font-size:10px;">attribute value change</span></p></td>
                <td><p><span style=" font-size:10px;">{code32}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">33</span></p></td>
                <td><p><span style=" font-size:10px;">attribute add committed</span></p></td>
                <td><p><span style=" font-size:10px;">{code33}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">34</span></p></td>
                <td><p><span style=" font-size:10px;">attribute delete committed</span></p></td>
                <td><p><span style=" font-size:10px;">{code34}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">35</span></p></td>
                <td><p><span style=" font-size:10px;">attribute values change committed</span></p></td>
                <td><p><span style=" font-size:10px;">{code35}</span></p></td>
            </tr>
            <tr>
                <td><p><span style=" font-size:10px;">50</span></p></td>
                <td><p><span style=" font-size:10px;">attribute values change committed</span></p></td>
                <td><p><span style=" font-size:10px;">{code50}</span></p></td>
            </tr>
        </table>
        </body></html>
        """
        self.ui.data_version_description.setText(data_version_html)  

    def populate_version_chart(self, data_counts, timeframe_counts):
        # Get theme colors
        palette = iface.mainWindow().palette()
        self.bg_hex = palette.color(QPalette.Window).name()
        self.fg_hex = palette.color(QPalette.WindowText).name()

        # If the canvas is already created, just clear the figure
        if hasattr(self, 'canvas'):
            self.figure.clear()  # Clear the figure
        else:
            # Create new figure + canvas only if not already created
            self.figure = Figure(facecolor=self.bg_hex)
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setStyleSheet(f"background-color: {self.bg_hex};")
            self.canvas.setAttribute(Qt.WA_TranslucentBackground)
            self.canvas.setAutoFillBackground(False)

            # Remove the old canvas widget, if any
            if self.ui.Chart.count() > 0:
                old_widget = self.ui.Chart.takeAt(0)
                if old_widget and old_widget.widget():
                    old_widget.widget().deleteLater()

            # Add the new canvas to UI container
            self.ui.Chart.addWidget(self.canvas)

        # Draw the chart
        self.figure.clear()
        self.draw_pie_chart(data_counts)
        self.draw_line_chart(timeframe_counts)
        self.canvas.draw()

    def draw_pie_chart(self, data):
        # --- Pie Chart (Top)
        ax1 = self.figure.add_subplot(211)
        ax1.set_facecolor(self.bg_hex)
        ax1.set_title("Type of change", color=self.fg_hex)

        pie_labels = list(data.keys())
        pie_sizes = list(data.values())

        def autopct_filter(pct):
            return f'{pct:.1f}%' if pct >= 10 else ''

        ax1.pie(
            pie_sizes,
            labels=pie_labels,
            autopct=autopct_filter,
            startangle=140,
            textprops={'color': self.fg_hex}
        )

    def draw_line_chart(self, data):
        # --- Line Chart (Bottom)
        ax2 = self.figure.add_subplot(212)
        ax2.set_facecolor(self.bg_hex)
        ax2.set_title("Timeframe of data changes", color=self.fg_hex)

        x_labels = list(data.keys())
        y_values = list(data.values())
        x_numeric = list(range(len(x_labels)))

        # --- Plot the actual line
        ax2.plot(x_numeric, y_values, marker='o', color=self.fg_hex)

        # --- Determine label interval
        length = len(x_numeric)
        if length <= 6:
            label_interval = 1
        elif length <= 12:
            label_interval = 2
        elif length <= 30:
            label_interval = 3
        else:
            label_interval = 5

        # --- Filter labels
        filtered_labels = [label if i % label_interval == 0 else '' for i, label in enumerate(x_labels)]
        ax2.set_xticks(x_numeric)
        ax2.set_xticklabels(filtered_labels, rotation=30, color=self.fg_hex, fontsize=5, ha='right')
        ax2.tick_params(axis='x', bottom=False)
        for i, label in enumerate(filtered_labels):
            if label != '':
                ax2.axvline(x=i, ymin=0, ymax=0.05, color=self.fg_hex, linewidth=1)

        # --- Y-axis style
        ax2.tick_params(axis='y', colors=self.fg_hex)
        for spine in ax2.spines.values():
            spine.set_color(self.fg_hex)