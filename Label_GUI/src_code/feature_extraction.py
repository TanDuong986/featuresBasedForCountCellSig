import numpy as np
import pandas as pd
import read_label_files
import features_define

class ExtractFeature():
    def __init__(self) -> None:
        self.true_labeled_timelist=[]
        self.false_labeled_valuelist=[]
        self.false_labeled_timelist=[]
        self.sample_true_instance=[]
        self.sample_false_instance=[]

        self.sample_preparing()

    def sample_preparing(self):
        folder_path='Label_GUI\All files labelling\output_labeling'
        self.sample_true_instance,self.true_labeled_timelist,self.false_labeled_valuelist,self.false_labeled_timelist=read_label_files.read_label_file(folder_path=folder_path)
        self.sample_false_instance=self.false_labeled_valuelist[0:5000]

    def feature_extract(self):
        for instance in range(len(self.sample_true_instance)):
            true_feature_calculate=features_define.FeatureDefine(self.sample_true_instance[instance],self.true_labeled_timelist[instance])
            euclid_distance=true_feature_calculate.fe_dist()
            margin_diff=true_feature_calculate.margin_diff()
            peakProp=true_feature_calculate.peakProp()
            left_slope, mid_slope, right_slope=true_feature_calculate.slope()
            left_ellipse_prop=true_feature_calculate.ellipse_prop()

