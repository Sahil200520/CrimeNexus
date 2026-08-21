import math
import pandas as pd
import re
import logging
import sys


import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

def ingest_crime_pattern_analysis():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_path = os.path.join(root_dir, "datasets", "FIR_Details_Data.csv")
    if not os.path.exists(data_path):
        data_path = os.path.join(root_dir, "Component_datasets", "Crime_Pattern_Analysis_Cleaned.csv")
    fir_details = pd.read_csv(data_path)
    logging.info("Ingested the raw datasets for Crime Pattern Analysis")

    #Feature selection
    fir_relevant = fir_details[['District_Name', 'UnitName', 'FIRNo', 'Year', 'Month',
    'FIR_Reg_DateTime', 'CrimeGroup_Name', 'Latitude', 'Longitude', 'Distance from PS', 'VICTIM COUNT', 'Accused Count']]


    raw_data = pd.DataFrame(fir_relevant)


    logging.info(" Raw dataset sucessfully created for the Crime Pattern Analysis Component")

    return raw_data


