import matplotlib.pyplot as plt
import numpy as np
import peak_test
import data_split
import file_split

input_file='data.txt'
output_file="file"
file_split.data_taking(input_file)
with open(input_file,'r') as f:
    time = []
    value = []
    for line in f:
        p = line.split()
        time.append(float(p[0]))
        value.append(float(p[1]))

true_peak_time, true_trough_time=peak_test.peak_detect(time, value)
filtered_data_time, filtered_data_value=data_split.data_split(true_peak_time, true_trough_time,time,value)
time_reference=[time for merge_time in filtered_data_time for time in merge_time]
file_split.column_creating(input_file,time_reference)
file_split.split_file_by_difference(input_file,output_file,1e-4)

# for i in range(len(filtered_data_time)):
#     plt.plot(filtered_data_time[i],filtered_data_value[i],'orange')
# plt.show()