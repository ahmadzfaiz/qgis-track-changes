from .code.main_plugin import TrackChangesPlugin

__version__ = "0.6.1"

def classFactory(iface):
    return TrackChangesPlugin(iface)
