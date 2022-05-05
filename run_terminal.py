#!/usr/bin/env python3

import sys
from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint
# from pyfiglet import figlet_format
from pyfiglet import figlet_format
from src.meric_data_load import *
##dodelat at to zapisuje dobre

class RunTerm:
    def __init__(self):


            cprint(figlet_format('KMR', font='doh'))
            # self.data_meric = {
            #     "selected_algor": ["AES;", "AES_optimalizations_cypton;", "AES_base_impl_py;", "3DES;", "RSA;",
            #                        "SHA256;True", "MD5;",
            #                        "AES_basic_implamantion;", "ComboAESRSA;", "AES_pyCrypto_low;"], "y": [],
            #     "root_path_data": "", "save_path": ""}
            self.data_meric = {"selected_algor": ["SHA256;"], "y": ["TIME [s]"],"root_path_data": "", "save_path": ""}
            print(
                'Welcome to the terminal version of the application Krypto_meric_radar. Please follow the instructions to start correctly.')
            print("")
            print("")
            print("First step")
            print('Enter Data path')
            x = input()
            #x = "/home/hynek/Dokumenty/lightest"
            self.data_meric["root_path_data"] = x
            print("Second step")
            print('Enter save path')
            y = input()
            #y = "/home/hynek/Dokumenty/vysledkytest"
            self.data_meric["save_path"] = y
            print("third step")
            # algoritmus = ["AES;", "AES_optimalizations_cypton;", "AES_base_impl_py;", "3DES;", "RSA;", "SHA256;", "MD5;",
            # "AES_basic_implamantion;", "ComboAESRSA;", "AES_pyCrypto_low;"]
            print(self.data_meric["selected_algor"])
            print(
                "all these operations will be measured, if you want to change the default settings, write the algorithms that you want to remove from the list")
            a = input()

            Measure(self, self.data_meric)


object = RunTerm()
print("done")