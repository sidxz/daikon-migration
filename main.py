from Validate import validateData
from apiClient import addScreen, terminateProject
from apiClient import addHit
from apiClient import getProjects
import datetime
import time
import pytz

from tracker import loadScreenTracker
from tracker import addToScreenTracker
from tracker import addToHitTracker
from tracker import loadHitTracker
from apiClient import addHA
from apiClient import addH2L
from apiClient import addLO
from apiClient import addSP
from apiClient import addIND
from apiClient import addP1
from apiClient import addPhenotypicScreen


def fdate(dstr):
  parse = str(datetime.datetime.strptime(
      dstr, '%m/%d/%y').strftime('%Y-%m-%dT%H:%M:%S'))
  return parse + '.840259Z'


# Validate Data
validatedProjects = validateData()


for projectName in validatedProjects:
  time.sleep(0.01)
  print("# --------------------------------")
  print(f"# For {projectName}")

  screenTracker = loadScreenTracker()
  hitTracker = loadHitTracker()
  project = validatedProjects[projectName]

  screenId = ''
  screenName = ''
  hitId = ''
  compoundId = ''

  if project.projectName not in screenTracker:
    if project.projectType == 'TargetBased':
      # Add a screen and save the screen id
      screenToAdd = {
          "targetId": project.targetId,
          "org": {"id": project.primaryOrgId},
          "method": "Legacy",
          "promotionDate": fdate('1/1/14'),
          "notes": "Imported from SharePoint"
      }
      print(f"# Will promote target {project.targetName}")
      print("Adding Screen...")
      print(screenToAdd);
      res, status = addScreen(screenToAdd)
      print(res, status)
      
      screenId = res['id']
      screenName = res['screenName']
      if status == 200:
        addToScreenTracker(project.projectName, project.targetId,
                           project.targetName, screenId, screenName)
    if project.projectType == 'Phenotypic':
      # Add a screen and save the screen id
      screenToAdd = {
          "screenName": project.projectName.replace(' ', '-'),
          "org": {"id": project.primaryOrgId},
          "method": "Legacy",
          "promotionDate": fdate('1/1/14'),
          "notes": "Imported from SharePoint"
      }
      print(f"# Will create phenotypic screen {project.targetName}")
      res, status = addPhenotypicScreen(screenToAdd)
      screenId = res['id']
      screenName = res['screenName']
      if status == 200:
        addToScreenTracker(project.projectName, 'Phenotypic',
                           'Phenotypic', screenId, screenName)

  if project.projectName not in hitTracker:
    # Add hit
    hitToAdd = {
        "screenId": screenId,
        "externalCompoundIds": project.externalCompoundIds,
        "Library": project.library,
        "method": project.method,
        "mic": "NA",
        "micCondition": "string",
        "iC50": "NA",
        "smile": project.smile,
        "clusterGroup": "1",
        "molWeight": "0",
        "molArea": "0"
    }
    print(hitToAdd)

    print(f"# Will add hit to {screenName}")
    res, status = addHit(hitToAdd)
    print(res)
    hitId = res['id']
    compoundId = res['compound']['id']
    if status == 200:
      addToHitTracker(project.projectName, project.targetId,
                      project.targetName, screenId, screenName, hitId, compoundId)
  # Project
  if screenId == '':
    screenId = screenTracker.get(project.projectName)['screenId']
  if hitId == '':
    hitId = hitTracker.get(project.projectName)['hitId']
    compoundId = hitTracker.get(project.projectName)['compoundId']
  # Create HA
  if project.haStart != '':
    print("# Will create new HA")
    newHA = {
        "projectName": project.projectName,
        "projectLegacyId" : project.projectLegacyId,
        "primaryOrg": {
            "id": project.primaryOrgId
        },
        "supportingOrgs": [
            {
                "id": project.primaryOrgId
            }
        ],
        "haStart": fdate(project.haStart),
        "haDescription": "",
        "ScreenId": screenId,
        "baseHits": [
            {
                "id": hitId,
                "screenId": screenId,
                "compoundId": compoundId,
                "mic": "NA",
                "iC50": "NA"
            }
        ],
        "representationStructure": {
            "id": compoundId,
            "mic": "NA",
            "iC50": "NA"
        }
    }
    print(newHA)
    res = addHA(newHA)
    print(res)

    time.sleep(0.01)
    existingProjects = dict()
    existingProjects.clear()
    existingProjects = getProjects()
    projectId = existingProjects.get(project.projectName)['id']

    # Create H2L
    if project.h2LStart != '':
      print("# Will create new H2L")
      newH2L = {
          "id": projectId,
          "h2LStart": fdate(project.h2LStart),
      }
      print(newH2L)
      res = addH2L(projectId, newH2L)
      print(res)

    # Create Lo
    if project.loStart != '':
      print("# Will create new LO")
      newLO = {
          "id": projectId,
          "loStart": fdate(project.loStart),
      }
      print(newLO)
      res = addLO(projectId, newLO)
      print(res)

    # Create SP
    if project.spStart != '':
      print("# Will create new SP")
      newSP = {
          "id": projectId,
          "spStart": fdate(project.spStart),
      }
      print(newSP)
      res = addSP(projectId, newSP)
      print(res)

    # Create IND
    print(project.indStart)
    if project.indStart != '':
      print("# Will create new IND")
      newIND = {
          "id": projectId,
          "indStart": fdate(project.indStart),
      }
      print(newIND)
      res = addIND(projectId, newIND)
      print(res)

    # Create P1
    print(project.clinicalP1Start)
    if project.clinicalP1Start != '':
      print("# Will create new P1")
      newP1 = {
          "id": projectId,
          "p1Start": fdate(project.clinicalP1Start),
      }
      print(newP1)
      res = addP1(projectId, newP1)
      print(res)

    # Active or Terminate
    if project.status == "Terminated":
      print("Project should be Terminated")
      term = {
          "id": projectId,
          "projectName": project.projectName
      }
      res = terminateProject(projectId, term)
      print(res)
    print("# -----------END--------------------")
