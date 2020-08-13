import logging
import os
import configparser
from logging import config
from carddatahandler.dataimporter import DataImport

# Initialize the log configuration file
logging.config.fileConfig(fname='init/log.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.info('Starting image download process')

# Initialize configuration file
parser = configparser.ConfigParser()
parser.read('init/conf.ini')

# Initialize Paths
PATH_IMG_DOWNLOAD = parser.get('Paths', 'img_download')
PATH_DATA_FILES = parser.get('Paths', 'data_dir')

# Initialize DataImporter

# Initialize WebHandler
DS_CARD_SEARCH_SITE_API = parser.get('Web_Handler', 'card_search_site_api')

logger.info('DS_CARD_SEARCH_SITE_API: ' + DS_CARD_SEARCH_SITE_API)
logger.info('PATH_IMG_DOWNLOAD: ' + PATH_IMG_DOWNLOAD)
logger.info('PATH_DATA_FILES: ' + PATH_DATA_FILES)

# Create download directory if not already exists
try:
    os.makedirs(PATH_IMG_DOWNLOAD, exist_ok=True)
except OSError as e:
    logger.exception(e)
    raise Exception


def main():
    print("1. Import Data")
    print("2. Search")
    print("3. Cancel")
    value = input("What would you like to do?")
    if value == 1:
        DataImport.import_data('test/test_data/Test_Yugioh_Catalog_Monster_Full.csv')
    elif value == 2:
        pass
    pass


if __name__ == "__main__":
    main()
