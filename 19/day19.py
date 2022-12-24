import numpy as np
import re
import json

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

def print2(inString): 
    if test: print(inString)
    
def getMaxWithRemaining(blueprint, robots, assets, remaining):
    # blueprint, robots and assets are 4x1 arrays in format [ore, clay, obsidian, geode]
    scores = []
    global iterations
    global maxAssets
    iterations += 1
    mins = (minutes - remaining + 1)
    depth = mins*2
    print2(" "*(depth) + "min "+ str(mins) + " (remaining "+ str(remaining) + "):")
    # print2(" "*(depth+1) + "blueprint: "+ str(blueprint))
    print2(" "*(depth+1) + "assets: "+ str(assets))
    print2(" "*(depth+1) + "robots: "+ str(robots))
    if remaining == 0:
        print2(" "*(depth+1) + "-END-")
        return scores
        
    # build one of the 4 robots or build nothing
    for r in range(len(blueprint),-1,-1):
        tempNewAssets = []
        newRobots = []
        if (r > 0) :
            # try to build a robot
            robotCost = blueprint[r-1]
            lessAssets = list(np.subtract(assets, robotCost))
            if all(i >= 0 for i in lessAssets):
                print2(" "*(depth+1) + "build robot " + str(r) + " at cost " + str(robotCost))
                print2(" "*(depth+2) + "with remaining: " + str(remaining))
                print2(" "*(depth+2) + "with assets: "+ str(assets))
                # build robot
                newRobots = [i for i in robots]
                newRobots[r-1] += 1
                tempNewAssets = [i for i in lessAssets]
            else:
                print2(" "*(depth+1) + "could not build robot " + str(r))
        else:           
            # don't build any robot, just gather assets
            print2(" "*(depth+1) + "don't build robot")
            newRobots = [i for i in robots]
            tempNewAssets = [i for i in assets]
        
        if len(newRobots) > 0:
            # add assets
            newAssets = list(np.add(tempNewAssets, robots)) 
            # recurse
            if remaining > 1:
                print2(" "*(depth+1) + "recurse")
                sc = getMaxWithRemaining(blueprint, newRobots, newAssets, remaining-1)
                # add obsidian to score if building the robot helped
                if len(sc) > 0:
                    scores.append(sc[0])
                    print2(" "*(depth+1) + "add score "+ str(sc[0]))
            else:
                finalAssets = list(np.add(assets ,robots))
                print2(" "*(depth+1) + "end: return last score: " + str(finalAssets[3]))
                scores.append(finalAssets[3])
                if finalAssets[3] > maxAssets[3]:
                    maxAssets = finalAssets
                    print(" new max assets: "+ str(maxAssets))
            break
        else:
            if (r== len(blueprint)) & all(i >=0 for i in np.subtract(np.add(assets, robots),robotCost)):
                r = 0
                continue
    
    # print counter
    if mins == 3:
        print(" " + str(round(iterations/(minutes*(minutes-1)*(minutes-2))*100,2)) + "% done")
    
    # sort and return
    return sorted(scores, reverse=True) 
    
# parse
input = readFile('example_blueprints.txt')
blueprintStrings = input.split('\n')
blueprints = []
for bs in blueprintStrings:
    m = re.match("^\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+$",bs)
    blueprints.append([int(i) for i in m.group(1,2,3,4,5,6,7)])

# refactor blueprints [4x[4x1]] arrays in format [ore, clay, obsidian, geode]
blueprints = [
    [
        [bp[1],0,0,0],
        [bp[2],0,0,0],
        [bp[3],bp[4],0,0],
        [bp[5],0,bp[6],0]
    ] for bp in blueprints
]
# print2(json.dumps(blueprints, indent=4))

# params
minutes = 24
test = False
iterations = 0

# cycle over all blueprints and get max score
mainScores = []
mainRobots = [1,0,0,0]
mainAssets = [0,0,0,0]

for bpi in range(0, len(blueprints)):
    bp = blueprints[bpi]
    print("blueprint: " + str(bpi+1))
    maxAssets = [0,0,0,0]
    sc = getMaxWithRemaining(bp, mainRobots, mainAssets, minutes)
    if len(sc) > 0:
        mainScores.append(sc[0])

qualityLevels = list(np.multiply(mainScores,[i+1 for i in range(0, len(mainScores))]))

print(" scores: " + str(mainScores))
print(" quality levels: " + str(qualityLevels))
print(" sum: " + str(sum(qualityLevels)))

