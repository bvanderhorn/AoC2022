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
nofRocks = 2022
xMin = 0
xMax = 6
l = '<'
r = '>'
startHeight = 3

# run
height = 0
jetIndex = 0
solid = []
for r in range(0,nofRocks):
    # appear
    rock = rocks[r % len(rocks)]
    rock = mapp(lambda i: [i[0]+2,i[1]+height+startHeight],rock)
    
    # fall
    while(True):
        # jet
        jet = gas[jetIndex:jetIndex+1]
        jetIndex = (jetIndex+1,0)[jetIndex==(len(gas)-1)]
        newRock = (right(rock),left(rock))[jet==l]
        rock = (newRock, rock)[outOfBounds(newRock)]
        
        # drop
        newRock = down(rock)
        if (outOfBounds(newRock)):
            # solidify and continue
            solid += rock
            break
        else:
            rock = newRock        
    height = ymax(solid) + 1
    if r % round(nofRocks/100) == 0: print(str(round(r/nofRocks*100,1)) + '% done')

# draw solid to check
print('')
print("height: " + str(height))
picture = paint(solid,True)
writeFile('solid.txt',picture)