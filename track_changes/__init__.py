from .code.main_plugin import TrackChangesPlugin

__version__ = "1.0.0"

def classFactory(iface):
    return TrackChangesPlugin(iface)
