from .code.main_plugin import TrackChangesPlugin

__version__ = "0.7.7"

def classFactory(iface):
    return TrackChangesPlugin(iface)
