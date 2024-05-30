import logging


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
    handler = logging.FileHandler(
        filename=logfile, 
        encoding='utf-8'
    )
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(message)s",
        datefmt="%d.%m.%y [%H:%M:%S]"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
