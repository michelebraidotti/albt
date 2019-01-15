import gi

from window import Window

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = Window(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)