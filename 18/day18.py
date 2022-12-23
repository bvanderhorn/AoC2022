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

print(' total free sides: ' + str(len(cubes)*6 - nofTouches*2))
    