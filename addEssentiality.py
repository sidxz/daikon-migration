import csv
from collections import Counter
from dbm.ndbm import library
import json
import os
import pprint
from operator import delitem
from apiClient import addEssentiality, getAppOrgs, getGenesWithAccessionKey
from apiClient import getTargets
from classes.Project import Project

# Define a list to hold the parsed essentiality data
parsedEssentiality = []
# Define a list to hold the formatted essentiality data with GeneID
formattedEssentiality = []
failedRvNumbers = []
apiResults = []

# Get the gene map from API
geneMap = getGenesWithAccessionKey()

# Define a function to get essentiality data from csv file and format it
def getEssentiality():
    with open('inp_data/Genes/Essentiality.csv', 'r') as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        next(csv_reader)  # To skip header row
        line_count = 0
        
        # Loop through each row in the csv file
        for row in csv_reader:
            line_count += 1 # Increment line count
            rowDict = {
              "RvNumber": row[0],
              "Classification": row[1],
              "Condition": row[2],
              "Strain": row[3],
              "Method": row[4],
              "Reference": row[5]
            }
            parsedEssentiality.append(rowDict)
        print ('Processed', line_count, 'lines.')

# Define a function to map Rv number to GeneID
def addGeneID():
    for element in parsedEssentiality:
        if element["RvNumber"] in geneMap:
            element["GeneID"] = geneMap[element["RvNumber"]]["id"]
            formattedEssentiality.append(element)
        else:
          print ("Rv number not found in geneMap : ", element["RvNumber"])
          failedRvNumbers.append(element)
    return parsedEssentiality

# Define function to add essentiality data to the database using API
def add():
    for element in formattedEssentiality:
        essentiality = {
            "classification": element["Classification"],
            "condition": element["Condition"],
            "strain": element["Strain"],
            "method": element["Method"],
            "reference": element["Reference"],
            "geneId": element["GeneID"],
        }
        # Add essentiality data to the database
        statusCode = addEssentiality(element["GeneID"], essentiality)
        essentiality["statusCode"] = statusCode
        essentiality["GeneID"] = element["GeneID"]
        essentiality["RvNumber"] = element["RvNumber"]
        apiResults.append(essentiality)
        print("Essentiality data added for GeneID: ", element["GeneID"], " with status code: ", statusCode)
        



## Main

# Get essentiality data  
getEssentiality()

# Map Rv number to GeneID
addGeneID()

# Write the formatted essentiality data to a json file for logs
with open('int_data/formatted_essentiality.json', 'w') as outfile:
    json.dump(formattedEssentiality, outfile, indent=4)
with open('int_data/formatted_essentiality_failed_no_rv.json', 'w') as outfile:
    json.dump(failedRvNumbers, outfile, indent=4)
    
# Check if the essentiality data is not empty
if len(formattedEssentiality) > 0:
    print("Starting to add essentiality data to the database...")
    add()
    with open('int_data/essentiality_api_results.json', 'w') as outfile:
        json.dump(apiResults, outfile, indent=4)
    print("Essentiality data added to the database.")
else:
    print("No essentiality data, Invalid Token?")
