import sys

from application import Application

app = Application()
exit_status = app.run(sys.argv)
sys.exit(exit_status)