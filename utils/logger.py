import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('NodeX-main-log')
logger.setLevel('DEBUG')
handler = RotatingFileHandler(
    filename = 'nodex.log',
    maxBytes = 50 * 1024 * 1024,
    backupCount = 5,
    encoding = 'utf-8',
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

handler.setFormatter(formatter)
logger.addHandler(handler)
