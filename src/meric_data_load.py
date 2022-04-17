#!/usr/bin/env python3
# import sys
# from PyQt5 import QtGui, QtCore, QtWidgets
# import os
# import glob
# import errno
# import sys
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QMainWindow
# from PyQt5.QtWidgets import QWidget
import hashlib
import os.path
import time
import csv
import glob
from Crypto.Cipher import AES
from src.AesFile import *
from src.RsaFile import *
from src.AESCrypt import *
from src.rsa_aes_file import *
from src.aes_low_pycrypto import *
from src.DES3 import *
from src.aes_base_impl import *
from src.aes_c.aes import *
from os import walk
from os import stat, remove
# encryption/decryption buffer size - 64K
# with stream-oriented functions, setting buffer size is mandatory

#pridat další krypto operace!!!!!!!!
#pokusit se o vlastní implementaci !!!!
#nahrat na git!!!


class Measure:

        def __init__(self, data, dat):
                print(data)
                print("dat")
                print(dat)
                self.wc = True
                self.algor = dat["selected_algor"]
                self.data_path = dat["root_path_data"]
                self.save_path = dat["save_path"]
                self.save_path_name = self.save_path + "/name.csv"
                #self.file_path = []
        #def Print_meric(self, data):
                print("meric_aaaaaaa")
                print(data)
                self.Data_path_find()
                self.Save_file("","")
                self.folden()
                self.Check_algo()


        def Data_path_find(self):
                self.f = []
                # for (dirpath, dirnames,filenames) in walk(self.data_path):
                #         f.exte
                root = self.data_path+"/*/*"
                self.file_path = glob.glob(root)
                #print(glob.glob(root))
                #print(glob.glob(self.data_path+"/*"))

        def Check_algo(self):
                for i in self.algor:
                        print(i)
                        a = i.split(";")[0]
                        if a == "SHA256":
                                print(a)
                                self.SHA256()
                        if a == "3DES":
                                print(a)
                                self.DES3()
                        if "MD5" in a:
                                print(a)
                                self.MD5()
                        if a == "AES" :
                                print(a)
                                self.AES()
                        if a == "AES_pyCrypto_low" :
                                print(a)
                                self.aes_low()
                        if a == "AES_basic_implamantion":
                                print(a)
                                self.AESbasicimplamantion()
                        if a == "RSA":
                                print(a)
                                self.RSA()
                        if a == "ComboAESRSA":
                                print(a)
                                self.CombinationAesRsa()
                        if a == "AES_optimalizations_cypton":
                                self.AES_optimalization()
                        if a == "AES_base_impl_py":
                                self.AES_base_impl_py()

        def AES_base_impl_py(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        menu_aes_base_impl_py(i)
                        end = time.time()
                        real_time = end - start
                        #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "AES_base_impl_py; " + str(real_time)
                        self.Save_file(string, data)


        def AES_optimalization(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        menu_aes_base_impl(i)
                        end = time.time()
                        real_time = end - start
                        #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "AES_optimalizations_cypton; " + str(real_time)
                        self.Save_file(string, data)

        def DES3(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        menu_3_DES(i)
                        end = time.time()
                        real_time = end - start
                        #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "3DES; " + str(real_time)
                        self.Save_file(string, data)

        def aes_low(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        aes(i)
                        end = time.time()
                        real_time = end - start
                        #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "AES_pyCrypto_low; " + str(real_time)
                        self.Save_file(string, data)
        def RSA(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        menu_RSA(i)
                        end = time.time()
                        real_time = end - start
                        #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "RSA; " + str(real_time)
                        self.Save_file(string, data)

        def AESbasicimplamantion(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        menu_AES(i)
                        end = time.time()
                        real_time = end - start
                        print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "AES_basic_implamantion; " + str(real_time)
                        self.Save_file(string, data)
        def AES(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        menu_AES_basic(i)
                        end = time.time()
                        real_time = end - start
                       #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "AES; " + str(real_time)
                        self.Save_file(string, data)

        def CombinationAesRsa(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        menuAesRsa(i)
                        end = time.time()
                        real_time = end - start
                       #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "AES_RSA_combo; " + str(real_time)
                        self.Save_file(string, data)


        def MD5(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        result = hashlib.md5()
                        with open(i, "rb") as f:
                                for byte_block in iter(lambda: f.read(4096), b""):
                                        result.update(byte_block)

                                #print(result.hexdigest())
                                end = time.time()
                                real_time = end - start
                                #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "MD5; " + str(real_time)
                        self.Save_file(string, data)

        def SHA256(self):
                #self.path = "/home/hynek/Stažené/landscape-of-mountains-and-forest-4k-vaporwave.jpg"
                #print(self.path)
                # return "ahoj"

                # filename = input("Enter the input file name: ")
                #print("sha")
                sha256_hash = hashlib.sha256()

                # print("hello")
                #self.list = [], []
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        with open(i, "rb") as f:
                                #print("open file")
                                # Read and update hash string value in blocks of 4K
                                for byte_block in iter(lambda: f.read(4096), b""):
                                        sha256_hash.update(byte_block)
                                #print(sha256_hash.hexdigest())
                                end = time.time()
                        # print(start)
                        # print("time")
                                real_time = end - start
                                #print(end - start)
                        string = "# " + filename + ";" + size + "[B]"
                        #self.list[0].append("SHA256")
                        #self.list[1].append(str(real_time))
                        data = "SHA256; " + str(real_time)
                        self.Save_file(string, data)


        def Save_file(self,string_save_id,data):
                #self.save_path = self.save_path + "name.csv"
                #f =open(self.save_path,"w")
                #f.close()
                cpu = self.CpuName()
                with open(self.save_path_name,'a+') as myfile:
                        #wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        #wr.writerow(string_save_id)
                        #wr.writerow(self.list)
                        #print("zapis")
                        #myfile.write(cpu + "Start")
                        #myfile.write("\n")
                        if self.wc:
                                myfile.write(cpu)
                                myfile.write("\n")
                                self.wc = False
                        else:
                                myfile.write(string_save_id)
                                myfile.write("\n")
                                myfile.write(data)
                                myfile.write("\n")
                        #myfile.write("\n")
                        #print(data)
                        #print(string_save_id)
                #print(self.save_path)

        def CpuName(self):
                with open('/proc/cpuinfo') as f:
                        for line in f:
                                # Ignore the blank line separating the information between
                                # details about two processing units
                                if line.strip():
                                        if line.rstrip('\n').startswith('model name'):
                                                model_name = line.rstrip('\n').split(':')[1]
                                                model = model_name
                                                model = model.strip()
                                                model = " cpuinfo " + model
                                                break
                return model
        def folden(self):
                path = self.save_path + "/"
                cpu = self.CpuName()
                if not os.path.exists(path + cpu):
                        os.mkdir(path + cpu)
                        for i in self.algor:
                                i= i.split(";")[0]
                                if not os.path.exists(path + cpu +"/" + i):
                                        os.mkdir(path + cpu +"/" + i)
                                        with open(path + cpu +"/" + i + "/" + "name.csv",'a+') as f:
                                                f.readline()
                                else:
                                        with open(path + cpu +"/" + i + "/" + "name.csv",'a+') as f:
                                                f.readline()
                else:
                        for i in self.algor:
                                i = i.split(";")[0]
                                if not os.path.exists(path + cpu +"/" + i):
                                        os.mkdir(path + cpu +"/" + i)
                                        with open(path + cpu +"/" + i + "/" + "name.csv",'a+') as f:
                                                f.write("uz je vytvoren")
                                else:
                                        with open(path + cpu +"/" + i + "/" + "name.csv",'a+') as f:
                                                f.write("uz je vytvoren")

