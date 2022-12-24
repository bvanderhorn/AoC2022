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
    
def getMaxWithRemaining(blueprint, robots, assets, remaining):
    # blueprint, robots and assets are 4x1 arrays in format [ore, clay, obsidian, geode]
    scores = []
    depth = minutes - remaining + 1
    print(" "*depth + "min "+ str(depth) + ":")
    print(" "*(depth+1) + "assets: "+ str(assets))
    if remaining == 0:
        print(" "*(depth+1) + "-END-")
        return scores

    # build one of the 4 robots or skip and just gather
    for r in range(0,len(blueprint)+1):
        if (r < len(blueprint)) :
            # try to build a robot
            rob = blueprint[r]
            lessAssets = list(np.subtract(assets, rob))
            if all(i >= 0 for i in lessAssets):
                print(" "*(depth+1) + "build robot " + str(r))
                # build robot
                moreRobots = robots
                moreRobots[r] += 1
                # add assets
                newAssets = list(np.add(lessAssets, robots)) 
                # recurse
                sc = getMaxWithRemaining(blueprint, moreRobots, newAssets, remaining-1)
                # add obsidian to score if building the robot helped
                if len(sc) > 0:
                    scores.append(sc[0])
                    print(" "*(depth+1) + "add score "+ str(sc[0]))
                
        else:           
            # don't build any robot, just gather assets
            newAssets = list(np.add(assets, robots))   
            print(" "*(depth+1) + "don't build robot")
            print(" "*(depth+1) + "new assets: "+ str(newAssets))         
            # recurse
            sc = getMaxWithRemaining(blueprint, robots, newAssets, remaining -1)
            # add obsidian to score
            if len(sc) > 0:
                print(" "*(depth+1) + "add new score "+ str(sc[0]))
                scores.append(sc[0]) 
            else :
                print(" "*(depth+1) + "add current score "+ str(assets[3]))
                scores.append(assets[3])
                
    # sort and return
    return sorted(scores, reverse=True) 
    
# parse
input = readFile('blueprints.txt')
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
# print(json.dumps(blueprints, indent=4))

# params
minutes = 24

# cycle over all blueprints and get max score
scores = []
robots = [1,0,0,0]
assets = [0,0,0,0]
for bp in [blueprints[0]]:
    sc = getMaxWithRemaining(bp, robots, assets, minutes)
    if len(sc) > 0:
        scores.append(sc[0])
scores = sorted(scores, reverse=True)

print(scores)