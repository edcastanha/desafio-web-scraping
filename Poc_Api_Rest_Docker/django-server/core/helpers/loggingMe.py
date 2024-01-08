import logging

logging.basicConfig(filename='logs/app-core.log')
# create logger
logger = logging.getLogger('** Scrapping App ::')
logger.setLevel(logging.DEBUG)


# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
