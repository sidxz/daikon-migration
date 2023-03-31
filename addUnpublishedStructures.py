import csv
from collections import Counter
from dbm.ndbm import library
import json
import os
import pprint
from operator import delitem
from apiClient import addUnpublished, getAppOrgs, getGenesWithAccessionKey
from apiClient import getTargets
from classes.Project import Project
import datetime

def fdate(dstr):
  parse = str(datetime.datetime.strptime(
      dstr, '%m/%d/%y').strftime('%Y-%m-%dT%H:%M:%S'))
  return parse + '.840259Z'

# Define a list to hold the parsed unpublishedStructures data
parsedUnpublishedStructures = []
# Define a list to hold the formatted unpublishedStructures data with GeneID
formattedUnpublishedStructures = []
failedRvNumbers = []
apiResults = []

# Get the gene map from API
geneMap = getGenesWithAccessionKey()

# Define a function to get unpublishedStructures data from csv file and format it
def getUnpublishedStructures():
    with open('inp_data/Genes/UnpublishedStructures.csv', 'r') as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        next(csv_reader)  # To skip header row
        line_count = 0
        
        # Loop through each row in the csv file
        for row in csv_reader:
            line_count += 1 # Increment line count
            rowDict = {
              "RvNumber": row[0],
              "Organization": row[1],
              "Method": row[2],
              "Resolution": row[3],
              "Ligands": row[4],
              "Researcher": row[5],
              "Reference": row[6],
              "Notes": row[7],
            }
            parsedUnpublishedStructures.append(rowDict)
        print ('Processed', line_count, 'lines.')

# Define a function to map Rv number to GeneID
def addGeneID():
    for element in parsedUnpublishedStructures:
        if element["RvNumber"] in geneMap:
            element["GeneID"] = geneMap[element["RvNumber"]]["id"]
            formattedUnpublishedStructures.append(element)
        else:
          print ("Rv number not found in geneMap : ", element["RvNumber"])
          failedRvNumbers.append(element)
    return parsedUnpublishedStructures

# Define function to add unpublishedStructures data to the database using API
def add():
    for element in formattedUnpublishedStructures:
        unpublishedStructures = {
            "organization": element["Organization"],
            "method": element["Method"],
            "resolution": element["Resolution"],
            "ligands": element["Ligands"],
            "researcher": element["Researcher"],
            "reference": element["Reference"],
            "notes": element["Notes"],
            "geneId": element["GeneID"],
        }
        # Add unpublishedStructures data to the database
        statusCode = addUnpublished(element["GeneID"], unpublishedStructures)
        unpublishedStructures["statusCode"] = statusCode
        unpublishedStructures["GeneID"] = element["GeneID"]
        unpublishedStructures["RvNumber"] = element["RvNumber"]
        apiResults.append(unpublishedStructures)
        print("UnpublishedStructures data added for GeneID: ", element["GeneID"], " with status code: ", statusCode)
        



## Main

# Get unpublishedStructures data  
getUnpublishedStructures()

# Map Rv number to GeneID
addGeneID()

# Write the formatted unpublishedStructures data to a json file for logs
with open('int_data/formatted_unpublishedStructures.json', 'w') as outfile:
    json.dump(formattedUnpublishedStructures, outfile, indent=4)
with open('int_data/formatted_unpublishedStructures_failed_no_rv.json', 'w') as outfile:
    json.dump(failedRvNumbers, outfile, indent=4)
    
# Check if the unpublishedStructures data is not empty
if len(formattedUnpublishedStructures) > 0:
    print("Starting to add unpublishedStructures data to the database...")
    add()
    with open('int_data/unpublishedStructures_api_results.json', 'w') as outfile:
        json.dump(apiResults, outfile, indent=4)
    print("UnpublishedStructures data added to the database.")
else:
    print("No unpublishedStructures data, Invalid Token?")
