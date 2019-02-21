import os
import sys
import time

import gi
from configuration import Configuration
from server_down_window import ServerDownWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainApp():

    def __init__(self):
        self.conf = Configuration()
        self.n_of_backup_server_ping_attempts = 0
        self.server_is_up = False

    def backup_server_is_up(self):
        response = os.system("ping -c 1 " + self.conf.backup_server)
        if response == 0:
            self.server_is_up = True
            return True
        else:
            self.n_of_backup_server_ping_attempts += 1
            self.server_is_up = False
            return False

    def execute_backup(self):
        print(self.conf.rsync_cmd)
        pass

    def check_server(self):
        while not self.backup_server_is_up():
            if self.n_of_backup_server_ping_attempts == 1:
                message = "The backup server '" + self.conf.backup_server + \
                          "' seems to be down. Check the server connection and try again."
            else:
                message = "Failed to contact the backup server '" + self.conf.backup_server \
                          + "', please try again (attempt " + str(self.n_of_backup_server_ping_attempts - 1) + ")."
            win = ServerDownWindow(message)
            win.show_all()
            Gtk.main()
            if win.button_try_again_pressed:
                win.destroy()
                continue
            else:
                break


main_app = MainApp()
main_app.check_server()
if main_app.server_is_up:
    main_app.execute_backup()
# if conf.last_backup_date + Configuration.MAX_TIME_BWEEN_BACKUPS > time.time():
#    execute_backup()

# app = Application()
# exit_status = app.run(sys.argv)
# sys.exit(exit_status)
