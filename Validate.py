import csv
from collections import Counter
from dbm.ndbm import library
import pprint
from operator import delitem
from apiClient import getAppOrgs
from apiClient import getTargets
from classes.Project import Project


def validateData(printLogs=True):
  appOrgs = getAppOrgs()

  targets = getTargets()

  validated = {}

  primaryOrgSuccess = []
  primaryOrgFails = []
  primaryOrgFailCount = 0

  targetsSuccess = []
  targetFails = []
  targetFailCount = 0

  smileFailCount = 0
  fhaFails = []
  FHAFailCount = 0
  total = 0
  validationSuccess = 0
  validationFail = 0
  with open('inp_data/project_csv.csv') as input_csv:
    csv_reader = csv.reader(input_csv, delimiter=',')
    next(csv_reader)  # To skip header row
    line_count = 0

    for row in csv_reader:
      total = total + 1
      flag = False
      validationFailMessage = ","
      targetName = row[2].replace(' ', '-')
      projectName = row[1]
      smile = row[31]
      primaryOrganization = row[18]
      externalCompoundIds = "LEGACY-"+row[0]
      primaryOrganizationAbb = primaryOrganization.upper().replace(" ", "")
      fhaDate = row[23]
      h2LStart = row[24]
      loStart = row[25]
      spStart = row[26]
      pcdDate = row[27]
      indStart = row[28]
      clinicalP1Start = row[29]

      if printLogs:
        print(f"# Project Name: {projectName}")
        print(f"# Target      : {targetName}")
        print(f"# Compound Id : {externalCompoundIds}")
        print(f"# primaryOrg  : {primaryOrganization}")
        print(f"# SMILE       : {smile}")
        print(f"# FHA DATE    : {fhaDate}")
        print("-------------------------------------------")

      if primaryOrganizationAbb in appOrgs:
        primaryOrgSuccess.append(primaryOrganizationAbb)
      else:
        primaryOrgFails.append(primaryOrganization)
        flag = True
        validationFailMessage = "primaryOrg|"
        primaryOrgFailCount = primaryOrgFailCount + 1
      if ((targetName in targets) or (targetName == 'unknown')):
        targetsSuccess.append(targetName)
      else:
        targetFails.append(targetName)
        flag = True
        validationFailMessage = "target|"
        targetFailCount = targetFailCount + 1

      if not smile:
        flag = True
        validationFailMessage = "smile|"
        smileFailCount = smileFailCount + 1
        # if clinical has a date previous stages must have dates aa well
      if clinicalP1Start != '':
        if indStart == '':
          indStart = '1/1/14'
        if spStart == '':
          spStart = '1/1/14'
        if loStart == '':
          loStart = '1/1/14'
        if h2LStart == '':
          h2LStart = '1/1/14'

      if indStart != '':
        if spStart == '':
          spStart = '1/1/14'
        if loStart == '':
          loStart = '1/1/14'
        if h2LStart == '':
          h2LStart = '1/1/14'

      if spStart != '':
        if loStart == '':
          loStart = '1/1/14'
        if h2LStart == '':
          h2LStart = '1/1/14'

      if loStart != '':
        if h2LStart == '':
          h2LStart = '1/1/14'

      if fhaDate == '':
        # flag = True
        validationFailMessage = "FHA Date|"
        # FHAFailCount = FHAFailCount + 1
        # fhaFails.append(projectName)
        fhaDate = '1/1/14'

      if flag:
        validationFail = validationFail + 1
      else:
        validationSuccess = validationSuccess + 1

        if targetName != 'unknown':
          validatedProject = Project(
              projectType="TargetBased",
              projectName=projectName,
              targetName=targetName,
              targetId=targets.get(targetName)["id"],
              smile=smile,
              primaryOrganization=primaryOrganization,
              primaryOrgId=appOrgs.get(primaryOrganization.upper()),
              externalCompoundIds=externalCompoundIds,
              library=row[30],
              method="Legacy",
              fhaStart=fhaDate,
              h2LStart=h2LStart,
              loStart=loStart,
              spStart=spStart,
              pcdDate=row[27],
              indStart=indStart,
              clinicalP1Start=clinicalP1Start,
              priority=row[35],
              probability=row[36],
              status=row[20]
          )
        else:
          validatedProject = Project(
              projectType="Phenotypic",
              projectName=projectName,
              targetName=targetName,
              smile=smile,
              primaryOrganization=primaryOrganization,
              primaryOrgId=appOrgs.get(primaryOrganization.upper()),
              externalCompoundIds=externalCompoundIds,
              library=row[30],
              method="Legacy",
              fhaStart=fhaDate,
              h2LStart=h2LStart,
              loStart=loStart,
              spStart=spStart,
              pcdDate=row[27],
              indStart=indStart,
              clinicalP1Start=clinicalP1Start,
              priority=row[35],
              probability=row[36],
              status=row[20]
          )
        validated[projectName] = validatedProject

  if printLogs:
    print("# ----PRIMARY ORG SUCCESS ----")
    pprint.pprint(Counter(primaryOrgSuccess))

    print("# ----PRIMARY ORG FAILS ----")
    pprint.pprint(Counter(primaryOrgFails))

    print("# ----TARGET SUCCESS ----")
    pprint.pprint(Counter(targetsSuccess))

    print("# ----TARGET FAILS ----")
    pprint.pprint(Counter(targetFails))

    print("# ----FHA DATE FAILS ----")
    pprint.pprint(Counter(fhaFails))

    print("# =========SUMMARY===========")
    print(f"# TOTAL : {total}")
    print(f"# VALIDATION SUCCESS  : {validationSuccess}")
    print(f"# VALIDATION FAIL     : {validationFail}")
    validationPercent = (validationSuccess/total)*100 if total != 0 else 0
    print(f"# VALIDATION %        : {validationPercent:.2f}")
    print("")
    print(f"# PRIMARY ORG FAIL    : {primaryOrgFailCount}")
    print(f"# TARGET FAIL         : {targetFailCount}")
    print(f"# SMILE FAIL          : {smileFailCount}")
    print(f"# FHA Date FAIL       : {FHAFailCount}")
  return validated
