import requests
import time
import logging
import datetime
import os
from requests.exceptions import Timeout

DATA_DIR = r'C:\dev\index_polo\pages'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
fh = logging.FileHandler('index_page.log')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


def get_page_w_backoff(page, max_backoff=512, timeout=20):
    logger.info('Getting page')
    backoff = 1
    response = None
    while not response and backoff <= max_backoff:
        try:
            response = requests.get(page, timeout=timeout)
        except Timeout:
            logger.debug('Timed out, retrying in {0}s'.format(backoff))
            time.sleep(backoff)
            backoff *= 2
    response = requests.get(page)
    return datetime.datetime.now(), response.text


def index_page():
    page = 'https://coinmarketcap.com/currencies/ethereum/#markets'
    time, response = get_page_w_backoff(page)
    filename = os.path.join(DATA_DIR, '{0}.html'.format(time.strftime('%m-%d-%Y-%M-%S-%f')))
    with open(filename, 'w') as f:
        f.write(response)
        logger.info('Saved to page {0}'.format(f))

if __name__ == '__main__':
    index_page()
