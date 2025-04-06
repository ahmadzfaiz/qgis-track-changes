from .code.main_plugin import TrackChangesPlugin

__version__ = "0.7.3-rc.1"

def classFactory(iface):
    return TrackChangesPlugin(iface)
