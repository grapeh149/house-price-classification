import pandas as pd
import numpy as np


district = "1"
current_path = "D:\Data Analyst Project\housing-price-classification\data\data_raw"
save_path = "D:\Data Analyst Project\housing-price-classification\data\clean_data"
path = f"{current_path}\\data_Quan{district}.csv"

data = pd.read_excel(path)

#processing about column Price

# data = data[data['Price'] != "Thỏa thuận"]
# data['Price'] = data['Price'].apply(lambda x: x.split(" ")[0])
# data['Price'] = data['Price'].apply(lambda x: x.replace(",", ".")).astype(float)
# Area (m^2)
print(data.info())
data['Area'] = data['Area'].apply(lambda x: x.split(" ")[0])
data['Area'] = data['Area'].apply(lambda x: x.replace(",", ".")).astype(float)

data['Bedroom'] = data['Bedroom'].apply(
    lambda x: str(x).split(" ")[0] if pd.notna(x) else np.nan
)

data['Toilet, Bathroom'] = data['Toilet, Bathroom'].apply(
    lambda x: str(x).split(" ")[0] if pd.notna(x) else np.nan
)

# data['Toilet, Bathroom'] = data['Toilet, Bathroom'].apply(lambda x:x.replace(",", ".")).astype(float)

data['Floor'] = data['Floor'].apply(
    lambda x: str(x).split(" ")[0] if pd.notna(x) else np.nan
)

data['Home Direction'] = data['Home Direction'].apply(
    lambda x: str(x).split(" ")[0] if pd.notna(x) else np.nan
)


data['Facade'] = data['Facade'].apply(lambda x: str(x).split(" ")[0] if pd.notna(x) else np.nan)
data['Facade'] = data['Facade'].apply(lambda x: x.replace(",", ".") if pd.notna(x) else np.nan)
data['Facade'] = pd.to_numeric(data['Facade'], errors='coerce')


data['Access'] = data['Access'].apply(lambda x: str(x).split(" ")[0] if pd.notna(x) else np.nan)
data['Access'] = data['Access'].apply(lambda x: x.replace(",", ".") if pd.notna(x) else np.nan)
data['Access'] = pd.to_numeric(data['Access'], errors='coerce')



data.columns = ['Price', 'Area (m2)','Bedroom', 'Toilet, Bathroom', 'Floor', 'Home Direction', 'Facade',
                'Access' ,'Papers','Interior','Balcony view','Address']
print(data.iloc[:,2:])
print(data.info())

new_path = f"{save_path}\\data_Quan{district}.csv"
print(data)
print(data.info())
data.to_excel(new_path, index=False)

