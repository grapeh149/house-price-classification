import pandas as pd
import os
import glob

def load_data():
    current_path = os.getcwd()
    folder_path = pd.read_csv(f'{current_path}\\clean_data')
    csv_files = glob.glob(os.path.join(folder_path , "*.csv"))
    all_data = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    all_data.drop(columns=['Unnamed: 0'], inplace=True)
    print(all_data)
    return all_data




