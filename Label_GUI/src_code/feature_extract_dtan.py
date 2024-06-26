import os
import pandas as pd
import numpy as np

def process_csv_files(folder_path):
    time_list = []
    value_list = []
    positive_mask_list = []
    negative_mask_list = []

    # Check if folder_path exists and is a directory
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist or is not a directory.")
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)
                
                # Ensure the necessary columns exist
                if not {'time', 'value', 'finalLabel'}.issubset(df.columns):
                    raise ValueError(f"The file '{filename}' does not contain the required columns.")
                
                # Extract the time, value, and mask columns
                time = df['time'].to_numpy()
                value = df['value'].to_numpy()
                mask = df['mask'].to_numpy()
                
                # Separate the mask into positive and negative classes
                positive_mask = np.where(mask == 1, value, np.nan)
                negative_mask = np.where(mask == -1, value, np.nan)
                
                # Append the arrays to the respective lists
                time_list.append(time)
                value_list.append(value)
                positive_mask_list.append(positive_mask)
                negative_mask_list.append(negative_mask)
            
            except pd.errors.EmptyDataError:
                print(f"Warning: The file '{filename}' is empty and has been skipped.")
            except pd.errors.ParserError:
                print(f"Warning: The file '{filename}' could not be parsed and has been skipped.")
            except Exception as e:
                print(f"Warning: An error occurred while processing the file '{filename}': {e}")
    
    return time_list, value_list, positive_mask_list, negative_mask_list

# Example usage
folder_path = 'path/to/csv/folder'
try:
    time_array, value_array, positive_mask_array, negative_mask_array = process_csv_files(folder_path)

    # Print lengths of the lists for verification
    print(f'Time array list length: {len(time_array)}')
    print(f'Value array list length: {len(value_array)}')
    print(f'Positive mask array list length: {len(positive_mask_array)}')
    print(f'Negative mask array list length: {len(negative_mask_array)}')

except Exception as e:
    print(f"Error: {e}")
