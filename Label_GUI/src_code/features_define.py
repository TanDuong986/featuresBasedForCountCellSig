import numpy as np
from scipy.optimize import curve_fit

#Điều chỉnh hệ số tương quan giữa 2 trục time và value
def axis_fix(signal_data_time):
    signal_data_time=np.array(signal_data_time)*800

    return signal_data_time

#Khoảng cách euclid giữa 2 điểm đầu và cuối
def e_distance(signal_data_time, signal_data_value):
    signal_data_time=axis_fix(signal_data_time)
    euclid_distance=np.sqrt((signal_data_time[-1]-signal_data_time[0])**2+(signal_data_value[-1]-signal_data_value[0])**2)

    return euclid_distance

#Khoảng chênh lệch theo phương dọc của 2 điểm đầu và cuối
def margin_difference(signal_data_value):
    signal_margin_diff=abs(signal_data_value[0]-signal_data_value[1])
    
    return signal_margin_diff

#Độ chênh lệch về giá trị của 2 đỉnh trên dưới
def peak_difference_proportion(signal_data_value):
    top_peak=max(signal_data_value)
    bot_peak=min(signal_data_value)
    if top_peak>abs(bot_peak):
        top_bot_diff=top_peak/(abs(bot_peak))
    else:
        top_bot_diff=abs(bot_peak)/top_peak

    return top_bot_diff

#Chênh lệch theo phương dọc của 2 giá trị tại đường cắt đôi tín hiệu
def cut_points_difference(signal_data_value):
    half_divide=np.array_split(signal_data_value,2)
    half_left=half_divide[0]
    half_right=half_divide[1]
    half_diff=abs(half_left[-1]-half_right[0])

    return half_diff

#Độ dốc tại các mốc đỉnh và hai biên
def left_slope(signal_data_time,signal_data_value):
    #Lấy các giá trị đầu cuối và thời gian tương ứng
    signal_data_time=axis_fix(signal_data_time)
    left_point_value=signal_data_value[0]
    right_point_value=max(signal_data_value)
    left_point_time=signal_data_time[0]
    right_point_time=signal_data_time[signal_data_value.index(right_point_value)]

    #Tính góc
    left_angle=np.tan((right_point_time-left_point_time)/(right_point_value-left_point_value))

    return left_angle

def middle_slope(signal_data_time,signal_data_value):
    #Lấy các giá trị đầu cuối và thời gian tương ứng
    signal_data_time=axis_fix(signal_data_time)
    left_point_value=max(signal_data_value)
    right_point_value=min(signal_data_value)
    left_point_time=signal_data_time[signal_data_value.index(left_point_value)]
    right_point_time=signal_data_time[signal_data_value.index(right_point_value)]

    #Tính góc
    middle_angle=np.tan((right_point_time-left_point_time)/(right_point_value-left_point_value))

    return middle_angle

def right_slope(signal_data_time,signal_data_value):
    #Lấy các giá trị đầu cuối và thời gian tương ứng
    signal_data_time=axis_fix(signal_data_time)
    left_point_value=min(signal_data_value)
    right_point_value=signal_data_value[-1]
    left_point_time=signal_data_time(signal_data_value.index(left_point_value))
    right_point_time=signal_data_time[-1]

    #Tính góc
    right_angle=np.tan((right_point_time-left_point_time)/(right_point_value-left_point_value))

    return right_angle

#Elipse fit với tín hiệu khi được chia đôi
def left_elipse_fitting(signal_data_time,signal_data_value):
    def ellipse_func(x, a, b, c, d, e):
        return a * np.cos(2 * np.pi * x / b) + c + d * np.sin(2 * np.pi * x / b) + e
    
    def shoelace_area(signal_data_time,signal_data_value):
        # Triển khai công thức Shoelace
        area = 0
        for signal_point in range(len(signal_data_time) - 1):
            area +=(signal_data_time[signal_point]*signal_data_value[signal_point+1]) - (signal_data_time[signal_point + 1]*signal_data_value[signal_point])

        # Xử lý đa giác kín (kết nối điểm cuối cùng với điểm đầu tiên)
        area += (signal_data_time[-1] * signal_data_value[0]) - (signal_data_time[0] * signal_data_value[-1])

        return abs(area / 2.0)  

    #Fix trục time theo value
    signal_data_time=axis_fix(signal_data_time)

    #Lấy nửa phần dữ liệu bên trái
    top_peak=max(signal_data_value)
    bot_peak=min(signal_data_value)
    index_difference=signal_data_value.index(bot_peak)-signal_data_value.index(top_peak)
    cut_point=int(index_difference/2)+signal_data_value.index(top_peak)

    half_left_value=signal_data_value[:cut_point]
    half_left_time=signal_data_time[:cut_point]

    #Thực hiện tìm giá trị bán trục lớn và nhỏ
    a0 = 0.01  
    b0 = 0.01  
    c0 = 0.01  
    d0 = 0.01  
    e0 = 0.01  

    # Thực hiện fitting
    popt_left,_ = curve_fit(ellipse_func, half_left_time, half_left_value, p0=[a0, b0, c0, d0, e0])

    #Tính diện tích ellipse
    a=popt_left[0]
    b=popt_left[1]
    Se=np.pi*a*b

    #Diện tích phần lồi
    bulge_area=shoelace_area(half_left_time,half_left_value)
        
    #Độ fit với ellipse
    fit_percentage=(Se-bulge_area)/Se

    return fit_percentage

def right_elipse_fitting(signal_data_time,signal_data_value):
    def ellipse_func(x, a, b, c, d, e):
        return a * np.cos(2 * np.pi * x / b) + c + d * np.sin(2 * np.pi * x / b) + e
    
    def shoelace_area(signal_data_time,signal_data_value):
        # Triển khai công thức Shoelace
        area = 0
        for signal_point in range(len(signal_data_time) - 1):
            area +=(signal_data_time[signal_point]*signal_data_value[signal_point+1]) - (signal_data_time[signal_point + 1]*signal_data_value[signal_point])

        # Xử lý đa giác kín (kết nối điểm cuối cùng với điểm đầu tiên)
        area += (signal_data_time[-1] * signal_data_value[0]) - (signal_data_time[0] * signal_data_value[-1])

        return abs(area / 2.0)  

    #Fix trục time theo value
    signal_data_time=axis_fix(signal_data_time)

    #Lấy nửa phần dữ liệu bên trái
    top_peak=max(signal_data_value)
    bot_peak=min(signal_data_value)
    index_difference=signal_data_value.index(bot_peak)-signal_data_value.index(top_peak)
    cut_point=int(index_difference/2)+signal_data_value.index(top_peak)

    half_left_value=signal_data_value[cut_point:]
    half_left_time=signal_data_time[cut_point:]

    #Thực hiện tìm giá trị bán trục lớn và nhỏ
    a0 = 0.01  
    b0 = 0.01  
    c0 = 0.01  
    d0 = 0.01  
    e0 = 0.01  

    # Thực hiện fitting
    popt_left,_ = curve_fit(ellipse_func, half_left_time, half_left_value, p0=[a0, b0, c0, d0, e0])

    #Tính diện tích ellipse
    a=popt_left[0]
    b=popt_left[1]
    Se=np.pi*a*b

    #Diện tích phần lồi
    bulge_area=shoelace_area(half_left_time,half_left_value)
        
    #Độ fit với ellipse
    fit_percentage=(Se-bulge_area)/Se

    return fit_percentage

