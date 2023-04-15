from collections import namedtuple
import os
import urllib.request as request
from zipfile import ZipFile
##Import user defined packages
from firstClassifier.entity import DataIngestionConfig
from firstClassifier import logger
from tqdm import tqdm

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
        logger.info(f"Trying to download file from {self.config.source_url}")
        ## Check if the file is present already or not.
        if not os.path.exists(self.config.local_data_file):
            ##Call the request to retrieve url
            filename, headers= request.urlretrieve(self.config.source_url, 
                                filename=self.config.local_data_file
                                )
            logger.info(f"file name downloaded: {filename} with following info:\n{headers}")

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
            logger.info(f"Removing file: {target_filepath}")

    def unzip_and_clean(self):
        """Unzip the file and clean the data by checking whether there are 
            any unwanted files that are present or not.
        """
        logger.info(f"Unzipping file and removing un wanted files")
        with ZipFile(file= self.config.local_data_file, mode= "r") as zf:
            ## Getting the list of all files available
            ## [file1, file/file2, file/file3]
            list_of_files= zf.namelist()
            ##Keep only useful files
            updated_list_of_files= self._get_updated_list_of_files(list_of_files)
            ##Preprocessing the files
            for f in tqdm(updated_list_of_files):
                self._preprocess(zf, f, self.config.unzip_dir)
    def create_test_data(self):
        """Seperates 30% of data into test data.
        """
        pass