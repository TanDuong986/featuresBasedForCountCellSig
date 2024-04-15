import main
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QFileDialog
import matplotlib.patches as patches 
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

import uuid
import numpy as np
import pandas as pd
import random
import sys
import os
import sip
import json

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
        self.time_list=[]
        self.value_list=[]
        self.data_processed=DataProcessing()
        # try:
        #     self.data_processed.peak_detect(self.time_list,self.value_list)
        #     self.data_processed.data_split(self.time_list,self.value_list)
        # except IndexError:
        #     pass
        #self.listIns = np.array([[97.027,1,97.032,-1.25],[97.06,1,97.068,-1.25]]) # n*4 with (x,y - top-left -> bot-right)
        self.labelMask = None
        self.header = dict({'src_path':'','des_path':'','index':self.index})
        self.name_out_file = None
        
        

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

    # #Tạo setter và getter cho time_list và value_list
    # @property
    # def time_list(self):
    #     return self._time_list
    
    # @time_list.setter
    # def time_list(self, new_time_list):
    #     self._time_list=new_time_list

    # @property
    # def value_list(self):
    #     return self._value_list
    
    # @value_list.setter
    # def value_list(self,new_value_list):
    #     self._value_list=new_value_list


    def getFile(self):
        """ This function will get the address of the csv file location
            also calls a readData function 
        """
        self.filename = QFileDialog.getOpenFileName(filter="txt (*.txt)")[0]
        self.destination = os.path.join(os.path.dirname(self.filename),self.prefixOutputName) # destination is ouput log_file path
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
        self.title = os.path.splitext(base_name)[0]
        self.name_out_file = os.path.join(self.destination,"label_"+self.title+".csv")
        # try:
        with open(self.filename, 'r') as file:
            lines = file.readlines()

        # Parse lines into lists of time and value using list comprehensions
        time = [float(line.split()[0]) for line in lines]
        value = [float(line.split()[1]) for line in lines]

        # Create a DataFrame
        self.df = pd.DataFrame({'time': time, 'value': value})
        self.labelMask = [0] * len(self.df['time'])
        # print(self.df.head(10))
        if os.path.exists(os.path.join(self.destination,"log.txt")):
            # If the file exists, read the JSON string from the file
            with open(os.path.join(self.destination,"log.txt"), 'r') as file:
                json_string = file.read()
            # Convert the JSON string to a dictionary
            json_string = json.loads(json_string)
            self.destination = json_string['des_path']
            self.filename = json_string['src_path']
            self.index = json_string['index']
            
        else:
            self.header = dict({'src_path':self.filename,'des_path':self.destination,'index':self.index})
        
        self.Update()
        # except Exception as e:
        #     print("An error occured: ",e)
        
    def choiceExport(self):
        self.destination = QFileDialog.getExistingDirectory(None, "Select a folder")
        print(f'path choice is {self.destination}')
        sp_src = self.shorcut_path(self.destination)
        self.destination_path.setText(sp_src)
     
    def Update_readdata(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()

        # Parse lines into lists of time and value using list comprehensions
        time = [float(line.split()[0]) for line in lines]
        value = [float(line.split()[1]) for line in lines]

        self.time_list=time
        self.value_list=value

    def trueLabel(self): # true label pressed, instances is assign to true
        try:
            # self.readData()
            # self.data_processed.peak_detect(self.time_list,self.value_list)
            # self.data_processed.data_split(self.time_list,self.value_list)
            # start_index = np.where(self.df['time'] == self.listIns[self.index][0])[0][0]
            # end_index = np.where(self.df['time'] == self.listIns[self.index][2])[0][0]
            start_index=self.data_processed.mark_index[self.index][0]
            end_index=self.data_processed.mark_index[self.index][1]
            self.labelMask[start_index:end_index] = [1]* (end_index-start_index)
            self.df['labelMask'] = self.labelMask
            self.df.to_csv(self.name_out_file, index=False)
            self.index +=1
            self.Update()
        except:
            print("Done job.")
            self.close()
        

    def falseLabel(self):# intance assign to false

        try:
            # self.data_processed.peak_detect(self.time_list,self.value_list)
            # self.data_processed.data_split(self.time_list,self.value_list)
            # start_index = np.where(self.df['time'] == self.listIns[self.index][0])[0][0]
            # end_index = np.where(self.df['time'] == self.listIns[self.index][2])[0][0]
            start_index=self.data_processed.mark_index[self.index][0]
            end_index=self.data_processed.mark_index[self.index][1]
            # print(start_index,end_index)
            self.labelMask[start_index:end_index] = [0]* (end_index-start_index)
            self.df['labelMask'] = self.labelMask
            self.df.to_csv(self.name_out_file, index=False)
            self.index +=1
            self.Update()
        except:
            print("Done job.")
            self.close()
        
    
    def backwardIns(self): #back to previous instance
         pass
    def forwardIns(self):
         pass
    def jumpTo(self): #Jump to specific positoin < current position
         pass


    def Update(self):
        plt.clf()
        
        #Cập nhật dữ liệu ban đầu cho def Update
        self.Update_readdata()
        self.data_processed.peak_detect(self.time_list,self.value_list)
        self.data_processed.data_split(self.time_list,self.value_list)
        
        # Remove the existing canvas and toolbar
        self.graph_layout.removeWidget(self.canv)
        self.toolbarLayout.removeWidget(self.toolbar)
        sip.delete(self.canv)
        sip.delete(self.toolbar)
        self.canv = None
        self.toolbar = None
        self.displayCur.display(self.index)

        self.header['src_path'] = self.filename
        self.header['des_path'] = self.destination
        self.header['index'] = self.index
        save_log = json.dumps(self.header)
        with open(os.path.join(self.destination,'log.txt'), 'w') as file:
            file.write(save_log)
        
        
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
        #self.df.reset_index(drop=True, inplace=True)  # Reset index to ensure time values are treated as data
        self.df.plot(x='time',y='value', ax=ax, legend=True)  # Plot the DataFrame with specified y column
        try:
            #xy = (self.listIns[self.index][0],self.listIns[self.index][1])
            xy= (self.data_processed.box[self.index][0],self.data_processed.box[self.index][1])
                # width = self.listIns[self.index][-2]-self.listIns[self.index][0]
                # height = self.listIns[self.index][-1]-self.listIns[self.index][1]
            width = self.data_processed.box[self.index][-2]-self.data_processed.box[self.index][0]
            height = self.data_processed.box[self.index][-1]-self.data_processed.box[self.index][1]
            rect = patches.Rectangle(xy,
                                    width=width,
                                    height=height,
                                    linewidth=1,edgecolor ='r',
                                    facecolor = 'None')
            ax.add_patch(rect)
            self.canv.draw()

        except IndexError:
            print(f'This job is already done !')
            self.close()
        
class DataProcessing:
    def __init__(self):
        self.init_list=None
        self.true_peak_time=[]
        self.true_trough_time=[]
        self.box=[]
        self.mark_index=[]
    def peak_detect(self,data_time,data_value):

        peaks,_ =find_peaks(data_value,height=1e-1,prominence=1e-1)
        troughs,_=find_peaks(-np.array(data_value),height=-1e-1,prominence=1e-1)
        length_peak=len(peaks)
        length_trough=len(troughs)
        true_peak_value=[]
        true_trough_value=[]
        trough_count=0
        peak_count=0

        for count in range(length_peak):
            peak_order=peaks[count]
            if data_value[peak_order]>0.1:
                peak_count=peak_count+1
                self.true_peak_time.append(data_time[peak_order])
                true_peak_value.append(data_value[peak_order])

        for i in range(length_trough):
            trough_order=troughs[i]
            if data_value[trough_order]<-0.1:
                trough_count=trough_count+1
                self.true_trough_time.append(data_time[trough_order])
                true_trough_value.append(data_value[trough_order])

        # plt.plot(time,value)

    def data_split(self,data_time,data_value):
        total_time=self.true_peak_time+self.true_trough_time
        total_time=sorted(total_time)

        #Tìm đỉnh đầu tiên, xóa phần thời gian phía trước
        index_of_peak = total_time.index(self.true_peak_time[0])
        total_time = total_time[index_of_peak:]

        #Xóa các đỉnh, đáy liên tiếp trùng nhau
        i=0
        while True:
            if total_time[i] in self.true_peak_time:
                while i + 1 < len(total_time) and total_time[i + 1] in self.true_peak_time:
                    total_time[i+1]=0
                    i=i+1
                i=i+1
            elif total_time[i] in self.true_trough_time:
                while i + 1 < len(total_time) and total_time[i + 1] in self.true_trough_time:
                    total_time[i+1]=0
                    i=i+1
                i=i+1
            if i==len(total_time):
                break
        total_time=[i for i in total_time if i!=0]
        
        #Xóa đỉnh thừa
        peak_count=sum(1 for c in self.true_peak_time if c in total_time)
        trough_count=sum(1 for c in self.true_trough_time if c in total_time)
        if peak_count>trough_count:
            total_time.pop()

        #Lấy từng cặp đỉnh đáy tương ứng để tham chiếu
        filtered_data_value=[]
        filtered_data_time=[]
        self.box=[]

        for i in range(int(((len(total_time)/2)))):

            peak_diff_list=[]
            trough_diff_list=[]
            signal_data_time=[]

            #Tìm vị trí tgian xuất hiện đỉnh, đáy
            peak_time_reference=total_time[2*i]
            peak_index_reference=data_time.index(peak_time_reference)
            right_peak_time=data_time[peak_index_reference]

            trough_time_reference=total_time[2*i+1]
            trough_index_reference=data_time.index(trough_time_reference)
            right_trough_time=data_time[trough_index_reference]

            #Lấy nửa dữ liệu bên trái đỉnh
            if i==0:
                former_time_range=int((total_time[2*i]-data_time[0])/1e-4)
                
            else:
                former_time_range=int((total_time[2*i]-total_time[2*i-1])/1e-4)
                
                
            signal_data_time.append(right_peak_time)

            for j in range(former_time_range):
                former_peak_time=data_time[peak_index_reference-j-1]
                later_peak_value=data_value[peak_index_reference-j]
                former_peak_value=data_value[peak_index_reference-j-1]
                peak_value_diff=later_peak_value-former_peak_value  

                peak_diff_list.append(peak_value_diff)
                signal_data_time.insert(0,former_peak_time)

                
                #Khi bắt được biên kề đinh
                if former_peak_value> later_peak_value:
                    del signal_data_time[0]
                    break
                else:
                    peak_check_item=0
                    for peak_diff_index in range(len(peak_diff_list)-1):
                        if peak_diff_list[peak_diff_index]>10*peak_diff_list[peak_diff_index+1]:
                            peak_check_item=1
                            break
                    if peak_check_item==1:
                        del signal_data_time[0]
                        break

            #Lấy đoạn dữ liệu từ phía đỉnh đến đáy( đoạn giữa)
            for interval_time in range(peak_index_reference+1,trough_index_reference):
                signal_data_time.append(data_time[interval_time])

            #Lấy nửa tín hiệu bên phải đáy
            #Khoảng cho phép lấy dữ liệu
            if i<int((len(total_time))/2)-1:
                later_time_range=int((total_time[2*(i+1)]-total_time[2*(i+1)-1])/1e-4)
                
            else:
                later_time_range=int((data_time[-1]-total_time[2*(i+1)-1])/1e-4)
                
            signal_data_time.append(right_trough_time)

            for k in range(later_time_range):
                later_trough_time=data_time[trough_index_reference+k+1]
                former_trough_value=data_value[trough_index_reference+k]
                later_trough_value=data_value[trough_index_reference+k+1]
                trough_value_diff=later_trough_value-former_trough_value

                trough_diff_list.append(trough_value_diff)
                signal_data_time.append(later_trough_time)

                #Khi bắt được biên kề đáy
                if later_trough_value< former_trough_value:
                    #signal_data_value.pop()
                    signal_data_time.pop()
                    break
                else:
                    trough_check_item=0
                    for trough_diff_index in range(len(trough_diff_list)-1):
                        if trough_diff_list[trough_diff_index]>10*trough_diff_list[trough_diff_index+1]:
                            trough_check_item=1
                            break
                    if trough_check_item==1:
                        signal_data_time.pop()
                        #signal_data_value.pop()
                        break

            #Đưa vector tín hiệu vào mảng tổng
            filtered_data_time.append(signal_data_time)

        #Lấy các cụm tế bào
        def remove_duplicates(lst):
            element_count = {}
            result = []
            for item in lst:
                if element_count.get(item, 0) == 0:
                    element_count[item] = 1
                    result.append(item)
            return result
        
        #Gộp các tín hiệu có phần dữ liệu chung
        for count in range(len(filtered_data_time)-1):
            intersection_check=any(time in filtered_data_time[count] for time in filtered_data_time[count+1])
            if intersection_check:
                filtered_data_time[count+1]= filtered_data_time[count]+ filtered_data_time[count+1]
                filtered_data_time[count]=[0]
        
        filtered_data_time=[time for time in filtered_data_time if time!=[0]]
        
        for last_count in range(len(filtered_data_time)):
            filtered_data_time[last_count]=remove_duplicates(filtered_data_time[last_count]) 
        

        #Tham chiếu lại value cho phần cụm 
        for vector_number in range(len(filtered_data_time)):
            signal_data_value=[]
            for vector_element_number in range(len(filtered_data_time[vector_number])):
                signal_time_index=data_time.index(filtered_data_time[vector_number][vector_element_number])
                signal_data_value.append(data_value[signal_time_index])
            filtered_data_value.append(signal_data_value)

        for vector_number in range(len(filtered_data_time)):
            #Lấy giá trị index theo trục x
            xleft_index= data_time.index(filtered_data_time[vector_number][0])
            xright_index=data_time.index(filtered_data_time[vector_number][-1])
            xleft_value=data_time[xleft_index]
            xright_value=data_time[xright_index]

            #Lấy giá trị theo trục y
            peak_value=max(filtered_data_value[vector_number])
            ytop_value=peak_value+1e-2
            trough_value=min(filtered_data_value[vector_number])
            ybottom_value=trough_value-1e-2

            mark=[xleft_index,xright_index]
            i_box=[xleft_value,ytop_value,xright_value,ybottom_value]
            self.box.append(i_box)
            self.mark_index.append(mark)
    
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	qt_app = LabelApp()
	qt_app.show()
	app.exec_()

