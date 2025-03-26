from .code.main_plugin import TrackChangesPlugin

__version__ = "0.4.2"

def classFactory(iface):
    return TrackChangesPlugin(iface)
