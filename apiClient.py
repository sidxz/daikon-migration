import requests
import json


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# ==========================================================================
authToken = ""
with open(".token") as tokenFile:
    authToken = tokenFile.read()
# ==========================================================================

# Local
baseUrl = "http://localhost:5005/api/"
# PROD
# baseUrl ="https://in.virt.snet.biobio.tamu.edu:5000/api/"

# ==========================================================================


head = {
    "Authorization": "Bearer {}".format(authToken),
    "Content-Type": "application/json",
}


def getAppOrgs():
    response = requests.get(baseUrl + "General/app-vars", headers=head)

    appOrgs = {}
    for appOrg in response.json()["appOrgs"]:
        appOrgs[appOrg["alias"].upper()] = appOrg["id"]
    return appOrgs


def addAppOrg(appOrg):
    request = requests.post(
        url=baseUrl + "elevated/Accounts/orgs", json=appOrg, headers=head
    )
    return request.status_code


def getGenesWithAccessionKey():
    response = requests.get(baseUrl + "gene", headers=head)
    genes = {}
    for gene in response.json():
        genes[gene["accessionNumber"]] = gene
    return genes


def getTargets():
    response = requests.get(baseUrl + "target", headers=head)
    targets = {}
    for target in response.json():
        targets[target["name"]] = target
    return targets


def getGeneGroups():
    response = requests.get(baseUrl + "elevated/gene/groups", headers=head)
    geneGroups = {}
    for geneGroup in response.json():
        geneGroups[geneGroup["name"]] = geneGroup
    return geneGroups


def addGeneGroup(geneGroup):
    request = requests.post(
        url=baseUrl + "elevated/gene/groups", json=geneGroup, headers=head
    )
    return request.status_code


def addScreen(screenToAdd):
    request = requests.post(url=baseUrl + "screen", json=screenToAdd, headers=head)
    y = json.loads(request.text)
    return y, request.status_code


def addPhenotypicScreen(screenToAdd):
    request = requests.post(
        url=baseUrl + "screen/phenotypic", json=screenToAdd, headers=head
    )
    y = json.loads(request.text)
    return y, request.status_code


def addHit(hitToAdd):
    request = requests.post(url=baseUrl + "hit", json=hitToAdd, headers=head)
    y = json.loads(request.text)
    return y, request.status_code


def addHA(haDetails):
    request = requests.post(
        url=baseUrl + "elevated/Project", json=haDetails, headers=head
    )
    return request.status_code


def getProjects():
    response = requests.get(baseUrl + "project", headers=head)
    projects = {}
    for project in response.json():
        projects[project["projectName"]] = project
    return projects


def addH2L(id, details):
    request = requests.post(
        url=baseUrl + "elevated/Project/" + id + "/createH2L",
        json=details,
        headers=head,
    )
    return request.status_code


def addLO(id, details):
    request = requests.post(
        url=baseUrl + "elevated/Project/" + id + "/createLO", json=details, headers=head
    )
    return request.status_code


def addSP(id, details):
    request = requests.post(
        url=baseUrl + "elevated/Project/" + id + "/createSP", json=details, headers=head
    )
    return request.status_code


def addIND(id, details):
    request = requests.post(
        url=baseUrl + "elevated/Project/" + id + "/createIND",
        json=details,
        headers=head,
    )
    return request.status_code


def addP1(id, details):
    request = requests.post(
        url=baseUrl + "elevated/Project/" + id + "/createP1", json=details, headers=head
    )
    return request.status_code


def terminateProject(id, details):
    request = requests.post(
        url=baseUrl + "elevated/Project/" + id + "/terminate",
        json=details,
        headers=head,
    )
    return request.status_code


def compoundDetailsByCompoundID(extCompoundId):
    response = requests.get(
        baseUrl + "compound/by-external-id/" + extCompoundId, headers=head
    )
    if response.status_code == 404:
        return {"id": 0}
    return response.json()


def compoundDetailsBySMILE(smile):
    response = requests.get(baseUrl + "compound/by-smile/" + smile, headers=head)
    if response.status_code == 404:
        return {"id": 0}
    return response.json()


def hitDetailsByCompoundID(compoundId):
    response = requests.get(baseUrl + "hit/by-compound-id/" + compoundId, headers=head)
    return response.json()


def importVote(voteJSON):
    request = requests.post(
        url=baseUrl + "elevated/vote/import", json=voteJSON, headers=head
    )
    return request.status_code
