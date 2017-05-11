import logging
import sys

DEBUG_LOG_FILENAME = "log/info.log"

# set up formatting
fh_formatter = logging.Formatter("%(levelname)-5s %(asctime)s %(module)s.%(funcName)s() [%(lineno)d]: %(message)s", "%Y-%m-%d %H:%M:%S")
sh_formatter = logging.Formatter("%(message)s")

# set up logging to STDOUT for all levels INFO and higher
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(sh_formatter)

# set up logging to a file for all levels DEBUG and higher
fh = logging.FileHandler(DEBUG_LOG_FILENAME)
fh.setLevel(logging.DEBUG)
fh.setFormatter(fh_formatter)

# create Logger object
mylogger = logging.getLogger('MyLogger')
mylogger.setLevel(logging.DEBUG)
mylogger.addHandler(sh)    # enabled: stdout
mylogger.addHandler(fh)    # enabled: file

# create shortcut functions
debug = mylogger.debug
info = mylogger.info
warning = mylogger.warning
error = mylogger.error
critical = mylogger.critical