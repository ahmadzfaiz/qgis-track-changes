from .code.main_plugin import TrackChangesPlugin

__version__ = "0.8.3"

def classFactory(iface):
    return TrackChangesPlugin(iface)
