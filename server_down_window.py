import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ServerDownWindow(Gtk.Window):

    def __init__(self, message):
        Gtk.Window.__init__(self, title="A Little Backup Tool")
        self.button_try_again_pressed = False
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)

        title_bar = Gtk.HeaderBar(title="A Little Backup Tool")
        title_bar.set_subtitle("In an attempt to help remembering backups!")
        title_bar.set_show_close_button(True)

        button_try = Gtk.Button(label="Try again")
        button_try.connect("clicked", self.on_try_again_clicked)

        label_msg = Gtk.Label(message, xalign=0)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(label_msg, True, True, 0)
        box.pack_start(button_try, True, True, 0)
        self.add(box)

        self.set_titlebar(title_bar)

    def on_try_again_clicked(self, button):
        # inform the main program that we want to try again
        Gtk.main_quit()
        self.button_try_again_pressed = True
