from apiClient import compoundDetailsByCompoundID
from apiClient import hitDetailsByCompoundID
from apiClient import importVote
import csv


_COMPOUND_NOT_FOUND = []

# Prechecks
# Check if compound exists
def checkCompoundExists(extCompoundId):
    compoundID = compoundDetailsByCompoundID(extCompoundId)["id"]
    # If compound is not found
    if compoundID == 0:
        print(f"{extCompoundId} : NOT FOUND 404")
        return
    print(f"{extCompoundId} : {compoundID}")
    hit = hitDetailsByCompoundID(compoundID)
    print(hit)
    # print(f"{extCompoundId} : Target={hit['targetName']} : Method={hit['method']} : Library={hit['library']} : ScreenID={hit['screenId']}")


# Export a vote to server based on compound External Id
def submitVote(extCompoundId, positive, negative, neutral):
    print ("-----------------------START--------------------------")
    # Get Compound Details
    print(f"() -> Getting compound details for {extCompoundId}")
    compoundID = compoundDetailsByCompoundID(extCompoundId)["id"]

    # If compund is not found
    if compoundID == 0:
        print("Compound Not Found 404")
        _COMPOUND_NOT_FOUND.append(compoundID)
        return

    print(f"Compound UUID = {compoundID}")

    # Get hit details
    print(f"() -> Getting hit details for {compoundID}")
    voteID = hitDetailsByCompoundID(compoundID)["voteId"]
    print(f"Vote ID = {voteID}")

    vote = {
        "id": voteID,
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
    }
    print(f"() -> voting {vote}")
    return importVote(vote)


# Read Voting data from CSV
def loadVoteMap():
    voteMap = []
    with open("inp_data/votes/rho.csv") as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        next(csv_reader)  # Skip header row
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
    checkCompoundExists(vote["compoundExtID"])
    res = submitVote(
        vote["compoundExtID"], vote["positive"], vote["negative"], vote["neutral"]
    )
    print (res)
