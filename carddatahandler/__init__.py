import configparser

# Initialize configuration file
parser = configparser.ConfigParser()
parser.read('init/conf.ini')

# Initialize Paths
PATHS_PROPERTIES = {
    'home_dir': parser.get('Paths', 'home_dir'),
    'img_download_dir': parser.get('Paths', 'img_download_dir'),
    'data_dir': parser.get('Paths', 'data_dir')
}

DATA_IMPORTER_PROPERTIES = {
    'data_files': parser.get('Data_Importer', 'data_files'),
    'batch_size': parser.get('Data_Importer', 'batch_size'),
    'batch_time_delay': parser.get('Data_Importer', 'batch_time_delay')
}


# Initialize WebHandler
WEB_HANDLER_PROPERTIES = {
    'card_search_site_api': parser.get('Web_Handler', 'card_search_site_api')
}

# Initialize DatabaseHandler
DATABASE_HANDLER_PROPERTIES = {
    'mongodb_client': parser.get('Database_Handler', 'mongodb_client'),
    'database': parser.get('Database_Handler', 'database'),
    'collection': parser.get('Database_Handler', 'collection'),
    'timeout': parser.get('Database_Handler', 'timeout')
}
