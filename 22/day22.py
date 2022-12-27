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

def print1(inString): 
    if test1: print(inString)
    
def print2(inString):
    # global runlog
    if test2:
        print(inString)
        # runlog.append(inString)
        
def mapSlice(direction, line, verbose = True):
    # return a list of characters along given direction
    if verbose: print('   mapSlice in direction '+ direction + " on line " + str(line))
    if direction in 'RL':  return map[line]
    else:                  return ''.join([i[line:line+1] for i in map])
    
def turn(curDir, lr):
    curIndex = directions.find(curDir)
    newIndex = curIndex + (-1,1)[lr=='R']
    return directions[newIndex % (len(directions))]

def endPos(slice, startPos, maxSteps):
    sliceMatch = re.search("\S+", slice)
    nonEmptySlice = sliceMatch.group(0)
    firstNonEmpty = sliceMatch.start()
    print('   non-Empty slice: ' + nonEmptySlice)
    print('   from ' + str(firstNonEmpty) + ' to ' + str(sliceMatch.end()-1))
    print('   start pos: '+ str(startPos))
    
    # correct for instructions that suggest more steps than the non-empty slice length
    steps = maxSteps % len(nonEmptySlice)
    
    # take a subslice starting from startPos to the end of the slice to check where we're going
    firstSlice = nonEmptySlice[startPos - firstNonEmpty:]
    print('   first slice: '+ firstSlice)
    
    # 1. check if we hit a wall
    firstWall = firstSlice.find('#')
    if (firstWall > 0) & (firstWall <= maxSteps):
        # we hit a wall: return last index before we hit the wall
        return startPos + (firstWall -1)
    
    # 2. check if we will run out of the map
    if maxSteps < len(firstSlice):
        # we did not run out of the map: return new position
        return startPos + steps
    
    # still here means we ran out of the map: record last position before end of map and continue
    lastPos = startPos + (len(firstSlice) -1)
    remSteps = steps - len(firstSlice)
    print('   eol -> to start of slice, with remaining steps: '+ str(remSteps))
    # with the '-1', we are already circling towards the first non-empty character of the slice
    
    # if the first non-empty character of the slice is a wall: return lastPos
    if nonEmptySlice[0] == '#':
        return lastPos
    
    # we are now on the first non-empty character of the slice, which is NOT a wall
    # we can also not run into the empty anymore, thanks to the modulo at the start    
    # continue search with another sub slice
    secondSlice = nonEmptySlice[0:remSteps + 1]
    firstWall2 = secondSlice.find('#')
    print('   second slice: ' + secondSlice)
    print('   first wall on ' + str(firstWall2))
    if firstWall2 > 0:
        # indeed we ran into a wall!
        return firstNonEmpty + (firstWall2 -1)
    
    # we did not run into a wall: we can run until the end of our remaining steps!
    return firstNonEmpty + remSteps

def newPosDir(oldPosDir, instruction):
    # oldPosDir and output are 3x1 list in format [Y, X, Dir]
    # instruction is a trace element
    newDir = turn(oldPosDir[2], instruction[0])
    sliceLine = (oldPosDir[1],oldPosDir[0])[newDir in 'RL']
    startIndex = (oldPosDir[0],oldPosDir[1])[newDir in 'RL']
    mapLength = (len(map),len(map[0]))[newDir in 'RL']
    
    # slice is left-to-right or up-to-down
    ms = mapSlice(newDir, sliceLine)
    
    # if direction is UP or LEFT, we need to revert the slice and index
    if newDir in 'LU':
        ms = ms[::-1]
        startIndex = (mapLength -1) - startIndex
        
    # find 1-D end position
    endIndex = endPos(ms,startIndex,int(instruction[1]))
    print('   end pos: '+ str(endIndex))
    
    # if direction is UP or LEFT, we need to revert the result back
    if newDir in 'LU':
        endIndex = (mapLength -1) - endIndex
        
    # ... and we can return!
    if newDir in 'RL':
        return [oldPosDir[0], endIndex, newDir]
    else:
        return [endIndex, oldPosDir[1], newDir]
    
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
test1 = False
test2 = True
part: int = 1
directions = 'RDLU'
firstDir = 'U'
firstTurn = 'R'
startRow = 0

# parse
input = readFile(fileName).split('\n\n')
trace = re.findall("(^|\D)(\d+)",input[1])
# fill map with spaces to make length and height uniform
map = input[0].split('\n')
Xlen = max([len(l) for l in map])
map = [l + (Xlen -len(l))*' ' for l in map]

# some visual checking
print(trace[0:10])
print(trace[0:10][0][1])
print(' total instructions: '+ str(len(trace)))

# part 1
startCol = map[0].find('.')
posDir = [startRow, startCol,firstDir]
print('initial posDir: ' + str(posDir))
drawMap = [i for i in map]
for trIndex in range(0,len(trace)):
    tr = (trace[trIndex], [firstTurn,trace[0][1]])[trIndex == 0]
    
    print('trace ' + str(trIndex+1) + ": " + str(tr))
    nextPosDir = newPosDir(posDir, tr)
    drawOnMap(posDir, nextPosDir)
    posDir = nextPosDir
    print(' new posDir: ' + str(posDir)) 

writeFile('drawmap.txt', '\n'.join(drawMap))
print('final position and direction: ' + str(posDir))
finalPassword = 1000*(posDir[0]+1) + 4*(posDir[1]+1) + directions.find(posDir[2])
print('final password: (1000*'+ str(posDir[0]+1) + ') + (4*' + str(posDir[1]+1) + ") + ("+ posDir[2] + " -> " +  str( directions.find(posDir[2])) + ') = ' + str(finalPassword))