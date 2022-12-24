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
    global bplog
    if test: 
        print(inString)
        bplog.append(inString)
    
def getMaxWithRemaining(blueprint, robots, assets, remaining):
    # blueprint, robots and assets are 4x1 arrays in format [ore, clay, obsidian, geode]
    global iterations
    global maxAssets
    global earliestFirstGeodeRobotAtMinute
    
    newRemaining = remaining - 1
    scores = []
    iterations += 1
    mins = (minutes - remaining + 1)
    depth = mins*2
    
    print2(" "*(depth+1) + "assets: "+ str(assets))
    print2(" "*(depth+1) + "robots: "+ str(robots))
    print2(" "*(depth) + "min "+ str(mins) + " (remaining after this: "+ str(newRemaining) + "):")
    
    # if it's been more than the current global earliest minute at which you could have finished a first geode 
    # robot, and you haven't: just forget about this branch
    if (mins > earliestFirstGeodeRobotAtMinute+ 1) & (assets[3] == 0):
        return scores
    
    # if it is impossible to build enough geode robots in the remaining time to pass the current max, 
    # just forget about this branch
    if (maxAssets[3] > assets[3] + robots[3]*remaining + sum(range(0,remaining))) :
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
                # print2(" "*(depth+2) + "with assets: "+ str(assets))
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
            if (r == len(blueprint)) & (mins < earliestFirstGeodeRobotAtMinute):
                # if you have the assets to make a geode robot:
                # save this minute if it is smaller than the previous earliest minute
                print(" could create first geode robot already at minute "+str(mins) + "!")
                earliestFirstGeodeRobotAtMinute = mins
            
            # add assets
            newAssets = list(np.add(tempNewAssets, robots)) 
            print2(" "*(depth+1) + "new assets: " + str(newAssets))
            print2(" "*(depth+1) + "new robots: " + str(newRobots))
            # recurse
            if newRemaining > 0:
                print2(" "*(depth+1) + "recurse")
                sc = getMaxWithRemaining(blueprint, newRobots, newAssets, newRemaining)
                # add obsidian to score if building the robot helped
                if len(sc) > 0:
                    scores.append(sc[0])
                    print2(" "*(depth+1) + "add score "+ str(sc[0]))
            else:
                finalAssets = list(np.add(assets ,robots))
                print2(" "*(depth+1) + "end: return last score: " + str(finalAssets[3]))
                scores.append(finalAssets[3])
                if finalAssets[3] > maxAssets[3]:
                    maxAssets = [i for i in finalAssets]
                    print(" new max assets: "+ str(maxAssets))
            
            if r == len(blueprint):
                # if you have the assets to make a geode robot: forget about alternatives for this strain
                break
        else:
            # if you tried to build a geode robot but couldn't but can build one with one more round of 
            # assets, forget about the alternatives and wait one round and build the geode robot
            if (r== len(blueprint)) & all(i >=0 for i in np.subtract(np.add(assets, robots),robotCost)):
                # skip everything, go straigt to gathering to build a geode robot next minute
                r = 0
    
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

for bpi in range(1, 2):
    print("blueprint: " + str(bpi+1))
    bplog = []
    bp = blueprints[bpi]
    maxAssets = [0,0,0,0]
    earliestFirstGeodeRobotAtMinute = minutes+1
    sc = getMaxWithRemaining(bp, mainRobots, mainAssets, minutes)
    if len(sc) > 0:
        mainScores.append(sc[0])
    if test: 
        writeFile('blueprint_'+str(bpi+1)+".txt",'\n'.join(bplog))
qualityLevels = list(np.multiply(mainScores,[i+1 for i in range(0, len(mainScores))]))

print(" scores: " + str(mainScores))
print(" quality levels: " + str(qualityLevels))
print(" sum: " + str(sum(qualityLevels)))

