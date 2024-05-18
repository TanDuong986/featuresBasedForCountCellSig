import numpy as np
from scipy.optimize import curve_fit
from scipy.spatial.distance import euclidean
import cvxpy as cp
import matplotlib.pyplot as plt
import pandas as pd
from itertools import groupby
from scipy.optimize import minimize
import read_label_files
from ellipse import LsqEllipse

class FeatureDefine():
    def __init__(self,value):
        self.value = value
        self.time=np.arange(len(value))/50
        self.left_list = []
        self.right_list = []
        self.ellipse_left = None
        self.ellipse_right = None

        self.split()
    
    
    def fe_dist(self): # eculien
        return euclidean((self.value[0],self.time[0]),(self.value[-1],self.time[-1]))
       
    def margin_diff(self):
        return abs(self.value[-1]-self.value[0])

    def peakProp(self):
        return abs(max(self.value)/min(self.value))
    
    def slope(self):
        p1 = (self.value[0],self.time[0])
        p2 = (max(self.value), self.time[np.argmax(self.value)])
        p3 = (min(self.value),self.time[np.argmin(self.value)])
        p4 = (self.value[-1],self.value[-1])
        def arctan(left_point,right_point):
            return np.tan((right_point[1]-left_point[1])/(right_point[0]-left_point[0]))
        return arctan(p2,p1),arctan(p3,p2),arctan(p4,p3)
    
    def shoelace_area(self,points):
        # Ensure the polygon is closed (first and last points are the same)
        if not np.allclose(points[0], points[-1]):
            points = np.vstack([points, points[0]])

        # Apply the Shoelace formula
        y = np.array(points[:, 1])
        x= np.array(points[:,0])
        area = 0.5 * np.abs(np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:]))

        return area

   

    def fit_ellipse(self,points):
        x2=np.array(points[:,1])
        x1=np.array(points[:,0])

        X = np.array(list(zip(x1, x2)))
        reg = LsqEllipse().fit(X)
        center, width, height, phi = reg.as_parameters()
        radii=[width,height]
        return center, radii,phi
    
    def compute_ellipse_area(self,radii):
        # Extract parameters
        radius_major, radius_minor = radii
        
        # Compute area
        area = np.pi * radius_major * radius_minor
        
        return area
    
    def split(self):
        split_point = (np.argmin(self.value)+np.argmax(self.value)) // 2
        self.left_list = np.vstack((self.time[0:split_point],self.value[0:split_point])).reshape(-1,2)
        self.right_list = np.vstack((self.time[split_point:-1],self.value[split_point:-1])).reshape(-1,2)
        self.ellipse_left = self.fit_ellipse(self.left_list)
        self.ellipse_right = self.fit_ellipse(self.right_list)
    
    #Tỉ lệ phần thừa của ellipse 
    def ellipse_prop(self,ellipse_list, left_list):
        area_ellipse = self.compute_ellipse_area(ellipse_list)
        area_left= self.shoelace_area(left_list)

        area_prop=abs(area_ellipse-area_left)/area_ellipse

        return area_prop 

    #Standard deviation
    def standard_deviation(self):
        return np.std(np.array(self.value))

