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
        
def printmap(mapIn, fromRow, toRow, fromCol, toCol):
    for row in mapIn[fromRow-1: toRow]:
        print(row[fromCol-1: toCol])
        
def mapSlice(direction, line):
    # return a list of characters along given direction
    if direction in 'RL':  return list(map[line])
    else:  return [i[line] for i in map]
    
def turn(curDir, lr):
    curIndex = directions.find(curDir)
    newIndex = curIndex + (-1,1)[lr=='R']
    return directions[newIndex % (len(directions))]

def endPos(slice, startPos, maxSteps):
    nonEmptySlice = [s for s in slice if s != ' ']
    firstNonEmpty = [i for (i,s) in enumerate(slice) if s != ' '][0]
    
    # correct for instructions that suggest more steps than the non-empty slice length
    steps = maxSteps % len(nonEmptySlice)
    
    # take a subslice starting from startPos to the end of the slice to check where we're going
    firstSlice = slice[startPos:startPos+steps+1]
    
    # 1. check if we hit a wall
    e = enumerate(firstSlice)
    walls1 = [i for (i,s) in e if s == '#']
    if len(walls1) > 0:
        # we hit a wall: return last index before we hit the wall
        return startPos + (walls1[0] -1)
    
    # 2. check if we ran out of the map
    ends1 = [i for (i,s) in e if s == ' ']
    if len(ends1) == 0:
        # we did not run out of the map: return new position
        return startPos + steps
    
    # still here means we ran out of the map: 
    # record last position before end of map and continue
    lastPos = startPos + (ends1[0] -1)
    remSteps = steps - lastPos - 1 
    # with the '-1', we are already circling towards the first non-empty character of the slice
    
    # if the first non-empty character of the slice is a wall: return lastPos
    if nonEmptySlice[0] == '#':
        return lastPos
    
    # we are now on the first non-empty character of the slice, which is NOT a wall
    # we can also not run into the empty anymore, thanks to the modulo at the start    
    # continue search with another sub slice
    secondSlice = nonEmptySlice(0,remSteps + 1)
    walls2 = [i for (i,s) in enumerate(secondSlice) if s == '#']
    if len(walls2) > 0:
        # indeed we ran into a wall!
        return firstNonEmpty + (walls2[0] -1)
    
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
        ms = list(reversed(ms))
        startIndex = (mapLength -1) - startIndex
        
    # find 1-D end position
    endIndex = endPos(ms,startIndex,int(instruction[1]))
    
    # if direction is UP or LEFT, we need to revert the result back
    if newDir in 'LU':
        endIndex = (mapLength -1) - endIndex
        
    # ... and we can return!
    if newDir in 'RL':
        return [oldPosDir[0], endIndex, newDir]
    else:
        return [endIndex, oldPosDir[1], newDir]


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
map = input[0].split('\n')
trace = re.findall("(^|\D)(\d+)",input[1])

# some visual checking
printmap(map,1,2,1,len(map[0]))
printmap(map,90,110,40,60)
print(trace[0:10])
print(trace[0:10][0][1])
print(' total instructions: '+ str(len(trace)))

# part 1
startCol = map[0].find('.')
posDir = [startRow, startCol,firstDir]
print('initial posDir: ' + str(posDir))
for trIndex in range(0,2):
    tr = (trace[trIndex], [firstTurn,trace[0][1]])[trIndex == 0]
    
    print('trace ' + str(trIndex+1) + ": " + str(tr))
    posDir = newPosDir(posDir, tr)
    print(' new posDir: ' + str(posDir))
    
    
print('final position and direction: ' + str(posDir))