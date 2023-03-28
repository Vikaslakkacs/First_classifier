from firstClassifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from firstClassifier.utils import read_yaml, create_directories
from firstClassifier.entity import DataIngestionConfig



class ConfigurationManager:
    """Pickup data from configuration.yaml and params.yaml file
       and read to find the folder paths and file paths of dataset
       and store it in Dataingestionconfig    
    """

    def __init__(
        self, 
        config_filepath = CONFIG_FILE_PATH,
        params_filepath= PARAMS_FILE_PATH
             ):
        """_summary_: Creates artifact directories taken from config.yaml file
        """
        self.config= read_yaml(config_filepath)
        self.params= read_yaml(params_filepath)
        ##Create directories
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self)->DataIngestionConfig:
        """Creates root directory for data ingestion and stores all the variables
            from config.yaml

        Returns:
            DataIngestionConfig: DataIngestionConfig
        """
        ##Config contains the attributes that are present in data ingestion in config.yaml
        config= self.config.data_ingestion
        ##Create directory from root_dir
        create_directories([config.root_dir])

        data_ingestion_config= DataIngestionConfig(   
            root_dir= config.root_dir,
            source_url= config.source_url,
            local_data_file= config.local_data_file,
            unzip_dir= config.unzip_dir
            )
        return data_ingestion_config