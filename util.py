import logging
from logging import debug, info, warn, error, critical

class CustomFormatter(logging.Formatter):

    # grey = "\x1b[38;20m"
    # yellow = "\x1b[33;20m"
    # red = "\x1b[31;20m"
    # bold_red = "\x1b[31;1m"
    # reset = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    
    grey = "\x1b[100;37;1m"
    yellow = "\x1b[1;33m"
    red = "\x1b[1;31m"
    blue = "\x1b[1;34m"
    reset = "\x1b[0m"
    format = "%(levelname)s - %(message)s"
    
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

lg = logging.getLogger('mylogger')
lg.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())
lg.addHandler(ch)

lg.propagate = False

def cdebug(msg, *args, **kwargs):
    lg.debug(msg, *args, **kwargs)
    pass

def cinfo(msg, *args, **kwargs):
    lg.info(msg, *args, **kwargs)
    pass

def cwarn(msg, *args, **kwargs):
    lg.warn(msg, *args, **kwargs)
    pass

def cerror(msg, *args, **kwargs):
    lg.error(msg, *args, **kwargs)
    pass

def ccritical(msg, *args, **kwargs):
    lg.critical(msg, *args, **kwargs)
    pass