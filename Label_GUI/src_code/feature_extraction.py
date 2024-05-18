import numpy as np
import pandas as pd
import read_label_files

from features_define import FeatureDefine
from sklearn.preprocessing import StandardScaler

class ExtractFeature():
    def __init__(self) -> None:
        self.true_labeled_timelist=[]
        self.false_labeled_valuelist=[]
        self.false_labeled_timelist=[]
        self.sample_true_instance=[]
        self.sample_false_instance=[]

        self.sample_preparing()
        self.feature_extract()

    def sample_preparing(self):
        folder_path='Label_GUI\All files labelling\output_labeling'

        #Lấy số lượng mẫu để trích xuất đặc trưng
        self.sample_true_instance,self.true_labeled_timelist,self.false_labeled_valuelist,self.false_labeled_timelist=read_label_files.read_label_file(folder_path=folder_path)
        self.sample_false_instance=self.false_labeled_valuelist[0:5000]

    #Scaling
    def standard_scale(self,feature_list):
         instance=StandardScaler()
         return instance.fit_transform(feature_list)
    
    #Normalizing
    def mad_normalize(self,feature_list):
        median = np.median(feature_list,axis=0)
        mad = np.median(np.abs(feature_list - median), axis=0)

        return (feature_list - median) / (mad + 1e-9)

    #Feature extracting
    def feature_extract(self):
        df= pd.DataFrame(columns=['euclid_distance','vertical_margin_diff','peakdiffProp','left_slope','mid_slope','right_slope',
                                  'left_ellipse_prop','right_ellipse_prop','standard_deviation','label'])
        
        true_instance_list=[]
        false_instance_list=[]
        for instance in range(len(self.sample_true_instance)):
            try:    
                true_feature_calculate=FeatureDefine(self.sample_true_instance[instance])
                euclid_distance=true_feature_calculate.fe_dist()
                vertical_margin_diff=true_feature_calculate.margin_diff()
                peakProp=true_feature_calculate.peakProp()
                left_slope, mid_slope, right_slope=true_feature_calculate.slope()
                left_ellipse_prop=true_feature_calculate.ellipse_prop(true_feature_calculate.ellipse_left[1],true_feature_calculate.left_list)
                right_ellipse_prop=true_feature_calculate.ellipse_prop(true_feature_calculate.ellipse_right[1],true_feature_calculate.right_list)
                standard_deviation=true_feature_calculate.standard_deviation()
                feature_list=[euclid_distance,vertical_margin_diff,peakProp,left_slope,mid_slope,right_slope,left_ellipse_prop,right_ellipse_prop,standard_deviation]

                normalized_feature=self.mad_normalize(np.array(feature_list))
                true_instance_list.append(list(normalized_feature))
                
            except Exception as e:
                print(f"Error: {e} occured at instance number: {instance}")
                continue

        true_scaled_feature=self.standard_scale(np.array(true_instance_list))
        for instance in range(len(true_scaled_feature)):     
            row=pd.DataFrame({'euclid_distance':[true_scaled_feature[instance][0]],
                'vertical_margin_diff':[true_scaled_feature[instance][1]],
                'peakdiffProp':[true_scaled_feature[instance][2]],
                'left_slope':[true_scaled_feature[instance][3]],
                'mid_slope':[true_scaled_feature[instance][4]],
                'right_slope':[true_scaled_feature[instance][5]],
                'left_ellipse_prop':[true_scaled_feature[instance][6]],
                'right_ellipse_prop':[true_scaled_feature[instance][7]],
                'standard_deviation':[true_scaled_feature[instance][8]],
                'label':1})
            
            df= pd.concat([df,row],ignore_index=True)

        df_true=df[df['label']==1]
        df_true.to_csv('true_instance_featureExtraction.csv',index=True)

        for instance in range(len(self.sample_false_instance)):
            try:
                false_feature_calculate=FeatureDefine(self.sample_false_instance[instance])
                euclid_distance=false_feature_calculate.fe_dist()
                vertical_margin_diff=false_feature_calculate.margin_diff()
                peakProp=false_feature_calculate.peakProp()
                left_slope, mid_slope, right_slope=false_feature_calculate.slope()
                left_ellipse_prop=false_feature_calculate.ellipse_prop(false_feature_calculate.ellipse_left[1],false_feature_calculate.left_list)
                right_ellipse_prop=false_feature_calculate.ellipse_prop(false_feature_calculate.ellipse_right[1],false_feature_calculate.right_list)
                feature_list=[euclid_distance,vertical_margin_diff,peakProp,left_slope,mid_slope,right_slope,left_ellipse_prop,right_ellipse_prop]

                normalized_feature=self.mad_normalize(np.array(feature_list))
                false_instance_list.append(normalized_feature)

            except Exception as e:
                continue

        false_scaled_feature=self.standard_scale(np.array(true_instance_list))
        for instance in range(len(false_scaled_feature)):

            row=pd.DataFrame({'euclid_distance':[false_scaled_feature[instance][0]],
                'vertical_margin_diff':[false_scaled_feature[instance][1]],
                'peakdiffProp':[false_scaled_feature[instance][2]],
                'left_slope':[false_scaled_feature[instance][3]],
                'mid_slope':[false_scaled_feature[instance][4]],
                'right_slope':[false_scaled_feature[instance][5]],
                'left_ellipse_prop':[false_scaled_feature[instance][6]],
                'right_ellipse_prop':[false_scaled_feature[instance][7]],
                'standard_deviation':[false_scaled_feature[instance][8]],
                'label':-1})
            
            df= pd.concat([df,row],ignore_index=True)

        df_false=df[df['label']==-1]
        df_false.to_csv('false_instance_featureExtraction.csv',index=True)


if __name__ == "__main__":
    feature_extract=ExtractFeature()