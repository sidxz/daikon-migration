import json
from Validate import validateData
from apiClient import addScreen, terminateProject
from apiClient import addHit
from apiClient import getProjects
import datetime
import time
import pytz

def fdate(dstr):
  parse = str(datetime.datetime.strptime(
      dstr, '%m/%d/%y').strftime('%Y-%m-%dT%H:%M:%S'))
  return parse + '.840259Z'


# Validate Data
validatedProjects = validateData()

results = []
for projectName in validatedProjects:
  time.sleep(0.01)
  print("# --------------------------------")
  print(f"# For {projectName}")
  project = validatedProjects[projectName]

  
  # Project
  existingProjects = dict()
  existingProjects.clear()
  existingProjects = getProjects()
  existing_project = existingProjects.get(project.projectName)
  if existing_project is not None:
      projectId = existing_project['id']
  else:
      projectId = None


  # Active or Terminate

  if project.status == "Terminated" and projectId is not None:
    print("Project should be Terminated")
    term = {
        "id": projectId,
        "projectName": project.projectName
    }
    res = terminateProject(projectId, term)
    term["StatusCode"] = res
    results.append(term)
    print(res)
  print("# -----------END--------------------")
with open('int_data/terminateProjects.json', 'w') as outfile:
  json.dump(results, outfile, indent=4)
