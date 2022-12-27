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

def moveLeft(inList, amount):
    return inList[amount:] + inList[:amount]

def checkPositions(pos, round):
    # returns a list of 4 x 3 positions an elf on position 'pos' should check in that order
    # if for a given sublist of 3 positions no other elf is present, planPos should become
    # the middle of that subset
    # all positions are in [Y (down), X (left)]
    North = [
        [pos[0]-1,pos[1]-1],
        [pos[0]-1,pos[1]  ],
        [pos[0]-1,pos[1]+1]
    ]
    South = [
        [pos[0]+1,pos[1]-1],
        [pos[0]+1,pos[1]  ],
        [pos[0]+1,pos[1]+1]
    ]
    West = [
        [pos[0]-1,pos[1]-1],
        [pos[0],  pos[1]-1],
        [pos[0]+1,pos[1]-1]
    ]
    East = [
        [pos[0]-1,pos[1]+1],
        [pos[0],  pos[1]+1],
        [pos[0]+1,pos[1]+1]
    ]
    checkPos = [North, South, West, East]
    return moveLeft(checkPos, round % len(checkPos))

def aroundPositions(pos):
    return [
        [pos[0]-1,pos[1]-1],
        [pos[0]-1,pos[1]  ],
        [pos[0]-1,pos[1]+1],
        [pos[0],  pos[1]-1],
        [pos[0]  ,pos[1]+1],
        [pos[0]+1,pos[1]-1],
        [pos[0]+1,pos[1]  ],
        [pos[0]+1,pos[1]+1],
    ]

def planPosition(curPos, round, allPositions):
    aroundPos = aroundPositions(curPos)
    checkPos = checkPositions(curPos, round)
    
    # if all around is empty: stay where you are
    isEmptyAround = [i for i in aroundPos if i in allPositions]
    if len(isEmptyAround) == 0: 
        return [i for i in curPos]
    
    # check all 4 directions and move to the middle one if all three are empty
    for dir in checkPos:
        emptyInDirection = [i for i in dir if i in allPositions]
        if len(emptyInDirection) == 0:
            return dir[1]
    
    # else: everything is blocked, stay where you are
    return [i for i in curPos]

# params
fileName = 'elves.txt'

# parse
input = readFile(fileName).split('\n')
startPositions = []
for i in range(0,len(input)):
    startPositions += [[i, m.start()] for m in re.finditer('#',input[i])]
print("number of elves: " + str(len(startPositions)))

# run
positions = [i for i in startPositions]
for round in range(0,10):
    print('round '+ str(round) + '...')
    pp = [planPosition(p,round,positions) for p in positions]
    
    # new positions: if planned occurs at least twice, stay where you are
    ppDoubles = [x for x in pp if pp.count(x) > 1]
    positions = [(pp[i],positions[i])[pp[i] in ppDoubles] for i in range(0,len(positions))]

# draw and calculate
xMin = min([i[1] for i in positions])
yMin = min([i[0] for i in positions])

# for drawing and ease of calculation: subtract xMin and yMin from each position
finalPositions = [[i[0]-yMin, i[1]-xMin] for i in positions]
xMax = max([i[1] for i in finalPositions])
yMax = max([i[0] for i in finalPositions])

for line in range(0,yMax+1):
    xPosInLine = [p[1] for p in finalPositions if p[0] == line]
    lineString = ''.join([('.','#')[i in xPosInLine] for i in range(0,xMax+1)])
    print(lineString)

nofSpaces = (yMax+1)*(xMax+1) - len(startPositions)
print(' number of spaces: '+ str(nofSpaces))
