import logging
import os
import shlex
import subprocess
from logging.handlers import MemoryHandler

import gi
from configuration import Configuration
from report_window import ReportWindow
from server_down_window import ServerDownWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainApp:

    def __init__(self):
        self.conf = Configuration()
        self.log_contents = None
        self.logger = None
        self.set_up_logging()
        self.n_of_backup_server_ping_attempts = 0
        self.server_is_up = False

    def set_up_logging(self):
        self.logger = logging.getLogger(__name__)
        if self.conf.log_level == 'info':
            self.logger.setLevel(logging.INFO)
        elif self.conf.log_level == 'critical':
            self.logger.setLevel(logging.CRITICAL)
        elif self.conf.log_level == 'error':
            self.logger.setLevel(logging.ERROR)
        elif self.conf.log_level == 'warning':
            self.logger.setLevel(logging.WARNING)
        elif self.conf.log_level == 'warn':
            self.logger.setLevel(logging.WARNING)
        elif self.conf.log_level == 'debug':
            self.logger.setLevel(logging.DEBUG)
        elif self.conf.log_level == 'notset':
            self.logger.setLevel(logging.NOTSET)
        else:
            self.logger.setLevel(logging.NOTSET)
        handler = logging.FileHandler(filename=self.conf.log_file)
        handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s'))
        self.logger.addHandler(handler)

    def backup_server_is_up(self):
        response = os.system("ping -c 1 " + self.conf.backup_server)
        if response == 0:
            self.logger.info("Sever up!")
            self.server_is_up = True
            return True
        else:
            self.n_of_backup_server_ping_attempts += 1
            print("Sever Down! Attempt n." + str(self.n_of_backup_server_ping_attempts))
            self.logger.info("Sever Down! Attempt n." + str(self.n_of_backup_server_ping_attempts))
            self.server_is_up = False
            return False

    def execute_backup(self):
        self.logger.info("***** Backup starting ... ")
        self.logger.info("Rsync command: " + self.conf.rsync_cmd)

        print(self.conf.rsync_cmd)
        out = subprocess.Popen(shlex.split(self.conf.rsync_cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()

        self.logger.info("**** Rsync output: ")
        self.logger.info(stdout.decode('ascii'))
        if stderr:
            self.logger.error("**** Rsync errors: ")
            self.logger.error(stderr.decode('ascii'))
        if stderr:
            win = ReportWindow(stdout.decode('ascii'), errors=stderr.decode('ascii'))
        else:
            win = ReportWindow(stdout.decode('ascii'), errors=None)
        win.show_all()
        Gtk.main()

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
main_app.logger.info("albt started")
main_app.check_server()
if main_app.server_is_up:
    main_app.execute_backup()
main_app.logger.info("albt ended")