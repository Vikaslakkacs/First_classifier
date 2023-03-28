from collections import namedtuple
import os
import urllib.request as request
from zipfile import ZipFile
##Import user defined packages
##Configuration and parameters variables
from firstClassifier.constants import *
##methods to read yaml files of config and parameters and create directories for the artifacts and datasets
from firstClassifier.utils.common import read_yaml, create_directories


##Creating Namedtuple for data ingestion configuration
DataIngestionConfig = namedtuple("DataIngestionConfig",
                                 [
                                    "root_dir",
                                    "source_url",
                                    "local_data_file",
                                    "unzip_dir"])


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
    

### Data ingestion component
class DataIngestion:
    """DataIngestion will takecares of initial stage of the project
    by downloading dataset and cleaning the data and providing error free dataset.
    """
    def __init__(self, config: DataIngestionConfig):
        self.config= config

    def download_file(self):
        """Downloads file from the link
        """
        ## Check if the file is present already or not.
        if not os.path.exists(self.config.local_data_file):
            ##Call the request to retrieve url
            filename, headers= request.urlretrieve(self.config.source_url, 
                                filename=self.config.local_data_file
                                )
    def _get_updated_list_of_files(self, list_of_files:list):
        """It gets the list of files that are necessary for the program
            files ends with .jpg and Cat or Dog in the file path are only considered

        Args:
            list_of_files (list): Contains list of files from unzip folder
        """

        return [f for f in list_of_files if f.endswith(".jpg") and ("Cat" in f or "Dog" in f)]
    
    def _preprocess(self, zf:ZipFile, f:str, working_dir:str):
        """Places all the files into target folder
           and ignores files which as zero size.

        Args:
            zf (ZipFile): Zipf file
            f (str): filename along with path
            working_dir (str): target working directory.
        """
        target_filepath= os.path.join(working_dir, f)
        if not os.path.exists(target_filepath):
            zf.extract(f, working_dir)
        
        if os.path.getsize(target_filepath)==0:
            os.remove(target_filepath)

    def unzip_and_clean(self):
        """Unzip the file and clean the data by checking whether there are 
            any unwanted files that are present or not.
        """
        with ZipFile(file= self.config.local_data_file, mode= "r") as zf:
            ## Getting the list of all files available
            ## [file1, file/file2, file/file3]
            list_of_files= zf.namelist()
            ##Keep only useful files
            updated_list_of_files= self._get_updated_list_of_files(list_of_files)
            ##Preprocessing the files
            for f in updated_list_of_files:
                self._preprocess(zf, f, self.config.unzip_dir)