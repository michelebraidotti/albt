# Test configuration
import datetime
import os

from configuration import Configuration

c = Configuration()
assert os.path.isdir(Configuration.DEFAULT_CONFIG_DIR), "Default dir was not created"
assert os.path.isfile(Configuration.DEFAULT_LAST_BACKUP_DATE_FILE), "Default backup date file is not created"
assert c.read_last_backup_timestamp() == 0, "Initial timestamp should be 0 (Jan. 1st, 1970)"

