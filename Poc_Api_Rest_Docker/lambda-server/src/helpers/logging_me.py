import logging

logging.basicConfig(filename='logs/jobs-scrapping.log')
logger = logging.getLogger('** Simple ::')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)