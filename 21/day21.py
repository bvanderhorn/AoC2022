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

def equationComponents(equation):
    return list(re.match("(\w+) (\W) (\w+)",equation).group(1,2,3))

def getComponents(monkey):
    return equationComponents(monkey[1])
    
def getUsedInMonkey(monkeyName):
    return [m for m in monkeys if monkeyName in m[1]][0]

def getMonkey(monkeyName):
    return [m for m in monkeys if m[0] == monkeyName][0]

def rewrite(monkeyName, usedInMonkey):
    components = getComponents(usedInMonkey)
    operator = components[1]
    main = usedInMonkey[0]
    left = components[0]
    right = components[2]
    notMonkey = (left,right)[monkeyName==left]
    
    if operator == '+':
        return main + " - " + notMonkey
    if operator == '-':
        if left == monkeyName:
            return main + ' + ' + notMonkey
        else:
            return notMonkey + ' - ' + main
    if operator == '*':
        return main + ' / ' + notMonkey
    if operator == '/':
        if left == monkeyName:
            return main + ' * ' + notMonkey
        else:
            return notMonkey + ' / ' + main
        

def getIndex(monkeyName):
    return [i for (i,m) in enumerate(monkeys) if m[0] == monkeyName][0]

def evaluate(monkeyName, extend = False, depth = 0):
    monkey = getMonkey(monkeyName)
    print2(" "*depth + " evaluate " + monkeyName + ": " + monkey[1])
    name = monkey[0]
    equate = monkey[1]
    equationMatch = re.match("(\w+) \W (\w+)",equate)
    intMatch = re.match("^\d+$",equate)
    if (monkeyName == human) & (part == 2): 
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
            return str(eval(equate))

def rewriteAndEvaluate(monkeyName):
    usedInMonkey = getUsedInMonkey(monkeyName)
    newEquation = rewrite(monkeyName, usedInMonkey)
    components = equationComponents(newEquation)
    leftMonkey = components[0]
    rightMonkey = components[2]
    for sub in [leftMonkey, rightMonkey]:
        if sub == notHumanHalf:
            value = notHumanHalfValue
        elif sub == usedInMonkey[1]:
            value = rewriteAndEvaluate(sub)
        else:
            value = evaluate(sub)
        newEquation = newEquation.replace(sub, value)
    return str(eval(newEquation))
    
    
# params
fileName = 'monkeys.txt'
human = 'humn'
root = 'root'
test = False
part: int = 2

# parse
input = readFile(fileName).split('\n')
monkeys = []
for i in range(0,len(input)):
    monkeyMatch = re.match("^(\w+): ([\s\S]+)$",input[i])
    monkeys.append(list(monkeyMatch.group(1,2)))

# part 1
if part == 1:
    print(evaluate(root))

# part 2
# update root equation
rootMonkey = getMonkey(root)
rootIndex = getIndex(root)
rootComponents = getComponents(rootMonkey)
monkeys[rootIndex][1] = rootMonkey[1].replace(rootComponents[1], "=")
print(monkeys[rootIndex])

# write full equation with only 'humn' written out
rootEvaluation = evaluate(root,True,0)
# print(rootEvaluation)
writeFile('rootEval.txt',rootEvaluation)

# evaluate left, right
rootHalfs = [rootComponents[0],rootComponents[2]]
print(" left: " + rootHalfs[0])
print(" right: " + rootHalfs[1])
for h in rootHalfs:
    try:
        notHumanHalfValue = evaluate(h)
        notHumanHalf = h
        print(' not-human half: ' + notHumanHalf + " = " + notHumanHalfValue)
    except:
        humanHalf = h
        print(' human half: ' + humanHalf)

# check if there are doubles ('abcd * abcd', 'defg / defg' etc.)
doubles = [m for m in [m0 for m0 in monkeys if re.match("\d+",m0[1]) is None] if getComponents(m)[0] == getComponents(m)[2]]
print(doubles)
# --> no doubles!

print(rewriteAndEvaluate(human))

