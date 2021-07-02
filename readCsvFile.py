import csv
import json
import os
import sys
import datetime

def readAllFiles(*args, readFunc):
    fileData = [ readFunc(x) for x in args ]
    return { k: v for map in fileData for k,v in map.items()}

def readSpreadsheet(fileName,emailCol="Email",fnCol="First Name", lnCol="Lastname", badgeStatusCol="Badge Status"):
    with open(fileName) as f:
        filterCriterion = lambda x: x[emailCol] and x[badgeStatusCol] != "Badge Activated"
        return  {row[emailCol].split("@")[0]: (row[fnCol], row[lnCol]) for row in csv.DictReader(f) if filterCriterion(row) }

def readSnow(fileName, emailCol="caller.user_name",nameCol="caller", locationCol="location", ticketStatus="state"):
    with open(fileName, encoding='latin-1') as f:
        filterCriterion = lambda x: x[ticketStatus] != "Cancelled"
        return { row[emailCol] : row[nameCol].split() + [row[locationCol]] for row in csv.DictReader(f,) if filterCriterion(row)}

def getNamesNotInSpreadsheet(spreadsheetNames, snowNames):
    # too concrete?
    intersection = spreadsheetNames.keys() & snowNames.keys()
    return { x : snowNames[x] for x in intersection}

def writeJsonToFile(data):
    # asserts dir named output in cwd
    timestamp = str(datetime.datetime.now())
    filePath = os.getcwd() + "/output/" +timestamp + ".json"
    with open(filePath, 'w') as f:
        json.dump(data,f, indent=4)

def getPathsFromDir(dirName):
    # assert no subdirs exist in subdir
    cwd = os.getcwd()
    subdir = os.path.join(cwd, dirName)
    return  [os.path.join(subdir, f) for f in os.listdir(subdir)]

def main():
    badges = readAllFiles(*getPathsFromDir("badges"),  readFunc=readSpreadsheet)
    snow = readAllFiles(*getPathsFromDir("snow"), readFunc=readSnow)
    results = getNamesNotInSpreadsheet(badges, snow)
    writeJsonToFile(results)

if __name__ == "__main__":
    print("reading from /badges and /snow --> output to /output")
    a = input("Press y to confirm this reminder    ")
    b = input("Press y to make sure the first line of the badges file is the column header    ")
    confirmed = a and b and a.index("y") >= 0 and b.index("y") >= 0
    if confirmed:
        main()