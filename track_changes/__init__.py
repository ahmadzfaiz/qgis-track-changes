from .code.main_plugin import TrackChangesPlugin

__version__ = "0.2.0"

def classFactory(iface):
    return TrackChangesPlugin(iface)
