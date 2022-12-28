import numpy as np
import re

# functions
def readFile(fName):
    inStream = open(fName,'r')
    out = inStream.read()
    inStream.close()
    return out

def prints(list1):
    for l in list1: print(l)

# params
fileName = 'snafu.txt'

# parse
input = readFile(fileName).split('\n')

# reverse strings -> start at lowest index (and split to list)
snafu = [list(i[::-1]) for i in input]
prints(snafu[0:3])

# replace -/= by -1/-2 and cast to int
for s in range(0,len(snafu)):
    snafu[s] = [((i,-2)[i=='='],-1)[i=='-'] for i in snafu[s]]
    snafu[s] = [int(i) for i in snafu[s]]
prints(snafu[0:3])
