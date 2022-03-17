#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from src.meric_data_load import *
from src import analyze
from PyQt5 import QtGui
from PyQt5.QtWidgets import QCheckBox
#import calendar
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QToolTip, QMessageBox, QLabel, QFrame, QLineEdit)
#trida vytvářející configurační okno pro merení kryptografických algoritmů
class Window2(QMainWindow):
    # (300, 300, 570, 330)
    # (self.top, self.left, self.width, self.height)
    def __init__(self):
        super().__init__()
        self.data = []
        self.y = []
        self.data_meric = {"selected_algor": [], "y": [], "root_path_data":"", "save_path":"" }
        self.algoritmus = ["AES","RSA","SHA256","MD5","AES_basic_implamantion","ComboAESRSA", "AES_pyCrypto_low"]
        self.save_path = False
        self.data_path = False
        self.setWindowTitle("Meric")


        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setLineWidth(1)
        self.frame.setGeometry(420, 40, 135, 260)
        self.frame_path = QFrame(self)
        self.frame_path.setFrameShape(QFrame.StyledPanel)
        self.frame_path.setLineWidth(1)
        self.frame_path.setGeometry(10, 40, 400, 260)
        #self.frame.resize(700, 494)
        #MainWindow.setFixedSize(300, 300):
        self.box = QCheckBox("TIME [s]", self)
        self.box.setGeometry(450, 30, 280, 80)
        self.menuConfAlg = self.menuBar().addMenu('configure Menu algorithm')
        self.pushButton_BrowseData = QtWidgets.QPushButton("Browse..",self)
        self.pushButton_BrowseData.setEnabled(True)
        self.pushButton_BrowseData.setGeometry(QtCore.QRect(250, 130, 130, 30))
        #self.pushButton_BrowseData.setObjectName("pushButton_BrowseData")
        self.label_Path_Data = QtWidgets.QLabel("Data path",self)
        self.label_Path_Data.setEnabled(True)
        self.label_Path_Data.setGeometry(QtCore.QRect(30, 50, 280, 30))
        self.textbox_data = QLineEdit(self)
        self.textbox_data.setGeometry(QtCore.QRect(30, 85, 350, 30))

        self.pushButton_Browse_Save = QtWidgets.QPushButton("Browse..", self)
        self.pushButton_Browse_Save.setEnabled(True)
        self.pushButton_Browse_Save.setGeometry(QtCore.QRect(250, 240, 130, 30))
        # self.pushButton_BrowseData.setObjectName("pushButton_BrowseData")
        self.label_Path_Save = QtWidgets.QLabel("Save path", self)
        self.label_Path_Save.setEnabled(True)
        self.label_Path_Save.setGeometry(QtCore.QRect(30, 160, 280, 30))
        self.textbox_Save = QLineEdit(self)
        self.textbox_Save.setGeometry(QtCore.QRect(30, 195, 350, 30))
        self.pushButton_Run = QtWidgets.QPushButton("Start", self)
        self.pushButton_Run.setEnabled(True)
        self.pushButton_Run.setGeometry(QtCore.QRect(10, 310, 545, 50))
        #self.label_PathToData.setObjectName("label_PathToData")
#action
        self.box.stateChanged.connect(self.clickBox)
        self.menuConfAlg.triggered.connect(self.AddValueAlgo)
        self.menuConfAlg.setToolTip("<h3>Click here to choice measurement confugure</h3>")
        self.pushButton_BrowseData.clicked.connect(self.BrowseData_path)
        self.pushButton_Browse_Save.clicked.connect(self.Save_path)
        self.pushButton_Run.clicked.connect(self.Run)
        #app.aboutToQuit.connect(self.closeEvent)

        len_algo = len(self.algoritmus)
        for i in range(len_algo):
            action = self.menuConfAlg.addAction(self.algoritmus[i])
            action.setCheckable(True)
#running okno
    def window4(self):# <===
        self.w = Window4()
        self.w.show()
        self.hide()

##podminky jsou zakomentovany
    def Run(self):
        print("ahoj")
        if len(self.data_meric["y"])==0:
            self.Error_msg("missing y label",
                           "Missing y label.\n YOU MUST TO SELECT Y LABEL IN LEFT SELECTION")
        elif len(self.data_meric["selected_algor"])==0:
            self.Error_msg("missing atribite in configure Menu algorithm",
                           "Missing CRYPTO algoritm label.\n YOU MUST TO CLICT ON configure Menu algorithm AND SELECT FROM LIST")
        elif self.data_path == False:
            self.Error_msg("missing data path",
                           "Missing data path.\n YOU MUST TO SELECT DATA PATH")
        elif self.save_path == False:
            self.Error_msg("missing save path",
                           "Missing save path.\n YOU MUST TO SELECT SAVE PATH")
        else:
            self.Info_msg("Measurement will be started",
                                    "Click ok.\n Please do not close next window")
            self.window4()
            p = Measure(self, self.data_meric)
            self.End_msg("The end of measurement",
                              "Now you can close all windows.")
        print("meric_data_load")
        # text = "ahoj"


        self.window4()


    def End_msg(self, text, mess):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(mess)
        msg.setWindowTitle(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Close)
        msg.exec_()

    def Info_msg(self, text, mess):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(mess)
        msg.setWindowTitle(text)
        #msg.setStandardButtons(QtWidgets.QMessageBox.Information)
        msg.exec_()

    def Error_msg(self, text, mess):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(mess)
        msg.setWindowTitle(text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Close)
        msg.exec_()

    def BrowseData_path(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        text =str(dlg.getExistingDirectory())
        self.textbox_data.setText(text)
        self.data_meric["root_path_data"] = text
        self.data_path = True
        if not text:
            self.data_path = False

    def Save_path(self):
        dlg_save = QtWidgets.QFileDialog()
        dlg_save.setFileMode(QtWidgets.QFileDialog.Directory)
        text = str(dlg_save.getExistingDirectory())
        self.textbox_Save.setText(text)
        self.data_meric["save_path"] = text
        self.save_path = True
        if not text:
            self.data_path = False

#funkce pridavajici do dic self.data.meric zvolene algoritmy
    def AddValueAlgo(self, action):
        #print('{0}-{1}'.format(action.text(), action.isChecked()))
        val_true = '{0};{1}'.format(action.text(), action.isChecked())
        val=action.text()
        print("val")
        print(val)
        print(val_true)
        if "True" in val_true:
            #self.data.append(val_true)
            if not val_true in self.data_meric["selected_algor"]:
                self.data_meric["selected_algor"].append(val_true)
        else:
            val_false = val_true.split(";")
            for i in self.data_meric["selected_algor"]:
                if val_false[0] in i:
                    #self.data.remove(i)
                    self.data_meric["selected_algor"].remove(i)
        #print(self.data)
        print(self.data_meric)
#funkce pridavajici do dic self.data_meric zavislosti jako napr cas
    def clickBox(self, state):

        if self.box.isChecked():
            if not self.box.text() in self.data:
                #self.y.append(self.box.text())
                self.data_meric["y"].append(self.box.text())
                self.show()
        else:
            print("ne")

        #print(self.data)
        print(self.data_meric)

class Window3(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analyze")
        dlg = QtWidgets.QFileDialog()
        text = str(dlg.getOpenFileName(filter='Text files (*.csv)')[0])
        #text = str(dlg.getExistingDirectory())
        print(text)
        self.data_for_vizu = {"selected_algor": [], "vel": [], "name": [], "path": "", "time": []}
        self.data_for_vizu["path"] = text
        number = 0
        #data_time = []
        with open(text, "r") as file:
            for line in file:
                if "# " in line:
                #if line.startswith("#"):
                    tmp = line
                    name = line.split(";")[0]
                    vel = line.split(";")[1].split("\n")[0]
                elif ";" in line and "# " in tmp:#tmp.startswith("#"):
                    line = line.split(";")
                    self.data_for_vizu["time"].append(line[1].split("\n")[0])
                    self.data_for_vizu["vel"] .append(vel)
                    self.data_for_vizu["selected_algor"].append(line[0])
                    self.data_for_vizu["name"].append(name)
                    number = number + 1
                    tmp = " "
        print(number)
        print(self.data_for_vizu)
        #analyze = Analyze(self, self.data_for_vizu)
        self.setGeometry(300, 300, 320, 200)
        self.pushButton_plot = QPushButton("Plot", self)
        self.pushButton_plot.setGeometry(10, 10, 300, 80)
        self.pushButton_table = QPushButton("Table", self)
        self.pushButton_table.setGeometry(10, 100, 300, 80)
        # self.pushButton_back = QPushButton("Back", self)
        # self.pushButton_back.setGeometry(10, 190, 300, 80)

        self.pushButton_plot.clicked.connect(self.plot)
    def plot(self):
        #p = Analyze(self,self.data_for_vizu)
        self.samples_window = analyze.Window(ownData=self.data_for_vizu, main_menu_instance=self)
        self.samples_window.show()

class Window4(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MEASUREMENT RUNING")
        self.setGeometry(300,300,300,300)



#třída vytvarejici prvni menu pro výber analyze nebo meric
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "measurement/analyze"
        self.top = 100
        self.left = 100
        self.width = 320
        self.height = 190

        self.pushButton_meric = QPushButton("Measurement", self)
        self.pushButton_meric.setGeometry(10, 10,  300, 80)
        self.pushButton_meric.setToolTip("<h3>Measurement cryptpography</h3>")
        self.pushButton_meric.clicked.connect(self.window2)

        self.pushButton_analize = QPushButton("Analyze", self)
        self.pushButton_analize.setGeometry(10, 100, 300, 80)
        self.pushButton_analize.setToolTip("<h3>Analyze cryptography</h3>")
        self.pushButton_analize.clicked.connect(self.window3)
        # <===

        self.main_window()

    def main_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def window2(self):# <===
        self.w = Window2()
        self.w.setGeometry(300, 300, 570, 370)
        self.w.show()
        self.hide()

    def window3(self):# <===
        self.w = Window3()
        self.w.show()
        self.hide()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    window = Window()
    sys.exit(app.exec())