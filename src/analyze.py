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
        self.ownData = ownData
        print(ownData)
        print(algo)
        self.setWindowFlags(QtCore.Qt.Window)
        # a figure instance to plot on
        self.figure = Figure()
        # self.ax = self.figure.add_subplot(111)
        self.ax = self.figure.add_axes([0.1, 0.25, 0.8, 0.7])  # left,bottom edge, width, height
        self.sw = False
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
        # hlayout.addWidget(self.checkbox_sw)
        # hlayout.addWidget(self.maxBox)

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

    def spinBoxCheck(self):
        if self.samples_data:
            if self.smoothWindowSizeSpinBox.value() % 2 == 0:
                QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 'Invalid input', 'Window size must be odd number.',
                                      QtWidgets.QMessageBox.Ok).exec()
                self.smoothWindowSizeSpinBox.setValue(self.smoothWindowSizeSpinBox.value() - 1)
                return 1
            if self.max_data_len < self.smoothWindowSizeSpinBox.value():
                QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 'Invalid input',
                                      'Maximum window length is number of '
                                      'samples.',
                                      QtWidgets.QMessageBox.Ok).exec()
                self.smoothWindowSizeSpinBox.setValue(self.max_data_len)
                return 1
        if self.smoothWindowSizeSpinBox.value() <= self.smoothpolyOrderSpinBox.value():
            QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 'Invalid input', 'Polynomial order must be less than '
                                                                                  'window length.',
                                  QtWidgets.QMessageBox.Ok).exec()
            self.smoothpolyOrderSpinBox.setValue(self.smoothWindowSizeSpinBox.value() - 1)
            return 1

        return 0

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

    # pridani dat do grafu
    # nepotrebne
    def addToPlot(self):
        #if self.fontSize.setEnabled(False):
        self.fontSize.setEnabled(True)
        self.number = []
        csv_name_string = ''
        for combo_param in self.combo_param_list:
            csv_name_string += combo_param.currentText() + '_'
        csv_name_string = csv_name_string[:-1]
        print("csv_name_string")
        print(csv_name_string)
        if "default" in csv_name_string:
            csv_name_string = "default"
        if "log" in csv_name_string:
            csv_name_string = "log"
        csv_path = self.root_folder + '/' + self.combo_reg.currentText() + '/' + csv_name_string + '.csv'
        if self.multiple_samples:
            self.samples_data_lables.append(self.combo_sample.currentText() + ' ' + self.combo_reg.currentText() + ' '
                                            + csv_name_string.replace('_', ' '))
        else:
            self.samples_data_lables.append(self.combo_reg.currentText() + ' ' + csv_name_string.replace('_', ' '))
        #self.load_samples_from_csv(csv_path)
        self.load_samples_from_csv_for_new_meric(csv_path)
        self.plot()

    def change_sw(self):
        self.sw = not self.sw
        self.plotA()


    # graf
    def plot(self):
        self.ax.clear()
        # self.ax = self.figure.add_axes([0.15,0.25,0.6,0.7])   # left,bottom edge, width, height

        if self.mult.text() in ["e", "."] or "," in self.mult.text() or self.mult.text().endswith(
                'e') or self.mult.text().startswith('e'):
            self.numMultiplier = 1.0
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Wrong multiplier format!\nPlease write the multiplier in form AeB (e.g. 1e-4).")
            msg.setWindowTitle("Invalid multiplier")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            self.mult.setText("1")
        elif not float(self.mult.text()):
            self.numMultiplier = 1.0
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Multiplier should be a positive number!\nPlease choose non-zero multiplier.')
            msg.setWindowTitle("Invalid multiplier")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            self.mult.setText("1")
        else:
            self.numMultiplier = float(self.mult.text())

        self.k = self.samples_data_lables

        self.keyStr = ""

        # for i in range(len(self.keyList)):
        #     if i == 0:
        #         self.keyStr = ", key: "
        #     self.keyStr = self.keyStr + self.keyList[i]
        #     if i < len(self.keyList)-1:
        #         self.keyStr = self.keyStr + ", "

        # self.K = self.plot_data[1]["heat_data"]
        self.K = self.samples_data
        #self.K = self.plot_data_samples
        # print("self.k")
        # print(self.K)
        # print(len(self.K))
        self.ky = [h[0] for h in self.K[0]]
        self.n = len(self.k)
        # self.T = self.samples_time
        # self.t = len(self.T)
        self.optx = self.plot_data[1]["optim_x_val"]
        self.optf = self.plot_data[1]["optim_func_label_value"]
        self.ymin = min([y[1] for y in self.K[0]])
        ymax = 0

        for i in range(0, len(self.K)):
            for j in range(0, len(self.K[i])):
                tmp = list(self.K[i][j])
                tmp[0] = self.numMultiplier * tmp[0]
                self.K[i][j] = tuple(tmp)

        # for i in range(0, len(self.T)):
        #     for j in range(0, len(self.T)):
        #         tmp = list(self.T)
        #         tmp[0] = self.numMultiplier * tmp[0]
        #         self.T = tuple(tmp)
        self.funcmax = 0
        colors = pl.cm.jet(np.linspace(0, 1, self.n))
        if len(colors) > 30:
            np.random.shuffle(colors)
        # print(self.n)
        # print(type(self.n))

        for m in range(0, self.n):
            # print("m")
            # print(m)
            #print(x[0])

            X = [x[0] for x in self.K[m]]
            Y = [x[1] for x in self.K[m]]
            #Y = [x[1] for x in self.T[m]]
            if self.use_logscaleX:
                self.ax.set_xscale('log')

            if self.use_logscaleY:
                self.ax.set_yscale('log')
            # print(" X ")
            print("x a y")
            print(len(X))
            # print(" Y ")
            print(len(Y))
            xmin = min(X)
            print(xmin)
            xmax = max(X)
            print(xmax)
            ymin0 = min(Y)
            print(ymin0)
            ymax0 = max(Y)
            print(ymax0)
            self.avx = 0.5 * (xmin + xmax)

            if self.ymin > ymin0:
                self.ymin = ymin0

            for idx, it in enumerate(Y):
                if it == ymax0 and it > ymax:
                    ymax = ymax0
                    xmax = X[idx]
                    self.funcmax = self.k[m]


            if self.sw:
                if self.plotType:
                    self.ax.scatter(Y, X, label=self.k[m], color=colors[m], s=self.dotSizeSpinBox.value())
                else:
                    if self.k[m] == 'Noisy samples':
                        self.ax.scatter(Y, X, label=self.k[m], color=colors[m], s=self.dotSizeSpinBox.value())
                    else:
                        self.ax.plot(Y, X, label=self.k[m], color=colors[m])
            else:
                if self.plotType:
                    self.ax.scatter(X, Y, label=self.k[m], color=colors[m], s=self.dotSizeSpinBox.value())
                else:
                    if self.k[m] == 'Noisy samples':
                        self.ax.scatter(X, Y, label=self.k[m], color=colors[m], s=self.dotSizeSpinBox.value())
                    else:
                        self.ax.plot(X, Y, label=self.k[m], color=colors[m])

        # plot structure
        self.xlab = self.samples_xlabel
        self.ylab = self.samples_ylabel
        print("self.ylab")
        print(self.ylab)

        if self.maxBox.isChecked():
            optStr = 'Maximum value is at sample: {}.'.format(int(xmax))
        else:
            optStr = ''

        if self.sw:
            self.ax.set_ylabel(self.xlab, fontsize=self.fontSize.value())
            self.ax.set_xlabel(self.ylab, fontsize=self.fontSize.value())
            self.ax.text(1.1 * self.ymin - 0.1 * ymax, 1.3 * xmin - 0.3 * xmax, optStr)
        else:
            self.ax.set_xlabel(self.xlab, fontsize=self.fontSize.value())
            self.ax.set_ylabel(self.ylab, fontsize=self.fontSize.value())
            self.ax.text(1.1 * xmin - 0.1 * xmax, 1.3 * self.ymin - 0.3 * ymax, optStr)

        self.ax.tick_params(labelsize=self.fontSize.value())

        self.ax.grid(linestyle='--')

        ylim_extension = self.max_sample_val * 0.01  # add one percent of max value to axis limit
        self.ax.set_ylim((self.min_sample_val - ylim_extension, self.max_sample_val + ylim_extension))

        handles, labels = self.ax.get_legend_handles_labels()
        self.legend_atribute = []
        print("textxt")
        print(handles)
        print("###")
        print(labels)
        self.label = []
        for i in labels:
            print("i v labels")
            print(i)
            i = self.text + i
            if i not in self.label:
                self.legend_atribute.append(i)

        # text
        # for i in self.legende_paramentr:
        #     #i = i + labels[idx]
        #     if "(" in i: #and i not in self.label:
        #         a = "".join(i)
        #         print(a)
        #         #a = i.split(self.combo_reg.currentText())[-1]
        #         res = re.search(r"\(([A-Za-z0-9_]+)\)", i)
        #         #res_2 = re.search(r"\[([A-Za-z0-9_]+)\]", i)
        #         #spl = res_2.group(1)
        #         #des = a.split("["+spl+"]")[-1]
        #         result = res.group(1) #+ " " + des
        #         print(result)
        #         self.legend_atribute.append(result)
        #         print(self.legend_atribute)
            self.label.append(i)
        print("____________________")
        print(self.legend_atribute)
        #print(self.legend_atribute)
        lgd = self.ax.legend(handles, self.legend_atribute, loc=2, bbox_to_anchor=(0.99, 1.00025), ncol=1, borderaxespad=0.,
                             prop={'size': self.fontSize.value()})
        # lgd.set_title("Clusters")

        for i in range(0, len(self.K)):
            for j in range(0, len(self.K[i])):
                tmp = list(self.K[i][j])
                tmp[0] = 1 / self.numMultiplier * tmp[0]
                self.K[i][j] = tuple(tmp)
        #self.typeButton_id_time.setEnabled(True)
        self.canvas.draw()
        if self.main_menu_instance:
            self.main_menu_instance.show()
        #print(self.main_menu_instance)
        # self.addButton.setEnabled(True)
        # self.resize((self.figure.get_size_inches()*self.figure.dpi)[0],self.height())


#novee
#pico tady to dodelej jinak te ondrej povesi za gule!!!!!!!!
#    !!!!!!!!
    def addAlgoToPlot(self):
        parameter = self.combo_algo.currentText()
        path = str(self.ownData["path"])
        data = []
        algo = []
        self.fontSize.setEnabled(True)
        csv_file = open(path, "r")
        if csv_file:
            reading = True
        for line in csv_file:
            if "#" in line and reading:
                str_prev = line
                size = line.split(";")[-1].strip("\n")
                size = float(size.split("[")[0])
            if parameter in line and "#" in str_prev:
                line = line.split(";")
                time = float(line[1].strip("\n"))
                tup = (size, time)
                data.append(tup)

                #algo.append(line[0])

        algo.append(parameter)

        csv_file.close()

        # data[0] = data[0][:len(data[1])]
        #
        # data = [[data[0][i], data[1][i]] for i in range(len(data[0]))]
        print(data)
        self.data.append(data)
        self.legenda.append(algo)
        print(self.data)
        self.number +=1
        self.plotA()

    def plotA(self):
        self.ax.clear()
        data = self.data
        legenda = self.legenda
        self.n = len(self.data)
        print(self.n)
        self.xlab = "size [b]"
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
                self.ax.scatter(X, Y, label=self.legenda[m], s=self.dotSizeSpinBox.value())
            else:
                self.ax.plot(X, Y, label=self.legenda[m])

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

