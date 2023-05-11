import random
from collections import deque
#inputs: x - x-coor., y - y-coor., dimensions - dimensions of cell
#outputs: True: cell not exterior, False: cell is exterior
#signifiy whether cell is a border cell
def isExterior(x, y, dimensions):
    #Is the cell a border cell?
    if x == 0 or y == 0:
        return True
    
    if x == dimensions - 1 or y == dimensions - 1:
        return True
    
    return False

from collections import deque

#inputs: board - current state of game with all elements
#outputs: True: game fair, False: game not fair
#calculate the difference in current power between the AI and the player
def checkFairness(board):
    numOutpost = 0
    numFarm = 0
    # Count the number of outposts and farms on the board
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 'Farm':
                numFarm += 1
            elif board[i][j] == 'Outpost':
                numOutpost += 1
    # Check if the number of outposts and farms is within the valid range
    if numOutpost < 2 or numOutpost > 5 or numFarm < 2 or numFarm > 5:
        return False
    return True
                
#inputs: board - current state of game with all elements
#output: False - ind
def checkMap(board):
    if checkFairness(board) == False:
        return False
    # Create a matrix to represent the board, where bad squares (ocean and mountain) are assigned a large value
    # and valid squares are assigned a small value
    badSquares = ['Ocean', 'Mountain']
    matrix = []
    validSquares = []
    for i in range(len(board)):
        matrix.append([])
        for j in range(len(board)):
            if board[i][j] in badSquares:
                matrix[i].append(120)
            else:
                matrix[i].append(1)
                validSquares.append((i, j))
    # Check if there exists a path between every pair of valid squares on the board using BFS
    for i in range(len(validSquares)):
        for j in range(i, len(validSquares)):
            start = validSquares[i]
            end = validSquares[j]
            if BFS(start, end, matrix) == -1:
                return False
    # Check if the game is fair again
    if checkFairness(board) == False:
        return False

    return True


def BFS(start, end, graph):
    queue = [[start]]
    seen = set([start])
    while queue:
        path = queue.pop(0)
        if len(path) > 20:
            # limit the maximum length of a path to 20 squares to prevent an infinite loop
            return False
        x, y = path[-1]
        if x == end[0] and y == end[1]:
            return True
        # Check the four adjacent squares of the current square and add them to the queue if they are valid
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < len(graph) and 0 <= y2 < len(graph) and graph[x2][y2] != 120 and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))


#input: dimensions - game dimensions
#output: board - current state of game with all elements
#generate map with images given dimensions
def generateMap(dimensions):
    
    # Initialize the board with grass in all cells
    board = [
        ['Grass' for i in range(dimensions)] for j in range(dimensions)
    ]
    

    #Name region

    # Define the names for different regions
    baseName = 'Base'
    grassName = 'Grass'
    mountainName = 'Mountain'
    oceanNmae = 'Ocean'

    kosbieName = 'Kosbie'
    taylorName = 'Taylor'
    outpostName = 'Outpost'
    farmName = 'Farm'

    # Define the names for specific outposts and farms
    kosbieOutpostName = outpostName + kosbieName
    taylorOutpostName = outpostName + taylorName

    kosbieFarmName = farmName + kosbieName
    taylorFarmName = farmName + taylorName

    #Probability Region
    probOutpostInterior = 50                      #We favour placing outposts near the middle for fairness.
    probOutpostExterior = 140                      

    probFarmInterior = 130                         #We favour placing farms along the edges.
    probFarmExterior = 50

    probOcean = 100                            #Oceans occupy multiple squares, so their probability is cumulative over their area.
    probMountain = 70                            #Mountains are one square types, so their probabilities are not cumulative.

    while True:
        # Iterate through each cell in the board
        for x in range(dimensions):
            for y in range(dimensions):
                cell = board[x][y]
                
                # If the cell is not grass, skip it (e.g. if it's already occupied by an ocean)
                if cell != grassName:                  #Taken, typically by an ocean as oceans exist as blocks.
                    continue
                # Generate random values to decide the type of the square
                randVal1 = random.randint(0, 1000)        #A random integer to decide the position of the square.
                randVal2 = random.randint(0, 1000)
                randVal3 = random.randint(0, 1000)
                randVal4 = random.randint(0, 1000)
                # Check if the cell is on the border of the map
                isBorder = isExterior(x, y, dimensions)    
                # Set the probabilities of placing outposts and farms based on whether the cell is on the border or not
                if isBorder == True:
                    probOutpost = probOutpostInterior
                    probFarm = probFarmInterior
                
                else:
                    probOutpost = probOutpostExterior
                    probFarm = probFarmExterior
                # Check the random values against the probabilities and update the cell type accordingly
                if randVal1 < probOcean:
                    board[x][y] = 'Ocean'
                    continue
                
                
                
                if randVal2 < probMountain:
                    board[x][y] = 'Mountain'
                    continue
                
                if randVal3 < probOutpost:
                    board[x][y] = 'Outpost'
                    continue
                
                if randVal4 < probFarm:
                    board[x][y] = 'Farm'
                    continue
        # Set the locations of the two bases
        board[0][0] = 'BaseKosbie'
        board[-1][-1] = 'BaseTaylor'
        # Check if the map is valid (e.g. both bases are present)
        if checkMap(board):
            return board
        # If the map is invalid, start over with a new board
        board = [
            ['Grass' for i in range(dimensions)] for j in range(dimensions)
        ]
