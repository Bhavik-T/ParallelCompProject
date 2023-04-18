from Pieces import *
from gameRules import *
import random
import copy

class Game(object):
    def __init__(self, app, me, opponent):
        self.app = app
        self.board = copy.deepcopy(app.board)
        self.allPieces = app.characters

        self.gold = app.gold1
        
        self.moves = []
        self.me = me
        self.opp = opponent
        self.turn = me

        self.pieces = []
        for piece in self.allPieces:
            if piece.owner == self.me:
                self.pieces.append(piece)
    
    def generateMoves(self):

        myOutposts = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if 'Outpost' in self.board[j][i] and 'Taylor' in self.board[j][i]:
                    myOutposts.append((i, j))
                if 'Base' in self.board[j][i] and 'Taylor' in self.board[j][i]:
                    myOutposts.append((i, j))
        canCreate = []
        if self.gold >= 4:
            canCreate.append('Soldier')
        if self.gold >= 6:
            canCreate.append('Archer')
        if self.gold >= 9:
            canCreate.append('Knight')
        createMoves = []
        for i in canCreate:
            for j in myOutposts:
                createMoves.append(['create', [i, j]])


        self.moves = createMoves
        for piece in self.pieces:
            allowed = piece.generateMovesAllowed(self.app)
            if len(allowed) > 0:
                self.moves.append(['move', piece, allowed])
    
    def pickMove(self):
        self.generateMoves()
        if len(self.moves) == 0:
            return 0
        return random.choice(self.moves)




def getMove(app):
    me = 'Taylor'
    game = Game(app, me, 'Kosbie')
    move = game.pickMove()
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
