class Piece(object):
    def __init__(self,x,y,attackDamage,movesAllowed,owner,health):
        self.x = x
        self.y = y
        self.attackDamage = attackDamage
        self.movesAllowed = movesAllowed
        self.health = health
        self.owner = owner
    
    def attack (self, other):
        other.health -= self.attackDamage

    def getX (self):
        return self.x
    
    def getY (self):
        return self.y

    def getCords(self):
        return (self.x,self.y)

    def getPieceInCell(self,row,col,app):
        for otherCharacter in app.characters:
                if otherCharacter.getCords() == (col,row):
                    return otherCharacter
        return None

    def generateMovesAllowed(self,app):
        generatedMovesAllowed = []
        if(isinstance(self,Archer)):
            for dx in range((-1*self.movesAllowed)-1, (self.movesAllowed)+2):
                for dy in range((-1*self.movesAllowed)-1, (self.movesAllowed)+2):
                    if dx == 0 and dy == 0:
                        continue
                    newX = self.x + dx
                    newY = self.y + dy
                    if newX < 0 or newX >= len(app.board) or newY < 0 or newY >= len(app.board):
                        continue
                    if (dx < (-1*self.movesAllowed) or dx > (self.movesAllowed)) or (dy < (-1*self.movesAllowed) or dy > (self.movesAllowed)):
                            pieceInCell = self.getPieceInCell(newY, newX, app)
                            if pieceInCell != None and pieceInCell.owner != self.owner:
                                generatedMovesAllowed.append((newY,newX))
                    else:
                        pieceInCell = self.getPieceInCell(newY,newX,app)
                        if pieceInCell != None and pieceInCell.owner == self.owner:
                            continue
                        if app.board[self.y+dy][self.x + dx] not in ["Ocean", "Mountain"]:
                            generatedMovesAllowed.append((self.y+dy,self.x+dx))
        else:
            for dx in range((-1*self.movesAllowed), (self.movesAllowed)+1):
                for dy in range((-1*self.movesAllowed), (self.movesAllowed)+1):
                    if dx == 0 and dy == 0:
                        continue
                    newX = self.x + dx
                    newY = self.y + dy

                    if newX < 0 or newX >= len(app.board) or newY < 0 or newY >= len(app.board):
                        continue

                    pieceInCell = self.getPieceInCell(newY,newX,app)
                    if pieceInCell != None and pieceInCell.owner == self.owner:
                        continue

                    if app.board[self.y+dy][self.x + dx] not in ["Ocean", "Mountain"]:
                        generatedMovesAllowed.append((self.y+dy,self.x+dx))
    
        return generatedMovesAllowed
    
    def move(self,app,targetRow,targetCol):
        
        enemyPiece = self.getPieceInCell(targetRow,targetCol,app)          #if enemy in targetRow, targetCol -> attack:
        print(enemyPiece)
        if enemyPiece != None and enemyPiece.owner != self.owner:
            self.attack(enemyPiece)
            if enemyPiece.health <= 0:
                app.characters.remove(enemyPiece)

            
        if self.getPieceInCell(targetRow,targetCol,app) == None: 
            self.x = targetCol
            self.y = targetRow
            if 'basetaylor' in app.board[targetRow][targetCol].lower() and self.owner == 'Kosbie':
                app.gameState = 1
            
            if 'basekosbie' in app.board[targetRow][targetCol].lower() and self.owner == 'Taylor':
                app.gameState = 2
            
            if 'outpost' in app.board[targetRow][targetCol].lower():
                app.board[targetRow][targetCol] = "Outpost" + self.owner

            if 'farm' in app.board[targetRow][targetCol].lower():
                app.board[targetRow][targetCol] = "Farm" + self.owner

        
        for dx in range(-1,2):                                                  
            for dy in range(-1,2):
                newX = self.x + dx
                newY = self.y + dy

                if newX < 0 or newX >= len(app.board) or newY < 0 or newY >= len(app.board):
                    continue
                if app.visibility[self.y+dy][self.x+dx] < 3 and app.visibility[self.y+dy][self.x+dx] != app.turn+1  :
                    app.visibility[self.y+dy][self.x+dx] += app.turn + 1


class Soldier(Piece):
    def __init__(self,x,y,owner):
        super().__init__(x,y,25,1,owner,50)

class Knight(Piece):
    def __init__(self,x,y,owner):
        super().__init__(x,y,40,2,owner,1)

class Archer(Piece):
    def __init__(self,x,y,owner):
        super().__init__(x,y,30,1,owner,40)