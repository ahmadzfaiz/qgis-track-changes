from .code.main_plugin import TrackChangesPlugin

__version__ = "0.9.2"

def classFactory(iface):
    return TrackChangesPlugin(iface)
