#!/usr/bin/env python3
import sys
import sys
from PyQt5 import QtGui, QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from pathlib import Path
import json
import matplotlib.pyplot as plt
# from scipy import signal
# from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pylab as pl
import copy as cp
from runpy import run_path
import numpy as np
import pprint
import os
import glob
import re
import textwrap
from shutil import copyfile
import warnings
import matplotlib.cbook



warnings.filterwarnings('ignore', category=matplotlib.cbook.mplDeprecation)

pp = pprint.PrettyPrinter(indent=4)


def metric(x, y, c1, c2):
    return c1 * (x[0] - y[0]) ** 2 + c2 * (x[1] - y[1]) ** 2


def similarity(x, y):
    return metric(x, y, 0.001, 0.85)


class Window(QtWidgets.QDialog):
    sendInfo = QtCore.pyqtSignal(object)
    #print("samples print")

    def __init__(self, ownData=None, parent=None, main_menu_instance=None):
        super(Window, self).__init__(parent)
        algo = ownData["selected_algor"]
        cpu = ownData["cpu"]
        self.ownData = ownData
        print(ownData)
        print(algo)
        self.setWindowFlags(QtCore.Qt.Window)
        # a figure instance to plot on
        self.figure = Figure()
        # self.ax = self.figure.add_subplot(111)
        self.ax = self.figure.add_axes([0.05, 0.16, 0.6, 0.8])  # left,bottom edge, width, height
        self.use_logscaleX = False
        self.use_logscaleY = False
        self.setWindowTitle("Plot")
        self.scater_line = 0
        self.data = []
        self.legenda = []
        self.number = 0
        self.main_menu_instance = main_menu_instance
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)



        self.typeButton = QtWidgets.QPushButton('Scatter plot')
        self.plotType = 0
        #self.typeButton.setFixedWidth(50)
        self.typeButton.clicked.connect(self.changeType)



        self.addButton = QtWidgets.QPushButton('Add to plot')
        self.addButton.clicked.connect(self.addAlgoToPlot)
        self.clearButton = QtWidgets.QPushButton('Clear plot')
        self.clearButton.clicked.connect(self.clearCanvas)
        self.combo_algo = QtWidgets.QComboBox(self)
        self.combo_algo.addItem("Choose algoritm")

        algo_one = []
        for i in algo:
            if not i in algo_one:
                algo_one.append(i)
        for i in algo_one:
            self.combo_algo.addItem(i)

        self.combo_cpu = QtWidgets.QComboBox(self)
        self.combo_cpu.addItem("Choose CPU")
        CPU = []
        for i in cpu:
            if not i in CPU:
                CPU.append(i)
        if len(CPU)>1:
            for i in CPU:
                self.combo_cpu.addItem(i)
                self.cpu = True
        else:
            self.cpu = False
            self.combo_cpu.setEnabled(False)
        print("cpu")
        print(CPU)
        print(cpu)
        self.bf = QtGui.QFont("Arial", 13, QtGui.QFont.Bold)

        self.mult = QtWidgets.QLineEdit("1")
        self.mult.setAlignment(QtCore.Qt.AlignCenter)
        self.mult.setValidator(QtGui.QDoubleValidator())


        self.multiple_samples = False
        self.legende_paramentr = []


        # set the layout
        layout = QtWidgets.QVBoxLayout()









        hlayout2 = QtWidgets.QHBoxLayout()

        self.addButton.setFixedWidth(130)
        hlayout2.addWidget(self.combo_algo)
        hlayout2.addWidget(self.combo_cpu)
        hlayout2.addWidget(self.addButton)
        hlayout2.setAlignment(QtCore.Qt.AlignRight)

        layout.addLayout(hlayout2)



        hlayout4 = QtWidgets.QHBoxLayout()
        self.clearButton.setFixedWidth(130)
        hlayout4.addWidget(self.clearButton)
        hlayout4.setAlignment(QtCore.Qt.AlignRight)
        layout.addLayout(hlayout4)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        labelDotsize = QtWidgets.QLabel("Dot size: ")
        labelDotsize.setFixedWidth(60)
        self.dotSizeSpinBox = QtWidgets.QSpinBox()
        self.dotSizeSpinBox.setFixedWidth(100)
        self.dotSizeSpinBox.setMinimum(1)
        self.dotSizeSpinBox.setMaximum(2147483647)
        self.dotSizeSpinBox.valueChanged.connect(self.dotSizeChanged)
        self.dotSizeSpinBox.setEnabled(False)

        #self.fontSize = QtWidgets.QLabel("Font size: ")
        labelFontsize = QtWidgets.QLabel("Font size: ")
        labelFontsize.setFixedWidth(60)
        self.fontSize = QtWidgets.QSpinBox()
        self.fontSize.setFixedWidth(100)
        self.fontSize.setValue(13)
        self.fontSize.setMinimum(10)
        self.fontSize.setSingleStep(1)
        self.fontSize.setMaximum(50)
        self.fontSize.valueChanged.connect(self.fontSizeChanged)
        self.fontSize.setEnabled(False)

        hlayout = QtWidgets.QHBoxLayout()


        hlayout.addWidget(labelFontsize)
        hlayout.addWidget(self.fontSize)
        hlayout.addWidget(labelDotsize)
        hlayout.addWidget(self.dotSizeSpinBox)
        hlayout.addWidget(self.typeButton)
        layout.addLayout(hlayout)



        self.setLayout(layout)

        #self.plot()
        self.resize(900, 900)






        print("samples konec")
        self.canvas.draw()
        print("draw")



    def fontSizeChanged(self):
        if self.data:
            self.plotA()

    def dotSizeChanged(self):
        if self.data:
            self.plotA()
    # zmena z line plot na scatter plot
    def changeType(self):
        #self.sw = not self.sw
        if self.data:
            self.plotType = not self.plotType
            if self.plotType:
                self.typeButton.setText('Line plot')
                self.dotSizeSpinBox.setEnabled(True)
                print("line")
                self.scater_line = True
            else:
                self.typeButton.setText('Scatter plot')
                self.dotSizeSpinBox.setEnabled(False)
                print("scater")
                self.scater_line = False
            self.plotA()

    # vymazani dat z grafu
    def clearCanvas(self):
        self.data = []
        self.legenda = []
        self.number = 0
        self.min_sample_val = float(99999999999999)
        self.max_sample_val = float(0)
        #self.typeButton_id_time.setEnabled(True)
        self.ax.clear()
        self.fontSize.setEnabled(False)
       # self.typeButton_id_time.setEnabled(True)
        # self.ax = self.figure.add_axes([0.15, 0.25, 0.6, 0.7])

        self.canvas.draw()


    def addAlgoToPlot(self):

        parameter = self.combo_algo.currentText()
        if self.cpu:
            cpu = self.combo_cpu.currentText()
        else:
            cpu = "cpuinfo "
        path = str(self.ownData["path"])
        data = []
        algo = []
        self.fontSize.setEnabled(True)
        csv_file = open(path, "r")
        if csv_file:
            reading = True
        for line in csv_file:
            if "cpuinfo " in line and cpu in line:
                cpu_ = line.split("cpuinfo ")[1].strip("\n")
                print("cpuinfo")
                print(cpu_)
                cpu_bool = True
            if "cpuinfo " in line and not cpu in line:
                cpu_bool = False
            if cpu_bool and "#" in line and reading:
                str_prev = line
                size = line.split(";")[-1].strip("\n")
                size = float(size.split("[")[0])
            if cpu_bool and parameter in line and "#" in str_prev:
                line = line.split(";")
                if parameter == line[0]:
                    time = float(line[1].strip("\n"))
                    tup = (size, time)
                    data.append(tup)

                #algo.append(line[0])
        # print("cpu")
        # print(cpu_)
        algo.append(parameter + " " + cpu)

        csv_file.close()
        print("-----------------------------------------")
        print(data)
        print(algo)
        data = sorted(data, key=lambda tup: tup[0])
        print(data)
        print("--------------------------------")
        self.data.append(data)
        self.legenda.append(algo)
        #print(self.data)
        self.number +=1
        self.plotA()

    def plotA(self):
        self.ax.clear()
        data = self.data
        legenda = self.legenda
        self.n = len(self.data)
        print(self.n)
        self.xlab = "size [B]"
        self.ylab = "time [s]"

        for m in range(0, self.n):
            X = []
            Y = []
            for i in data[m]:
                X.append(i[0])
                Y.append(i[1])
            leg = legenda[m]
            # if self.data:
            #     if self.plotType:
            #         self.ax.scatter(Y, X, label=self.legenda[m], s=self.dotSizeSpinBox.value())
            #     else:
            #         self.ax.plot(Y, X, label=self.legenda[m])
            # else:
            #     if self.plotType:
            #         self.ax.scatter(X, Y, label=self.legenda[m], s=self.dotSizeSpinBox.value())
            #     else:
            #         self.ax.plot(X, Y, label=self.legenda[m])
            if self.scater_line == True:
                self.ax.scatter(X, Y, label=self.legenda[m],marker= "D", s=self.dotSizeSpinBox.value())
            else:
                self.ax.plot(X, Y, label=self.legenda[m],marker= "D")

        if self.data:
            self.ax.set_xlabel(self.xlab, fontsize=self.fontSize.value())
            self.ax.set_ylabel(self.ylab, fontsize=self.fontSize.value())




        self.ax.tick_params(labelsize=self.fontSize.value())

        self.ax.grid(linestyle='--')

        # ylim_extension = self.max_sample_val * 0.01  # add one percent of max value to axis limit
        # self.ax.set_ylim((self.min_sample_val - ylim_extension, self.max_sample_val + ylim_extension))

        handles, labels = self.ax.get_legend_handles_labels()
        lgd = self.ax.legend(handles, self.legenda, loc=2, bbox_to_anchor=(0.99, 1.00025), ncol=1,
                             borderaxespad=0.,
                             prop={'size': self.fontSize.value()})
        self.canvas.draw()
        if self.main_menu_instance:
            self.main_menu_instance.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window(2)
    main.show()

    sys.exit(app.exec_())

