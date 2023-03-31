import csv
from collections import Counter
from dbm.ndbm import library
import json
import os
import pprint
from operator import delitem
from apiClient import addCompass, getAppOrgs, getTargets
from apiClient import getTargets
from classes.Project import Project

# Define a list to hold the parsed compass data
parsedCompass = []
# Define a list to hold the formatted compass data with GeneID
formattedCompass = []
failedTarget = []
apiResults = []

# Get the gene map from API
targetMap = getTargets()

# Define a function to get compass data from csv file and format it
def getCompass():
    with open('inp_data/Targets/Compass.csv', 'r') as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        next(csv_reader)  # To skip header row
        line_count = 0
        
        # Loop through each row in the csv file
        for row in csv_reader:
            line_count += 1 # Increment line count
            rowDict = {
              "Target": row[0],
              "background": row[1],
              "enablement": row[2],
              "challenges": row[3],
              "strategy": row[4],
            }
            parsedCompass.append(rowDict)
        print ('Processed', line_count, 'lines.')

# Define a function to map Rv number to GeneID
def addTargetID():
    for element in parsedCompass:
        if element["Target"] in targetMap:
            element["TargetId"] = targetMap[element["Target"]]["id"]
            formattedCompass.append(element)
        else:
          print ("Target not found in targetMap : ", element["Target"])
          failedTarget.append(element)
    return parsedCompass

# Define function to add compass data to the database using API
def add():
    for element in formattedCompass:
        
        
        compass = {
            "targetId": element["TargetId"],
            "background": element["background"],
            "enablement": element["enablement"],
            "challenges": element["challenges"],
            "strategy": element["strategy"],
        }
        
        # Add compass data to the database
        statusCode = addCompass(element["TargetId"], compass)
        compass["statusCode"] = statusCode
        compass["TargetId"] = element["TargetId"]
        compass["Target"] = element["Target"]
        apiResults.append(compass)
        print("Compass data added for Target: ", element["Target"], " with status code: ", statusCode)
        



## Main

# Get compass data  
getCompass()

# Map Rv number to GeneID
addTargetID()

# Write the formatted compass data to a json file for logs
with open('int_data/formatted_compass.json', 'w') as outfile:
    json.dump(formattedCompass, outfile, indent=4)
with open('int_data/formatted_compass_failed_no_target.json', 'w') as outfile:
    json.dump(failedTarget, outfile, indent=4)
    
# Check if the compass data is not empty
if len(formattedCompass) > 0:
    print("Starting to add compass data to the database...")
    add()
    with open('int_data/compass_api_results.json', 'w') as outfile:
        json.dump(apiResults, outfile, indent=4)
    print("Compass data added to the database.")
else:
    print("No compass data, Invalid Token?")
