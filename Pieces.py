class Piece(object):
    def __init__(self,x,y,attackDamage,movesAllowed,owner,health):
        self.x = x
        self.y = y
        self.attackDamage = attackDamage
        self.movesAllowed = movesAllowed
        self.health = health
        self.owner = owner
        
    # Method to attack another piece and reduce its health by this piece's attack damage
    def attack (self, other):
        other.health -= self.attackDamage
    # Getter methods for the x and y coordinates of the piece
    def getX (self):
        return self.x
    
    def getY (self):
        return self.y
    # Getter method to return a tuple containing the x and y coordinates of the piece
    def getCords(self):
        return (self.x,self.y)
    # Method to get the piece located in a specific cell of the board
    def getPieceInCell(self,row,col,app):
        # Loop through all the pieces in the app
        for otherCharacter in app.characters:
            # Check if the piece's coordinates match the specified row and column
                if otherCharacter.getCords() == (col,row):
                    # Return the piece if found
                    return otherCharacter
        # Return None if no piece was found
        return None
    
    # Method to generate a list of valid moves for this piece based on its type and the state of the board
    def generateMovesAllowed(self,app):
        generatedMovesAllowed = []
        # If the piece is an Archer, calculate the valid moves based on the allowed range
        if(isinstance(self,Archer)):
            for dx in range((-1*self.movesAllowed)-1, (self.movesAllowed)+2):
                for dy in range((-1*self.movesAllowed)-1, (self.movesAllowed)+2):
                    if dx == 0 and dy == 0:
                        continue
                    newX = self.x + dx
                    newY = self.y + dy
                    # Check if the new coordinates are outside the board boundaries
                    if newX < 0 or newX >= len(app.board) or newY < 0 or newY >= len(app.board):
                        continue
                    # Check if the move is within the allowed range
                    if (dx < (-1*self.movesAllowed) or dx > (self.movesAllowed)) or (dy < (-1*self.movesAllowed) or dy > (self.movesAllowed)):
                            # Check if the move captures an enemy piece
                            pieceInCell = self.getPieceInCell(newY, newX, app)
                            if pieceInCell != None and pieceInCell.owner != self.owner:
                                generatedMovesAllowed.append((newY,newX))
                    else:
                        # Check if the move is already occupied by a friendly piece
                        pieceInCell = self.getPieceInCell(newY,newX,app)
                        if pieceInCell != None and pieceInCell.owner == self.owner:
                            continue
                        # Check if the cell contains an obstacle that prevents movement
                        if app.board[self.y+dy][self.x + dx] not in ["Ocean", "Mountain"]:
                            generatedMovesAllowed.append((self.y+dy,self.x+dx))
        else:
            # If the piece is a Soldier or Knight, calculate the valid moves based on the allowed range
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
    
    # Define a method for moving a piece
    def move(self,app,targetRow,targetCol):
        # Check if there is an enemy piece in the target row and column
        enemyPiece = self.getPieceInCell(targetRow,targetCol,app)          #if enemy in targetRow, targetCol -> attack:
        # Print the enemy piece for debugging purposes
        print(enemyPiece)
        # If there is an enemy piece and it belongs to a different player, attack it
        if enemyPiece != None and enemyPiece.owner != self.owner:
            self.attack(enemyPiece)
            # If the enemy piece has no health remaining, remove it from the game
            if enemyPiece.health <= 0:
                app.characters.remove(enemyPiece)

        # If there is no piece in the target cell, move the piece to the target cell
        if self.getPieceInCell(targetRow,targetCol,app) == None: 
            self.x = targetCol
            self.y = targetRow
            # If the piece reaches the enemy's base, change the game state to "Kosbie Wins"
            if 'basetaylor' in app.board[targetRow][targetCol].lower() and self.owner == 'Kosbie':
                app.gameState = 1
            # If the piece reaches the player's own base, change the game state to "Taylor Wins"
            if 'basekosbie' in app.board[targetRow][targetCol].lower() and self.owner == 'Taylor':
                app.gameState = 2
            # If the piece reaches an outpost, change the cell name to "Outpost + owner"
            if 'outpost' in app.board[targetRow][targetCol].lower():
                app.board[targetRow][targetCol] = "Outpost" + self.owner
            # If the piece reaches a farm, change the cell name to "Farm + owner"
            if 'farm' in app.board[targetRow][targetCol].lower():
                app.board[targetRow][targetCol] = "Farm" + self.owner

        # For each adjacent cell to the piece, update the visibility of the cell
        for dx in range(-1,2):                                                  
            for dy in range(-1,2):
                newX = self.x + dx
                newY = self.y + dy
                
                # If the new cell is out of the game board, continue to the next cell
                if newX < 0 or newX >= len(app.board) or newY < 0 or newY >= len(app.board):
                    continue
                # If the cell is not visible, update the visibility to the current turn + 1
                if app.visibility[self.y+dy][self.x+dx] < 3 and app.visibility[self.y+dy][self.x+dx] != app.turn+1  :
                    app.visibility[self.y+dy][self.x+dx] += app.turn + 1

# Define a Soldier class that inherits from the Piece class
class Soldier(Piece):
    def __init__(self,x,y,owner):
        super().__init__(x,y,25,1,owner,50)
# Define a Knight class that inherits from the Piece class
class Knight(Piece):
    def __init__(self,x,y,owner):
        super().__init__(x,y,40,2,owner,1)
# Define an Archer class that inherits from the Piece class
class Archer(Piece):
    def __init__(self,x,y,owner):
        super().__init__(x,y,30,1,owner,40)
