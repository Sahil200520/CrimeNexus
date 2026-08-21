import pandas as pd
import os

def ingest_recidivism_data():
   root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
   accused_path = os.path.join(root_dir, "datasets", "AccusedData.csv")
   if not os.path.exists(accused_path):
       cleaned_path = os.path.join(root_dir, "Component_datasets", "Recidivism_cleaned_data.csv")
       return pd.read_csv(cleaned_path)
   acused = pd.read_csv(accused_path)

   acused.dropna(subset = ['age', 'Caste', 'Profession', 'Sex',
       'PresentCity', 'PresentState', 'Person_No'], inplace = True)
      
   acused.drop_duplicates(inplace = True)

   # Count the number of occurrences for each Person_No and Arr_ID combination
   acused['Recidivism'] = acused.groupby(['Person_No', 'Arr_ID'])['Person_No'].transform('size') > 1

   # Convert boolean to integer (1 for True, 0 for False)
   acused['Recidivism'] = acused['Recidivism'].astype(int)

   acused.drop(columns = [ 'UnitName', 'FIRNo', 'Year', 'Month', 'AccusedName',
       'Person_Name','PresentAddress','PermanentAddress', 'PermanentCity',
       'PermanentState', 'Nationality_Name', 'DOB', 'Person_No', 'Arr_ID',
       'crime_no','PresentState','Sex'], inplace = True)
      
   acused.drop_duplicates(inplace = True)

   acused = acused[(acused["age"]>7) & (acused["age"]<=100)]

   return acused



