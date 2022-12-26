import numpy as np
import json

# functions
def readFile(fName):
    inStream = open(fName,'r')
    out = inStream.read()
    inStream.close()
    return out

def getNextNotMoved(array1):
    notMoved = [i for (i,a) in enumerate(array1) if a['moved']==False]
    return (-1, notMoved[0])[len(notMoved)>0]

def getNewIndex(index, move, arrayLength):
    others = arrayLength -1
    return (move + index) % others
    

# params
fileName = 'file.txt'
key = 0
after = [1000,2000,3000]

# parse
input = readFile(fileName)
bareNumbers = [int(i) for i in input.split('\n')]
numbers = [{'num':i, 'moved':False} for i in bareNumbers]
print(json.dumps(numbers[0:3],indent=4))
print([i['num'] for i in numbers[0:3]])
print(min(bareNumbers))
print(max(bareNumbers))

totalAmount = len(numbers)
for n in range(0,totalAmount):
    curIndex = getNextNotMoved(numbers)
    number = numbers.pop(curIndex)
    number['moved'] = True
    numbers.insert(getNewIndex(curIndex,number['num'],totalAmount), number)

zeroIndex = [i for (i,n) in enumerate(numbers) if n['num']==0][0]
getIndices = np.mod(np.add(after,zeroIndex), totalAmount)
values =[j['num'] for j in [numbers[i] for i in getIndices]]
print(' 0 on index: ' + str(zeroIndex))
print(' get indices: '+str(getIndices))
print(' values: '+ str(values))
print(' sum:'+str(sum(values)))
    
    