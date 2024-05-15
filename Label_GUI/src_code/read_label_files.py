import os
import pandas as pd

# Đường dẫn tới folder chứa các file csv
folder_path = r'Label_GUI/All files labelling/output_labeling'

# Khởi tạo các danh sách để lưu trữ dữ liệu từ các cột
true_labeled_timelist=[]
true_labeled_valuelist=[]
false_labeled_timelist=[]
false_labeled_valuelist=[]

# Lặp qua tất cả các file trong folder
for filename in os.listdir(folder_path):
    time_list = []
    value_list = []
    signal_mask_list = []

    true_labeled_signalTime=[]
    true_labeled_signalValue=[]
    false_labeled_signalTime=[]
    false_labeled_signalValue=[]

    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
    else:
        continue

    # Đọc file csv sử dụng pandas
    df = pd.read_csv(file_path)
    # print(df.head(5))
    # Thêm dữ liệu từ các cột vào các danh sách
    try:
        time_list.extend(df['time'].tolist())
        value_list.extend(df['value'].tolist())
        signal_mask_list.extend(df['finalLabel'].tolist())
    except:
        print(df.head()) 

    #Lấy các giá trị nhãn vào
    for signal_point in range(len(signal_mask_list)):
        #Lấy các giá trị time và value tương ứng với tín hiệu được đánh nhãn True
        if signal_mask_list[signal_point]==1:
            true_labeled_signalTime.append(time_list[signal_point])
            true_labeled_signalValue.append(value_list[signal_point])

            if signal_point==len(signal_mask_list)-1:
                true_labeled_timelist.append(true_labeled_signalTime)
                true_labeled_valuelist.append(true_labeled_signalValue)

        #Lấy các giá trị time và value tương ứng với tín hiệu được đánh nhãn False    
        elif signal_mask_list[signal_point]==-1:
            false_labeled_signalTime.append(time_list[signal_point])
            false_labeled_signalValue.append(value_list[signal_point])

            if signal_point==len(signal_mask_list)-1:
                false_labeled_timelist.append(false_labeled_signalTime)
                false_labeled_valuelist.append(false_labeled_signalValue)

        else:
            #Thêm True signal vào list True label
            if true_labeled_signalTime:
                true_labeled_timelist.append(true_labeled_signalTime)
                true_labeled_valuelist.append(true_labeled_signalValue)
                true_labeled_signalTime=[]
                true_labeled_signalValue=[]

            #Thêm False signal vào list False label
            elif false_labeled_signalTime:
                false_labeled_timelist.append(false_labeled_signalTime)
                false_labeled_valuelist.append(false_labeled_signalValue)
                false_labeled_signalTime=[]
                false_labeled_signalValue=[]


#Đếm số lượng True và False instance
true_instance_number=len(true_labeled_timelist)
false_instance_number=len(false_labeled_timelist)

print("Number of true instance: ",true_instance_number)
print("Number of false instance: ",false_instance_number)

print("first false instance: ",false_labeled_timelist[0])
print("first true instance: ",true_labeled_timelist[0])