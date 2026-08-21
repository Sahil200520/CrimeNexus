import pandas as pd
import os

def ingest_criminal_profiling():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    mob_path = os.path.join(root_dir, "datasets", "MOBsData.csv")
    rowdy_path = os.path.join(root_dir, "datasets", "RowdySheeterDetails.csv")
    accused_path = os.path.join(root_dir, "datasets", "AccusedData.csv")

    if not os.path.exists(mob_path):
        cleaned_path = os.path.join(root_dir, "Component_datasets", "Criminal_Profiling_cleaned.csv")
        return pd.read_csv(cleaned_path)

    MOB = pd.read_csv(mob_path)
    rowdy = pd.read_csv(rowdy_path)
    accused = pd.read_csv(accused_path)

    accused = accused[(accused['age'] <= 100) & (accused['age'] >= 7) ]

    accused =  accused.rename(columns = {'UnitName': 'Unit_Name'})
    accused =  accused.rename(columns = {'AccusedName': 'Name'})

    mob_relevant = MOB[['District_Name', 'Unit_Name', 'Name',
       'Occupation', 'ActSection', 'Crime_Group1',
       'Crime_Head2',
       ]]

    rowdy_relevant = rowdy[['District_Name', 'Unit_Name', 'Name',
      'Rowdy_Classification_Details',
       'Activities_Description',  'PrevCase_Details']]

    accused_relevant = accused[['District_Name', 'Unit_Name', 'Year', 'Month', 'Name',
        'age', 'Caste',  'Sex', 'PresentAddress', 'PresentCity']]

    merge = pd.merge(mob_relevant, rowdy_relevant,  on = ['District_Name', 'Unit_Name', 'Name',], how = 'inner' )
    merge = pd.merge(merge, accused_relevant,  on = ['District_Name', 'Unit_Name', 'Name', ], how = 'inner' )

    Criminal_Profiling = pd.DataFrame(merge)

    Criminal_Profiling = Criminal_Profiling.drop_duplicates()

    return Criminal_Profiling

