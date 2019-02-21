import datetime
import json
import logging
import os
import random
import time
import configparser
from pathlib import Path


class Configuration:
    DEFAULT_HOME_DIR = os.path.join(os.path.expanduser('~'), '.albt')
    DEFAULT_LOG_DIR = os.path.join(os.path.expanduser('~'), '.albt')
    DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_HOME_DIR, 'config.json')
    DEFAULT_BACKUP_SERVER = 'localhost'
    DEFAULT_LOG_LEVEL = 'info'
    DEFAULT_MAX_TIME_BWEEN_BACKUPS = 3*24*60*60 # Three days in secs

    def __init__(self, config_file = ""):
        self.backup_server = self.DEFAULT_BACKUP_SERVER
        self.home_dir = self.DEFAULT_HOME_DIR
        self.log_dir = self.DEFAULT_LOG_DIR
        self.max_time_bween_backups = self.DEFAULT_MAX_TIME_BWEEN_BACKUPS
        self.log_level = self.DEFAULT_LOG_LEVEL
        self.rsync_cmd = ""
        self.setup(config_file) # If possible overrides defaults
        if not os.path.isdir(self.home_dir):
            os.makedirs(self.home_dir)
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)
        self.logger = None
        self.set_up_logging()
        self.last_backup_date = None
        self.last_backup_date_file = os.path.join(self.home_dir, 'last_backup')
        self.set_last_backup_date()

    def setup(self, config_file):
        if config_file == "":
            config_file = self.DEFAULT_CONFIG_FILE
        if os.path.isfile(config_file):
            with open(config_file) as json_config_file:
                conf = json.load(json_config_file)
                if 'home_dir' in conf:
                    self.home_dir = conf['home_dir']
                if 'backup_server' in conf:
                    self.backup_server = conf['backup_server']
                if 'log_dir' in conf:
                    self.log_dir = conf['log_dir']
                if 'max_time_bween_backups' in conf:
                    self.max_time_bween_backups = conf['max_time_bween_backups']
                if 'log_level' in conf:
                    self.log_level = conf['log_level']
                if 'rsync_cmd' in conf:
                    self.rsync_cmd = conf['rsync_cmd']
        # else the defaults will be used

    def set_up_logging(self):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
        random_digits = "{:03d}".format(random.randint(0, 999))
        log_file = os.path.join(self.log_dir, timestamp + "_" + random_digits + ".log")
        logger = logging.getLogger(self.log_dir)
        if self.log_level == 'info':
            logger.setLevel(logging.INFO)
        elif self.log_level == 'critical':
            logger.setLevel(logging.CRITICAL)
        elif self.log_level == 'error':
            logger.setLevel(logging.ERROR)
        elif self.log_level == 'warning':
            logger.setLevel(logging.WARNING)
        elif self.log_level == 'warn':
            logger.setLevel(logging.WARNING)
        elif self.log_level == 'debug':
            logger.setLevel(logging.DEBUG)
        elif self.log_level == 'notset':
            logger.setLevel(logging.NOTSET)
        else:
            logger.setLevel(logging.NOTSET)
        handler = logging.FileHandler(filename=log_file)
        handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s'))
        logger.addHandler(handler)
        self.logger = logger

    def set_last_backup_date(self):
        if os.path.isfile(self.last_backup_date_file):
            f = open(self.last_backup_date_file, 'r')
            self.last_backup_date = f.read()
        else:
            # Create the empty file
            open(self.last_backup_date_file, 'a').close()
            # Sets timestamp to 0 (Jan. 1st 1970)
            self.last_backup_date = datetime.datetime(1970, 1, 1, 1, 0).timestamp()
            f = open(self.last_backup_date_file, 'w')
            f.write(str(self.last_backup_date))
            f.close()

    def touch_last_backup_timestamp(self):
        self.last_backup_date = time.time()