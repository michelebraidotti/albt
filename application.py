import time

import gi

from window import Window
from configuration import Configuration

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def backup_server_is_up():
    pass


class Application(Gtk.Application):

    def __init__(self):
        self.win = None
        self.conf = Configuration()
        Gtk.Application.__init__(self)

    def do_activate(self):
        if self.conf.last_backup_date + Configuration.MAX_TIME_BWEEN_BACKUPS > time.time():
            while not backup_server_is_up():
                continue
                # show a window that asks the user to activate the backup server
                # self.win = Window(self)
                # self.win.show_all()
            self.execute_backup()



    def do_startup(self):
        Gtk.Application.do_startup(self)


    def execute_backup(self):

            dialog_backup = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK_CANCEL, "Backup is old.")
            response = dialog_backup.format_secondary_text("You should backup your data now.\n"
                                                "Press OK to backup now, Cancel to backup later.")
            if response == Gtk.ResponseType.OK:
                while not backup_server_is_up():
                    dialog_bup_server = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                                          Gtk.ButtonsType.OK_CANCEL, "Backup server not available")
                    dialog_bup_server.format_secondary_text(
                        "Check backup server status and try again.")
                    response = dialog_bup_server.run()
                    if response == Gtk.ResponseType.OK:
                        # loop again to check if the server is online
                        continue
                    elif response == Gtk.ResponseType.CANCEL:
                        dialog_bup_server.destroy()
                        self.win.destroy()
                    dialog_bup_server.destroy()
            elif response == Gtk.ResponseType.CANCEL:
                dialog_backup.destroy()
                self.win.destroy()



