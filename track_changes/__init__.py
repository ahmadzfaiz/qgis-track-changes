from .code.main_plugin import TrackChangesPlugin

__version__ = "0.6.0-rc.1"

def classFactory(iface):
    return TrackChangesPlugin(iface)
