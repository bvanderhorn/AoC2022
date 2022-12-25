import numpy as np
import re
import json
import timeit
import time

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
    # substract robot costs from current assets
    newAssets = list(np.subtract(assets, blueprint[robot]))
    
    # find out how many rounds we need to afford the robot (and add a round to build the robot)
    if all(j>=0 for j in newAssets):
        rounds = 1
    else:
        robotsCheck = [i for i in robots if i > 0]
        newAssetsCheck = newAssets[0:len(robotsCheck)]
        rounds = -int(min(np.floor(np.divide(newAssetsCheck,robotsCheck)))) + 1
        
    # add gathered assets in those rounds
    newAssets = list(np.add(newAssets, np.multiply(robots,rounds)))
    
    # return result
    newRemaining = remaining - rounds
    newRobots = [n for n in robots]
    newRobots[robot] += 1
    return [newRobots, newAssets, newRemaining]
            
def getMaxWithRemaining(blueprint, robots, assets, remaining, depth, path ):
    # blueprint, robots and assets are 4x1 arrays in format [ore, clay, obsidian, geode]
    global maxAssets
    global earliestGeodeRobots
    mins = minutes-remaining+1
    scores = []
     # if it's been more than the current global earliest minute at which you could have finished a first geode 
    # robot, and you haven't: just forget about this branch
    if robots[3] == len(earliestGeodeRobots):
        print('forgot to update earliest geode robots: '+ str(earliestGeodeRobots) + ", but nof geode robots is "+ str(robots[3]))
    if mins > (earliestGeodeRobots[robots[3]]+ 1):
        return scores
            
    for r in range(len(blueprint)-1, -1,-1):
        if (r>0) & (robots[r-1] == 0):
            # if you have robots ore and clay (1,2), you can build robots ore, clay and obs (1,2,3)
            continue
            
        next = getRobot(blueprint, robots, assets, remaining, r)
        if ((r == 3) & (next[2] > 0)) | (next[2] > 1) :
            # only consider this alternative if building this robot actually leaves some harvest time after.
            # building a non-geode robot only makes sense if you have at least the time left to build another geode robot after
            creationMinute = minutes-next[2]
            
            if (r == 3) & ( earliestGeodeRobots[robots[3]] > creationMinute):
                # if you have the assets to make a geode robot, and it is quicker than you could before: save this minute
                earliestGeodeRobots[robots[3]] = creationMinute
                if robots[3] == (len(earliestGeodeRobots) -1):
                    earliestGeodeRobots.append(minutes+1)
                print(" updated geode robot " + str(robots[3]) + " creation minimum: "+str(earliestGeodeRobots))
                
            sc = getMaxWithRemaining(blueprint, next[0],next[1],next[2], depth + 1, [i for i in path] + [[r, next[2]]])
            if len(sc) > 0:
                scores.append(sc[0])
                if (r==len(blueprint)-1) & (next[2]== (remaining-1)):
                    # if it is possible to build a geode robot this very minute: don't consider alternatives, build the geode robot!
                    break
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

for bpi in range(0,2):
    start = timeit.default_timer()
    
    print("blueprint " + str(bpi+1) + ": " + str(blueprints[bpi]))
    bplog = []
    bp = blueprints[bpi]
    maxAssets = [0,0,0,0]
    earliestGeodeRobots = [minutes+1]
    sc = getMaxWithRemaining(bp, mainRobots, mainAssets, minutes, 0, [])
    mainScores.append(sc[0])
    
    stop = timeit.default_timer()
    runTime = time.strftime('%H:%M:%S', time.gmtime(stop - start))
    print("runtime blueprint " + str(bpi+1) + ": " + runTime)
    
    
qualityLevels = list(np.multiply(mainScores,[i+1 for i in range(0, len(mainScores))]))
print('')
print(" scores: " + str(mainScores))
print(" quality levels: " + str(qualityLevels))
print(" sum: " + str(sum(qualityLevels)))
print(' product of scores: ' + str(np.prod(mainScores)))

