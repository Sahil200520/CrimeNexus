import pandas as pd
import os

def ingest_resource_data():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_path = os.path.join(root_dir, "datasets", "FIR_Details_Data.csv")
    if not os.path.exists(data_path):
        data_path = os.path.join(root_dir, "Component_datasets", "Resource_Allocation_Cleaned.csv")
        return pd.read_csv(data_path)
    df = pd.read_csv(data_path)

    df.drop(columns= df.columns[~df.columns.isin(['District_Name', 'UnitName', 'FIRNo', 'CrimeGroup_Name',
        'Beat_Name', 'Village_Area_Name',
       ])],inplace = True)

    df.drop_duplicates(inplace =  True)

    return df