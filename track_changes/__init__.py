from .code.main_plugin import TrackChangesPlugin

__version__ = "0.8.0"

def classFactory(iface):
    return TrackChangesPlugin(iface)
