# Presentation 1
# Darrell Corn
# 2/11/2021
# Find something interesting to present by Monday.

import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import numpy as np

def main():

    # Read the files
    print("Reading data...")
    dfAthlete = pd.read_csv("athlete_events_correct.csv")
    countries = gpd.read_file("TM_WORLD_BORDERS-0.3.shp")
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

    # Create geodataframe
    total = pd.merge(dfAthlete, countries, on = ['ISO3'], how = 'outer')
    gTotal = GeoDataFrame(total)

    # Create heat map
    fig, ax=plt.subplots(1, figsize=(13,8))
    gTotal.plot(column='MPC', linewidth=0.8, ax = ax, legend = True, missing_kwds={'color': 'lightgrey'})
    plt.show()

    # Create bar chart
    total = total.dropna()
    topC = total.nlargest(20, ['MPC'])
    topC.plot(x = 'NAME', y = 'MPC', kind = 'barh')
    #plt.show()

    # Create stacked bar chart
    topM = total.nlargest(20, ['Total Medals'])
    topM['bars'] = topM['Gold Medals'] + topM['Silver Medals']
    p1 = plt.barh(topM['NAME'], topM['Gold Medals'], label = 'Gold', color = 'gold')
    p2 = plt.barh(topM['NAME'], topM['Silver Medals'], label = 'Silver', color = 'silver', left=topM['Gold Medals'])
    p3 = plt.barh(topM['NAME'], topM['Bronze Medals'], label = 'Bronze', color = 'brown', left=topM['bars'])
    ax.legend()
    #plt.show()
main()
