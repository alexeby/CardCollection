import logging
import os
import configparser
from logging import config
from cardcollection.dataimport import DataImport

# Initialize the log configuration file
logging.config.fileConfig(fname='init/log.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.info('Starting image download process')

# Initialize configuration file
parser = configparser.ConfigParser()
parser.read('init/conf.ini')
SITE_URL = parser.get('Websites', 'image_search_site')
IMG_DOWNLOAD = parser.get('Paths', 'img_download')
DATA_FILE_PATH = parser.get('Paths', 'data_dir')
logger.info('SITE_URL: ' + SITE_URL)
logger.info('IMG_DOWNLOAD: ' + IMG_DOWNLOAD)
logger.info('DATA_FILE_PATH: ' + DATA_FILE_PATH)

# Create download directory if not already exists
try:
    os.makedirs(IMG_DOWNLOAD, exist_ok=True)
except OSError as e:
    logger.exception(e)
    raise Exception


def main():
    pass


if __name__ == "__main__":
    main()
