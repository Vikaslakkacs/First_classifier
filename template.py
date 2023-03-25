import os
from pathlib import Path ## Helps to create path either forward or backward slash depends on the system
## Logging
import logging
logging.basicConfig(level= logging.INFO, format= '[%(asctime)s]: %(message)s: ')
project_name="firstClassifier"

## Create list of files
list_of_files= [
    ".github/workflows/.gitkeep",## For Ci/Cd pipelines
    ## Src(srcipt folder)
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "configs/config.yaml",
    "dvc.yaml",### Data version control pipeline
    "params.yaml",
    "init_setup.sh", #It helps to create environment
    "requirements.txt",
    "requirement_dev.txt",## Requirement for development purpose
    "setup.py",
    "setup.cgf",
    "pyproject.toml",##If we are creating python package it is required.
    "tox.ini",##Testing of project locally
    "research/stage_01.ipynb"## Jupyter notebook files
]

##Creating files
for filepath in list_of_files:
    filepath= Path(filepath)
    ##Extract the folder path from entire file path
    file_dir, filename= os.path.split(filepath)
    ## There is only file name then it would create folder with empty string
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Creating Directory: {file_dir} for file {filename}")
    
    ## Creating files inside directort
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath, "w") as f:
            logging.info(f"Creating empty file for {filename}")
            pass ##Creates empty file does nothing and saves it.
    else:
        logging.info(f"{filename} already exists")
    