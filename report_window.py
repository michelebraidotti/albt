import gi

from albt_windows import AlbtWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ReportWindow(AlbtWindow):

    def __init__(self, output, errors):
        AlbtWindow.__init__(self)
        self.set_default_size(300, 450)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        output_label = Gtk.Label("Output")
        output_text_vew = ReportWindow.build_text_view(output)
        box.pack_start(output_label, True, True, 0)
        box.pack_start(output_text_vew, True, True, 0)

        if errors:
            errors_label = Gtk.Label("Errors")
            errors_text_vew = ReportWindow.build_text_view(errors)
            box.pack_start(errors_label, True, True, 0)
            box.pack_start(errors_text_vew, True, True, 0)

        self.add(box)

    def build_text_view(content):
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)

        text_buffer = Gtk.TextBuffer()
        text_buffer.set_text(content)

        text_view = Gtk.TextView()
        text_view.set_buffer(text_buffer)

        scrolled_window.add(text_view)
        return scrolled_window
