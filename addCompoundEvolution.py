import csv
import json
import datetime

from apiClient import addCompoundEvolution, getProjects

CECompounds = []
Projects = []
FormattedCompoundEvolution = []

def fdate(dstr):
  parse = str(datetime.datetime.strptime(
      dstr, '%m/%d/%y').strftime('%Y-%m-%dT%H:%M:%S'))
  return parse + '.840259Z'


# Read compounds from Compound EVolution CSV
def readCECompounds():
    with open("inp_data/Compounds/CompoundEvolution.csv", "r") as f:
        CECompounds = []
        csv_reader = csv.reader(f)
        next(csv_reader)  # To skip header row
        for row in csv_reader:
            compound = {
                "Date": fdate(row[0]),
                "LegacyProjectID": row[1],
                "Stage": row[3],
                "SMILES": row[4],
                "CompoundID": row[5],
            }
            CECompounds.append(compound)
    return CECompounds


def addProjectId(CECompounds, Projects):
    formattedCompoundEvolution = []
    formattedCompoundEvolutionFailed = []
    for compound in CECompounds:
        for project in Projects.values():
            if compound["LegacyProjectID"] == project["projectLegacyId"]:
                compound["ProjectID"] = project["id"]
                break
        if "ProjectID" in compound:
            formattedCompoundEvolution.append(compound)
        else:
            formattedCompoundEvolutionFailed.append(compound)
            
    with open('int_data/formatted_compound_evolution.json', 'w') as outfile:
      json.dump(formattedCompoundEvolution, outfile, indent=4)
    with open('int_data/formatted_compound_evolution_failed.json', 'w') as outfile:
      json.dump(formattedCompoundEvolutionFailed, outfile, indent=4)
      
    return formattedCompoundEvolution

def addEvolution(CEs):
    results = []
    for ce in CEs:
        ceToAdd = {
            "smile" : ce["SMILES"],
            "projectId": ce["ProjectID"],
            "notes": "Imported from Share Point",
            "addedOnStage" : ce["Stage"],
            "addedOnDate" : ce["Date"],
            "externalCompoundIds" : ce["CompoundID"],
        }
        statusCode = addCompoundEvolution(ce["ProjectID"], ceToAdd);
        ceToAdd["statusCode"] = statusCode
        print(ceToAdd)
        results.append(ceToAdd)
    with open('int_data/compound_evolution_add_results.json', 'w') as outfile:
      json.dump(results, outfile, indent=4)
    
CECompounds = readCECompounds()
Projects = getProjects()

FormattedCompoundEvolution = addProjectId(CECompounds, Projects)

addEvolution(FormattedCompoundEvolution)

