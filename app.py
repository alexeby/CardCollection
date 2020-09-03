import logging.config
import sys
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

# Arguments
action = sys.argv[1]
arg = sys.argv[2]


def main():
    if action == '-s':
        result = DatabaseHandler.execute_query({'name': arg})
        print(result)
    elif action == '-i':
        # Only allow fresh collection to import files.
        num_records = DatabaseHandler.count_number_records()
        if num_records == 0:
            files: List[str] = DATA_FILES.split(',')
            for file in files:
                DataImport.import_data(DATA_PATH + file)
        else:
            logger.error('Number of records in database is ' + str(num_records) + '. Should be 0 to import files.')


if __name__ == '__main__':
    main()


