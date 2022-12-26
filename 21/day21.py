import numpy as np
import re

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

def getMonkey(monkeyName):
    return [m for m in monkeys if m[0] == monkeyName][0]

def getMonkeyIndex(monkeyName):
    return [i for (i,m) in enumerate(monkeys) if m[0] == monkeyName][0]

def evaluate(monkeyName, extend, depth):
    monkey = getMonkey(monkeyName)
    print2(" "*depth + " evaluate " + monkeyName + ": " + monkey[1])
    name = monkey[0]
    equate = monkey[1]
    equationMatch = re.match("(\w+) \W (\w+)",equate)
    intMatch = re.match("^\d+$",equate)
    out = ""
    if (monkeyName == human) & extend: 
        print2(" "*depth + "  --> return " + human)
        return human
    elif (intMatch != None):
        return equate
    else:
        m1 = equationMatch.group(1)
        m2 = equationMatch.group(2)
        equate = equate.replace(m1,evaluate(m1,extend,depth+1)).replace(m2,evaluate(m2,extend,depth+1))
        
    print2(" "*depth + " returning " + monkeyName + ": " + equate)
    if extend:
        return "("+ equate +")"
    else:
        return(str(eval(out)))

# params
fileName = 'monkeys.txt'
human = 'humn'
root = 'root'
test = False

# parse
input = readFile(fileName).split('\n')
monkeys = []
for i in range(0,len(input)):
    monkeyMatch = re.match("^(\w+): ([\s\S]+)$",input[i])
    monkeys.append(list(monkeyMatch.group(1,2)))

# part 1
# print(evaluate(root))

# part 2
# update root equation
rootMonkey = getMonkey(root)
rootOriginalOperation = re.match("\w+ (\W) \w+",rootMonkey[1]).group(1)
monkeys[getMonkeyIndex(root)][1] = rootMonkey[1].replace(rootOriginalOperation, "=")
print(monkeys[getMonkeyIndex(root)])

rootEvaluation = evaluate(root,True,0)
print(rootEvaluation)
writeFile('rootEval.txt',rootEvaluation)