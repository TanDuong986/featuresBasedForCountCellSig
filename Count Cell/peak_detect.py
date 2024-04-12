import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def peak_detect(time,value):

    # Prominence: lấy theo ngưỡng bên Tự Nhiên cung cấp
    peaks,_ =find_peaks(value,height=1e-1,prominence=1e-1)
    troughs,_=find_peaks(-np.array(value),height=-1e-1,prominence=1e-1)
    length_peak=len(peaks)
    length_trough=len(troughs)
    true_peak_time=[]
    true_peak_value=[]
    true_trough_time=[]
    true_trough_value=[]
    trough_count=0
    peak_count=0

    for count in range(length_peak):
        peak_order=peaks[count]
        if value[peak_order]>0.1:
            peak_count=peak_count+1
            true_peak_time.append(time[peak_order])
            true_peak_value.append(value[peak_order])

    for i in range(length_trough):
        trough_order=troughs[i]
        if value[trough_order]<-0.1:
            trough_count=trough_count+1
            true_trough_time.append(time[trough_order])
            true_trough_value.append(value[trough_order])

    # print('So peak: ',peak_count)
    # print('So trough: ',trough_count)

    plt.plot(time,value)
    # plt.plot(true_peak_time, true_peak_value, 'x')
    # plt.plot(true_trough_time,true_trough_value,'x')
    # plt.axhline(y=0, color='gray', linestyle='--')
    # plt.show()

    return true_peak_time, true_trough_time
    

