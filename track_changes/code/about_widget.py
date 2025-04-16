import json
import os
import re
import sqlite3
from typing import Optional
import humanize
from datetime import datetime, timezone
from PyQt5.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QAbstractItemView,
    QTableWidget,
    QWidget,
)
from qgis.core import Qgis
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QPalette, QColor
import pandas as pd
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ..ui.about_dialog import Ui_About

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qgis.gui import QgsInterface


def get_plugin_version() -> str:
    from track_changes import __version__

    return __version__


class AboutWidget(QDialog):
    """A dialog window for the About section."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.ui = Ui_About()
        self.ui.setupUi(self)
        mpl.rcParams["font.size"] = 8

        about_html = f"""
        <html><head/><body>
        <p>
            <img src="{self.get_icon_path("../icon.png")}" height="100"><br/>
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

        self.ui.inputGpkgFile.setFilter("GeoPackage (*.gpkg);;Log Files (*.log)")
        self.ui.inputGpkgFile.fileChanged.connect(self.populate_change_history)

        self.ui.file_compare_1.setFilter("GeoPackage (*.gpkg)")
        self.ui.file_compare_2.setFilter("GeoPackage (*.gpkg)")
        self.ui.compare_button.clicked.connect(self.compare_data)

    def compare_data(self) -> None:
        conn1 = sqlite3.connect(self.ui.file_compare_1.filePath())
        conn2 = sqlite3.connect(self.ui.file_compare_2.filePath())

        query = "SELECT DISTINCT data_version, data_version_id FROM gpkg_changelog"
        df1 = pd.read_sql_query(query, conn1)
        df2 = pd.read_sql_query(query, conn2)

        merged = df1.merge(
            df2,
            on="data_version",
            how="outer",
            suffixes=("_df1", "_df2"),
            indicator=True,
        )
        merged["status"] = merged.apply(self.compare_row, axis=1)
        self.insert_table_from_df(merged[["data_version", "status"]])

        conn1.close()
        conn2.close()

    def compare_row(self, row: pd.Series) -> str:
        if pd.isna(row["data_version_id_df1"]):
            return "⬅🟡 missing in left"
        elif pd.isna(row["data_version_id_df2"]):
            return "🟡➡ missing in right"
        elif row["data_version_id_df1"] == row["data_version_id_df2"]:
            return "✅ equal"
        else:
            return "🛑 not equal"

    def insert_table_from_df(self, df: pd.DataFrame) -> None:
        # Remove existing widgets in layout_compare
        while self.ui.layout_compare.count():
            old_widget = self.ui.layout_compare.takeAt(0).widget()
            if old_widget:
                old_widget.deleteLater()

        table = QTableWidget()
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)

        for row_idx, (_, row) in enumerate(df.iterrows()):
            for col_idx, (col_name, value) in enumerate(row.items()):
                item = QTableWidgetItem(str(value))

                # Apply color if column is 'status'
                if col_name == "status":
                    color = None
                    status = str(value).lower()
                    if "✅ equal" == status:
                        color = QColor("green")
                    elif "not equal" in status:
                        color = QColor("red")
                    elif "missing" in status:
                        color = QColor("orange")

                    if color:
                        item.setBackground(color)

                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        self.ui.layout_compare.addWidget(table)

    def get_icon_path(self, path: str) -> str:
        """Return the absolute path to the plugin icon."""
        return os.path.join(os.path.dirname(__file__), path)

    def populate_change_history(self, file_path: str) -> None:
        """Fill the change history table or handle log files depending on file type."""
        _, ext = os.path.splitext(file_path.lower())

        if ext == ".gpkg":
            self._fetch_and_populate_changelog(
                file_path, self.ui.changeHistoryTable, iface
            )
            self._fetch_and_populate_dashboard(file_path)
        elif ext == ".log":
            self._fetch_and_populate_logfile(file_path, self.ui.changeHistoryTable)
        else:
            print(f"Unsupported file type: {ext}")

    def round_down_to_6_hours(self, dt: datetime) -> str:
        timestamp = dt.replace(
            hour=(dt.hour // 6) * 6, minute=0, second=0, microsecond=0
        )
        return timestamp.strftime("%d %b %y\n%H:%M")

    def add_key_in_dict(self, my_dict: dict[str, int], key: str) -> None:
        if key in my_dict:
            my_dict[key] += 1
        else:
            my_dict[key] = 0

    def _fetch_and_populate_logfile(self, file_path: str, table: QTableWidget) -> None:
        # Dashboard Config
        data_counts = {
            10: 0,
            11: 0,
            20: 0,
            21: 0,
            22: 0,
            23: 0,
            24: 0,
            25: 0,
            26: 0,
            30: 0,
            31: 0,
            32: 0,
            33: 0,
            34: 0,
            35: 0,
            50: 0,
        }
        timeframe_counts: dict[str, int] = {}
        self.ui.version_picker.clear()

        # Table Config
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setRowCount(0)  # Clear table before populating

        if not file_path:
            return

        entries = self.parse_log(file_path)
        table.setRowCount(len(entries))

        for row_idx, entry in enumerate(entries):
            timestamp = entry["timestamp"]
            author = ""
            layer_id = ""
            feature_id = ""
            message = ""
            data = ""
            try:
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=timezone.utc)
                pretty_time = humanize.naturaltime(
                    datetime.now(timezone.utc) - timestamp
                )
            except Exception:
                pretty_time = timestamp

            self.add_key_in_dict(
                timeframe_counts, self.round_down_to_6_hours(timestamp)
            )

            if entry["code"] == "00":
                pattern = re.compile(
                    r'^(?P<author>.+?) activated the track changes of layer "(?P<layer_id>[^"]+)" using QGIS version (?P<qgis_version>[\w\.\-]+)$'
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "activate track change"
            elif entry["code"] == "01":
                pattern = re.compile(
                    r'^(?P<author>.+?) deactivated the track changes of layer "(?P<layer_id>[^"]+)" using QGIS version (?P<qgis_version>[\w\.\-]+)$'
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "deactivate track change"
            elif entry["code"] == "10":
                data_counts[10] += 1
                pattern = re.compile(
                    r'^(?P<author>[^>]+)\sstarted editing of layer\s"(?P<layer_id>[^"]+)"$'
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "start editing"
            elif entry["code"] == "11":
                data_counts[11] += 1
                pattern = re.compile(
                    r'^(?P<author>.+?)\sstopped editing of layer\s"(?P<layer_id>[^"]+)"$'
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "stop editing"
            elif entry["code"] == "20":
                data_counts[20] += 1
                pattern = re.compile(
                    r"^(?P<author>.+?) selecting feature\. Layer ID: (?P<layer_id>[^.]+)\. Feature ID: (?P<feature_id>\d+)\. Properties: (?P<data>\{.*\})$"
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    feature_id = groups["feature_id"]
                    message = "selecting feature"
                    data = groups["data"]
            elif entry["code"] == "21":
                data_counts[21] += 1
                pattern = re.compile(
                    r"^(?P<author>.+?) added feature\. Layer ID: (?P<layer_id>[^.]+)\. Feature ID: (?P<feature_id>-?\d+)\. Properties: (?P<data>\{.*\})$"
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    feature_id = groups["feature_id"]
                    message = "add feature"
                    data = groups["data"]
            elif entry["code"] == "22":
                data_counts[22] += 1
                pattern = re.compile(
                    r"^(?P<author>.+?) deleted feature\. Layer ID: (?P<layer_id>[^.]+)\. Feature ID: (?P<feature_id>-?\d+)$"
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    feature_id = groups["feature_id"]
                    message = "delete feature"
            elif entry["code"] == "23":
                data_counts[23] += 1
                pattern = re.compile(
                    r"^(?P<author>.+?) changed geometry\. Layer ID: (?P<layer_id>[^.]+)\. Feature ID: (?P<feature_id>-?\d+)\. New geometry: (?P<geometry>[A-Za-z]+ \([^)]+\))$"
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    feature_id = groups["feature_id"]
                    message = "geometry change"
                    data = json.dumps({"geometry": groups["geometry"]})
            elif entry["code"] == "26":
                data_counts[26] += 1
                pattern_1 = re.compile(
                    r"^Geometries changes by (?P<author>.+?) is committed\. Layer ID: (?P<layer_id>[^.]+)$"
                )
                pattern_2 = re.compile(
                    r"^Committed changed geometry by (?P<author>.+?)\. Layer ID: (?P<layer_id>[^.]+)\. Feature ID: (?P<feature_id>-?\d+)\. New geometry: (?P<geometry>[A-Za-z]+ \([^)]+\))$"
                )
                match_1 = pattern_1.match(entry["message"])
                match_2 = pattern_2.match(entry["message"])
                if match_1:
                    groups = match_1.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "commit geometry change"
                elif match_2:
                    groups = match_2.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    feature_id = groups["feature_id"]
                    message = "commited geometry change"
                    data = json.dumps({"geometry": groups["geometry"]})
            elif entry["code"] == "30":
                data_counts[30] += 1
                pattern = re.compile(
                    r"^(?P<author>.+?) added attribute\. Layer ID: (?P<layer_id>[^.]+)\. Field name: (?P<field_name>\w+)$"
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "add field"
                    data = json.dumps({"field_name": groups["field_name"]})
            elif entry["code"] == "31":
                data_counts[31] += 1
                pattern = re.compile(
                    r"^(?P<author>.+?) deleted attribute\. Layer ID: (?P<layer_id>[^.]+)\. Field name: (?P<field_name>\w+)$"
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "remove field"
                    data = json.dumps({"field_name": groups["field_name"]})
            elif entry["code"] == "32":
                data_counts[32] += 1
                pattern = re.compile(
                    r"^(?P<author>.+?) changed attribute\. Layer ID: (?P<layer_id>[^.]+)\. Feature ID: (?P<feature_id>-?\d+)\. Field name: (?P<field_name>\w+)\. Field content: (?P<field_content>.+)$"
                )
                match = pattern.match(entry["message"])
                if match:
                    groups = match.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "change attribute"
                    data = json.dumps(
                        {
                            "field_name": groups["field_name"],
                            "field_content": groups["field_content"],
                        }
                    )
            elif entry["code"] == "33":
                data_counts[33] += 1
                pattern_1 = re.compile(
                    r"^Attributes added by (?P<author>.+?) is committed\. Layer ID: (?P<layer_id>[^.]+)$"
                )
                pattern_2 = re.compile(
                    r"^Committed added attribute by (?P<author>.+?)\. Layer ID: (?P<layer_id>[^.]+)\. New field: (?P<field_name>\w+)\. Field type: (?P<field_type>\w+(?:\(\d+\))?)$"
                )
                match_1 = pattern_1.match(entry["message"])
                match_2 = pattern_2.match(entry["message"])
                if match_1:
                    groups = match_1.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "commit add field"
                elif match_2:
                    groups = match_2.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "committed add field"
                    data = json.dumps(
                        {
                            "field_name": groups["field_name"],
                            "field_type": groups["field_type"],
                        }
                    )
            elif entry["code"] == "34":
                data_counts[34] += 1
                pattern_1 = re.compile(
                    r"^Attributes deleted by (?P<author>.+?) is committed\. Layer ID: (?P<layer_id>[^.]+)$"
                )
                pattern_2 = re.compile(
                    r"^Committed deleted attribute by (?P<author>.+?)\. Layer ID: (?P<layer_id>[^.]+)\. Remove field: (?P<field_name>\w+)$"
                )
                match_1 = pattern_1.match(entry["message"])
                match_2 = pattern_2.match(entry["message"])
                if match_1:
                    groups = match_1.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "commit remove field"
                elif match_2:
                    groups = match_2.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "committed remove field"
                    data = json.dumps({"field_name": groups["field_name"]})
            elif entry["code"] == "35":
                data_counts[35] += 1
                pattern_1 = re.compile(
                    r"^Attributes changes by (?P<author>.+?) is committed\. Layer ID: (?P<layer_id>[^.]+)$"
                )
                pattern_2 = re.compile(
                    r"^Committed changed attribute by (?P<author>.+?)\. Layer ID: (?P<layer_id>[^.]+)\. Feature ID: (?P<feature_id>-?\d+)\. Field name: (?P<field_name>\w+)\. Field content: (?P<field_content>.+)$"
                )
                match_1 = pattern_1.match(entry["message"])
                match_2 = pattern_2.match(entry["message"])
                if match_1:
                    groups = match_1.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "commit change attribute"
                elif match_2:
                    groups = match_2.groupdict()
                    author = groups["author"]
                    layer_id = groups["layer_id"]
                    message = "committed change attribute"
                    data = json.dumps(
                        {
                            "field_name": groups["field_name"],
                            "field_content": groups["field_content"],
                        }
                    )

            row_data = (pretty_time, "", author, layer_id, feature_id, message, data)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        max_width = 300
        for col in range(table.columnCount()):
            current_width = table.columnWidth(col)
            if current_width > max_width:
                table.setColumnWidth(col, max_width)

        # Populate the dashboard
        self.populate_version_detail("No version", data_counts)
        self.populate_version_chart(data_counts, timeframe_counts)

    def parse_log(self, log_path: str) -> list[dict]:
        parsed_entries = []
        log_pattern = re.compile(
            r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - "
            r"(?P<level>\w+) - "
            r"(?P<code>\d+)\s\|\s(?P<message>.*)$"
        )

        with open(log_path, "r") as f:
            for line in f:
                match = log_pattern.match(line.strip())
                if match:
                    data = match.groupdict()
                    data["timestamp"] = datetime.strptime(
                        data["timestamp"], "%Y-%m-%d %H:%M:%S,%f"
                    )
                    parsed_entries.append(data)

        return parsed_entries

    def _fetch_and_populate_changelog(
        self, file_path: str, table: QTableWidget, iface_ref: "QgsInterface"
    ) -> None:
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

                row_data = (pretty_time,) + row[1:]  # Create tuple for table row
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
                    duration=5,
                )
            else:
                iface_ref.messageBar().pushMessage(
                    "Error", f"Database error: {e}", level=Qgis.Critical, duration=5
                )
        except Exception as e:
            iface_ref.messageBar().pushMessage(
                "Error",
                f"An unexpected error occurred: {e}",
                level=Qgis.Critical,
                duration=5,
            )
            print(f"An unexpected error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def _fetch_and_populate_dashboard(self, file_path: str) -> None:
        self.ui.version_picker.clear()
        self.file_path = file_path

        try:
            self.ui.version_picker.currentTextChanged.disconnect(self.change_dashboard)
        except Exception:
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

            cursor.execute(
                """
                SELECT 
                    json_extract(data, '$.old_version') AS previous_version
                FROM gpkg_changelog
                WHERE change_code = 50 
                    AND data_version = ?
                    AND json_extract(data, '$.message') != "No version update"
            """,
                (current_version,),
            )
            last_version = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT change_code, COUNT(*)
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY change_code
            """,
                (last_version,),
            )
            data_counts = {}
            for item in cursor.fetchall():
                data_counts[item[0]] = item[1]

            cursor.execute(
                """
                SELECT
                    (strftime('%s', timestamp) / 1800) * 1800 AS interval_start,
                    COUNT(*)
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY interval_start
                ORDER BY interval_start;
            """,
                (last_version,),
            )
            timeframe_counts = {}
            for item in cursor.fetchall():
                formatted = datetime.fromtimestamp(item[0], tz=timezone.utc).strftime(
                    "%d %b %y\n%H:%M"
                )
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

    def change_dashboard(self, version: str) -> None:
        try:
            conn = sqlite3.connect(self.file_path, timeout=30)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT 
                    json_extract(data, '$.old_version') AS previous_version
                FROM gpkg_changelog
                WHERE change_code = 50 
                    AND data_version = ?
                    AND json_extract(data, '$.message') != "No version update"
            """,
                (version,),
            )
            last_version = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT change_code, COUNT(*)
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY change_code
            """,
                (last_version,),
            )
            data_counts = {}
            for item in cursor.fetchall():
                data_counts[item[0]] = item[1]

            cursor.execute(
                """
                SELECT
                    (strftime('%s', timestamp) / 1800) * 1800 AS interval_start,
                    COUNT(*)
                FROM gpkg_changelog
                WHERE data_version = ?
                GROUP BY interval_start
                ORDER BY interval_start;
            """,
                (last_version,),
            )
            timeframe_counts = {}
            for item in cursor.fetchall():
                formatted = datetime.fromtimestamp(item[0], tz=timezone.utc).strftime(
                    "%d %b %y\n%H:%M"
                )
                timeframe_counts[formatted] = item[1]

            conn.close()
        except Exception:
            last_version = "0.0.0"
            data_counts = {}
            timeframe_counts = {}

        self.populate_version_detail(version, data_counts)
        self.populate_version_chart(data_counts, timeframe_counts)

    def populate_version_detail(
        self, last_version: str, data_counts: dict[int, int]
    ) -> None:
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

    def populate_version_chart(
        self, data_counts: dict[int, int], timeframe_counts: dict[str, int]
    ) -> None:
        # Get theme colors
        palette = iface.mainWindow().palette()
        self.bg_hex = palette.color(QPalette.Window).name()
        self.fg_hex = palette.color(QPalette.WindowText).name()

        # If the canvas is already created, just clear the figure
        if hasattr(self, "canvas"):
            self.figure.clear()  # type: ignore
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

    def draw_pie_chart(self, data: dict) -> None:
        # --- Pie Chart (Top)
        ax1 = self.figure.add_subplot(211)
        ax1.set_facecolor(self.bg_hex)
        ax1.set_title("Type of change", color=self.fg_hex)

        pie_labels = list(data.keys())
        pie_sizes = list(data.values())

        def autopct_filter(pct: float) -> str:
            return f"{pct:.1f}%" if pct >= 10 else ""

        ax1.pie(
            pie_sizes,
            labels=pie_labels,
            autopct=autopct_filter,
            startangle=140,
            textprops={"color": self.fg_hex},
        )

    def draw_line_chart(self, data: dict) -> None:
        # --- Line Chart (Bottom)
        ax2 = self.figure.add_subplot(212)
        ax2.set_facecolor(self.bg_hex)
        ax2.set_title("Timeframe of data changes (UTC)", color=self.fg_hex)

        x_labels = list(data.keys())
        y_values = list(data.values())
        x_numeric = list(range(len(x_labels)))

        # --- Plot the actual line
        ax2.plot(x_numeric, y_values, marker="o", color=self.fg_hex)

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
        filtered_labels = [
            label if i % label_interval == 0 else "" for i, label in enumerate(x_labels)
        ]
        ax2.set_xticks(x_numeric)
        ax2.set_xticklabels(
            filtered_labels, rotation=30, color=self.fg_hex, fontsize=5, ha="right"
        )
        ax2.tick_params(axis="x", bottom=False)
        for i, label in enumerate(filtered_labels):
            if label != "":
                ax2.axvline(x=i, ymin=0, ymax=0.05, color=self.fg_hex, linewidth=1)

        # --- Y-axis style
        ax2.tick_params(axis="y", colors=self.fg_hex)
        for spine in ax2.spines.values():
            spine.set_color(self.fg_hex)
