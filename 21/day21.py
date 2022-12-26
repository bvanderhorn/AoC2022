import numpy as np
import json
import re

# functions
def readFile(fName):
    inStream = open(fName,'r')
    out = inStream.read()
    inStream.close()
    return out

def evaluate(monkeyName):
    monkey = [m for m in monkeys if m[0] == monkeyName][0]
    name = monkey[0]
    equate = monkey[1]
    equationMatch = re.match("(\w+) \W (\w+)",equate)
    intMatch = re.match("^\d+$",equate)
    if (intMatch != None):
        return equate
    else:
        m1 = equationMatch.group(1)
        m2 = equationMatch.group(2)
        equate = equate.replace(m1,evaluate(m1)).replace(m2,evaluate(m2))
    return str(eval(equate))

# params
fileName = 'monkeys.txt'

# parse
input = readFile(fileName).split('\n')
monkeys = []
for i in range(0,len(input)):
    monkeyMatch = re.match("^(\w+): ([\s\S]+)$",input[i])
    monkeys.append(list(monkeyMatch.group(1,2)))

print(evaluate('root'))
