import gi

from albt_windows import AlbtWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ServerDownWindow(AlbtWindow):

    def __init__(self, message):
        AlbtWindow.__init__(self)
        self.button_try_again_pressed = False
        button_try = Gtk.Button(label="Try again")
        button_try.connect("clicked", self.on_try_again_clicked)

        label_msg = Gtk.Label(message, xalign=0)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(label_msg, True, True, 0)
        box.pack_start(button_try, True, True, 0)
        self.add(box)

    def on_try_again_clicked(self, button):
        # inform the main program that we want to try again
        Gtk.main_quit()
        self.button_try_again_pressed = True
