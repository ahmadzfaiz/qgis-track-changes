from .code.main_plugin import TrackChangesPlugin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qgis.gui import QgsInterface

__version__ = "1.0.0"


def classFactory(iface: "QgsInterface") -> TrackChangesPlugin:
    return TrackChangesPlugin(iface)
