from .code.main_plugin import TrackChangesPlugin

__version__ = "0.7.3"

def classFactory(iface):
    return TrackChangesPlugin(iface)
