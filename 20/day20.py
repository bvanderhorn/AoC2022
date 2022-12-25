import numpy as np
import json


# functions
def readFile(fName):
    inStream = open(fName,'r')
    out = inStream.read()
    inStream.close()
    return out

# params
fileName = 'file.txt'
key = 0
after = [1000,2000,3000]

# parse
input = readFile(fileName)
numbers = [{'num':int(i), 'moved':False} for i in input.split('\n')]
print(json.dumps(numbers[0:3],indent=4))
print([i['num'] for i in numbers[0:3]])