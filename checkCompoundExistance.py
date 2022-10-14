from apiClient import compoundDetailsByCompoundID
from apiClient import hitDetailsByCompoundID
from apiClient import compoundDetailsBySMILE
import csv


_COMPOUND_NOT_FOUND = []

# Prechecks
# Check if compound exists
def checkCompoundExistsbyID(extCompoundId):
    compoundID = compoundDetailsByCompoundID(extCompoundId)["id"]
    # If compound is not found
    if compoundID == 0:
        print(f"{extCompoundId} : NOT FOUND 404")
        return
    print(f"{extCompoundId} : {compoundID}")
    
    return
    hit = hitDetailsByCompoundID(compoundID)
    print(hit)
    #print(f"{extCompoundId} : Target={hit['targetName']} : Method={hit['method']} : Library={hit['library']} : ScreenID={hit['screenId']}")


def checkCompoundExistsbySMILE(extCompoundId):
    compoundID = compoundDetailsBySMILE(extCompoundId)["id"]
    # If compound is not found
    if compoundID == 0:
        print(f"{extCompoundId} : NOT FOUND 404")
        return
    print(f"{extCompoundId} : {compoundID}")
    
    return
    hit = hitDetailsByCompoundID(compoundID)
    print(hit)
    #print(f"{extCompoundId} : Target={hit['targetName']} : Method={hit['method']} : Library={hit['library']} : ScreenID={hit['screenId']}")


# Read Voting data from CSV
def loadVoteMap():
    voteMap = []
    with open("inp_data/votes/rho.csv") as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        next(csv_reader) # Skip header row
        for row in csv_reader:
            vote = {
                "compoundExtID": row[0],
                "smile": row[1],
                "positive": row[2],
                "negative": row[3],
                "neutral": row[4],
            }
            voteMap.append(vote)
    return voteMap


_VOTE_MAP = loadVoteMap()

for vote in _VOTE_MAP:
  checkCompoundExistsbySMILE(vote['smile'])
  
