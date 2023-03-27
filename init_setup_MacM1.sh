echo [$(date)]: "Start"
conda init bash
# Installing jupyter
echo [$(date)]: "Mac M1 steps"
conda install -y jupyter --y
echo [$(date)]: "De-activating conda (If using Mac M1 and trying to install tensorflow this is must)"
echo [$(date)]:"Create env with python 3.8 version with "
conda env create -f requirements_dev.yml
echo [$(date)]: "activating the environment"
conda activate firstClassifier
echo [$(date)]: "Register for Jupyter notebook, This is for M1 Mac"
python -m ipykernal install --user --name firstClassifier --display-name "firstClassifier tensorflow edition"
##Installing Tensorflow in Mac M1
echo ["$(date)"]: "End"