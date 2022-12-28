import re
import numpy as np
import timeit
import time
import json

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

def getOneDeeper(posMinPath):
    # instead of going recursive, just find the free neighbours, return, add to stack and repeat
    # needs and returns in format [pos, min, path]
    pos = posMinPath[0]
    min = posMinPath[1]
    path = posMinPath[2]
    
    # 0. check for looping
    lp = len(path)
    if lp >= cycle:
        if path[lp - cycle] == pos:
           return []
    
    # 1. check which neighbours are free on the next minute
    returnArray = []
    newCycleMin = (min+1) % cycle
    bliz = mergeSubLists(allPos[newCycleMin])
    for nb in  getNeighbours(pos):
        if nb not in bliz:
            newPath = [i for i in path]
            newPath.append(nb)
            returnArray.append([nb, min+1,newPath])
    return returnArray

def pathToString(path):
    return '   '+'\n   '.join([ '['+str(i[0])+', '+str(i[1])+']'  for i in path])

def runTime(sec):
    return time.strftime('%H:%M:%S', time.gmtime(sec))

# params
example = False
fileName = 'blizzards.txt'
if example:
    fileName = 'example_' + fileName
inf = 100000000000
startPos = [0,0]
cycle = (600,12)[example]

# parse
input = readFile(fileName).split('\n')
initialMap = [i[1:-1] for i in input[1:-1]]
Xlen = len(initialMap[0])
Ylen = len(initialMap)
goalPos = [Ylen-1,Xlen-1]

# extract positions of up/down/left/right going blizzards
uppies = getPositions(initialMap,'^')
downies = getPositions(initialMap,'v')
lefties = getPositions(initialMap, '<')
righties = getPositions(initialMap,'>')

# calculate blizard locations on each cycle minute
print('\n pre-calculating blizzard positions on all '+str(cycle)+ ' cycle minutes...')
start = timeit.default_timer()
allPos0 = [uppies, downies, lefties, righties]
allPos = [moveAllMinutes(allPos0, m) for m in range(1,cycle)]
allPos.insert(0,allPos0)
stop = timeit.default_timer()
print(' -> '+ runTime(stop-start))

# loop over all free minutes and try to find the shortest path
fm0 = getFreeMinutes(startPos)
if fm0[0] == 0:
    fm0 = moveLeft(fm0,1)
    fm0[-1] = cycle
print('\n possible start minutes: '+ str(fm0)+ '\n')

startMinute = fm0.pop(0)
curMinute = startMinute
print('start minute: ' + str(fm0[0]))
todo = [
    [startPos,startMinute,[startPos]]
]

start = timeit.default_timer()
while(len(todo) > 0):
    # insert new start minute if appropriate
    todoMin = todo[0][1]
    if len(fm0) > 0:
        if fm0[0] < todoMin:
            insertMin = fm0.pop(0)
            todo.insert(0,[startPos,insertMin,[startPos]])
        
    # get next from stack
    curTodo = todo.pop(0)
    
    # check if new minute and if so, report
    if curTodo[1] > curMinute:
        curMinute = curTodo[1]
        print(' minute: '+ str(curMinute))
        
    # find free neighbours on next minute to add to stack
    newTodos = getOneDeeper(curTodo)
    
    # check if we found the goalPos
    gp = [i for i in newTodos if i[0] == goalPos]
    if len(gp) > 0:
        goalPosMinPath = gp[0]
        break
    
    # else: add new ones to stack and continue
    todoPosMin = [[i[0],i[1]] for i in todo]
    todo += [i for i in newTodos if [i[0],i[1]] not in todoPosMin]

stop = timeit.default_timer()
print('\nrun time: '+ runTime(stop-start))

# some after-analysis
thisMin = goalPosMinPath[1]
print('\n'+'-'*50+'\n  reached goal in minutes: '+ str(thisMin+1)+'\n'+'-'*50)
writeFile(('','example_')[example] + 'posMinPath.txt',' pos: ' + str(goalPosMinPath[0]) + '\n min: '+str(goalPosMinPath[1]+1) + '\n path: \n' + pathToString(goalPosMinPath[2]))
