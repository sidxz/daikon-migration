import csv
from collections import Counter
from dbm.ndbm import library
import json
import os
import pprint
from operator import delitem
from apiClient import addProteinProduction, getAppOrgs, getGenesWithAccessionKey
from apiClient import getTargets
from classes.Project import Project
import datetime

def fdate(dstr):
  parse = str(datetime.datetime.strptime(
      dstr, '%m/%d/%y').strftime('%Y-%m-%dT%H:%M:%S'))
  return parse + '.840259Z'

# Define a list to hold the parsed proteinProduction data
parsedProteinProduction = []
# Define a list to hold the formatted proteinProduction data with GeneID
formattedProteinProduction = []
failedRvNumbers = []
apiResults = []

# Get the gene map from API
geneMap = getGenesWithAccessionKey()

# Define a function to get proteinProduction data from csv file and format it
def getProteinProduction():
    with open('inp_data/Genes/ProteinProduction.csv', 'r') as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        next(csv_reader)  # To skip header row
        line_count = 0
        
        # Loop through each row in the csv file
        for row in csv_reader:
            line_count += 1 # Increment line count
            rowDict = {
              "RvNumber": row[0],
              "Production": row[1],
              "Method": row[2],
              "Purity": row[3],
              "Date": fdate(row[4]),
            }
            parsedProteinProduction.append(rowDict)
        print ('Processed', line_count, 'lines.')

# Define a function to map Rv number to GeneID
def addGeneID():
    for element in parsedProteinProduction:
        if element["RvNumber"] in geneMap:
            element["GeneID"] = geneMap[element["RvNumber"]]["id"]
            formattedProteinProduction.append(element)
        else:
          print ("Rv number not found in geneMap : ", element["RvNumber"])
          failedRvNumbers.append(element)
    return parsedProteinProduction

# Define function to add proteinProduction data to the database using API
def add():
    for element in formattedProteinProduction:
        proteinProduction = {
            "production": element["Production"],
            "method": element["Method"],
            "purity": element["Purity"],
            "dateProduced": element["Date"],
            "geneId": element["GeneID"],
        }
        # Add proteinProduction data to the database
        statusCode = addProteinProduction(element["GeneID"], proteinProduction)
        proteinProduction["statusCode"] = statusCode
        proteinProduction["GeneID"] = element["GeneID"]
        proteinProduction["RvNumber"] = element["RvNumber"]
        apiResults.append(proteinProduction)
        print("ProteinProduction data added for GeneID: ", element["GeneID"], " with status code: ", statusCode)
        



## Main

# Get proteinProduction data  
getProteinProduction()

# Map Rv number to GeneID
addGeneID()

# Write the formatted proteinProduction data to a json file for logs
with open('int_data/formatted_proteinProduction.json', 'w') as outfile:
    json.dump(formattedProteinProduction, outfile, indent=4)
with open('int_data/formatted_proteinProduction_failed_no_rv.json', 'w') as outfile:
    json.dump(failedRvNumbers, outfile, indent=4)
    
# Check if the proteinProduction data is not empty
if len(formattedProteinProduction) > 0:
    print("Starting to add proteinProduction data to the database...")
    add()
    with open('int_data/proteinProduction_api_results.json', 'w') as outfile:
        json.dump(apiResults, outfile, indent=4)
    print("ProteinProduction data added to the database.")
else:
    print("No proteinProduction data, Invalid Token?")
