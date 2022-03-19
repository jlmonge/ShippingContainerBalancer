from queue import PriorityQueue
import util
import math

TRUCK_TO_SHIP_COST_MINUTES = 2

class Node:

    def __init__(self, ship, selectedOffload) -> None:
        self.state = [[None for i in range(0, 12)] for i in range(0, 8)]
        self.containers_on_top = [None for i in range(0,12)]
        self.selectedOffload = selectedOffload
        self.cost = 0
        self.heuristic = 0
        self.ship = ship
        self.action = (None, "to", None)
        self.timeCost = 0

        for id, item in enumerate(ship):
            row = item[0][0]
            col = item[0][1]

            item = [item[0], item[1], item[2]] #remove id

            self.setStateAt(row, col, item)

        # Locate the topmost container in each column
        for row in range(1, 9):
            for col in range(1, 13):
                item = self.getStateAt(row, col)

                if self.containers_on_top[col-1] == None and item[2] == "UNUSED":
                    self.containers_on_top[col-1] = item
                elif item[2] != "UNUSED" and item[2] != "NAN":
                    self.containers_on_top[col-1] = item

    def setAction(self, initialPosition, destinationPosition):   
        if destinationPosition == (9,1):
            self.action = ((initialPosition[0], initialPosition[1]), "to", (9,1))
        else:
            self.action = ((initialPosition[0], initialPosition[1]), "to", (destinationPosition[0], destinationPosition[1]))

    def calcHeuristic(self):

        # the number of containers above a container selected for offloading
        for selected in self.selectedOffload:
            for item in self.containers_on_top:
                if item[0][1] == selected[0][1]:
                    self.heuristic += (item[0][0] - selected[0][1])

        # count the number of unused columns (columns that don't have a container)
        highest_row = 0
        for container in self.containers_on_top:
            if container[2] == "UNUSED" or container[2] == "NAN": 
                self.heuristic -= 1
            else:
                highest_row = max(highest_row, container[0][0])

        #height diff between goal cell (9,1) and highest container
        self.heuristic -= (9 - highest_row + 1)
            
        
        

    def calculateCostFromAToB(start, end):
        x1, y1 = start[0], start[1]
        x2, y2 = end[0], end[1]

        return abs(x2-x1) + abs(y2-y1)
        

    def atGoalState(self):

        def stringifyItem(item):
            return "{} {} {}".format(item[0], item[1], item[2])

        s = set()
        
        for offload in self.selectedOffload:
            s.add(stringifyItem(offload))

        for i in range(1, 9):
            for j in range(1, 13):
                item = self.getStateAt(i,j)
                if stringifyItem(item) in s: return False
        
        
        return True


    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def getStateAt(self, row, col):
        return self.state[8-row][col-1]

    def setStateAt(self, row, col, item):
        self.state[8-row][col-1] = item

    def __str__(self) -> str:
        s = ""
        for i in range(1,9):
            for j in range(1, 13):
                item = self.getStateAt(i, j)
                s += item[2] + " "
        
        return s
    
    def printState(self):
        for i in range(0, len(self.state)):
            for j in range(0, len(self.state[0])):
                print(self.state[i][j][2], end=" ")
            print()

    def copy(self):


        newNode = Node(self.ship, self.selectedOffload)

        for i in range(0, len(self.containers_on_top)):
            newNode.containers_on_top[i] = self.containers_on_top[i]

        newNode.cost = self.cost
        newNode.heuristic = self.heuristic
        newNode.action = ""

        for i in range(0, len(self.state)):
            for j in range(0, len(self.state[0])):
                newNode.state[i][j] = self.state[i][j]

        return newNode 

    def executeOperations(self):

        newNodes = []

        selectedContainers = self.selectedOffload

        # Remove a container selected for offloading if no containers on top of it
        for ((r,c), w, d) in selectedContainers:
            for position, weight, desc in self.containers_on_top:
                if d == desc:
                    newNode = self.copy()
                    newNode.setStateAt(position[0], position[1], [(position[0], position[1]), 0, "UNUSED"])
                    newNode.timeCost = Node.calculateCostFromAToB((9,1), (r,c))
                    newNode.cost += math.sqrt(newNode.timeCost)
                    newNode.setAction(position, (9,1))
                    
                    if position[0] > 1:
                        below = newNode.getStateAt(position[0]-1, position[1])

                        if below[2] != "NAN" and below[2] != "UNUSED":
                            newNode.containers_on_top[c-1] = newNode.getStateAt(position[0]-1, position[1])
                        else:
                            newNode.containers_on_top[c-1] = newNode.getStateAt(position[0], position[1])
                    else:
                        newNode.containers_on_top[c-1] = newNode.getStateAt(position[0], position[1])
                    
                    newNode.calcHeuristic()
                    newNodes.append(newNode)

        if newNodes: return newNodes

        # Expand node, tries to put the container in the other columns
        for item1 in self.containers_on_top:
            row1 = item1[0][0]
            col1 = item1[0][1]
            desc1 = item1[2]

            if desc1 == "NAN" or desc1 == "UNUSED": continue # only containers that exist can move
            
            for j in range(0, len(self.containers_on_top)):
                item2 = self.containers_on_top[j]
                row2 = item2[0][0]
                col2 = item2[0][1]
                desc2 = item2[2]

                if col1 == col2: continue


                if desc2 == "UNUSED":
                    newNode = self.copy()
                    newNode.setStateAt(row2, col2, [ (row2, col2), item1[1], desc1] )
                    newNode.setStateAt(row1, col1, [ (row1, col1), 0, "UNUSED"])
                    newNode.timeCost = Node.calculateCostFromAToB((row1,col1), (row2, col2))
                    newNode.cost += math.sqrt(newNode.timeCost)
                    newNode.setAction((row1, col1), (row2, col2))

                    if row1 > 1:
                        below = newNode.getStateAt(row1-1, col1)
                        if below[2] != "NAN" and below[2] != "UNUSED":
                            newNode.containers_on_top[col1-1] = newNode.getStateAt(row1-1, col1)
                            newNode.containers_on_top[col2-1] = newNode.getStateAt(row2, col2)
                        else:
                            newNode.containers_on_top[col1-1] = newNode.getStateAt(row1, col1)
                            newNode.containers_on_top[col2-1] = newNode.getStateAt(row2, col2)
                    else:
                        newNode.containers_on_top[col1-1] = newNode.getStateAt(row1, col1)
                        newNode.containers_on_top[col2-1] = newNode.getStateAt(row2, col2)

                    
                    
                    newNode.calcHeuristic()
                    newNodes.append(newNode)
                elif desc2 != "NAN" and row2+1 < 8:
                    newNode = self.copy()
                    newNode.setStateAt(row2+1, col2, [ (row2+1, col2), item1[1], desc1] )
                    newNode.setStateAt(row1, col1, [ (row1, col1), 0, "UNUSED"])
                    newNode.timeCost = Node.calculateCostFromAToB((row1,col1), (row2+1, col2))
                    newNode.cost += math.sqrt(newNode.timeCost)
                    newNode.setAction((row1, col1), (row2+1, col2))
                    
                    if row1 > 1:
                        below = newNode.getStateAt(row1-1, col1)
                        if below[2] != "NAN" and below[2] != "UNUSED":
                            newNode.containers_on_top[col1-1] = newNode.getStateAt(row1-1, col1)
                            newNode.containers_on_top[col2-1] = newNode.getStateAt(row2+1, col2)
                        else:
                            newNode.containers_on_top[col1-1] = newNode.getStateAt(row1, col1)
                            newNode.containers_on_top[col2-1] = newNode.getStateAt(row2+1, col2)
                    else:
                        newNode.containers_on_top[col1-1] = newNode.getStateAt(row1, col1)
                        newNode.containers_on_top[col2-1] = newNode.getStateAt(row2+1, col2)

                    newNode.calcHeuristic()
                    newNodes.append(newNode)

        return newNodes
           


class GeneralGrid:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.buffer = [[[(self.height-j, i+1), 0, "UNUSED"] for i in range(0,self.width)] for j in range(0,self.height)]

    def getCell(self, row, col):
        return self.buffer[self.height-row][col-1]

    def setCell(self, row, col, item):
        self.buffer[self.height-row][col-1] = item

    def fillClosestEmptyCell(self, item):
    
        for col in range(self.width, 0, -1):
            for row in range(self.height, 0, -1):
                if self.getCell(row, col)[2] == "UNUSED":
                    self.setCell(row, col, [(row, col), item[1], item[2]])
                    return (row, col)
        
        return None

    def getClosestEmptyCellRight(self):
    
        for col in range(self.width, 0, -1):
            for row in range(self.height, 0, -1):
                if self.getCell(row, col)[2] == "UNUSED":
                    return self.getCell(row, col)
        
        return None
    def getClosestOccupiedCellLeft(self):
    
        for col in range(1, self.width+1):
            for row in range(self.height+1, 0, -1):
                if self.getCell(row, col)[2] != "UNUSED" and self.getCell(row, col)[2] != "NAN":
                    return self.getCell(row, col)
        
        return None

    def clearCell(self, row, col):
        self.setCell(row, col, [(row, col), 0, "UNUSED"])



def solve(ship, selected_offloads, selected_onloads):

    q = PriorityQueue()
    n = Node(ship, selected_offloads)
    q.put(n)
    s = set()


    # buffer_gg = GeneralGrid(24, 4)
    # ship_gg = GeneralGrid(12, 8)
    history = []

    # for i in range(0, len(ship)):
    #     item = ship[i]
    #     pos = item[0]
    #     ship_gg.setCell(pos[0], pos[1], item)

    # used_cells = 0
    # for i in range(1, 9):
    #     for j in range(1,13):
    #         item = ship_gg.getCell(i,j)
    #         if item[2] != "UNUSED": used_cells += 1


    # while used_cells > 70:
    #     item = ship_gg.getClosestOccupiedCellLeft()
    #     ship_gg.clearCell(item[0][0], item[0][1])
    #     pos = buffer_gg.fillClosestEmptyCell(item)
    #     used_cells -= 1

    #     for so in selected_offloads:
    #         if item[0] == so[0][0] and item[1] == so[0][1]:
    #             pass
    
    while not q.empty():
        node : Node = q.get()

        if node.atGoalState(): 
            history.append(node)
            # node.printState()
            # print("----")
            break

        node_str = str(node)

        if node_str not in s:
            s.add(node_str)

            if node.action[0] != None: history.append(node)
            # node.printState()
            # print("----")
            expandedNodes = node.executeOperations()
            for en in expandedNodes:
                q.put(en)
    

    moves = [] #format  (initial_pos, "to", final_pos, "seconds it takes")

    for node in history:
        moves.append((node.action[0], node.action[1], node.action[2], node.timeCost))


    if history:
        for j in range(1, 13):
            for i in range(1, 9):
                item = history[-1].getStateAt(i,j)

                if item[2] == "UNUSED" and selected_onloads:
                    moves.append( (selected_onloads[0], "to", item, TRUCK_TO_SHIP_COST_MINUTES + Node.calculateCostFromAToB((9,1), item[0]) ) )
                    selected_onloads = selected_onloads[1:]
                


    for move in moves:
        print(move)
    
    
if __name__ == "__main__":
    fname = "5_deep_offload_onload.txt"

    offloads = [
        [(1,7), 2000, "Pikachu"]
    ]

    onloads = [
        [1000, "Uranium"],
        [50, "Gold"],

    ]

    solve(util.parseManifest(fname), offloads, onloads)
