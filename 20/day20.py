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
encryptionKey = 811589153
rounds = 10

# parse
input = readFile(fileName)
bareNumbers = [int(i)*encryptionKey for i in input.split('\n')]
numbers = [{'value':j,'index':idx} for (idx,j) in enumerate(bareNumbers)]
# print(json.dumps(numbers[0:3],indent=4))

# run
totalAmount = len(bareNumbers)
for j in range(0,rounds):
    print(' round '+ str(j+1) + '...')
    for index in range(0,totalAmount):
        curIndex = [i for (i,n) in enumerate(numbers) if n['index']==index][0]
        number = numbers.pop(curIndex)
        newIndex = (number['value'] + curIndex) % (totalAmount-1)
        numbers.insert(newIndex, number)

zeroIndex = [i for (i,n) in enumerate(numbers) if n['value']==0][0]
getIndices = np.mod(np.add(after,zeroIndex), totalAmount)
values =[j['value'] for j in [numbers[i] for i in getIndices]]
print(' 0 on index: ' + str(zeroIndex))
print(' get indices: '+str(getIndices))
print(' values: '+ str(values))
print(' sum:'+str(sum(values)))