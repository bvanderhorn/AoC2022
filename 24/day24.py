import re
import numpy as np

# functions
def readFile(fName):
    inStream = open(fName,'r')
    out = inStream.read()
    inStream.close()
    return out

def writeFile(fName,outString):
    outStream = open(fName,'w')
    outStream.write(outString)
    outStream.close()
    
def mergeSubLists(list1):
    return [j for i in list1 for j in i]
    
def getPositions(map,char):
    # for a given map and character (like '<'), return a list of [Y,X] positions
    pos = []
    checkChar = (char, '\\'+ char)[char in '\[]^$-|?!()']
    for i in range(0,len(map)):
        pos += [[i, m.start()] for m in re.finditer(checkChar,map[i])]
    return pos

def moveMinutes(pos, dir, minutes):
    add = { 'u':[-1,0], 'd':[1,0], 'l':[0,-1], 'r':[0,+1] }
    return list(np.mod(np.add(np.multiply(add[dir],minutes), pos), [Ylen, Xlen]))

def moveAllMinutes(allPos, mins):
    # calculate all new positions after moving 'mins' minutes
    # allPos and return are 4x1xN coordinate lists in format [U, D, L, R]
    return [
        [moveMinutes(u,'u',mins) for u in allPos[0]],
        [moveMinutes(d,'d',mins) for d in allPos[1]],
        [moveMinutes(l,'l',mins) for l in allPos[2]],
        [moveMinutes(r,'r',mins) for r in allPos[3]]
    ]
    
def getNeighbours(pos):
    # return all possible neighbours (up/down/left/right) of current position
    nb = [ [pos[0]-1, pos[1]], [pos[0]+1, pos[1]], [pos[0], pos[1]-1], [pos[0], pos[1]+1] ]
    return [i for i in nb if (i[0]>= 0) and (i[0] < Ylen) and (i[1]>= 0) and (i[1] < Xlen) ]

def theoMin(pos,min):
    # calculate theoretical minimum minutes of reaching the goalPos from current position
    return sum(np.subtract(goalPos,pos)) + min

def getMaxWithRemaining(bliz, pos, min, depth=0):
    # get minimum minutes of all possible remaining paths of reaching goalPos (or return INF if impossible)
    # bliz in format [ups, downs, lefts, rights]
    global minMinutes
    global maxDepth
    d2 = depth*2
    d2a = d2+1
    # print(' '*d2 + 'min '+str(min) + ', pos: '+str(pos))
    if depth > maxDepth:
        maxDepth = depth
        print(' new max depth: '+str(depth))
    
    if minMinutes <= theoMin(pos,min): return inf
    elif pos == goalPos:
        minMinutes = min
        print(' -> found new minimum: ' + str(min) + ' minutes')
        return min
    
    # 1. move blizzards
    newBliz = moveAllMinutes(bliz,1)
    
    # 2. check which neighbours are free
    freeNb = [i for i in getNeighbours(pos) if i not in mergeSubLists(newBliz)]
    # print(' '*d2a + 'free nb: '+ str(freeNb))
    if len(freeNb) == 0:
        # print(' '*d2a + ' -> no neighbours: INF')
        return inf
    
    # 3. loop and find minima for each option
    minMins = []
    for nb in freeNb:
        nbMins = getMaxWithRemaining(newBliz,nb,min+1,depth+1)
        minMins.append(nbMins)
        
    # 4. return the minimum of the found minima
    # print(' '*d2 + 'return : ' + str(minMins))
    return sorted(minMins,reverse=True)[0]


# params
fileName = 'blizzards.txt'
Xlen = 120
Ylen = 25
inf = 100000000000
startPos = [0,0]
goalPos = [24,119]

# parse
input = readFile(fileName).split('\n')
initialMap = [i[1:-1] for i in input[1:-1]]
# print('\n'.join(initialMap))

# extract positions of up/down/left/right going blizzards
uppies = getPositions(initialMap,'^')
downies = getPositions(initialMap,'v')
lefties = getPositions(initialMap, '<')
righties = getPositions(initialMap,'>')
# print(lefties[0:10])

# find possible start minutes: minutes (starting at 1) at which [0,0] is NOT occupied by a blizzard
# possible start minutes are only influenced by ups/downs at X=0 and lefts/rights at Y=0
# len/height = 120x25 -> blizzard pos repeats every 600 minutes
u0 = [u for u in uppies if u[1] == 0]
d0 = [d for d in downies if d[1] == 0]
l0 = [l for l in lefties if l[0] == 0]
r0 = [r for r in righties if r[0] == 0]

# print(moveMinutes([1,2],'l',3))
freeMinutes = []
for m in range(1,601):
    bliz0s = moveAllMinutes([u0,d0,l0,r0],m)
    if [0,0] not in mergeSubLists(bliz0s):
        freeMinutes.append(m)
print(len(freeMinutes))

# loop over all free minutes and try to find the shortest path
minMinutes = inf
for fm in freeMinutes[0:1]:
    print('start minute: ' + str(fm))
    if minMinutes <= theoMin(startPos, fm):
        print(' theoretically not possible to find a quicker solution with this start minute or higher -> BREAK')
        break
    # calculate start positions
    bliz = moveAllMinutes([uppies, downies, lefties, righties],fm)
    pos = startPos
    maxDepth = 0
    curMin = getMaxWithRemaining(bliz,pos,fm)
    if curMin < minMinutes:
        minMinutes = curMin
