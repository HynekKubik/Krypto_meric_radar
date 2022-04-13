#!/usr/bin/env python3
import sys
from PyQt5 import QtGui, QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.cbook




class Window(QtWidgets.QDialog):
    sendInfo = QtCore.pyqtSignal(object)
    #print("samples print")

    def __init__(self, ownData=None, parent=None, main_menu_instance=None):
        super(Window, self).__init__(parent)
        # algo = ownData["selected_algor"]
        # self.ownData = ownData
        # print(ownData)
        # print(algo)
        self.ownData = ownData
        self.setWindowFlags(QtCore.Qt.Window)
        # a figure instance to plot on
        self.figure = Figure()
        # self.ax = self.figure.add_subplot(111)
        self.ax = self.figure.add_axes([0.1, 0.25, 0.8, 0.7])  # left,bottom edge, width, height
        self.use_logscaleX = False
        self.use_logscaleY = False
        self.setWindowTitle("Average bytes per second")
        self.scater_line = 0
        self.data = []
        self.legenda = []
        self.number = 0
        self.main_menu_instance = main_menu_instance
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)



        #self.typeButton = QtWidgets.QPushButton('Scatter plot')
        self.plotType = 0
        #self.typeButton.setFixedWidth(50)
        #self.typeButton.clicked.connect(self.changeType)



        #self.addButton = QtWidgets.QPushButton('Add to plot')
        #self.addButton.clicked.connect(self.addAlgoToPlot)
        #self.clearButton = QtWidgets.QPushButton('Clear plot')
        #self.clearButton.clicked.connect(self.clearCanvas)
        #self.combo_algo = QtWidgets.QComboBox(self)
        #self.combo_algo.addItem("Choose algoritm")
        # algo_one = []
        # for i in algo:
        #     if not i in algo_one:
        #         algo_one.append(i)
        # for i in algo_one:
        #     self.combo_algo.addItem(i)


        self.bf = QtGui.QFont("Arial", 13, QtGui.QFont.Bold)

        self.mult = QtWidgets.QLineEdit("1")
        self.mult.setAlignment(QtCore.Qt.AlignCenter)
        self.mult.setValidator(QtGui.QDoubleValidator())


        #self.multiple_samples = False
        self.legende_paramentr = []


        # set the layout
        layout = QtWidgets.QVBoxLayout()









        hlayout2 = QtWidgets.QHBoxLayout()

        #self.addButton.setFixedWidth(130)
        #hlayout2.addWidget(self.combo_algo)
        #hlayout2.addWidget(self.addButton)
        #hlayout2.setAlignment(QtCore.Qt.AlignRight)

        #layout.addLayout(hlayout2)



        #hlayout4 = QtWidgets.QHBoxLayout()
        #self.clearButton.setFixedWidth(130)
        #hlayout4.addWidget(self.clearButton)
        #hlayout4.setAlignment(QtCore.Qt.AlignRight)
        #layout.addLayout(hlayout4)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        #labelDotsize = QtWidgets.QLabel("Dot size: ")
        #labelDotsize.setFixedWidth(60)
        #self.dotSizeSpinBox = QtWidgets.QSpinBox()
        #self.dotSizeSpinBox.setFixedWidth(100)
        #self.dotSizeSpinBox.setMinimum(1)
        #self.dotSizeSpinBox.setMaximum(2147483647)
        #self.dotSizeSpinBox.valueChanged.connect(self.dotSizeChanged)
        #self.dotSizeSpinBox.setEnabled(False)

        #self.fontSize = QtWidgets.QLabel("Font size: ")
        # labelFontsize = QtWidgets.QLabel("Font size: ")
        # labelFontsize.setFixedWidth(60)
        # self.fontSize = QtWidgets.QSpinBox()
        # self.fontSize.setFixedWidth(100)
        # self.fontSize.setValue(13)
        # self.fontSize.setMinimum(10)
        # self.fontSize.setSingleStep(1)
        # self.fontSize.setMaximum(50)
        # #self.fontSize.valueChanged.connect(self.fontSizeChanged)
        # self.fontSize.setEnabled(False)
        #
        # hlayout = QtWidgets.QHBoxLayout()
        #
        #
        # hlayout.addWidget(labelFontsize)
        # hlayout.addWidget(self.fontSize)
        #hlayout.addWidget(labelDotsize)
        #hlayout.addWidget(self.dotSizeSpinBox)
        #hlayout.addWidget(self.typeButton)
        # layout.addLayout(hlayout)



        self.setLayout(layout)


        self.resize(900, 900)





        self.data = {"parameter" : [], "val" : []}
        print("samples konec")
        self.canvas.draw()
        self.load_file()
        print("draw")

    # def fontSizeChanged(self):
    #     if self.data:
    #         self.plot_bar()

    def load_file(self):
        path = str(self.ownData["path"])
        data = []
        algo = []
        #self.fontSize.setEnabled(True)
        csv_file = open(path, "r")
        if csv_file:
            reading = True
        for line in csv_file:
            if "#" in line and reading:
                str_prev = line
                size = line.split(";")[-1].strip("\n")
                size = float(size.split("[")[0])
                continue
            if ";" in line and "#" in str_prev and "[" in str_prev:
                line = line.split(";")
                #if parameter == line[0]:
                parameter = line[0]
                time = float(line[1].strip("\n"))
                print(size)
                print(time)
                if size == 0:
                    size=1
                avr = size/time
                tup = (parameter, avr)
                data.append(tup)
                str_prev = ""
                if not parameter in algo:
                    algo.append(parameter)

                #algo.append(line[0])

        #algo.append(parameter)

        csv_file.close()
        print("-----------------------------------------")
        print(data)

        data = sorted(data, key=lambda tup: tup[0])
        print(data)
        print("--------------------------------")
        #self.data.append(data)
        self.legenda.append(algo)
        #print(self.data)
        self.number +=1
        for i in algo:
            num = 0
            val = 0
            for j in data:
                print(i)
                if i == j[0]:
                    val =  val + j[1]
                    num = num + 1

            avg = val/num
            self.data["parameter"].append(i)
            self.data["val"].append(avg)
        self.plot_bar()
        print(self.data)

    def plot_bar(self):
        x = self.data["parameter"]
        y = self.data["val"]
        for i in range(len(x)):
            self.ax.bar(x[i], y[i])
        #if self.data:
            #self.ax.set_xlabel(x, fontsize=self.fontSize.value())
            #self.ax.set_ylabel(x, fontsize=self.fontSize.value())
        self.ax.set_ylabel("avg bytes per secund")#,fontsize = fontSize.value())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window(2)
    main.show()

    sys.exit(app.exec_())