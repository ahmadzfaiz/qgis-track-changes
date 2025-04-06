from .code.main_plugin import TrackChangesPlugin

__version__ = "0.8.6-rc.1"

def classFactory(iface):
    return TrackChangesPlugin(iface)
