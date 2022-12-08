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
    haFails = []
    HAFailCount = 0
    total = 0
    validationSuccess = 0
    validationFail = 0
    with open("inp_data/project_csv.csv") as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=",")
        next(csv_reader)  # To skip header row
        line_count = 0

        for row in csv_reader:
            total = total + 1
            flag = False
            validationFailMessage = ","
            targetName = row[2].replace(" ", "-")
            projectName = row[1]
            smile = row[23]
            primaryOrganization = row[4]
            externalCompoundIds = "LEGACY-" + row[0]
            primaryOrganizationAbb = primaryOrganization.upper().replace(" ", "")
            haDate = row[8]
            h2LStart = row[10]
            loStart = row[12]
            spStart = row[14]
            indStart = row[16]
            clinicalP1Start = row[18]
            currentStage = row[5]

            if printLogs:
                print(f"# Project Name: {projectName}")
                print(f"# Target      : {targetName}")
                print(f"# Compound Id : {externalCompoundIds}")
                print(f"# primaryOrg  : {primaryOrganization}")
                print(f"# SMILE       : {smile}")
                print(f"# HA DATE    : {haDate}")
                print("-------------------------------------------")

            if primaryOrganizationAbb in appOrgs:
                primaryOrgSuccess.append(primaryOrganizationAbb)
            else:
                primaryOrgFails.append(primaryOrganization)
                flag = True
                validationFailMessage = "primaryOrg|"
                primaryOrgFailCount = primaryOrgFailCount + 1
            if (targetName in targets) or (targetName == "unknown"):
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
            if currentStage == "P1":
                if clinicalP1Start == "":
                    clinicalP1Start = "1/1/14"
                if indStart == "":
                    indStart = "1/1/14"
                if spStart == "":
                    spStart = "1/1/14"
                if loStart == "":
                    loStart = "1/1/14"
                if h2LStart == "":
                    h2LStart = "1/1/14"
            if currentStage == "IND":
                clinicalP1Start = ""
                if indStart == "":
                    indStart = "1/1/14"
                if spStart == "":
                    spStart = "1/1/14"
                if loStart == "":
                    loStart = "1/1/14"
                if h2LStart == "":
                    h2LStart = "1/1/14"

            if currentStage == "SP":
                clinicalP1Start = ""
                indStart = ""
                if spStart == "":
                    spStart = "1/1/14"
                if loStart == "":
                    loStart = "1/1/14"
                if h2LStart == "":
                    h2LStart = "1/1/14"

            if currentStage == "LO":
                clinicalP1Start = ""
                indStart = ""
                spStart = ""
                if loStart == "":
                    loStart = "1/1/14"
                if h2LStart == "":
                    h2LStart = "1/1/14"

            if currentStage == "H2L":
                clinicalP1Start = ""
                indStart = ""
                spStart = ""
                loStart = ""
                if h2LStart == "":
                    h2LStart = "1/1/14"
                if h2LStart == "":
                    h2LStart = "1/1/14"

            if currentStage == "HA":
                clinicalP1Start = ""
                indStart = ""
                spStart = ""
                loStart = ""
                h2LStart = ""
                if haDate == "":
                    haDate = "1/1/14"

            if currentStage == "Screen":
                clinicalP1Start = ""
                indStart = ""
                spStart = ""
                loStart = ""
                h2LStart = ""
                haDate = ""

            if flag:
                validationFail = validationFail + 1
            else:
                validationSuccess = validationSuccess + 1

                if targetName != "unknown":
                    validatedProject = Project(
                        projectType="TargetBased",
                        projectName=projectName,
                        targetName=targetName,
                        targetId=targets.get(targetName)["id"],
                        smile=smile,
                        primaryOrganization=primaryOrganization,
                        primaryOrgId=appOrgs.get(primaryOrganization.upper()),
                        externalCompoundIds=externalCompoundIds,
                        library=row[19],
                        method="Legacy",
                        haStart=haDate,
                        h2LStart=h2LStart,
                        loStart=loStart,
                        spStart=spStart,
                        indStart=indStart,
                        clinicalP1Start=clinicalP1Start,
                        priority=row[21],
                        probability=row[22],
                        status=row[6],
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
                        library=row[19],
                        method="Legacy",
                        haStart=haDate,
                        h2LStart=h2LStart,
                        loStart=loStart,
                        spStart=spStart,
                        indStart=indStart,
                        clinicalP1Start=clinicalP1Start,
                        priority=row[21],
                        probability=row[22],
                        status=row[6],
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

        print("# ----HA DATE FAILS ----")
        pprint.pprint(Counter(haFails))

        print("# =========SUMMARY===========")
        print(f"# TOTAL : {total}")
        print(f"# VALIDATION SUCCESS  : {validationSuccess}")
        print(f"# VALIDATION FAIL     : {validationFail}")
        validationPercent = (validationSuccess / total) * 100 if total != 0 else 0
        print(f"# VALIDATION %        : {validationPercent:.2f}")
        print("")
        print(f"# PRIMARY ORG FAIL    : {primaryOrgFailCount}")
        print(f"# TARGET FAIL         : {targetFailCount}")
        print(f"# SMILE FAIL          : {smileFailCount}")
        print(f"# HA Date FAIL       : {HAFailCount}")
    return validated
