from .code.main_plugin import TrackChangesPlugin

__version__ = "0.1.0"

def classFactory(iface):
    return TrackChangesPlugin(iface)
