from .code.main_plugin import TrackChangesPlugin

__version__ = "0.7.5"

def classFactory(iface):
    return TrackChangesPlugin(iface)
