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

def getRobot(blueprint, robots, assets, remaining, robot):
    robotCost = blueprint[robot]
    newAssets = list(np.subtract(assets, robotCost))
    i=0
    while(True):
        newAssets = list(np.add(newAssets, robots))
        i += 1
        if all(j>=0 for j in newAssets): break

    newRemaining = remaining - i
    newRobots = [n for n in robots]
    newRobots[robot] += 1
    return [newRobots, newAssets, newRemaining]
            
def getMaxWithRemaining(blueprint, robots, assets, remaining, depth, path ):
    # blueprint, robots and assets are 4x1 arrays in format [ore, clay, obsidian, geode]
    global maxAssets
    global earliestFirstGeodeRobotAtMinute
    mins = minutes-remaining+1
    scores = []
     # if it's been more than the current global earliest minute at which you could have finished a first geode 
    # robot, and you haven't: just forget about this branch
    if (mins > earliestFirstGeodeRobotAtMinute+ 1) & (assets[3] == 0):
        return scores
    
    # if you have robots ore and clay (1,2), you can build robots ore, clay and obs (1,2,3)
    emptyRobots = [i for i, x in enumerate(robots) if x==0]
    if len(emptyRobots) > 0:  firstEmptyRobot = emptyRobots[0]
    else: firstEmptyRobot = 3
    # print(" "*d + " min "+ str(minutes-remaining+1)+ ","+ " up to robot: "+ str(firstEmptyRobot+1))
        
    for r in range(firstEmptyRobot, -1,-1):
        # print(" "*(d+1) + " build robot " + str(r) )
        next = getRobot(blueprint, robots, assets, remaining, r)
        if next[2] > 0 :
            sc = getMaxWithRemaining(blueprint, next[0],next[1],next[2], depth + 1, [i for i in path] + [[r, next[2]]])
            scores.append(sc[0])
            if (r == len(blueprint)) & ((minutes-next[2]+1) < earliestFirstGeodeRobotAtMinute):
                    # if you have the assets to make a geode robot:
                    # save this minute if it is smaller than the previous earliest minute
                    print(" could create first geode robot already at minute "+str((minutes-next[2]+1)) + "!")
                    earliestFirstGeodeRobotAtMinute = (minutes-next[2]+1)
    if len(scores) == 0:
        newAssets = list(np.add(assets, np.multiply(robots, remaining)))
        if newAssets[3] > maxAssets[3]:
            maxAssets = [i for i in newAssets]
            print(" new max assets: " + str(maxAssets))
            print("  path: "+ str(path))
        scores.append(assets[3] + robots[3]*remaining)
    return sorted(scores, reverse = True)
    
# parse
input = readFile('example_blueprints.txt')
blueprintStrings = input.split('\n')
blueprints = []
for bs in blueprintStrings:
    m = re.match("^\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+$",bs)
    blueprints.append([int(i) for i in m.group(1,2,3,4,5,6,7)])

# refactor blueprints to [4x[4x1]] arrays in format [ore, clay, obsidian, geode]
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

for bpi in range(0, 1):
    print("blueprint " + str(bpi+1) + ": " + str(blueprints[bpi]))
    bplog = []
    bp = blueprints[bpi]
    maxAssets = [0,0,0,0]
    earliestFirstGeodeRobotAtMinute = minutes+1
    sc = getMaxWithRemaining(bp, mainRobots, mainAssets, minutes, 0, [])
    mainScores.append(sc[0])
    
qualityLevels = list(np.multiply(mainScores,[i+1 for i in range(0, len(mainScores))]))

print(" scores: " + str(mainScores))
print(" quality levels: " + str(qualityLevels))
print(" sum: " + str(sum(qualityLevels)))

