import logging
import os
import shutil
from logging import config
from typing import List

from carddatahandler import PATHS_PROPERTIES, DATA_IMPORTER_PROPERTIES
from carddatahandler.databasehandler import DatabaseHandler
from carddatahandler.dataimporter import DataImport

# Initialize the log configuration file
logging.config.fileConfig(fname='init/log.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.info('Starting image download process')

# Initialize Paths
PATH_IMG_DOWNLOAD = PATHS_PROPERTIES.get('img_download_dir')
DATA_PATH = PATHS_PROPERTIES.get('data_dir')

# Initialize DataImporter
DATA_FILES = DATA_IMPORTER_PROPERTIES.get('data_files')

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
    value = input("What would you like to do?\n")
    if value == '1':
        # Only allow fresh collection to import files.
        num_records = DatabaseHandler.count_number_records()
        if num_records == 0:
            files: List[str] = DATA_FILES.split(',')
            for file in files:
                DataImport.import_data(DATA_PATH+file)
        else:
            logger.error('Number of records in database is ' + str(num_records) + '. Should be 0 to import files.')
    elif value == '2':
        pass
    elif value == '3':
        pass
    elif value == 'deletealldata':
        DatabaseHandler.delete_all_records()
        try:
            shutil.rmtree(PATH_IMG_DOWNLOAD)
            logger.info('Deleted path: ' + PATH_IMG_DOWNLOAD)
        except OSError as ose:
            logger.error(ose)
    pass


if __name__ == "__main__":
    main()
