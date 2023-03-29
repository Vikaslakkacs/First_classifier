from firstClassifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from firstClassifier.utils import read_yaml, create_directories
from firstClassifier.entity import DataIngestionConfig, PrepareBaseModelConfig
from pathlib import Path


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
    
    def get_prepare_base_model_config(self)->PrepareBaseModelConfig:
        """Creates root directory for preparing base model and stores all the variables
            from config.yaml
        Returns:
            PrepareBaseModelConfig: PrepareBaseModelConfig
        """
        ##Config contains the attributes that are present in prepare_base_model in config.yaml
        
        config= self.config.prepare_base_model
        params= self.params
        ##Create directory from root_dir
        create_directories([config.root_dir])
        

        prepare_base_model_config= PrepareBaseModelConfig(   
                    root_dir= Path(config.root_dir),
                    base_model_path= Path(config.base_model_path),
                    updated_base_model_path= Path(config.updated_base_model_path),
                    params_image_size= params.IMAGE_SIZE,
                    params_learning_rate= params.LEARNING_RATE,
                    params_include_top= params.INCLUDE_TOP,
                    params_weights= params.WEIGHTS,
                    params_classes= params.CLASSES
            )
        return prepare_base_model_config