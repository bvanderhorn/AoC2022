import numpy as np
import json

# functions
def readFile(fName):
    inStream = open(fName,'r')
    out = inStream.read()
    inStream.close()
    return out

def getNextNotMoved(array1):
    notMoved = [i for i,a in array1 if a['moved']==False]
    return (-1, notMoved[0])[len(notMoved)>0]

# params
fileName = 'file.txt'
key = 0
after = [1000,2000,3000]

# parse
input = readFile(fileName)
bareNumbers = [int(i) for i in input.split('\n')]
numbers = np.array([{'num':i, 'moved':False} for i in bareNumbers])
print(json.dumps(list(numbers[0:3]),indent=4))
print([i['num'] for i in numbers[0:3]])
print(min(bareNumbers))
print(max(bareNumbers))

for n in range(0,len(numbers)):
    0