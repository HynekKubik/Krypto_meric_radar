#!/bin/sh


for mod in os-sys cython pyqt5 pycrypto pycryptodome pyCrypto pycryptomex times rsa matplotlib glob
do
        python3 -m pip install $mod
done
