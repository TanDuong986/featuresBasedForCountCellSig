import main
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QFileDialog
import matplotlib.patches as patches 
import matplotlib.pyplot as plt

import uuid
import numpy as np
import pandas as pd
import random
import sys
import os
import sip

class MatplotlibCanvas(FigureCanvasQTAgg):
	def __init__(self,parent=None, dpi = 200):
		fig = Figure(dpi = dpi)
		self.axes = fig.add_subplot(111)
		super(MatplotlibCanvas,self).__init__(fig)
		fig.tight_layout()

class LabelApp(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(LabelApp, self).__init__()
        self.filename = ''
        self.title =''
        self.df = None
        self.destination =''
        self.cur1_path ='' #path of lastest file saved
        self.index =0
        self.label_tag = False
        self.prefixOutputName = 'out_label'
        self.listIns = np.array([[97.027,1,97.032,-1.25],[97.06,1,97.068,-1.25]]) # n*4 with (x,y - top-left -> bot-right)
        

        self.setupUi(self)
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv, self)
        self.toolbarLayout = QVBoxLayout(self.toolBarBox)
        self.toolbarLayout.addWidget(self.toolbar)

        # self.showFullScreen()
        self.showMaximized()
        self.setWindowTitle("Demo version")
        self.true_button.clicked.connect(self.trueLabel)
        self.false_button.clicked.connect(self.falseLabel)
        self.actionContinue.triggered.connect(self.getFile)
        self.actionExport.triggered.connect(self.choiceExport)
        self.actionExit.triggered.connect(self.close)
        self.backward.clicked.connect(self.backwardIns)
        self.forward.clicked.connect(self.forwardIns)
        self.Jump.clicked.connect(self.jumpTo)

        

    def getFile(self):
        """ This function will get the address of the csv file location
            also calls a readData function 
        """
        self.filename = QFileDialog.getOpenFileName(filter="txt (*.txt)")[0]
        self.destination = os.path.join(os.path.dirname(self.filename),self.prefixOutputName)
        if not os.path.exists(self.destination):
            os.makedirs(self.destination)
            print(f"(X) Output label folder does not exist. Created !!!.")
        else:
            print(f"(V) Out folder have been existed")

        
        sp_src = self.shorcut_path(self.filename)
        sp_des = self.shorcut_path(self.destination)

        self.src_path.setText(sp_src) # source path
        self.destination_path.setText(sp_des)
        self.readData()

    def shorcut_path(self,path):
        parts = path.split("/")
        sp = ".../"+ "/".join(parts[-4:])
        return sp
    def readData(self):
        
        base_name = os.path.basename(self.filename)
        self.source = os.path.dirname(self.filename)
        self.title = os.path.splitext(base_name)[0]
        # try:
        with open(self.filename, 'r') as file:
            lines = file.readlines()

        # Parse lines into lists of time and value using list comprehensions
        time_list = [float(line.split()[0]) for line in lines]
        value_list = [float(line.split()[1]) for line in lines]

        # Create a DataFrame
        self.df = pd.DataFrame({'time': time_list, 'value': value_list})
        # print(self.df.head(10))
        self.Update()
        # except Exception as e:
        #     print("An error occured: ",e)
    
    def choiceExport(self):
        self.destination = QFileDialog.getExistingDirectory(None, "Select a folder")
        print(f'path choice is {self.destination}')
        sp_src = self.shorcut_path(self.destination)
        self.destination_path.setText(sp_src)
     
    def trueLabel(self): # true label pressed, instances is assign to true
        pass
    def falseLabel(self):# intance assign to false
        pass
    
    def backwardIns(self): #back to previous instance
         pass
    def forwardIns(self):
         pass
    def jumpTo(self): #Jump to specific positoin < current position
         pass
    
    def saveState(self):
        '''purposes of this function is save 
        - file name (processing)
        - index of order instance
        - output path
        - the last save file
        '''
        pass

    def Update(self):
        plt.clf()
        
        # Remove the existing canvas and toolbar
        self.graph_layout.removeWidget(self.canv)
        self.toolbarLayout.removeWidget(self.toolbar)
        sip.delete(self.canv)
        sip.delete(self.toolbar)
        self.canv = None
        self.toolbar = None
        
        # Reinitialize the canvas and toolbar
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv, self.centralwidget)
        self.toolbarLayout.addWidget(self.toolbar)
        self.graph_layout.addWidget(self.canv)

        # Clear the axes and plot the DataFrame
        self.canv.axes.cla()
        ax = self.canv.axes
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Voltage (V)')
        # self.df.reset_index(drop=True, inplace=True)  # Reset index to ensure time values are treated as data
        self.df.plot(x='time',y='value', ax=ax, legend=True)  # Plot the DataFrame with specified y column
        xy = (self.listIns[self.index][0],self.listIns[self.index][1])
        width = self.listIns[self.index][-2]-self.listIns[self.index][0]
        height = self.listIns[self.index][-1]-self.listIns[self.index][1]
        rect = patches.Rectangle(xy,
                                 width=width,
                                 height=height,
                                 linewidth=1,edgecolor ='r',
                                 facecolor = 'None')
        print(xy,width,height)
        ax.add_patch(rect)
        self.canv.draw()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	qt_app = LabelApp()
	qt_app.show()
	app.exec_()

