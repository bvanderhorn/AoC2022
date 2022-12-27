import re

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
        
def mapSlice(direction, line, verbose = True):
    # return a list of characters along given direction
    if verbose: print('   mapSlice in direction '+ direction + " on line " + str(line))
    if direction in 'RL':  return map[line]
    else:                  return ''.join([i[line:line+1] for i in map])
    
def turn(curDir, lr):
    curIndex = directions.find(curDir)
    newIndex = curIndex + (-1,1)[lr=='R']
    return directions[newIndex % (len(directions))]

def move1D(slice, startPos, steps):
    # make a 1-D move forward on given slice, starting at given startPos, 
    # having to take a maximum op 'steps' steps
    # will return in format [endPos, remainingSteps] 
    #  --> if remainingSteps > 0: need to possibly continue on another slice
    sliceMatch = re.search("\S+", slice)
    nonEmptySlice = sliceMatch.group(0)
    firstNonEmpty = sliceMatch.start()
    print('   non-Empty slice: ' + nonEmptySlice)
    print('   from ' + str(firstNonEmpty) + ' to ' + str(sliceMatch.end()-1))
    print('   start pos: '+ str(startPos))
    
    # take a subslice starting from startPos to the end of the slice to check where we're going
    subSlice = nonEmptySlice[startPos - firstNonEmpty:]
    print('   sub slice: '+ subSlice)
    
    # 1. check if we hit a wall
    firstWall = subSlice.find('#')
    if firstWall == 0:
        # -> the very start pos is a wall: return empty
        return []
    if (firstWall > 0) & (firstWall <= steps):
        # we hit a wall: return last index before we hit the wall
        return [startPos + (firstWall -1), 0]
    
    # 2. check if we will run out of the map
    if steps < len(subSlice):
        # we did not: return new position
        return [startPos + steps, 0]
    else:
        # we did: return the end of the slice and remaining steps
        return [startPos + len(subSlice) -1, steps - len(subSlice) + 1]
    
def moveOnSlice(posDir,steps):
    # given a position, direction and number of steps: 
    # return position and number of steps after the next move on the same slice
    dir = posDir[2]
    sliceLine = (posDir[1],posDir[0])[dir in 'RL']
    startIndex = (posDir[0],posDir[1])[dir in 'RL']
    mapLength = (len(map),len(map[0]))[dir in 'RL']
    
    ms = mapSlice(dir, sliceLine)
    
    # if direction is UP or LEFT, we need to revert the slice and index
    if dir in 'LU':
        ms = ms[::-1]
        startIndex = (mapLength -1) - startIndex
        
    # find next position and remaining steps on this slice
    endPosSteps = move1D(ms,startIndex,steps)
    print('   end pos and steps remaining: '+ str(endPosSteps))
    
    # if the very start position on the slice was a wall: return empty
    if len(endPosSteps) == 0:  return []
    
    # if direction is UP or LEFT, we need to revert the final index back
    if dir in 'LU':
        endPosSteps[0] = (mapLength -1) - endPosSteps[0]
    
    if dir in 'RL':
        return [posDir[0], endPosSteps[0], endPosSteps[1]]
    else:
        return [endPosSteps[0], posDir[1], endPosSteps[1]]

def newPosDir(oldPosDir, instruction):
    # oldPosDir and output are 3x1 list in format [Y, X, Dir]
    # instruction is a trace element in format [Dir, Steps]
    maxSteps = int(instruction[1])
        
    # loop over slices until end position is found
    remSteps = maxSteps
    curDir = turn(oldPosDir[2], instruction[0])
    curPosDir = [oldPosDir[0],oldPosDir[1],curDir]
    prevPosDir = [i for i in curPosDir]
    while(True):
        newPosSteps = moveOnSlice(curPosDir, remSteps)
        
        # if we are on the edge of a slice and there is a wall on the very
        # point on the next slice we're trying to go: return last posDir
        if len(newPosSteps) == 0:
            return prevPosDir
        
        curPosDir = [newPosSteps[0], newPosSteps[1], curDir]
        remSteps = newPosSteps[2]
        
        # else, if remSteps = 0: return new posdir
        if  remSteps == 0:
            return curPosDir
        
        # if there are still steps remaining: 
        # find position and direction on next face and repeat
        prevPosDir = [i for i in curPosDir]
        curPosDir = switchFace(curPosDir[0:2])
        remSteps -= 1
    
def getPath(posDirA, posDirB):
    # return an array of coordinates from pos a to pos b in direction posDirB[2]
    pos = [i for i in posDirA[0:2]]
    coor = [[pos[0], pos[1]]]
    dir = posDirB[2]
    goalPos = posDirB[0:2]
    
    sliceLine = (posDirA[1],posDirA[0])[dir in 'RL']
    slice = mapSlice(dir, sliceLine, False)
    sliceMatch = re.search("\S+", slice)
    nonEmptySlice = sliceMatch.group(0)
    first = sliceMatch.start()
    last = first + len(nonEmptySlice) - 1
    
    while(pos != goalPos):
        if dir == 'R':    pos = [pos[0],(pos[1] +1,first)[pos[1] == last]]
        if dir == 'L':    pos = [pos[0],(pos[1]-1,last)[pos[1] == first]]
        if dir == 'D':    pos = [(pos[0]+1,first)[pos[0] == last],pos[1]]
        if dir == 'U':    pos = [(pos[0]-1,last)[pos[0] == first],pos[1]]

        coor.append([pos[0], pos[1]])
    return coor

def drawOnMap(posDir1, posDir2):
    global drawMap
    signDict = {'R':'>','L':'<','D':'v','U':'^'}
    sign = signDict[posDir2[2]]
    
    drawPath = getPath(posDir1, posDir2)
    for co in drawPath:
        stringList = list([i for i in drawMap[co[0]]])
        stringList[co[1]] = sign
        drawMap[co[0]] = ''.join(stringList)

# params
fileName = 'mapandtrace.txt'
directions = 'RDLU'
firstDir = 'U'
firstTurn = 'R'
startRow = 0
part:int = 1

# parse
input = readFile(fileName).split('\n\n')
trace = re.findall("(^|\D)(\d+)",input[1])
# fill map with spaces to make length and height uniform
map = input[0].split('\n')
Xlen = max([len(l) for l in map])
map = [l + (Xlen -len(l))*' ' for l in map]

# some visual checking
print(' total instructions: '+ str(len(trace)))
maxTrace = max([int(i[1]) for i in trace])
print(' max instruction length: ' + str(maxTrace))

# part 1
startCol = map[0].find('.')
posDir = [startRow, startCol,firstDir]
print('initial posDir: ' + str(posDir))
drawMap = [i for i in map]
for trIndex in range(0,3):
    tr = (trace[trIndex], [firstTurn,trace[0][1]])[trIndex == 0]
    
    print('trace ' + str(trIndex+1) + ": " + str(tr))
    nextPosDir = newPosDir(posDir, tr)
    if part == 1: drawOnMap(posDir, nextPosDir)
    posDir = nextPosDir
    print(' new posDir: ' + str(posDir)) 

if part == 1: writeFile('drawmap.txt', '\n'.join(drawMap))
print('final position and direction: ' + str(posDir))
finalPassword = 1000*(posDir[0]+1) + 4*(posDir[1]+1) + directions.find(posDir[2])
print('final password: (1000*'+ str(posDir[0]+1) + ') + (4*' + str(posDir[1]+1) + ") + ("+ posDir[2] + " -> " +  str( directions.find(posDir[2])) + ') = ' + str(finalPassword))