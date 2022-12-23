# functions
def xmin(rock):
    return min(list(map(lambda r: r[0],rock)))
def ymin(rock):
    return min(list(map(lambda r: r[1],rock)))
def xmax(rock):
    return max(list(map(lambda r: r[0],rock)))
def ymax(rock):
    return max(list(map(lambda r: r[1],rock)))
def down(rock):
    return list(map(lambda r:[r[0],r[1]-1],rock))
def left(rock):
    return list(map(lambda r:[r[0]-1,r[1]],rock))
def right(rock):
    return list(map(lambda r:[r[0]+1,r[1]],rock))
def overlapsWithSolid(rock):
    return len([i for i in rock if i in solid]) > 0
def outOfBounds(rock):
    return (xmin(rock) < 0) | (xmax(rock) > 6) | (ymin(rock) < 0) | overlapsWithSolid(rock)
def combine(array1,array2):
    if len(array1) == 0:
        return array2
    elif len(array2) == 0:
        return array1
    else: 
        array1.extend(array2)
        return array1

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
inStream = open('gas.txt','r')
gas = inStream.read()
inStream.close()

# print(gas[0:1])
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
    rock = list(map(lambda i: [i[0]+2,i[1]+height+startHeight],rock))
    
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
            solid = combine(solid,rock)
            break
        else:
            rock = newRock        
    height = ymax(solid) + 1
    if r % round(nofRocks/100) == 0:
        print(str(round(r/nofRocks*100,1)) + '% done')
# draw solid to check
print('')
picture = paint(solid,True)
print("height: " + str(height))
outStream = open('solid.txt','w')
outStream.write(picture)
outStream.close()