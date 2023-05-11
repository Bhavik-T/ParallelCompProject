from Pieces import *
from gameRules import *
import random
import copy

# Input: object
# Define the 'Game' class
class Game(object):
    # Inputs: self, app, me - player, opponent - AI
    # Initialize game AI
    def __init__(self, app, me, opponent):
        # Store the app object, board state, all pieces, gold reserves, player and opponent, and the current turn
        self.app = app
        self.board = copy.deepcopy(app.board)
        self.allPieces = app.characters

        self.gold = app.gold1
        
        self.moves = []
        self.me = me
        self.opp = opponent
        self.turn = me
        
         # Filter the list of all pieces to only include pieces owned by the player
        self.pieces = []
        for piece in self.allPieces:
            if piece.owner == self.me:
                self.pieces.append(piece)
    #input self
    #generate possible actionable playable moves for AI
    def generateMoves(self):
        # Find all outposts and bases owned by the player
        myOutposts = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if 'Outpost' in self.board[j][i] and 'Taylor' in self.board[j][i]:
                    myOutposts.append((i, j))
                if 'Base' in self.board[j][i] and 'Taylor' in self.board[j][i]:
                    myOutposts.append((i, j))
                    
        # Determine which pieces can be created based on the player's gold reserves
        canCreate = []
        if self.gold >= 4:
            canCreate.append('Soldier')
        if self.gold >= 6:
            canCreate.append('Archer')
        if self.gold >= 9:
            canCreate.append('Knight')
            
        # Generate a list of all possible create moves
        createMoves = []
        for i in canCreate:
            for j in myOutposts:
                createMoves.append(['create', [i, j]])

        # Generate a list of all possible moves for each existing piece
        self.moves = createMoves
        for piece in self.pieces:
            allowed = piece.generateMovesAllowed(self.app)
            if len(allowed) > 0:
                self.moves.append(['move', piece, allowed])
    #input: self
    #outputs: random.choice(self.moves) - move from self.move picked randomly; 0 - NA move
    #pick move randomly for AI
    def pickMove(self):
        self.generateMoves()
        if len(self.moves) == 0:
            return 0
        return random.choice(self.moves)



#input: app
#assign move for each given non-playable-character AI
def getMove(app):
    # Set the player and opponent names
    me = 'Taylor'
    game = Game(app, me, 'Kosbie')
    # Get a random move for the AI
    move = game.pickMove()
    
    # Execute the chosen move
    if move == 0:
        return
    if move[0] == 'move':
        piece = move[1]
        targRow, targCol = random.choice(move[2])

        piece.move(app, targRow, targCol)
    
    elif move[0] == 'create':
        loc = move[1][1]
        piece = move[1][0]
        if piece == 'Soldier':
            app.gold1 -= 4
            app.characters.append(Soldier(loc[1],loc[0],'Taylor'))
        
        elif piece == 'Archer':
            app.gold1 -= 6
            app.characters.append(Archer(loc[1],loc[0],'Taylor'))
        
        elif piece == 'Knight':
            app.gold1 -= 9
            app.characters.append(Knight(loc[1],loc[0],'Taylor'))
