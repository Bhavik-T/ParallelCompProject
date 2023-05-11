from graphicLib import *
from gameRules import *
from Pieces import *    #TODO: Gaurav
from AI import * #TODO: Gaurav

# takes in app object; initiates app properties
def appStarted(app):

    #initialze game properties
    app.gold0 = 10
    app.gold1 = 10
    app.turn = 0
    app.timerDelay = 500
    app.gameState = 0

    # set up game board
    app.board = generateMap(6)
    app.visibility = [([0] * 6) for i in range(6)]
    app.visibility[0][0] = 1
    app.visibility[0][1] = 1
    app.visibility[1][0] = 1
    app.visibility[1][1] = 1

    # initialize game characters and selection options
    app.characters = []
    app.selected = None
    app.createable = 0
    app.moveable = []

    # set up game modes and dimensions
    app.mode = 'titleScreen'
    app.border = 30
    app.squareLength = (app.height - 2 * app.border) // 6 #len(app.board)
    app.rows = len(app.board)
    app.cols = len(app.board[0])

    #loading images

 
    #load game images
    app.cloudBackground = app.loadImage('Images/tiles/fog/fog_tile.png')
    app.cloudBackground = app.scaleImage(app.cloudBackground, app.squareLength/100)
    app.grassBackground = app.loadImage('Images/tiles/grassland/grassland_tile.png')
    app.grassBackground = app.scaleImage(app.grassBackground, app.squareLength/100)
    app.waterBackground = app.loadImage('Images/tiles/ocean/water_tile.png')
    app.waterBackground = app.scaleImage(app.waterBackground, app.squareLength/100)
    app.mountainBackground = app.loadImage('Images/tiles/mountains/mountain_tile.png')
    app.mountainBackground = app.scaleImage(app.mountainBackground, app.squareLength/100)
    app.baseK = app.loadImage('Images/tiles/bases/blue_flag.png')
    app.baseK = app.scaleImage(app.baseK, app.squareLength/100)
    app.baseT = app.loadImage('Images/tiles/bases/red_flag.png')
    app.baseT = app.scaleImage(app.baseT, app.squareLength/100)
    app.outpostK = app.loadImage('Images/tiles/outposts/outpost_blue.png')
    app.outpostK = app.scaleImage(app.outpostK, app.squareLength/100)
    app.outpostT = app.loadImage('Images/tiles/outposts/outpost_red.png')
    app.outpostT = app.scaleImage(app.outpostT, app.squareLength/100)
    app.outpost = app.loadImage('Images/tiles/outposts/outpost.png')
    app.outpost = app.scaleImage(app.outpost, app.squareLength/100)
    app.farmK = app.loadImage('Images/tiles/farm/farm_b.png')
    app.farmK = app.scaleImage(app.farmK, app.squareLength/100)
    app.farmT = app.loadImage('Images/tiles/farm/farm_r.png')
    app.farmT = app.scaleImage(app.farmT, app.squareLength/100)
    app.farm = app.loadImage('Images/tiles/farm/farm_g.png')
    app.farm = app.scaleImage(app.farm, app.squareLength/100)

    app.archerK = app.loadImage('Images/sprites/archerB.png')
    app.archerK = app.scaleImage(app.archerK, app.squareLength/100)
    app.archerT = app.loadImage('Images/sprites/archerR.png')
    app.archerT = app.scaleImage(app.archerT, app.squareLength/100)
    app.knightK = app.loadImage('Images/sprites/knightB.png')
    app.knightK = app.scaleImage(app.knightK, app.squareLength/100)
    app.knightT = app.loadImage('Images/sprites/knightR.png')
    app.knightT = app.scaleImage(app.knightT, app.squareLength/100)
    app.warriorK = app.loadImage('Images/sprites/soilderB.png')
    app.warriorK = app.scaleImage(app.warriorK, app.squareLength/100)
    app.warriorT = app.loadImage('Images/sprites/soilderR.png')
    app.warriorT = app.scaleImage(app.warriorT, app.squareLength/100)

 
    app.game_background = app.loadImage('Images/game_background.png')
    app.game_background = app.scaleImage(app.game_background, 1/3)

 
    app.game_lore = app.loadImage('Images/lore.png')

  
    app.win_screen = app.loadImage('Images/pcompWscreen.png')
    app.win_screen = app.scaleImage(app.win_screen, 3/5)

    app.lose_screen = app.loadImage('Images/pcompLscreen.png')
    app.lose_screen = app.scaleImage(app.lose_screen, 3/5)

    app.help_screen = app.loadImage('Images/pcompHelp.png')
    #app.help_screen = app.scaleImage(app.help_screen, 3/5)

#take in app; start timer
def gameMode_timerFired(app):
    # check if the game has been won or lost and update the mode accordingly
    if app.gameState == 1:
        app.mode = "winScreen"
    elif app.gameState == 2:
        app.mode = "loseScreen"
        # if it is player 2's turn, update their gold and moves allowed and switch turns to player 1
    elif app.turn == 1:
        getGold(app)
        getMove(app)
        app.turn = 1 - app.turn

#take in app; augment gold per each sides' gold farm
def getGold(app):
    # update player 1's gold
    app.gold0 += 1
    for i in app.board:
            app.gold0 += i.count('FarmKosbie')
    
    # update player 2's gold
    app.gold1 += 1
    for i in app.board:
            app.gold1 += i.count('FarmTaylor')
#take in app and event; process mouse input to yield appropriate game outcome
def gameMode_mousePressed(app,event):
    row = getDim(app,event.y)
    col = getDim(app,event.x)
    options_center = (2 * app.border +  app.squareLength * len(app.board))
    options_center = options_center + (app.width - options_center) // 2 
    
    #check if help menu was clicked
    if (event.x > options_center - 100 and event.x < options_center + 100 and
        event.y > 620 and event.y < 680):
        app.mode = "helpScreen"
    # check if it is player 1's turn
    if app.turn == 0:
        # check if the click was within the game board
        if (row >= 0 and row < len(app.board) and
            col >= 0 and col < len(app.board)):

            #check if there is a piece selected
            if app.selected != None and type(app.selected) != tuple and app.selected.owner == 'Kosbie':
                # check if the selected piece can move to the clicked location
                if (row,col) in app.moveable:
                    # move the piece to the clicked location and switch turns to player 2
                    app.selected.move(app,row,col)
                    app.turn = 1 - app.turn
                # clear the selection if a valid move was not made
                clearSelection(app)

            #if nothing is selected, then tries to select a piece or structure
            else:
                #check if piece there
                soldier = soldierSelected(app,row,col)
                if soldier != None and soldier.owner == 'Kosbie':
                    # select the soldier and generate its allowed moves
                    app.selected = soldier
                    app.moveable = soldier.generateMovesAllowed(app)
                
                #check is structure there
                elif app.board[row][col] == 'OutpostKosbie' or app.board[row][col] == 'BaseKosbie':
                    app.selected = (row,col)
                    app.createable = generateCreateable(app)

        #the click is outside of the game board
        else:
            #creating a character
            if type(app.selected) == tuple:
                if (event.x > options_center - 150 and event.x < options_center + 150 and
                    event.y > 280 and event.y < 340 and app.createable > 2):
                    app.characters.append(Knight(app.selected[1],app.selected[0],'Kosbie'))
                    app.gold0 -= 9
                    app.turn = 1 - app.turn
        
                if (event.x > options_center - 150 and event.x < options_center + 150 and
                    event.y > 200 and event.y < 260 and app.createable > 1):
                    app.characters.append(Archer(app.selected[1],app.selected[0],'Kosbie'))
                    app.gold0 -= 6
                    app.turn = 1 - app.turn
                
                if (event.x > options_center - 150 and event.x < options_center + 150 and
                    event.y > 120 and event.y < 180 and app.createable > 0):
                    app.characters.append(Soldier(app.selected[1],app.selected[0],'Kosbie'))
                    app.gold0 -= 4
                    app.turn = 1 - app.turn
            
            clearSelection(app)
#input: app; delete selected item in-game
def clearSelection(app):
    # clear the selected item and reset the moveable and createable options
    app.selected = None
    app.moveable = []
    app.createable = 0
#
# check how many characters can be created based on the player's gold
def generateCreateable(app):
    if app.gold0 >= 9:
        return 3
    elif app.gold0 >= 6:
        return 2
    elif app.gold0 >= 4:
        return 1 
    else:
        return 0


#inputs: app, dim - set value of dimmness; dims borders of game
def getDim(app,dim):
     # calculate the row or column based on the given dimension
    return (dim - app.border) // app.squareLength

#inputs: app, row - x-coor, col - y-coor; select soldier; return selected soldier
def soldierSelected(app,row,col):
    # check if there is a soldier at the given row and column and return it if found
    for character in app.characters:
        if character.x == col and character.y == row:
            return character
        # return None if no soldier was found at the given location
    return None

        
#inputs: app, canvas - drawable space; iniate all visual elements    
def gameMode_redrawAll(app,canvas):
    # draw the game board and all visual elements
    canvas.create_rectangle(0,0,800,800, fill = 'blue')
    drawBoard(app,canvas)
    drawCharacters(app,canvas)
    drawCreateOptions(app,canvas)
    drawMovesAllowed(app,canvas)
    drawFog(app, canvas)

#inputs: app, canvas - drawable space; draw cloud background
def drawFog(app, canvas):
    # draw the fog of war on the game board based on the visibility matrix
    for row in range(len(app.visibility)):
        for col in range(len(app.visibility)):
            if app.visibility[col][row] % 2 != 1:
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.cloudBackground))

#inputs: app, canvas - drawable space; illustrate possible moves to player
def drawMovesAllowed(app,canvas):
    # draw circles on the game board to indicate where a selected piece can move to
    for (row,col) in app.moveable:
        circleCenterX = col * app.squareLength + app.border + app.squareLength // 2
        circleCenterY = row * app.squareLength + app.border + app.squareLength //2

        canvas.create_oval(circleCenterX - 10, circleCenterY - 10, circleCenterX + 10,
                           circleCenterY + 10, fill = 'brown')

#inputs: app, canvas - drawable space; draw user-interface for player to access settings
def drawCreateOptions(app,canvas):
    # calculate the center of the options menu
    options_center = (2 * app.border +  app.squareLength * len(app.board))
    options_center = options_center + (app.width - options_center) // 2 
    
    # draw the create menu text
    canvas.create_text(options_center, 50, text = "Create Menu", font = 'Arial 40 underline', fill='black')
    # draw the createable character options based on the player's gold
    if app.createable > 2:
        canvas.create_rectangle(options_center - 150, 280, options_center + 150, 340)
        canvas.create_text(options_center, 310, text = 'Knight\t\t9G', font = 'Arial 20', fill='gray')
    
    if app.createable > 1:
        canvas.create_rectangle(options_center - 150, 200, options_center + 150, 260)
        canvas.create_text(options_center, 230, text = 'Archer\t\t6G', font = 'Arial 20', fill='gray')
    
    if app.createable > 0:
        canvas.create_rectangle(options_center - 150, 120, options_center + 150, 180)
        canvas.create_text(options_center, 150, text = 'Soldier\t\t4G', font = 'Arial 20', fill='gray')
    
    # draw the help menu button and player information
    canvas.create_rectangle(options_center - 100, 620, options_center + 100, 680, fill = 'gray')
    canvas.create_text(options_center, 650, text = 'Help', font = 'Arial 30')
    canvas.create_text(options_center, 500, text = f'Player Gold: {app.gold0}', font = 'Arial 30', fill='gray')
    canvas.create_text(options_center, 400,text = f'Player Turn: {app.turn + 1}', font = 'Arial 30', fill='gray')





        
#inputs: app, canvas - drawable space; illustrate characters
def drawCharacters(app,canvas):
    # draw the characters on the game board based on their type and owner
    for character in app.characters:
        if type(character) == Archer:
            if character.owner == 'Kosbie':
                canvas.create_image(character.x * app.squareLength + app.border + app.squareLength // 2,
                                    character.y * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.archerK))
            else:
                canvas.create_image(character.x * app.squareLength + app.border + app.squareLength // 2,
                                    character.y * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.archerT))
        
        if type(character) == Soldier:
            if character.owner == 'Kosbie':
                canvas.create_image(character.x * app.squareLength + app.border + app.squareLength // 2,
                                    character.y * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.warriorK))
            else:
                canvas.create_image(character.x * app.squareLength + app.border + app.squareLength // 2,
                                    character.y * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.warriorT))

        if type(character) == Knight:
            if character.owner == 'Kosbie':
                canvas.create_image(character.x * app.squareLength + app.border + app.squareLength // 2,
                                    character.y * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.knightK))
            else:
                canvas.create_image(character.x * app.squareLength + app.border + app.squareLength // 2,
                                    character.y * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.knightT))


#draws images for each terrain
def drawBoard(app,canvas):
    # draw the game board based on the board matrix
    for row in range(len(app.board)):
        for col in range(len(app.board)):
            if app.board[col][row] == 'Grass':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.grassBackground))
            
            elif app.board[col][row] == 'Ocean':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.waterBackground))

            elif app.board[col][row] == 'Mountain':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.mountainBackground))

            elif app.board[col][row] == 'Outpost':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.outpost))
            
            elif app.board[col][row] == 'OutpostTaylor':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.outpostT))

            elif app.board[col][row] == 'OutpostKosbie':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.outpostK))
            
            elif app.board[col][row] == 'Farm':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.farm))

            elif app.board[col][row] == 'FarmTaylor':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.farmT))
            
            elif app.board[col][row] == 'FarmKosbie':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.farmK))
            
            elif app.board[col][row] == 'BaseTaylor':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.baseT))
            
            elif app.board[col][row] == 'BaseKosbie':
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.baseK))
            
           




#inputs: app, canvas - drawable space; indicate win for player
def winScreen_redrawAll(app,canvas):
    # draw the win screen image
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.win_screen))
#inputs: app, canvas - drawable space; indicate lose for player
def loseScreen_redrawAll(app,canvas):
    # draw the lose screen image
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.lose_screen))
#inputs: app, canvas - drawable space; show interface for help with game
def helpScreen_redrawAll(app,canvas):
    # draw the help screen image and return button
    canvas.create_image(app.width//2, app.height//2 - 50,
                        image=ImageTk.PhotoImage(app.help_screen))
    canvas.create_rectangle(app.width // 2 - 100, app.height // 2 + 265, app.width // 2 + 100, 
                            app.height // 2 + 335, fill = 'red')
    canvas.create_text(app.width//2, app.height//2 + 300, text = "Return", font = 'Arial 40', fill = 'white')
#inputs: app, canvas - drawable space; use mouse to interface with help screen
def helpScreen_mousePressed(app,event):
    # check if the return button was clicked and switch back to the game mode if it was
    if (event.x > app.width // 2 - 100 and event.x < app.width // 2 + 100 and
        event.y > app.height // 2 + 265 and event.y < app.height // 2 + 335):
            app.mode = 'gameMode'

#inputs: app, canvas - drawable space; redraw titlescreen 
def titleScreen_redrawAll(app,canvas):
    # draw the title screen background and start button
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.game_background))\

    canvas.create_rectangle(app.width // 2 - 100, app.height // 2 + 165, app.width // 2 + 100, 
                            app.height // 2 + 235, fill = 'red')
    canvas.create_text(app.width//2, app.height//2 + 200, text = "Start", font = 'Arial 40', fill = 'white')

    

    
#inputs: app, canvas - drawable space; use mouse input to interface with title-screen
def titleScreen_mousePressed(app,event):
    # check if the start button was clicked and switch to the lore screen if it was
    if (event.x > app.width // 2 - 100 and event.x < app.width // 2 + 100 and
        event.y > app.height // 2 + 165 and event.y < app.height // 2 + 235):
            app.mode = 'LoreScreen'

#inputs: app, canvas - drawable space; display lore 
def LoreScreen_redrawAll(app,canvas):
    # draw the lore screen image and next button
    canvas.create_image(app.width//2, app.height//2 - 75,
                        image=ImageTk.PhotoImage(app.game_lore))
    
    canvas.create_rectangle(app.width // 2 - 100, app.height // 2 + 260, app.width // 2 + 100, 
                            app.height // 2 + 330, fill = 'gray')
    canvas.create_text(app.width//2, app.height//2 + 295, text = "Next", font = 'Arial 40', fill = 'white')
#inputs: app, canvas - drawable space; use mouse input to interface with lore-screen
def LoreScreen_mousePressed(app,event):
    # check if the next button was clicked and switch to the game mode if it was
    if (event.x > app.width // 2 - 100 and event.x < app.width // 2 + 100 and
        event.y > app.height // 2 + 260 and event.y < app.height // 2 + 330):
            app.mode = 'gameMode'

#start the game
runApp(width = 1200, height = 800)
