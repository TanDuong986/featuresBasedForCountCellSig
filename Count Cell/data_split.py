import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def data_split(true_peak_time, true_trough_time, data_time, data_value):
    total_time=true_peak_time+true_trough_time
    total_time=sorted(total_time)

    #Tìm đỉnh đầu tiên, xóa phần thời gian phía trước
    index_of_peak = total_time.index(true_peak_time[0])
    total_time = total_time[index_of_peak:]

    #Xóa các đỉnh, đáy liên tiếp trùng nhau
    i=0
    while True:
        if total_time[i] in true_peak_time:
            while i + 1 < len(total_time) and total_time[i + 1] in true_peak_time:
                total_time[i+1]=0
                i=i+1
            i=i+1
        elif total_time[i] in true_trough_time:
            while i + 1 < len(total_time) and total_time[i + 1] in true_trough_time:
                total_time[i+1]=0
                i=i+1
            i=i+1
        if i==len(total_time):
            break
    total_time=[i for i in total_time if i!=0]
    
    #Xóa đỉnh thừa
    peak_count=sum(1 for c in true_peak_time if c in total_time)
    trough_count=sum(1 for c in true_trough_time if c in total_time)
    if peak_count>trough_count:
        total_time.pop()
    print("Len totaltime: ",len(total_time))

    # total_value=[]
    # for index in range(len(total_time)):
    #     true_index=data_time.index(total_time[index])
    #     true_value=data_value[true_index]
    #     total_value.append(true_value)

    # d_y_list=[]
    # d_x_list=[]
    
    # for test in range(0,len(total_time),2):
    #     d_y=abs(float(total_value[test]))
    #     d_x=abs(float(total_value[test]/total_value[test+1]))

    #     d_y_list.append(d_y)
    #     d_x_list.append(d_x)
    # total_time.insert(0,0)  

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

        # #Bounding box
        # #Lấy giá trị index theo trục x
        # xleft_index= data_time.index(filtered_data_time[0])-1
        # xright_index=data_time.index(filtered_data_time[-1])+1

        # #Lấy giá trị theo trục y
        # peak_value=data_value(data_time.index(total_time[i]))
        # ytop_value=peak_value+1e-2
        # trough_value=data_value(data_time.index(total_time[i+1]))
        # ybottom_value=trough_value-1e-2
    return filtered_data_time,filtered_data_value