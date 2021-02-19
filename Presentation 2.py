# Presentation 2
# Darrell Corn
# 2/11/2021
# Find something interesting to present by Tuesday.

import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

def main():

    # Read the files
    print("Reading data...")
    dfAthlete = pd.read_csv("athlete_events_correct.csv")
    dfUrbPop = pd.read_csv("UrbanPop.csv")
    dfGDP = pd.read_csv("GDP.csv")
    dfUnemp = pd.read_csv('Unemployment.csv')
    print("Data read!")

    # Create new columns that display medals as integers
    # Thanks https://www.dataquest.io/blog/tutorial-add-column-pandas-dataframe-based-on-if-else-condition/
    dfAthlete['Bronze Medals'] = np.where(dfAthlete['Medal'] == 'Bronze', 1, 0)
    dfAthlete['Silver Medals'] = np.where(dfAthlete['Medal'] == 'Silver', 1, 0)
    dfAthlete['Gold Medals'] = np.where(dfAthlete['Medal'] == 'Gold', 1, 0)
    dfAthlete['Total Medals'] = np.where(dfAthlete['Medal'] == 'Gold', 1,
        (np.where(dfAthlete['Medal'] == 'Silver', 1,
            (np.where(dfAthlete['Medal'] == 'Bronze', 1, 0)))))

    # Create columns of useful data
    dfAthlete = dfAthlete[['ISO3','Bronze Medals','Silver Medals','Gold Medals', 'Total Medals', 'Contestants']]
    dfAthlete = dfAthlete.groupby('ISO3', as_index=False).sum()
    dfAthlete['MPC'] = dfAthlete['Total Medals']/dfAthlete['Contestants']*100
    
    # Merge Medals with Urban Pop
    dfUrbPop = dfUrbPop[['Name','ISO3','Urban Pop']]
    total = pd.merge(dfAthlete, dfUrbPop, on = "ISO3")

    # Merge total with GDP
    dfGDP = dfGDP[['ISO3','GDP']]
    total = pd.merge(total, dfGDP, on = 'ISO3')

    # Merge total with Unemployment
    dfUnemp = dfUnemp[['ISO3','Unemp']]
    total = pd.merge(total, dfUnemp, on = 'ISO3')
    #print(total)
    
    total.to_excel(r'C:\Users\Darrell Corn\Desktop\df3.xlsx', index = False, header=True)
    print('Exported "df3.xlsx" to desktop.')
main()

