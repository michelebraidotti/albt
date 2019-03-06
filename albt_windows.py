import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AlbtWindow(Gtk.Window):
    TITLE = "A Little Backup Tool"
    SUBTITLE = "In an attempt to help to remember backups!"

    def __init__(self):
        Gtk.Window.__init__(self, title=self.TITLE)
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)
        self.set_resizable(False)

        title_bar = Gtk.HeaderBar(title=self.TITLE)
        title_bar.set_subtitle(self.SUBTITLE)
        title_bar.set_show_close_button(True)

        self.set_titlebar(title_bar)
