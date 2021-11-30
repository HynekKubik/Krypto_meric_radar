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

from os import walk
from os import stat, remove
# encryption/decryption buffer size - 64K
# with stream-oriented functions, setting buffer size is mandatory



class Analize:

        def __init__(self, data, dat):
                print(data)
                print("dat")
                print(dat)

                self.algor = dat["selected_algor"]
                self.data_path = dat["root_path_data"]
                self.save_path = dat["save_path"]
                self.save_path = self.save_path + "/name.csv"
                #self.file_path = []
        #def Print_meric(self, data):
                print("meric_aaaaaaa")
                print(data)
                self.Data_path_find()
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
                        if "SHA256" in i:
                                self.SHA256()
                        if "MD5" in i:
                                self.MD5()
        def MD5(self):
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        result = hashlib.md5()
                        with open(i, "rb") as f:
                                for byte_block in iter(lambda: f.read(4096), b""):
                                        result.update(byte_block)

                                print(result.hexdigest())
                                end = time.time()
                                real_time = end - start
                                print(end - start)
                        string = "# " + filename + ";" + size + "[b]"
                        # self.list[0].append("SHA256")
                        # self.list[1].append(str(real_time))
                        data = "MD5; " + str(real_time)
                        self.Save_file(string, data)
        def SHA256(self):
                #self.path = "/home/hynek/Stažené/landscape-of-mountains-and-forest-4k-vaporwave.jpg"
                #print(self.path)
                # return "ahoj"

                # filename = input("Enter the input file name: ")
                print("sha")
                sha256_hash = hashlib.sha256()

                # print("hello")
                #self.list = [], []
                for i in self.file_path:
                        filename = i.split("/")[-1]
                        size = str(os.path.getsize(i))
                        start = time.time()
                        with open(i, "rb") as f:
                                print("open file")
                                # Read and update hash string value in blocks of 4K
                                for byte_block in iter(lambda: f.read(4096), b""):
                                        sha256_hash.update(byte_block)
                                print(sha256_hash.hexdigest())
                                end = time.time()
                        # print(start)
                        # print("time")
                                real_time = end - start
                                print(end - start)
                        string = "# " + filename + ";" + size + "[b]"
                        #self.list[0].append("SHA256")
                        #self.list[1].append(str(real_time))
                        data = "SHA256; " + str(real_time)
                        self.Save_file(string, data)


        def Save_file(self,string_save_id,data):
                #self.save_path = self.save_path + "name.csv"
                #f =open(self.save_path,"w")
                #f.close()
                with open(self.save_path,'a+') as myfile:
                        #wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        #wr.writerow(string_save_id)
                        #wr.writerow(self.list)
                        #print("zapis")
                        myfile.write(string_save_id)
                        myfile.write("\n")
                        myfile.write(data)
                        myfile.write("\n")
                print(self.save_path)