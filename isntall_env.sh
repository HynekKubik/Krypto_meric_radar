#!/bin/bash

if ! command -v python3 &>/dev/null
then
        echo "ERROR: Python3 is not installed"
        exit 1
fi

if ! command -v python3 -m pip &>/dev/null
then
        echo "ERROR: Python3 pip module not installed"
        exit 1
fi

ENV_DIR=environment
python3 -m venv $ENV_DIR

source $ENV_DIR/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade setuptools
for mod in scikit-learn matplotlib packaging seaborn enum34==1.1.6 pwlf h5py PyQt5 hashlib times python-csv glob pycrypto pytest-warnings argparse pycryptodomex pycryptodome rsa os-sys pycrypto
do
        python3 -m pip install $mod
done

python3 -m pip list

deactivate

