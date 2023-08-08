import matplotlib.pyplot as plt 
import pandas as pd
import csv
import os
from tkinter import messagebox as mb

csvList = os.listdir("sheets")
data = {}
offset = 0

for csvName in csvList:
    # opens csv files in sheet directory and reads desired columns
    df = pd.read_csv("sheets/" + csvName)
    thetaData = df.iloc[26:1550, 0].values
    intensityData = df.iloc[26:1550, 2].values
    
    # convert intensity data list into an array of floats in order 
    # to accurately grab the max value
    floatData = []
    for num in intensityData:
        floatData.append(float(num))
    
    maxIntensity = max(floatData)
    
    # format the data and store in hashmap in order to display it later if needed
    normalized_intensity = []
    formatted_theta_list = []
    
    for i in range(len(intensityData)):
        formatted_theta_list.append(float(thetaData[i]))
        normalized_intensity.append(float(intensityData[i]) / float(maxIntensity))
    data[csvName] = [[formatted_theta_list], [normalized_intensity]]
    
    # plotting every set of data from the the sheets directory
    plt.plot(formatted_theta_list, [val + offset for val in normalized_intensity], label=csvName)
    offset += 0.1
 
plt.xlabel("Angle")
plt.ylabel("Normlized Intensity")
plt.title("Mg Data")
plt.legend()
plt.show()

# creates modified csv file that holds all of the data if 
# data was deemed valuable 
result = mb.askquestion('Results', 'Create csv files with this data?')

if result == 'yes':
    filename = "modified_data.csv"
    
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        for csvName in data:     
            csvwriter.writerows([[csvName + " angle"], [csvName + " intensity"]])

            for arr in data[csvName]:
                csvwriter.writerow(arr[0])
    
    csvfile.close()
