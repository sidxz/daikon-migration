from Validate import validateData
import csv
import pprint

print("Starting Validation")
validatedProjects = validateData()

# Print the length of the validatedProjects list
print("Length of validatedProjects: ", len(validatedProjects))


pp = pprint.PrettyPrinter(indent=4)


with open("test.csv", mode="w", newline="") as output_csv:
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

    for validatedProject in validatedProjects.values():
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
