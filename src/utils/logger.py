import logging

log_format = '%(funcName) -35s %(lineno) -5d: %(message)s'

logging.basicConfig(
    level=logging.INFO, 
    format=log_format, 
    handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)