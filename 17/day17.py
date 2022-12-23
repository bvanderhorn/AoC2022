# functions
def mapp(predicate, iterable): return list(map(predicate,iterable))
def xmin(rock): return min(mapp(lambda r: r[0],rock))
def ymin(rock): return min(mapp(lambda r: r[1],rock))
def xmax(rock): return max(mapp(lambda r: r[0],rock))
def ymax(rock): return max(mapp(lambda r: r[1],rock))
def down(rock): return mapp(lambda r:[r[0],r[1]-1],rock)
def left(rock): return mapp(lambda r:[r[0]-1,r[1]],rock)
def right(rock): return mapp(lambda r:[r[0]+1,r[1]],rock)
def overlapsWithSolid(rock): return len([i for i in rock if i in solid]) > 0
def outOfBounds(rock): return (xmin(rock) < xMin) | (xmax(rock) > xMax) | (ymin(rock) < 0) | overlapsWithSolid(rock)

def deltas(array1):
    deltas = []
    i0 = 0
    for i in array1: 
        deltas.append(i-i0)
        i0=i
    return deltas

def readFile(fName):
    inStream = open(fName,'r')
    out = inStream.read()
    inStream.close()
    return out

def writeFile(fName,outString):
    outStream = open(fName,'w')
    outStream.write(outString)
    outStream.close()

def paint(rock,walls=False):
    canvas = ''
    for y in range(ymax(rock),-1, -1):
        line = ('','|')[walls]
        for x in range(0,(xmax(rock)+1, 7)[walls]):
            line += ('.', '#')[[x,y] in rock]
        line += ('','|')[walls] + '\n'
        canvas += line
    canvas += ('','+-------+')[walls]
    return canvas

def shortestPath(fr,to,fieldArray):
    # applies Dijkstra to find a shortest path between two points in the solid
    inf = 10000000000
    dist = [[index,(inf,0)[el==fr]] for index, el in enumerate(fieldArray)]
    visited = []
    
    def getNearestUnvisited():
        unvisited = [i for i in dist if i[0] not in visited]
        return sorted(unvisited, key=lambda u: u[1])[0]
    
    def neighbours(slab) :
        nb = []
        potentialNb = [
            [slab[0]-1,slab[1]],
            [slab[0]+1,slab[1]],
            [slab[0],slab[1]-1],
            [slab[0],slab[1]+1]
        ]
        for pn in potentialNb:
            if pn in fieldArray: nb.append(pn)
        return nb
    
    for dummy in range(0,len(dist)):
        curDist = getNearestUnvisited()
        curSolid = fieldArray[curDist[0]]
        if curSolid == to:
            return curDist[1]
        for n in neighbours(curSolid):
            nIndex = fieldArray.index(n)
            nDist = [i for i in dist if i[0] == nIndex][0]
            newDist = curDist[1]+1
            if nDist[1] > newDist:
                dist[dist.index(nDist)][1] = newDist
        visited.append(curDist[0])
     
# parse
gas = readFile('gas.txt')
rocks = [
    [[0,0],[1,0],[2,0],[3,0] ],
    [[1,0],[0,1],[1,1],[2,1],[1,2]],
    [[0,0],[1,0],[2,0],[2,1],[2,2]],
    [[0,0],[0,1],[0,2],[0,3]],
    [[0,0],[1,0],[0,1],[1,1]]
]
for rock in rocks:
    print(paint(rock,False))
    print('')

# params
part = 2
nofRocks1 = 2022
nofRocks2 = 10000
nofRocks2Real = 1000000000000
xMin = 0
xMax = 6
l = '<'
r = '>'
startHeight = 3

# run
nofRocks = (nofRocks1,nofRocks2)[part == 2]
height = 0
choppedHeight = 0
jetIndex = 0
solid = []
jet0rocks = []
jet0heights = []
for r in range(0,nofRocks):
    # appear
    rockIndex = r % len(rocks)
    rock = rocks[rockIndex]
    rock = mapp(lambda i: [i[0]+2,i[1]+height+startHeight],rock)
    
    # fall
    fallsteps = 0
    while(True):
        # jet
        jet = gas[jetIndex:jetIndex+1]
        jetIndex = (jetIndex+1,0)[jetIndex==(len(gas)-1)]
        newRock = (right(rock),left(rock))[jet==l]
        rock = (newRock, rock)[outOfBounds(newRock)]
        
        if jetIndex == 0: 
            jet0rocks.append(r)
            jet0heights.append(height + choppedHeight)
            print("jet reset, rock " + str(r) + " with index "+ str(rockIndex) +", steps after appearance: "+ str(fallsteps))
        fallsteps +=1
        
        # drop
        newRock = down(rock)
        if (outOfBounds(newRock)):
            # solidify and continue
            solid += rock
            break
        else:
            rock = newRock        
    height = ymax(solid) + 1
    if (r % round(nofRocks/100) ) == 0: print(str(round(r/nofRocks*100,2)) + '% done')
    
    # every 100 drops: find highest solid chain, drop all solid coordinates below
    if (r % 100 == 0) & (len(solid) > 0):
        lefties = [i for i in solid if i[0]==xMin]
        righties = [i for i in solid if i[0]==xMax]
        if (len(lefties) > 0) & (len(righties) > 0):
            # calculate highest unbroken chain
            hLeft = sorted(lefties, key=lambda s: s[1], reverse=True)[0]
            hRight = sorted(righties, key=lambda s: s[1], reverse=True)[0]
            sp = shortestPath(hLeft, hRight,solid)
            yLowest = min([hLeft[1],hRight[1]])
            yHighest = max([hLeft[1],hRight[1]])
            yUnderLowest = round((sp-(xMax - xMin)-(yHighest-yLowest))/2)+1
            newYMin = yLowest - yUnderLowest
            
            # chop
            solid = [[s[0],s[1]-newYMin] for s in solid if s[1] >= newYMin]
            choppedHeight += newYMin
            height -= newYMin
            
            # print('highest left: ' + str(hLeft) + ", highest right: " + str(hRight) + ", shortest path: " + str(sp) + ", yDown: " + str(yUnderLowest) + ", newYMin: " + str(newYMin))

# draw solid to check
print('')
print("height: " + str(height) + ", chopped height: " + str(choppedHeight) + ", total: " + str(height + choppedHeight))
picture = paint(solid,True)
writeFile('solid.txt',picture)

print("jet0 rocks: " + str(jet0rocks))
deltaRocks = deltas(jet0rocks)
print(" delta rocks: "+ str(deltaRocks))
print("Part 2 end rock: ("+ str(nofRocks2Real) + " - "+ str(deltaRocks[0]) + ") % "+ str(deltaRocks[1]) + " = " + str((nofRocks2Real - deltaRocks[0]) % deltaRocks[1]))

print("jet0 heights: " + str(jet0heights))
deltaHeights = deltas(jet0heights)
print(" delta heights: "+ str(deltaHeights))
print('')