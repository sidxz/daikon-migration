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
            currentStage = row[5]
            projectLegacyId = row[0]
            primaryOrganization = row[4]
            externalCompoundIds = "SPPCID-" + row[0]
            primaryOrganizationAbb = primaryOrganization.upper().replace(" ", "")
            haDate = row[8]
            h2LStart = row[10]
            loStart = row[12]
            spStart = row[14]
            indStart = row[16]
            clinicalP1Start = row[18]

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
                if len(clinicalP1Start) == 0:
                    clinicalP1Start = "1/1/14"
                if len(indStart) == 0:
                    indStart = "1/1/14"
                if len(spStart) == 0:
                    spStart = "1/1/14"
                if len(loStart) == 0:
                    loStart = "1/1/14"
                if len(h2LStart) == 0:
                    h2LStart = "1/1/14"
                if len(haDate) == 0:
                    haDate = "1/1/14"

            if currentStage == "IND":
                clinicalP1Start = ""
                if len(indStart) == 0:
                    indStart = "1/1/14"
                if len(spStart) == 0:
                    spStart = "1/1/14"
                if len(loStart) == 0:
                    loStart = "1/1/14"
                if len(h2LStart) == 0:
                    h2LStart = "1/1/14"
                if len(haDate) == 0:
                    haDate = "1/1/14"

            if currentStage == "SP":
                clinicalP1Start = ""
                indStart = ""
                if len(spStart) == 0:
                    spStart = "1/1/14"
                if len(loStart) == 0:
                    loStart = "1/1/14"
                if len(h2LStart) == 0:
                    h2LStart = "1/1/14"
                if len(haDate) == 0:
                    haDate = "1/1/14"

            if currentStage == "LO":
                clinicalP1Start = ""
                indStart = ""
                spStart = ""
                if len(loStart) == 0:
                    loStart = "1/1/14"
                if len(h2LStart) == 0:
                    h2LStart = "1/1/14"
                if len(haDate) == 0:
                    haDate = "1/1/14"

            if currentStage == "H2L":
                clinicalP1Start = ""
                indStart = ""
                spStart = ""
                loStart = ""
                if len(h2LStart) == 0:
                    h2LStart = "1/1/14"
                if len(haDate) == 0:
                    haDate = "1/1/14"

            if currentStage == "HA":
                clinicalP1Start = ""
                indStart = ""
                spStart = ""
                loStart = ""
                h2LStart = ""
                if len(haDate) == 0:
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
                        currentStage=currentStage,
                        projectLegacyId=projectLegacyId,
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
                        currentStage=currentStage,
                        projectLegacyId=projectLegacyId,
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

        with open("int_data/projects_validated.csv", mode="w", newline="") as output_csv:
            csv_writer = csv.writer(
                output_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            # Writing headers
            csv_writer.writerow(
                [
                    "projectType",
                    "projectLegacyId",
                    "projectName",
                    "targetName",
                    "status",
                    "currentStage",
                    "haStart",
                    "h2LStart",
                    "loStart",
                    "spStart",
                    "indStart",
                    "clinicalP1Start",
                    "primaryOrganization",
                    "primaryOrgId",
                    "externalCompoundIds",
                    "library",
                    "method",
                    "priority",
                    "probability",
                    "smile",
                ]
            )

            for validatedProject in validated.values():
                csv_writer.writerow(
                    [
                        validatedProject.projectType,
                        validatedProject.projectLegacyId,
                        validatedProject.projectName,
                        validatedProject.targetName,
                        validatedProject.status,
                        validatedProject.currentStage,
                        validatedProject.haStart,
                        validatedProject.h2LStart,
                        validatedProject.loStart,
                        validatedProject.spStart,
                        validatedProject.indStart,
                        validatedProject.clinicalP1Start,
                        validatedProject.primaryOrganization,
                        validatedProject.primaryOrgId,
                        validatedProject.externalCompoundIds,
                        validatedProject.library,
                        validatedProject.method,
                        validatedProject.priority,
                        validatedProject.probability,
                        validatedProject.smile,
                    ]
                )

    return validated
