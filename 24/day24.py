import re
import numpy as np
import timeit
import time

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

def moveLeft(inList, amount):
    return inList[amount:] + inList[:amount]
    
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
    nb = [ [pos[0]-1, pos[1]], [pos[0]+1, pos[1]], [pos[0], pos[1]-1], [pos[0], pos[1]+1] , pos]
    return [i for i in nb if (i[0]>= 0) and (i[0] < Ylen) and (i[1]>= 0) and (i[1] < Xlen) ]

def theoMin(pos,min):
    # calculate theoretical minimum minutes of reaching the goalPos from current position
    return sum(np.subtract(goalPos,pos)) + min

def getFreeMinutes(pos, verbose = False):
    # for a given [Y,X] position, return list of cycle minutes (1-600) in which it is free
    if verbose: print(' free minutes calculation for '+ str(pos))
    u0 = [u for u in uppies if u[1] == pos[1]]
    d0 = [d for d in downies if d[1] == pos[1]]
    l0 = [l for l in lefties if l[0] == pos[0]]
    r0 = [r for r in righties if r[0] == pos[0]]
    if verbose:
        print('  blizzards on minute 0:')
        print('  up: ' + str(u0))
        print('  dn: ' + str(d0))
        print('  le: ' + str(l0))
        print('  ri: ' + str(r0))
    
    freeMinutes = []
    for m in range(0,cycle):
        bliz = moveAllMinutes([u0,d0,l0,r0],m)
        if pos not in mergeSubLists(bliz):
            freeMinutes.append(m)
    
    if verbose: print('  free minutes: '+ str(freeMinutes))
    return freeMinutes

def getMaxWithRemaining(pos, min, verbose=False, path=[], depth=0):
    # get minimum minutes of all possible remaining paths of reaching goalPos (or return INF if impossible)
    global minMinutes
    global maxDepth
    d2 = depth*2
    d2a = d2+1
    if verbose: print(' '*d2 + 'min '+str(min) + ', pos: '+str(pos))
    if len(path) >= cycle:
        if path[len(path)- cycle] == pos:
           if verbose: print(' '*d2 + '=> LOOPING: return INF') 
           return inf
    
    if depth > maxDepth:
        maxDepth = depth
        # print(' new max depth: '+str(depth))
    
    if minMinutes <= theoMin(pos,min): return inf
    elif pos == goalPos:
        minMinutes = min
        print(' -> found new minimum: ' + str(min) + ' minutes')
        return min
    
    # 1. check which neighbours are free on the next minute
    freeNb = []
    for nb in  getNeighbours(pos):
        if ((min+1) % cycle) in allFreeMinutes[nb[0]][nb[1]]:
            freeNb.append(nb)
    if verbose: print(' '*d2a + 'free nb: '+ str(freeNb))
    
    if len(freeNb) == 0:
        if verbose: print(' '*d2a + ' -> no neighbours: INF')
        return inf
    
    # 2. loop and find minima for each option
    minMins = []
    for nb in freeNb:
        newPath = [i for i in path]
        newPath.append(pos)
        nbMins = getMaxWithRemaining(nb,min+1,verbose,newPath,depth+1)
        minMins.append(nbMins)
        
    # 4. return the minimum of the found minima
    if verbose: 
        print(' '*d2 + 'return : ' + str(minMins))
    return sorted(minMins,reverse=True)[0]

# params
fileName = 'example_blizzards.txt'
inf = 100000000000
startPos = [0,0]
# cycle = 600
cycle = 12

# parse
input = readFile(fileName).split('\n')
initialMap = [i[1:-1] for i in input[1:-1]]
Xlen = len(initialMap[0])
Ylen = len(initialMap)
goalPos = [Ylen-1,Xlen-1]
# print('\n'.join(initialMap))

# extract positions of up/down/left/right going blizzards
uppies = getPositions(initialMap,'^')
downies = getPositions(initialMap,'v')
lefties = getPositions(initialMap, '<')
righties = getPositions(initialMap,'>')
# print(lefties[0:10])

allFreeMinutes = []
for y in range(0,Ylen):
    print(' calculating fm for y = '+ str(y)+'...')
    start = timeit.default_timer()
    allFreeMinutes.append([getFreeMinutes([y,x]) for x in range(0,Xlen)])
    stop = timeit.default_timer()
    runTime = time.strftime('%H:%M:%S', time.gmtime(stop - start))
    print('  -> ' + runTime)

# loop over all free minutes and try to find the shortest path
fm0 = allFreeMinutes[0][0]
if fm0[0] == 0:
    fm0 = moveLeft(fm0,1)
print(' free start minutes: '+ str(fm0))
minMinutes = inf
for fm in fm0:
    maxDepth = 0
    print('start minute: ' + str(fm))
    if minMinutes <= theoMin(startPos, fm):
        print(' theoretically not possible to find a quicker solution with this start minute or higher -> BREAK')
        break
    # calculate start positions
    bliz = moveAllMinutes([uppies, downies, lefties, righties],fm)
    pos = startPos
    
    curMin = getMaxWithRemaining(pos,fm)
    if curMin < minMinutes:
        minMinutes = curMin
        
print('\n'+'-'*30+'\n  minimal minutes: '+ str(minMinutes)+'\n'+'-'*30)

getFreeMinutes([1,2],True)