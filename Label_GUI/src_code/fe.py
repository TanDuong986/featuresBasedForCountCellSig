import numpy as np
import pandas as pd
import read_label_files

from features_define import FeatureDefine
from sklearn.preprocessing import StandardScaler

class ExtractFeature:
    def __init__(self) -> None:
        self.true_labeled_timelist = []
        self.false_labeled_valuelist = []
        self.false_labeled_timelist = []
        self.sample_true_instance = []
        self.sample_false_instance = []

        self.sample_preparing()
        self.feature_extract()

    def sample_preparing(self):
        folder_path = 'Label_GUI/All files labelling/output_labeling'

        # Assuming read_label_files.read_label_file is defined and imported
        self.sample_true_instance, self.true_labeled_timelist, self.false_labeled_valuelist, self.false_labeled_timelist = read_label_files.read_label_file(folder_path=folder_path)
        self.sample_false_instance = self.false_labeled_valuelist[:5000]

    def standard_scale(self, feature_list):
        scaler = StandardScaler()
        return scaler.fit_transform(feature_list)
    
    def mad_normalize(self, feature_list):
        median = np.median(feature_list, axis=0)
        mad = np.median(np.abs(feature_list - median), axis=0)
        return (feature_list - median) / (mad + 1e-9)

    def feature_extract(self):
        def extract_features(instances, label):
            feature_list = []
            for instance in instances:
                try:
                    features = FeatureDefine(instance)
                    feature_values = [
                        features.fe_dist(),
                        features.margin_diff(),
                        features.peakProp(),
                        *features.slope(),
                        features.ellipse_prop(features.ellipse_left[1], features.left_list),
                        features.ellipse_prop(features.ellipse_right[1], features.right_list),
                        features.standard_deviation()
                    ]
                    if len(feature_values) == 9:
                        normalized_features = self.mad_normalize(np.array(feature_values))
                        feature_list.append(normalized_features)
                    else:
                        print(f"Error: Received incorrect number of features ({len(feature_values)}) for instance {instance}")
                except Exception as e:
                    print(f"Error: {e} occurred at instance {instance}")
            return feature_list

        true_features = extract_features(self.sample_true_instance, label=1)
        false_features = extract_features(self.sample_false_instance, label=-1)

        if true_features:
            true_scaled_features = self.standard_scale(true_features)
            self.save_to_csv(true_scaled_features, 'true_instance_featureExtraction.csv', label=1)

        if false_features:
            false_scaled_features = self.standard_scale(false_features)
            self.save_to_csv(false_scaled_features, 'false_instance_featureExtraction.csv', label=-1)

    def save_to_csv(self, scaled_features, filename, label):
        columns = ['euclid_distance', 'vertical_margin_diff', 'peakdiffProp', 'left_slope', 'mid_slope', 'right_slope', 
                   'left_ellipse_prop', 'right_ellipse_prop', 'standard_deviation']

        df = pd.DataFrame(scaled_features, columns=columns)
        df['label'] = label
        df.to_csv(filename, index=False)

if __name__ == "__main__":
    ExtractFeature()