from Container import *
from Node import *

def rfileUpdate(status, manifest, temprows, buffer, onloadList, moves, currMove):
    file = open('devlog/recovery.txt', 'w+')
    file.write(str(status) + "\n")
    file.write(str(manifest) + "\n")
    if (temprows):
        file.write("TEMPROWS\n")
        for container in temprows:
            file.write(repr(container)+"\n")
    if (buffer):
        file.write("BUFFER\n")
        for container in buffer:
            file.write(repr(container)+"\n")
    if (onloadList):
        file.write("ONLOAD\n")
        for container in onloadList:
            file.write(repr(cointainer)+"\n")
    file.write("MOVELIST\n")
    for move in moves:
        file.write(repr(move)+"\n")
    file.write(str(currMove))
    file.close()

def rfileRead():
    file = open('devlog/recovery.txt')
    lines = file.readlines()
    file.close()
    varno = 1
    status = 0
    manifest = ""
    temprows = []
    buffer = []
    onloadList = []
    moves = []
    currMove = 0
    for L in lines:
        L.replace("\n","")
        L.strip()
        if varno == 1:
            status = int(L)
            varno = 2
        elif varno == 2:
            manifest = L
            varno = 3
        elif varno == 3:
            if L == "TEMPROWS":
                continue
            elif L == "BUFFER":
                varno = 4
            elif L == "ONLOAD":
                varno = 5
            elif L == "MOVELIST":
                varno = 6
            else:
                temprows.append(lineToContainer(L))
        elif varno == 4:
            if L == "ONLOAD":
                varno = 5
            if L == "MOVELIST":
                varno = 6
            else:
                buffer.append(lineToContainer(L))
        elif varno == 5:
            if L == "MOVELIST":
                varno = 6
                buffer.append(lineToContainer(L))
        elif varno == 6:
            if lines.index(L) == len(lines) - 2:
                varno = 7
            moves.append(lineToMove(L))
        elif varno == 7:
            currMove = int(L)
        else:
            print('HELP', flush = True)
    return status, manifest, temprows, buffer, onloadList, moves, currMove

def lineToContainer(line):
    row = 0
    if line[1] == 0:
        row = int(line[2])
    else:
        row = int(line[1] + line[2])
    col = 0
    if line[4] == 0:
        row = int(line[5])
    else:
        row = int(line[4] + line[5])
    weight = 0
    index = line.find("{")
    index2 = line.find("}")
    weight = str(line[index+1:index2:1])
    desc = ""
    index = index2 + 3
    index2 = len(line)-1
    desc = str(line[index:index2:1])
    return Container(row, col, weight, desc)

def lineToMove(line):
    row1 = 0
    index = line.find("[") + 1
    if line[index] == 0:
        row1 = int(line[index+2])
    else:
        row1 = int(line[index+1] + line[index+2])
    col1 = 0
    index = line.find(",", index)
    if line[index] == 0:
        col1 = int(line[index+2])
    else:
        col1 = int(line[index+1] + line[index+2])
    row2 = 0
    index = line.find("[", index) + 1
    if line[index] == 0:
        row2 = int(line[index+2])
    else:
        row2 = int(line[index+1] + line[index+2])
    col2 = 0
    index = line.find(",", index)
    if line[index] == 0:
        col2 = int(line[index+2])
    else:
        col2 = int(line[index+1] + line[index+2])
    return Move(row1, col1, row2, col2)
    
