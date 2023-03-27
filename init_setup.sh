echo [$(date)]: "START"
echo [$(date)]: "Creating environment with python 3.8 version"
conda create --prefix ./env python=3.8 -y
echo [$(date)]: "Activating Environment"
source activate ./env
echo [$(date)]: "Installing Dev requirements"
pip install -r requirement_dev.txt
echo [$(date)]: "END"