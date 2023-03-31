import csv
from collections import Counter
from dbm.ndbm import library
import json
import os
import pprint
from operator import delitem
from apiClient import addProteinActivityAssay, getAppOrgs, getGenesWithAccessionKey
from apiClient import getTargets
from classes.Project import Project
import datetime

def fdate(dstr):
  parse = str(datetime.datetime.strptime(
      dstr, '%m/%d/%y').strftime('%Y-%m-%dT%H:%M:%S'))
  return parse + '.840259Z'

# Define a list to hold the parsed proteinActivityAssay data
parsedProteinActivityAssay = []
# Define a list to hold the formatted proteinActivityAssay data with GeneID
formattedProteinActivityAssay = []
failedRvNumbers = []
apiResults = []

# Get the gene map from API
geneMap = getGenesWithAccessionKey()

# Define a function to get proteinActivityAssay data from csv file and format it
def getProteinActivityAssay():
    with open('inp_data/Genes/ProteinActivityAssay.csv', 'r') as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        next(csv_reader)  # To skip header row
        line_count = 0
        
        # Loop through each row in the csv file
        for row in csv_reader:
            line_count += 1 # Increment line count
            rowDict = {
              "RvNumber": row[0],
              "Assay": row[1],
              "Method": row[2],
              "Throughput": row[3],
            }
            parsedProteinActivityAssay.append(rowDict)
        print ('Processed', line_count, 'lines.')

# Define a function to map Rv number to GeneID
def addGeneID():
    for element in parsedProteinActivityAssay:
        if element["RvNumber"] in geneMap:
            element["GeneID"] = geneMap[element["RvNumber"]]["id"]
            formattedProteinActivityAssay.append(element)
        else:
          print ("Rv number not found in geneMap : ", element["RvNumber"])
          failedRvNumbers.append(element)
    return parsedProteinActivityAssay

# Define function to add proteinActivityAssay data to the database using API
def add():
    for element in formattedProteinActivityAssay:
        proteinActivityAssay = {
            "assay": element["Assay"],
            "method": element["Method"],
            "throughput": element["Throughput"],
           
            "geneId": element["GeneID"],
        }
        # Add proteinActivityAssay data to the database
        statusCode = addProteinActivityAssay(element["GeneID"], proteinActivityAssay)
        proteinActivityAssay["statusCode"] = statusCode
        proteinActivityAssay["GeneID"] = element["GeneID"]
        proteinActivityAssay["RvNumber"] = element["RvNumber"]
        apiResults.append(proteinActivityAssay)
        print("ProteinActivityAssay data added for GeneID: ", element["GeneID"], " with status code: ", statusCode)
        



## Main

# Get proteinActivityAssay data  
getProteinActivityAssay()

# Map Rv number to GeneID
addGeneID()

# Write the formatted proteinActivityAssay data to a json file for logs
with open('int_data/formatted_proteinActivityAssay.json', 'w') as outfile:
    json.dump(formattedProteinActivityAssay, outfile, indent=4)
with open('int_data/formatted_proteinActivityAssay_failed_no_rv.json', 'w') as outfile:
    json.dump(failedRvNumbers, outfile, indent=4)
    
# Check if the proteinActivityAssay data is not empty
if len(formattedProteinActivityAssay) > 0:
    print("Starting to add proteinActivityAssay data to the database...")
    add()
    with open('int_data/proteinActivityAssay_api_results.json', 'w') as outfile:
        json.dump(apiResults, outfile, indent=4)
    print("ProteinActivityAssay data added to the database.")
else:
    print("No proteinActivityAssay data, Invalid Token?")
