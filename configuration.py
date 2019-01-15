import datetime
import os
import time
from pathlib import Path


class Configuration:
    DEFAULT_CONFIG_DIR = os.path.join(Path.home(), '.albt')
    DEFAULT_LAST_BACKUP_FLAG = os.path.join(DEFAULT_CONFIG_DIR, 'last_backup')

    def __init__(self):
        self.last_backup_date
        # look for the config dir
        # check the last backup
        if not os.path.isdir(self.DEFAULT_CONFIG_DIR):
            os.makedirs(self.DEFAULT_CONFIG_DIR)
        if os.path.isfile(self.DEFAULT_LAST_BACKUP_FLAG):
            self.last_backup_date = self.read_last_backup_date()
        else:
            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
            self.last_backup_date = datetime.date(1970, 1, 1)

    def read_last_backup_date(self):
        f = open(self.DEFAULT_LAST_BACKUP_FLAG, 'r')
        time_string = f.read()
        return datetime.datetime.fromtimestamp(float(time_string))

    def write_backup_date(self):
        # Will overwrite the default last backp info with
        # current time and date
        f = open(self.DEFAULT_LAST_BACKUP_FLAG, 'w')
        f.write(str(time.time()))
        f.close()

