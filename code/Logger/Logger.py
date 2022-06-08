## @package LOGGER
## @author PZSP2-22L Firewall Team
## @date 05.005.2022
## @copyright All rights reserved
# Module implements logging feature executive.

import logging
from logging.handlers import RotatingFileHandler

## Documentation of Logger
#
# Logger is a class storing responsible for logging
# firewall  events in network to a log file

class Logger:

    ## Constructor
    # @param self The object pointer
    # @param logfile Path to file storing events logs
    # @param level Level of log: INFO, DEBUG, WARNING, ERROR
    def __init__(self, logfile, level=logging.DEBUG):
        self.logfile = logfile
        self.level = level
        logging.basicConfig(filename=logfile, format='%(levelname)s: %(asctime)s %(message)s', filemode='w', level=level)
        self.logger = logging.getLogger("Rotating Log")
        handler = RotatingFileHandler(logfile, maxBytes=524288,
                                      backupCount=3)
        self.logger.addHandler(handler)


    ## Method logging a message to the file
    # @param self The object pointer
    def log(self, message, level=logging.DEBUG):
        if level == logging.DEBUG:
            self.logger.debug(message)
        if level == logging.INFO:
            self.logger.info(message)
        if level == logging.WARNING:
            self.logger.warning(message)
        if level == logging.ERROR:
            self.logger.error(message)
