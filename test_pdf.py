import pandas as pd

df = pd.DataFrame(columns=['euclid_distance','vertical_margin_diff','peakdiffProp','left_slope','mid_slope','right_slope',
                                  'left_ellipse_prop','right_ellipse_prop','standard_deviation'])


new_row_df = pd.DataFrame([[1,2,3,4,5,6,7,8,9]], columns=df.columns)
df = pd.concat([df, new_row_df],ignore_index=True)
print(df)