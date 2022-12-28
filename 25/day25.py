import numpy as np

# functions
def readFile(fName):
    inStream = open(fName,'r')
    out = inStream.read()
    inStream.close()
    return out

def prints(list1):
    print('')
    for l in list1: print(l)

def printt(el):
    print('\n'+str(el))

# params
fileName = 'snafu.txt'

# parse
input = readFile(fileName).split('\n')

# reverse strings -> start at lowest index (and split to list)
snafu = [list(i[::-1]) for i in input]
prints(snafu[0:3])

# replace -/= by -1/-2 and cast to int
for s in range(0,len(snafu)):
    snafu[s] = [int(j) for j in [((i,-2)[i=='='],-1)[i=='-'] for i in snafu[s]]]
prints(snafu[0:3])

# make all snafus same length
maxLen = max([len(i) for i in snafu])
snafu = [s + [0]*(maxLen-len(s)) for s in snafu]

printt(' max length: '+ str(maxLen))
prints(snafu[0:3])

# add all sublist elements together
sumAll = list(np.array(snafu).sum(axis=0))
printt(sumAll)

# add some trailing zeros to allow the rewrite
sumAll += [0]*10
printt(sumAll)

# go through each item, add from previous, update to fall between (-2,2) and calculate what to add to the next
minVal = -2
maxVal = 2
addToItem = 0
corrected = []
for s in range(0,len(sumAll)):
    q = sumAll[s]
    
    # subtract previous correction from this item
    q -= addToItem
    
    # correct this item and calculate addition to next
    addToItem = 0
    if (q < minVal):
        diff = minVal - q
        addToItem = np.ceil(diff/5)
    elif (q > maxVal):
        diff = maxVal - q
        addToItem = np.floor(diff/5)
    
    # save to new list
    corrected.append(int(q + 5*addToItem))
    
printt(corrected)

# revert back to snafu
newSnafu = [((str(i),'=')[i==-2],'-')[i==-1] for i in corrected]
newSnafu = ''.join(newSnafu[::-1]).lstrip('0')
printt(newSnafu)