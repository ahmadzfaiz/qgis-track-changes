from .code.main_plugin import TrackChangesPlugin

__version__ = "0.5.0-rc.3"

def classFactory(iface):
    return TrackChangesPlugin(iface)
