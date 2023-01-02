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

def print2(inString): 
    print(inString)

        
def getRobot(blueprint, robots, assets, remaining, robot):
    # subtract robot costs from current assets
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

def fancySort(state):
    # sort function to determine which state has the highest potential
    # sort by: # geode (1), obsidian (2), clay (3), ore (3) assets available
    return [-asset for asset in state[2][::-1]]

# params
part : int = 2
useExample = False   # use example
minutes = (24,32)[part==2]
N = 10              # number of highest potential branches to be evaluated every loop

# parse
input = readFile(('','example_')[useExample] + 'blueprints.txt')
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

# cycle over all blueprints and get max score
divider = "-"*90
maxStates = []
for bpi in range(0,(len(blueprints),3)[(not useExample) & (part == 2)]):
    # prep and alert
    start = timeit.default_timer()
    print2(divider + "\nblueprint " + str(bpi+1) + ": " + str(blueprints[bpi]) + "\n" + divider)

    # run a Dijkstra with smart sorting over the possibilities of this blueprint
    bp = blueprints[bpi]
    mainRobots = [1,0,0,0]
    mainAssets = [0,0,0,0]
    # todo is a list of states on THIS MINUTE that are starting points to further look into
    # each state is given in format: [blueprint, robots, assets, remaining]
    todo = [ 
        [bp, mainRobots, mainAssets, minutes]
    ]
    
    # todoAfter is a list of states on LATER MINUTES that we will look into once all 
    # interesting states on this minute have been investigated
    todoAfter = []
    
    # finalStates is a list of states after the final minute. If a state is evaluated and 
    # building either of the four robots is not possible anymore within the time remaining,
    # the final state is calculated and added to this list
    # in format [robots, assets]
    finalStates = []
    
    while (len(todo) > 0):
        current = todo.pop(0)
        robots = current[1]
        
        # get list of next robots that CAN be built 
        nextRobots = range(0,max([i for i,r in enumerate(robots) if r>0])+2)
        
        # convert to list of next possible states
        nextStates = [[bp] + getRobot(bp, robots, current[2], current[3], r) for r in nextRobots]
        
        # extract the states which may be added to the todoAfter list (all states with remaining > 0)
        toBeAddedStates = [s for s in nextStates if s[3] > 0]
        todoAfter += toBeAddedStates        
        
        # if no toBeAddedStates: calculate finalState of current state and add to finalStates
        if not toBeAddedStates:
            finalStates.append([robots, np.add(current[2], np.multiply(robots, current[3]))])
        
        # if todo is depleted and todoAfter is not empty: 
        # extract the ones with the lowest minute remaining, do a fancy sort and add the N ones 
        # with the highest potential to 'todo'
        if (not todo) and todoAfter:
            minMin = max([t[3] for t in todoAfter])
            # get the next set with highest remaining minutes
            todo = [t for t in todoAfter if t[3] == minMin]
            # apply fancy sort on assets
            todo.sort(key=lambda x: x[2])
            
            # only take the N highest potentials
            todo = todo[-N:]
            
            # extract new todos from todoAfter list
            todoAfter = [t for t in todoAfter if t[3] != minMin]
            
    # return the final state with highest geode score in finalStates
    maxState = [s for s in finalStates if s[1][3] == max([fs[1][3] for fs in finalStates])][0]
    maxStates.append(maxState)
    
    # post process and alert
    stop = timeit.default_timer()
    runTime = time.strftime('%H:%M:%S', time.gmtime(stop - start))
    print2(divider +"\nmax state: "+str(maxState) + "\nmax number of geodes: "+ str(maxState[1][3]) +"\nruntime blueprint " + str(bpi+1) + ": " + runTime + "\n" + divider)
    
# calculate end result
scores = [ms[1][3] for ms in maxStates]
qualityLevels = list(np.multiply(scores,[i+1 for i in range(0, len(scores))]))
print2("\n scores: " + str(scores))
print2(" quality levels: " + str(qualityLevels))
print2(" sum: " + str(sum(qualityLevels)))
print2(' product of scores: ' + str(np.prod(scores)))