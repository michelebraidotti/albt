import datetime
import logging
import os
import time
import configparser
from pathlib import Path


class Configuration:
    DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.albt')
    DEFAULT_LAST_BACKUP_DATE_FILE = os.path.join(DEFAULT_CONFIG_DIR, 'last_backup')
    DEFAULT_BACKUP_SERVER = 'silverbox'
    MAX_TIME_BWEEN_BACKUPS = 3*24*60*60 # Three days in secs

    def __init__(self):
        self.last_backup_date = None
        self.backup_server = self.DEFAULT_BACKUP_SERVER
        # look for the config dir
        # check the last backup
        if not os.path.isdir(self.DEFAULT_CONFIG_DIR):
            os.makedirs(self.DEFAULT_CONFIG_DIR)
        if os.path.isfile(self.DEFAULT_LAST_BACKUP_DATE_FILE):
            self.last_backup_date = self.read_last_backup_timestamp()
        else:
            # Create the empty file
            open(self.DEFAULT_LAST_BACKUP_DATE_FILE, 'a').close()
            # Sets timestamp to 0 (Jan. 1st 1970)
            self.last_backup_date = datetime.datetime(1970, 1, 1, 1, 0).timestamp()
            self.write_last_backup_timestamp()
        # Read config file
        if os.path.isfile(os.path.join(self.DEFAULT_CONFIG_DIR, 'conf')):
            c = configparser.ConfigParser()
            c.read()
        # Set up logging
        log_file = os.path.join(self.output_dir, self.LOG_FILE_NAME)
        logger = logging.getLogger(self.output_dir)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename=log_file)
        handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s'))
        logger.addHandler(handler)
        self.logger = logger

    def read_last_backup_timestamp(self):
        f = open(self.DEFAULT_LAST_BACKUP_DATE_FILE, 'r')
        timestamp_str = f.read()
        return float(timestamp_str)

    def touch_last_backup_timestamp(self):
        self.last_backup_date = time.time()

    def write_last_backup_timestamp(self):
        f = open(self.DEFAULT_LAST_BACKUP_DATE_FILE, 'w')
        f.write(str(self.last_backup_date))
        f.close()
