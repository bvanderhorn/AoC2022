import numpy as np

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
    
def coordinates(line):
    spl = line.split(',')
    return [int(c) for c in spl]

def touch(cube1, cube2):
    return sum(np.abs(np.subtract(cube1, cube2))) == 1 

def uniqueNestedList(list1): return [list(y) for y in set([tuple(x) for x in list1])]
def getFreeNeighbours(c, cubes, upcoming, visited):
    adjacent = [
        [c[0],c[1],c[2]-1],
        [c[0],c[1],c[2]+1],
        [c[0],c[1]-1,c[2]],
        [c[0],c[1]+1,c[2]],
        [c[0]-1,c[1],c[2]],
        [c[0]+1,c[1],c[2]]
    ]
    return [a for a in adjacent if a not in (cubes + upcoming + visited) and 
            a[0]>=xMin and a[0]<=xMax and a[1]>=yMin and a[1]<=yMax and a[2]>=zMin and a[2]<=zMax]

# parse
input = readFile('cubes.txt')
cubeStrings = input.split('\n')
cubes = [coordinates(c) for c in cubeStrings]

# run
nofTouches = 0
for c in range(1,len(cubes)):
    prev = cubes[0:c]
    cube = cubes[c]
    nofTouches += len([i for i in prev if touch(i,cube)])

print(' cubes: '+ str(len(cubes)))
print(' touches: ' + str(nofTouches))
print(' total free sides: ' + str(len(cubes)*6 - nofTouches*2))

# part 2
xMin = min([c[0] for c in cubes])
xMax = max([c[0] for c in cubes])
yMin = min([c[1] for c in cubes])
yMax = max([c[1] for c in cubes])
zMin = min([c[2] for c in cubes])
zMax = max([c[2] for c in cubes])
print(" extremes: " + str([[xMin, xMax],[yMin,yMax],[zMin,zMax]]))

# find all free spaces which are adjacent to either of the extremities
borders = []
for i in range(xMin, xMax+1):
    borders += [[i,j,zMin] for j in range(yMin,yMax+1)]
    borders += [[i,j,zMax] for j in range(yMin,yMax+1)]
for j in range(yMin, yMax+1):
    borders += [[xMin,j,k] for k in range(zMin,zMax+1)]
    borders += [[xMax,j,k] for k in range(zMin,zMax+1)]
for k in range(zMin, zMax+1):
    borders += [[i,yMin,k] for i in range(xMin,xMax+1)]
    borders += [[i,yMax,k] for i in range(xMin,xMax+1)]

borders = [b for b in uniqueNestedList(borders) if b not in cubes]

visited = []
upcoming = borders
while (len(upcoming)>0):
    cur = upcoming.pop(0)
    upcoming += getFreeNeighbours(cur,cubes,upcoming, visited)
    visited.append(cur)

print(" free outside: " + str(len(visited)))
print(" trapped pockets: " + str((xMax-xMin+1)*(yMax-yMin+1)*(zMax-zMin+1) - len(cubes) - len(visited)))

all = []
for i in range(xMin,xMax+1):
    for j in range(xMin,xMax+1):
        all += [[i,j,k] for k in range(zMin,zMax+1)]

trapped = [i for i in all if i not in (visited + cubes)]
print(" trapped pockets located: " + str(len(trapped)))
print(trapped[0:10])

nofInsideSides = 0
for t in range(0,len(trapped)):
    nofInsideSides += len([i for i in cubes if touch(i,trapped[t])])

print(" nof inside sides: "+ str(nofInsideSides))
print(' total free outside sides: ' + str(len(cubes)*6 - nofTouches*2 - nofInsideSides))
    