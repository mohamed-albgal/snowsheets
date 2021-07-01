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
    with open(fileName, 'w') as f:
        json.dump(data,f, indent=4)

def main():
    spreadsheets = readAllFiles("us.csv", "sr.csv", "con.csv", "van.csv", readFunc=readSpreadsheet)
    snow = readAllFiles('bou.csv', "mor.csv", "pla.csv", "sea.csv", "sfo.csv", "tys.csv", "lon.csv",'sjsnow.csv', 'vn.csv',  readFunc=readSnow)
    results = getNamesNotInSpreadsheet(spreadsheets, snow)
    writeJsonToFile("output.json", results)
main()
