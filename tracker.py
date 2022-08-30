import csv

# Screen Tracker
#  projectName, targetId | targetName | screenId | screenName |


def loadScreenTracker():
    screens = {}
    with open('int_data/screen.csv') as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=',')
        for row in csv_reader:
            screen = {
                "projectName": row[0],
                "targetId": row[1],
                "targetName": row[2],
                "screenId": row[3],
                "screenName": row[4]
            }
            screens[row[0]] = screen
    return screens


def addToScreenTracker(projectName, targetId, targetName, screenId, screenName):
    with open('int_data/screen.csv', 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        data = [projectName, targetId, targetName, screenId, screenName]
        writer.writerow(data)

# Hit Tracker
#  projectName, targetId | targetName | screenId | screenName | HitId


def loadHitTracker():
    screens = {}
    with open('int_data/hit.csv') as input_csv:
        csv_reader = csv.reader(input_csv, delimiter=',')
        for row in csv_reader:
            hit = {
                "projectName": row[0],
                "targetId": row[1],
                "targetName": row[2],
                "screenId": row[3],
                "screenName": row[4],
                "hitId": row[5],
                "compoundId": row[6]
            }
            screens[row[0]] = hit
    return screens


def addToHitTracker(projectName, targetId, targetName, screenId, screenName, hitId, compoundId):
    with open('int_data/hit.csv', 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        data = [projectName, targetId, targetName,
                screenId, screenName, hitId, compoundId]
        writer.writerow(data)
