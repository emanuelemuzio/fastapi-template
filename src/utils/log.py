import logging
from .date import now
from ..config.constants import YYYY_MM_DD

def get_logger():

    logging.basicConfig(
        filename=f"log/{now(format=YYYY_MM_DD)}.log",
        filemode='a',
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    logger = logging.getLogger('appLogger') 

    return logger