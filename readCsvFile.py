import csv
import json


def readAllFiles(*args, readFunc):
    fileData = [ readFunc(x) for x in args ]
    return { k: v for map in fileData for k,v in map.items()}

def readSpreadsheet(fileName,emailCol="Email",fnCol="First Name", lnCol="Lastname"):
    with open(fileName) as f:
        return {row[emailCol].split("@")[0]: (row[fnCol], row[lnCol]) for row in csv.DictReader(f) if row["Email"] and row["Badge Status"] != "Badge Activated"}

def readSnow(fileName):
    with open(fileName) as f:
        return { row["caller.user_name"] : row["caller"].split() + [row["location"]] for row in csv.DictReader(f) if row["state"] != "Cancelled"}

def getNamesNotInSpreadsheet(spreadsheetNames, snowNames):
    intersection = spreadsheetNames.keys() & snowNames.keys()
    return { x : snowNames[x] for x in intersection}

def writeJsonToFile(fileName, data):
    with open("output.json", 'w') as f:
        for key in sorted(data.keys()):
            f.write(key + '\n')
        json.dump(data,f, indent=4)

def main():
    spreadsheet = readSpreadsheet("badges.csv")
    snownames = readSnow("u_facilities.csv")
    results = getNamesNotInSpreadsheet(spreadsheet, snownames)
    writeJsonToFile("output.json", results)
"""
merge all spread sheet tabs
get spreadsheet data via GET
write to spreadsheet?


"""