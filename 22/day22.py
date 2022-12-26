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

def print1(inString): 
    if test1: print(inString)
    
def print2(inString):
    # global runlog
    if test2:
        print(inString)
        # runlog.append(inString)
        
def printmap(mapIn, fromRow, toRow, fromCol, toCol):
    for row in mapIn[fromRow-1: toRow]:
        print(row[fromCol-1: toCol])

# params
fileName = 'mapandtrace.txt'
human = 'humn'
root = 'root'
test1 = False
test2 = True
part: int = 1

# parse
input = readFile(fileName).split('\n\n')
map = input[0].split('\n')
trace = input[1]
printmap(map,1,2,1,len(map[0]))
printmap(map,90,110,40,60)
print(trace)