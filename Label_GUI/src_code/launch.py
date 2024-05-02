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
import itertools

import numpy as np
import pandas as pd
import glob
import sys
import os
import sip
import json

nickname = 'dtan986'

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
        self.out_folder_all =''
        self.index =0 # for counting only
        self.label_tag = False
        self.prefixOutputFolder = 'output_labeling'
        self.time_list=[]
        self.value_list=[]
        self.left_list =[]
        self.all_input_file_name = []

        # self.current_file_name = ''
        self.display_index =0 # index for display choose in terminal
        self.num_file_all = 0
        self.num_file_left = 0
        self.num_box_done = 0

        self.data_processed=DataProcessing()
        # try:
        #     self.data_processed.peak_detect(self.time_list,self.value_list)
        #     self.data_processed.data_split(self.time_list,self.value_list)
        # except IndexError:
        #     pass
        #self.listIns = np.array([[97.027,1,97.032,-1.25],[97.06,1,97.068,-1.25]]) # n*4 with (x,y - top-left -> bot-right)
        self.labelMask = None
        self.header = dict({'src_path':'','des_path':'','sum_file':0,'index':self.index,'left_list':''})
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

    def resett_val(self): #reset number of index and add name file to save log
        pass

    def getFile(self):
        """ This function will get the address of the csv file location
            also calls a readData function 
        """
        # self.filename = QFileDialog.getOpenFileName(filter="txt (*.txt)")[0]
        self.source_folder_path = QFileDialog.getExistingDirectory(caption='Select source data folder')
        self.out_folder_all = os.path.join(self.source_folder_path,self.prefixOutputFolder) # out_folder_all is ouput folder
        
        # self.all_input_path_src = os.path.basename([i for i in glob.glob(self.source_folder_path + "/*.txt")])
        self.all_input_file_name = [os.path.basename(file) for file in glob.glob(os.path.join(self.source_folder_path, '*.txt'))]
        self.num_file_all = len(self.all_input_file_name)

        if not os.path.exists(self.out_folder_all): #check xem da co folder out chua
            os.makedirs(self.out_folder_all)
            print(f'(X) Output folder does not exist. Created at \n{self.out_folder_all}\n')
        else:
            print(f"(V) Out folder have been existed at \n{self.out_folder_all}\n")
        
        self.readData()

    def shorcut_path(self,path):
        parts = path.split("/")
        sp = ".../"+ "/".join(parts[-3:])
        return sp
    
    def readData(self):
        self.data_processed=DataProcessing()
        # self.left_list = self.all_input_file_name
        self.num_file_left = self.num_file_all

        # khi da co file log thi vao day de lay tham so
        if os.path.exists(os.path.join(self.out_folder_all,"log.txt")):
            # print("da co file log roi")
            # If the file exists, read the JSON string from the file
            with open(os.path.join(self.out_folder_all,"log.txt"), 'r') as file:
                json_string = file.read()
                # Convert the JSON string to a dictionary
                json_string = json.loads(json_string)
                self.out_folder_all = json_string['des_path']
                self.source_folder_path = json_string['src_path']
                self.num_file_all = int(json_string['sum_file'])
                # self.index = json_string['index']
                self.left_list = list(json_string['left_list'])
                #print(f'day la danh sach log left {self.left_list}')
                self.num_file_left = len(self.left_list)
            
        else: # chua co file log thi khai bao cac bien o day
            # print('ghi nhan la chua co file log nha ')
            self.left_list = self.all_input_file_name
            self.header = dict({'src_path':self.source_folder_path,'des_path':self.out_folder_all,
                                'sum_file':self.num_file_all,'index':self.index,
                                'left_list':self.left_list})

        try:
            self.filename = self.left_list[-1] # lay file cuoi de cho vao chay luot dau tien
        except:
            print("Done job!")
            self.close()
            sys.exit()
        # print(f'left list is {self.left_list}')
        # print(f'path de mo la {os.path.join(self.source_folder_path,self.filename)}')

        sp_src = self.shorcut_path(self.filename) # thay vi hien thi folder source, hien thi file dang thuc thi, cap nhat theo update khi next file moi
        sp_des = self.shorcut_path(self.out_folder_all)

        
        self.src_path.setText(sp_src) # source path
        self.destination_path.setText(sp_des)
        
        self.title = os.path.splitext(self.filename)[0] # file_12323
        
        # print(f'\n\n {self.out_folder_all}\n {self.title}')
        self.name_out_file = os.path.join(self.out_folder_all,"label_"+self.title+".csv") # label for each indivisual csv file in 
        # try:
        with open(os.path.join(self.source_folder_path,self.filename), 'r') as file:
            lines = file.readlines()
            # Parse lines into lists of time and value using list comprehensions
            self.time_list = [float(line.split()[0]) for line in lines]
            self.value_list = [float(line.split()[1]) for line in lines]

            # Create a DataFrame
            try:
                self.data_processed.peak_detect(self.time_list,self.value_list)
                filtered_data_time=self.data_processed.data_split(self.time_list,self.value_list)
                reference_time=list(itertools.chain.from_iterable(filtered_data_time))
                signalMask=[0]*len(self.time_list)
                self.df = pd.DataFrame({'time': self.time_list, 'value': self.value_list,'signalMask':signalMask})
                self.df.loc[self.df['time'].isin(reference_time), 'signalMask'] = -1
                self.labelMask = [0] * len(self.df['time'])
                
            except:
                self.num_box_done =0
                self.index = 0
                self.filename = self.left_list.pop()
                self.save_state()
                self.readData()
                return
        
        self.Update()
        # except Exception as e:
        #     print(f'[{nickname}] Error in read file {self.filename}, error is: {e}')

    def choiceExport(self):
        self.out_folder_all = QFileDialog.getExistingDirectory(None, "Select a folder")
        print(f'path choice is {self.out_folder_all}')
        sp_src = self.shorcut_path(self.out_folder_all)
        self.out_folder_all.setText(sp_src)

    def trueLabel(self): # true label pressed, instances is assign to true
        # try:
        if self.num_box_done == len(self.data_processed.box):
            #Cập nhật label của instance cuối cùng
            start_index=self.data_processed.mark_index[self.index][0]
            end_index=self.data_processed.mark_index[self.index][1]
            self.labelMask[start_index:end_index+1] = [2]* (end_index-start_index+1)
            self.df['labelMask'] = self.labelMask
            self.df["finalLabel"] = self.df[["signalMask", "labelMask"]].apply(sum, axis=1)
            self.df.to_csv(self.name_out_file, index=False,float_format='%.6f')
            
            # self.filename = self.all_input_file_name.pop()
            self.num_box_done =0
            self.index = 0
            self.filename = self.left_list.pop()
            self.save_state()
            self.readData()
            return
        start_index=self.data_processed.mark_index[self.index][0]
        end_index=self.data_processed.mark_index[self.index][1]
        self.labelMask[start_index:end_index+1] = [2]* (end_index-start_index+1)
        self.df['labelMask'] = self.labelMask
        self.df["finalLabel"] = self.df[["signalMask", "labelMask"]].apply(sum, axis=1)
        self.df.to_csv(self.name_out_file, index=False,float_format='%.6f')
        self.index +=1
        self.Update()

        # except Exception as e:
        #     print(f'Error is: {e}')
        #     self.close()
        

    def falseLabel(self):# intance assign to false

        try:
            # self.data_processed.peak_detect(self.time_list,self.value_list)
            # self.data_processed.data_split(self.time_list,self.value_list)
            # start_index = np.where(self.df['time'] == self.listIns[self.index][0])[0][0]
            # end_index = np.where(self.df['time'] == self.listIns[self.index][2])[0][0]
            if self.num_box_done == len(self.data_processed.box):
                # self.filename = self.all_input_file_name.pop()
                self.num_box_done =0
                self.index = 0
                self.filename = self.left_list.pop()
                self.save_state()
                self.readData()
                return
            start_index=self.data_processed.mark_index[self.index][0]
            end_index=self.data_processed.mark_index[self.index][1]
            # print(start_index,end_index)
            self.labelMask[start_index:end_index+1] = [0]* (end_index-start_index+1)
            self.df['labelMask'] = self.labelMask
            self.df["finalLabel"] = self.df[["signalMask", "labelMask"]].apply(sum, axis=1)
            self.df.to_csv(self.name_out_file,index=False, float_format='%.6f')
            self.index +=1
            self.Update()
        # except IndexError:
        #     self.num_box_done =0
        #     self.index = 0
        #     self.filename = self.left_list.pop()
        #     self.save_state()
        #     self.readData()
        except:
            self.close()
        
    def backwardIns(self): #back to previous instance
         pass
    def forwardIns(self):
         pass
    def jumpTo(self): #Jump to specific positoin < current position
         pass
    
    def save_state(self):
        self.header['src_path'] = self.source_folder_path
        self.header['des_path'] = self.out_folder_all
        self.header['index'] = self.index
        self.header['left_list'] = self.left_list
        self.header['sum_file'] = self.num_file_all
        save_log = json.dumps(self.header)
        with open(os.path.join(self.out_folder_all,'log.txt'), 'w') as file:
            file.write(save_log)

    def Update(self):
        plt.clf()
        
        #Cập nhật dữ liệu ban đầu cho def Update
        # self.Update_readdata()
        self.data_processed.peak_detect(self.time_list,self.value_list)
        self.data_processed.data_split(self.time_list,self.value_list)
        if self.num_box_done < len(self.data_processed.box):
            self.num_box_done +=1

        # Remove the existing canvas and toolbar
        self.graph_layout.removeWidget(self.canv)
        self.toolbarLayout.removeWidget(self.toolbar)
        sip.delete(self.canv)
        sip.delete(self.toolbar)
        self.canv = None
        self.toolbar = None
        self.displayCur.display(self.index)
        
        self.save_state()
        
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
        self.errorCheck=0
        self.box=[]
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
        
        #Gộp các tín hiệu có phần dữ liệu chung
        for count in range(len(filtered_data_time)-1):
            intersection_check=any(time in filtered_data_time[count] for time in filtered_data_time[count+1])
            if intersection_check:
                filtered_data_time[count+1]= filtered_data_time[count]+ filtered_data_time[count+1]
                filtered_data_time[count]=[0]
        
        filtered_data_time=[time for time in filtered_data_time if time!=[0]]
        
        for last_count in range(len(filtered_data_time)):
            filtered_data_time[last_count]=self.remove_duplicates(filtered_data_time[last_count]) 
        
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
        # print(f'Number of box is {len(self.box)}')

        return filtered_data_time
    
    def remove_duplicates(self,lst):
            element_count = {}
            result = []
            for item in lst:
                if element_count.get(item, 0) == 0:
                    element_count[item] = 1
                    result.append(item)
            return result
    
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	qt_app = LabelApp()
	qt_app.show()
	app.exec_()