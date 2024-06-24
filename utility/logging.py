import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


def disable_aiogram():
    for logger in logging.root.manager.loggerDict:
        if 'aiogram' in logger:
            logging.getLogger(logger).disabled = True
    

def set_format():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%d.%m.%y [%H:%M:%S]"
    )


def get_logger(logfile: str):
    logger = logging.getLogger('main')
    handler = TimedRotatingFileHandler(
        filename=logfile+f'/vinyl.log', 
        when='midnight',
        interval=1,
        encoding='utf-8'
    )
    handler.suffix = datetime.now().strftime('%d.%m.%Y')
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(message)s",
        datefmt="%d.%m.%y [%H:%M:%S]"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


