from .code.main_plugin import TrackChangesPlugin

__version__ = "0.8.4"

def classFactory(iface):
    return TrackChangesPlugin(iface)
