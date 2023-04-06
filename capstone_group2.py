"""
Created on Thu Mar 23 22:31:31 2023

@author: sreed
"""

import requests
import csv
import pandas as pd
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt
import folium


#from sklearn.model_selection import train_test_split


def api(url):
    #get call to REST API
    response = requests.get(url)
    res = response.json()
    #traversing through json to gether required information
    crime_data = res['result']['records']
    #headers: all the columns present within the dataset
    headers = list(crime_data[0].keys())
    #writing the json file to data.csv file
    with open('data.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = headers)
        writer.writeheader() 
        for row in crime_data:
            writer.writerow(row)
    crime = pd.read_csv('data.csv', header=0)
    return crime

def culmap(data,typeofcrime):
    try:
        #Filtering data based on Offense_description
        crime = data[data['OFFENSE_DESCRIPTION'] == typeofcrime]
        map_center = [42.361145, -71.057083]  # Boston City coordinates
        my_map = folium.Map(location=map_center, zoom_start=12)
        # Create a feature group for the scatter plot points
        point_fg = folium.FeatureGroup(name="Scatter Plot")

        # Add each scatter plot point to the feature group
        for lat, lon in zip(crime['Lat'], crime['Long']):
            point_fg.add_child(folium.CircleMarker(location=[lat, lon], radius=2, color='red', fill=True, fill_color='red'))

        # Add the feature group to the map
        my_map.add_child(point_fg)
        return my_map
    except:
        print("An error has occured,Please check the dataset and the offense_description provided!!!")



def fill_missing_values(df, column, fill_method):
  
    if fill_method == 'mode':
        fill_value = df[column].mode()[0]
    elif fill_method == 'median':
        fill_value = df[column].median()
    elif fill_method == 'mean':
        fill_value = df[column].mean()
    elif fill_method == 'ffill':
        fill_value = None  # use default value of fillna
    elif fill_method == 'bfill':
        fill_value = None  # use default value of fillna
    else:
        raise ValueError("Invalid fill method: {}".format(fill_method))

    df[column] = df[column].fillna(fill_value)
    return df



if __name__ == '__main__':
    crime = api('https://data.boston.gov/api/3/action/datastore_search?resource_id=b973d8cb-eeb2-4e7e-99da-c92938efc9c0&limit=100000')
    print(crime.dtypes)
