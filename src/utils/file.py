from flask import json

def writeFile(fileLocation, data):
    TheFile = open(fileLocation, 'w')
    TheFile.write(str(json.dumps(data)))

def readFile(fileLocation):
    theFile = open(fileLocation)
    data = json.load(theFile)
    return data   

def checkFile():

    return "checkFile"