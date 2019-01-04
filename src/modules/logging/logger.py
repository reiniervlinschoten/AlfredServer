import logging
import logging.handlers as handlers


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # TODO: make windows compatible
    fh = handlers.RotatingFileHandler("logs/" + name + '.log', maxBytes=5000000, backupCount=2)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
