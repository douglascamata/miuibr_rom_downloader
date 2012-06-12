import logging

def configura_log(nivel):
    LOG_FORMAT = '%(levelname)s - %(asctime)s - %(message)s'
    log_level = getattr(logging, nivel.upper(), None)
    logging.basicConfig(format=LOG_FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p', level=log_level)
    return logging.getLogger('miui_dev_downloader')

def configura_log_db(nivel):
    log_level = nivel.upper() or logging.WARNING
    logging.getLogger('sqlalchemy.engine').setLevel(log_level)
