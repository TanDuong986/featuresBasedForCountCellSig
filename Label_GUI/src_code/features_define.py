import numpy as np
from scipy.optimize import curve_fit
from scipy.spatial.distance import euclidean
import cvxpy as cp
import matplotlib.pyplot as plt
import pandas as pd
from itertools import groupby
from scipy.optimize import minimize

class FeatureExtraction():
    def __init__(self,value,time,alpha=800):
        self.value = value
        self.alpha = alpha
        self.numpoint = len(value)
        self.label = False
        self.left_list = []
        self.righ_list = []
        self.ellipse_left = None
        self.ellipse_right = None

        self.prop_left =0
        self.prop_right =0

        self.time = self.scale_axis(time)
        self.split()
    
    def scale_axis(self, time):
        return np.array(time) * self.alpha
    
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
        x = points[:, 0]
        y = points[:, 1]
        area = 0.5 * np.abs(np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:]))

        return area

    # def fit_ellipse(self, points):
    #     n, d = points.shape
        
    #     # Create optimization variables
    #     A = cp.Variable((d, d), symmetric=True)
    #     b = cp.Variable((d, 1))
    #     c = cp.Variable(1)
        
    #     # Objective: Minimize volume of ellipse
    #     objective = cp.Minimize(cp.log_det(A))
        
    #     # Constraints: All points lie inside or on the boundary of the ellipse
    #     constraints = [cp.norm(A @ points[i, :][:, np.newaxis] + b) <= 1 + c for i in range(n)]

        
    #     # Form and solve problem
    #     problem = cp.Problem(objective, constraints)
    #     problem.solve()
        
    #     # Extract ellipse parameters
    #     center = -np.linalg.inv(A.value) @ b.value
    #     radii = np.sqrt(1 / np.diag(A.value))
    #     orientation = np.arctan2(A.value[1, 0], A.value[0, 0])
        
    #     return center, radii, orientation

    def fit_ellipse(self, points):
        # Extract x and y coordinates of points
        x = points[:, 0]
        y = points[:, 1]

        # Objective function: minimize sum of squared errors between points and ellipse
        def objective(params):
            a, b, c, d, e = params
            return np.sum(((a * x + b * y + c) ** 2) / (x ** 2 + y ** 2 + 1e-10) + ((d * x + e * y + 1) ** 2) / (x ** 2 + y ** 2 + 1e-10))

        # Initial guess for ellipse parameters
        params0 = [1, 0, 0, 0, 1]

        # Minimize the objective function to find ellipse parameters
        result = minimize(objective, params0, method='Nelder-Mead')
        params = result.x

        # Extract ellipse parameters
        a, b, c, d, e = params
        A = np.array([[a, b], [d, e]])
        center = np.linalg.inv(A) @ np.array([[-c], [-1]])
        radii = np.sqrt(np.linalg.eigvals(A))
        orientation = np.arctan2(A[1, 0], A[0, 0])

        return center, radii, orientation
    
    def compute_ellipse_area(self,radii):
        # Extract parameters
        radius_major, radius_minor = radii
        
        # Compute area
        area = np.pi * radius_major * radius_minor
        
        return area
    
    def plot_ellipse(center, radii, orientation, ax=None, color='blue', label=None):
        if ax is None:
            ax = plt.gca()

        # Generate angle values from 0 to 2*pi
        theta = np.linspace(0, 2*np.pi, 100)

        # Compute ellipse points
        x = center[0] + radii[0] * np.cos(theta) * np.cos(orientation) - radii[1] * np.sin(theta) * np.sin(orientation)
        y = center[1] + radii[0] * np.cos(theta) * np.sin(orientation) + radii[1] * np.sin(theta) * np.cos(orientation)

        # Plot ellipse
        ax.plot(x, y, color=color, label=label)
        ax.set_aspect('equal', 'box')
        ax.grid(True)
        ax.legend()

    def split(self):
        split_point = (np.argmin(self.value)+np.argmax(self.value)) // 2
        self.left_list = np.vstack((self.time[0:split_point],self.value[0:split_point])).reshape(-1,2)
        self.righ_list = np.vstack((self.time[split_point:-1],self.value[split_point:-1])).reshape(-1,2)
        self.ellipse_left = self.fit_ellipse(self.left_list)
        
        area_ellipse_left = self.compute_ellipse_area(self.ellipse_left[1])
        area_left_chain = self.shoelace_area(self.left_list)

        self.prop_left = area_left_chain/area_ellipse_left

        self.ellipse_right = self.fit_ellipse(self.righ_list)
        area_ellipse_right = self.compute_ellipse_area(self.ellipse_right[1])
        area_right_chain = self.shoelace_area(self.righ_list)

        self.prop_right = area_right_chain/area_ellipse_right
        self.plot_ellipse(self.ellipse_left)


    #chia doi dai tin hieu de fit ellipse
    #tinh gia tri cao do tu diem o giua den 0 la 1 dac trung
    #viet ham tinh ti le cua phan thua so voi dien tich ellipse
if __name__ == "__main__":
    data = pd.read_csv('H:/UET/MEMS/CountCell/featuresBasedForCountCellSig/Label_GUI/100_files_test/output_labeling/label_file1496.csv')
    groups = []
    interMask = data[data['labelMask'] == 1]
    for key, group in groupby(enumerate(interMask.index), lambda x: x[1] - x[0]):
        group = list(map(lambda x: x[1], group))
        instance = FeatureExtraction(data.loc[group,'value'],data.loc[group,'time'],800)
        groups.append(group)
        print("\n")
    
    # print(groups)
