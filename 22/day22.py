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

def switchFace(edgePosDir):
    # given a current pos and dir on a face edge, return first 
    # position and direction on the new face
    # edgePosDir and return in format [Y, X, Dir]
    print('    switch face from current posDir: '+ str(edgePosDir))
    edgeLength = 50
    Y = edgePosDir[0]
    X = edgePosDir[1]
    D = edgePosDir[2]
    
    # list of map edges in format [Along, line, minIndex, maxIndex]
    edges = [
        ['X',   0,  50,  99], # 0
        ['X',   0, 100, 149], # 1
        ['Y', 149,   0,  49], # 2
        ['X',  49, 100, 149], # 3
        ['Y',  99,  50,  99], # 4
        ['Y',  99, 100, 149], # 5
        ['X', 149,  50,  99], # 6
        ['Y',  49, 150, 199], # 7
        ['X', 199,   0,  49], # 8
        ['Y',   0, 150, 199], # 9
        ['Y',   0, 100, 149], # 10
        ['X', 100,   0,  49], # 11
        ['Y',  50,  50,  99], # 12
        ['Y',  50,   0,  49]  # 13
    ]
    
    # list of edge touches in format [edgeAIndex, edgeBIndex, reverse (True/False)]
    if part == 2:
        edgeLinks = [
            [ 0,  9, False],
            [ 1,  8, False],
            [ 2,  5, True ],
            [ 3,  4, False],
            [ 6,  7, False],
            [10, 13, True ],
            [11, 12, False]
        ]
    else: # if part == 1
        edgeLinks = [
            [ 0,  6, False],
            [ 1,  3, False],
            [ 2, 13, False],
            [ 4, 12, False],
            [ 5, 10, False],
            [ 7,  9, False],
            [ 8, 11, False]
        ]
    
    # find the current edge, the associated link, the new edge and the new coordinates and direction
    # current edge
    curAlong = ('X','Y')[D in 'RL']
    curAlongPos = (X,Y)[curAlong == 'Y']
    curLine = (Y,X)[curAlong == 'Y']
    curLineDir = ('X','Y')[curAlong == 'X']
    print('    cur Along ' + curAlong + ' with along pos ' + curAlong + ' = ' + str(curAlongPos) + ' and line pos ' + curLineDir + ' = ' + str(curLine))
    curEdgeIndex = [i for (i,e) in enumerate(edges) if (e[0] == curAlong) and (e[1] == curLine) and (e[2] <= curAlongPos) and (e[3] >= curAlongPos)][0]
    curEdge = edges[curEdgeIndex]
    curAlongIndex = curAlongPos - curEdge[2]
    print('    current edge '+ str(curEdgeIndex) + ': '+ str(curEdge) + ' with rel position '+ str(curAlongIndex))
    
    # link
    link = [l for l in edgeLinks if curEdgeIndex in l[0:2]][0]
    print('   link: '+ str(link))
    
    # new edge
    newEdgeIndex = [i for i in link[0:2] if i != curEdgeIndex][0]
    newEdge = edges[newEdgeIndex]
    newAlong = newEdge[0]
    newAlongIndex = (curAlongIndex, (edgeLength - 1) - curAlongIndex)[link[2]]
    newAlongPos = range(newEdge[2], newEdge[3]+1)[newAlongIndex]
    print('    new edge '+ str(newEdgeIndex) + ': '+ str(newEdge) + ' with rel position '+ str(newAlongIndex) + ' -> ' + str(newAlongPos))
    
    # new pos
    newPos = ([newEdge[1],newAlongPos],[newAlongPos,newEdge[1]])[newAlong == 'Y']
    print('    new pos: '+ str(newPos))
    
    # new dir (always inward-facing)
    if newAlong == 'X':
        newDir = ('U','D')[(newEdge[1] % edgeLength) == 0]
    else: # newAlong == 'Y'
        newDir = ('L','R')[(newEdge[1] % edgeLength) == 0]
    print('    new dir: ' + newDir)
        
    return [newPos[0], newPos[1], newDir]

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
            print('   first pos on new face is a wall : return previous posDir: '+ str(prevPosDir))
            return prevPosDir
        
        curPosDir = [newPosSteps[0], newPosSteps[1], curPosDir[2]]
        remSteps = newPosSteps[2]
        
        # else, if remSteps = 0: return new posdir
        if  remSteps == 0:
            return curPosDir
        
        # if there are still steps remaining: 
        # find position and direction on next face and repeat
        prevPosDir = [i for i in curPosDir]
        curPosDir = switchFace(curPosDir)
        remSteps -= 1
    
def getPath(posDirA, posDirB):
    # return an array of coordinates from pos a to pos b with direction per coordinate
    # in format [Y, X, Dir]
    print('  posDirA: '+ str(posDirA))
    print('  posDirB: '+ str(posDirB))
    pos = [i for i in posDirA[0:2]]
    dir = posDirA[2]
    coor = [[pos[0], pos[1], dir]]
    goalPos = posDirB[0:2]
    
    sliceLine = (posDirA[1],posDirA[0])[dir in 'RL']
    slice = mapSlice(dir, sliceLine, False)
    
    while(pos != goalPos):
        posMatter = (pos[0],pos[1])[dir in 'RL']
        isEdgePos = ((dir in 'DR') & ((slice + ' ')[posMatter+1] == ' ')) | \
                    ((dir in 'LU') & ((' ' + slice)[posMatter] == ' '))
                    
        if isEdgePos:
            print('    - edgePosDir while drawing: ' + str([pos[0],pos[1],dir]) + ' with posMatter: '+ str(posMatter))
            newPosDir = switchFace([pos[0],pos[1],dir])
            pos = newPosDir[0:2]
            dir = newPosDir[2]
            sliceLine = (pos[1],pos[0])[dir in 'RL']
            slice = mapSlice(dir, sliceLine, False)
        else:
            if dir == 'R':    pos = [pos[0],   pos[1]+1]
            if dir == 'L':    pos = [pos[0],   pos[1]-1]
            if dir == 'D':    pos = [pos[0]+1, pos[1]  ]
            if dir == 'U':    pos = [pos[0]-1, pos[1]  ]

        coor.append([pos[0], pos[1], dir])
    return coor

def drawOnMap(posDir1, posDir2):
    print(' ----- drawing logic ------')
    global drawMap
    signDict = {'R':'>','L':'<','D':'v','U':'^'}
    
    drawPath = getPath(posDir1, posDir2)
    for co in drawPath:
        sign = signDict[co[2]]
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
Ylen = len(map)
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
for trIndex in range(0,len(trace)):
    tr = (trace[trIndex], [firstTurn,trace[0][1]])[trIndex == 0]
    
    print('trace ' + str(trIndex+1) + ": " + str(tr))
    nextPosDir = newPosDir(posDir, tr)
    drawOnMap([posDir[0],posDir[1],turn(posDir[2],tr[0])], nextPosDir)
    posDir = nextPosDir
    print(' new posDir: ' + str(posDir)) 

writeFile('drawmap_'+ str(part) +'.txt', '\n'.join(drawMap))
print('final position and direction: ' + str(posDir))
finalPassword = 1000*(posDir[0]+1) + 4*(posDir[1]+1) + directions.find(posDir[2])
print('final password: (1000*'+ str(posDir[0]+1) + ') + (4*' + str(posDir[1]+1) + ") + ("+ posDir[2] + " -> " +  str( directions.find(posDir[2])) + ') = ' + str(finalPassword))