import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="A Little Backup Tool", application=app)