import os
import requests
import numpy
import urllib
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gp
import descartes as dct
import geopy
import codecs
from datetime import datetime, date, timedelta

#gotten from stack overflow through JAN 21 lecture which Dr. Williams used
def download_file(url, filename):
    ''' Downloads file from the url and save it as filename '''
    # check if file already exists
    if not os.path.isfile(filename):
        print('Downloading File')
        response = requests.get(url)
        # Check if the response is ok (200)
        if response.status_code == 200:
            # Open file and write the content
            with open(filename, 'wb') as file:
                # A chunk of 128 bytes
                for chunk in response:
                    file.write(chunk)
    else:
        print('File exists')

athleteDF = pd.read_csv("athlete_events.csv")
print(athleteDF)

#Got to do some data cleaning in order to be able to do some mathematics
#to determine the best build for each sport

#First, convert Medal values to numerical values.
#   No medal will be converted to 1 , since it should still
#   count for something to even make it to the Olympics
#   Bronze medal will be converted to 3
#   Silver medal will be converted to 5
#   Gold medal will be converted to 10

athleteDF['Medal'] = athleteDF['Medal'].replace('Gold', '10')
athleteDF['Medal'] = athleteDF['Medal'].replace('Silver', '5')
athleteDF['Medal'] = athleteDF['Medal'].replace('Bronze', '3')
athleteDF['Medal'] = athleteDF['Medal'].fillna('1')
athleteDF['Medal'] = pd.to_numeric(athleteDF['Medal'], errors='coerce')

athleteDF['Weight'] = athleteDF[['Weight']].mul(other=2.20462)
athleteDF['Height'] = athleteDF[['Height']].mul(other=0.393701)

#Second, clean up NA values in the Age, Height, and Weight columns.
#   Group athletes by sport, and where there are missing values for athletes of that
#   sport, replace it with the average of athletes in that sport.
#SOURCE for unique: https://chrisalbon.com/python/data_wrangling/pandas_list_unique_values_in_column/
sports = athleteDF['Sport'].unique()
frames = []

for sport in sports:
    currentSportDF = athleteDF.loc[athleteDF['Sport'] == sport]
    currentMeanAge = currentSportDF['Age'].mean()
    currentMeanHeight = currentSportDF['Height'].mean()
    currentMeanWeight = currentSportDF['Weight'].mean()
    currentSportDF['Age'] = currentSportDF['Age'].fillna(currentMeanAge)
    currentSportDF['Height'] = currentSportDF['Height'].fillna(currentMeanHeight)
    currentSportDF['Weight'] = currentSportDF['Weight'].fillna(currentMeanWeight)

    frames.append(currentSportDF)
    print(currentSportDF['Sport'])

athleteDF = pd.concat(frames)

#After rebuilding the dataframe, drop any rows that still have NaN for
#   Age, Height, or Weight. If the sport was in the Olympics before
#   athlete measurements were really recorded, the sport will likely be dropped
athleteDF = athleteDF.dropna(subset=['Age', 'Height', 'Weight'])
print(athleteDF[['Name', 'Age', 'Height', 'Weight', 'Medal']])

def getBestBuild(sportName, gender):
    #Want an: Age, Height, Weight, NOC
    #Take the weighted average of ages of medal winners

    medalWinnersDF = athleteDF[athleteDF['Medal'] != 1]
    medalWinnersDF = medalWinnersDF[medalWinnersDF['Sport'] == sportName]
    medalWinnersDF = medalWinnersDF[medalWinnersDF['Sex'] == gender]
    ageSum, heightSum, weightSum, rowCount = 0, 0, 0, 0
    for index, row in medalWinnersDF.iterrows():
        for i in range(row['Medal']):
            ageSum = ageSum + row['Age']
            heightSum = heightSum + row['Height']
            weightSum = weightSum + row['Weight']
            rowCount = rowCount + 1
    
    bestAge = ageSum / rowCount
    bestHeight = heightSum / rowCount
    bestWeight = weightSum / rowCount
    bestCountry = medalWinnersDF['NOC'].mode()

    print(bestCountry)

    print("Best Age:", bestAge)
    print("Best Height:", bestHeight)
    print("Best Weight:", bestWeight)
    print("Best Country:", bestCountry)



#Or maybe find the range of values based on medal
#Or maybe both




