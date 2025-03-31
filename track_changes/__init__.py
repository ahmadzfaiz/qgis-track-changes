from .code.main_plugin import TrackChangesPlugin

__version__ = "0.5.0-rc.2"

def classFactory(iface):
    return TrackChangesPlugin(iface)
