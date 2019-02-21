# Test configuration
import datetime
import os

from configuration import Configuration

c = Configuration()
assert os.path.isdir(c.home_dir), "Default dir was not exists"
assert os.path.isdir(c.log_dir), "Default log dir does not exists"

