from .main_plugin import TrackChangesPlugin

def classFactory(iface):
    return TrackChangesPlugin(iface)