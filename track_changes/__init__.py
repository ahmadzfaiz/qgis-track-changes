from .code.main_plugin import TrackChangesPlugin

__version__ = "0.7.4-rc.3"

def classFactory(iface):
    return TrackChangesPlugin(iface)
