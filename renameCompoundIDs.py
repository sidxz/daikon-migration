# Read Backtracked Compounds from CSV

import csv
import json

from apiClient import editCompoundExternalId, getCompoundIDfromExternalID


backtrackedCompounds = []
CECompounds = []
MatchedCompounds = []


def readBacktrackedCompounds():
    backtrackedCompounds = []
    with open("inp_data/Compounds/ProjectSMILESBacktrack.csv", "r") as f:

        csv_reader = csv.reader(f)
        next(csv_reader)  # To skip header row
        for row in csv_reader:
            compound = {
                "ProjectID": row[0],
                "LegacyCompoundID": row[1],
                "SMILES": row[2],
            }
            backtrackedCompounds.append(compound)
    return backtrackedCompounds


# Read compounds from Compound EVolution CSV
def readCECompounds():
    with open("inp_data/Compounds/CompoundEvolution.csv", "r") as f:
        CECompounds = []
        csv_reader = csv.reader(f)
        next(csv_reader)  # To skip header row
        for row in csv_reader:
            compound = {
                "Date": row[0],
                "ProjectID": row[1],
                "Stage": row[3],
                "SMILES": row[4],
                "CompoundID": row[5],
            }
            CECompounds.append(compound)
    return CECompounds


# Find compounds in CE that have same smile string as compound in backtracked
def findMatchedCompounds(backtrackedCompounds, CECompounds):
    MatchedCompounds = []
    for backtrackedCompound in backtrackedCompounds:
        for CECompound in CECompounds:
            if backtrackedCompound["SMILES"] == CECompound["SMILES"]:
                compoundId = getCompoundIDfromExternalID(
                    backtrackedCompound["LegacyCompoundID"]
                )
                compound = {
                    "id": compoundId,
                    "LegacyCompoundID": backtrackedCompound["LegacyCompoundID"],
                    "CECompoundID": CECompound["CompoundID"],
                    "SMILES": backtrackedCompound["SMILES"],
                }
                MatchedCompounds.append(compound)
                break
    with open('int_data/formatted_compounds_id_replaced.json', 'w') as outfile:
      json.dump(MatchedCompounds, outfile, indent=4)
    return MatchedCompounds

# Replace with API call
def replaceID(MatchedCompounds):
    result = []
    for compound in MatchedCompounds:
        resCompound = {
          "id": compound["id"],
          "externalCompoundIds": compound["CECompoundID"],
        }
        res = editCompoundExternalId(compound["id"], resCompound)
        resCompound["res"] = res
        resCompound["legacyCompoundId"] = compound["LegacyCompoundID"]
        result.append(resCompound)
        print (resCompound)
    with open('int_data/compound_id_replaced.json', 'w') as outfile:
      json.dump(result, outfile, indent=4)
      
      


backtrackedCompounds = readBacktrackedCompounds()
CECompounds = readCECompounds()


# # Print backtracked compounds
# print ("Backtracked Compounds")
# for compound in backtrackedCompounds:
#     print(compound)

# # Print CE Compounds
# print ("CE Compounds")
# for compound in CECompounds:
#     print(compound)

# Find compounds in CE that have same smile string as compound in backtracked
MatchedCompounds = findMatchedCompounds(backtrackedCompounds, CECompounds)

# Print Matched Compounds
# for compound in MatchedCompounds:
#     print(compound)

# Replace with API call
replaceID(MatchedCompounds)