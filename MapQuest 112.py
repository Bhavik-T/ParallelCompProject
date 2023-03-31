from cmu_112_graphics import *
from gameRules import *
from Pieces import *
from AI import *

def appStarted(app):

    app.gold0 = 10
    app.gold1 = 10
    app.turn = 0
    app.timerDelay = 500
    app.gameState = 0

    #board
    app.board = generateMap(6)
    app.visibility = [([0] * 6) for i in range(6)]
    app.visibility[0][0] = 1
    app.visibility[0][1] = 1
    app.visibility[1][0] = 1
    app.visibility[1][1] = 1

    
    app.characters = []
    app.selected = None
    app.createable = 0
    app.moveable = []

    app.mode = 'titleScreen'
    app.border = 30
    app.squareLength = (app.height - 2 * app.border) // 6 #len(app.board)
    app.rows = len(app.board)
    app.cols = len(app.board[0])

    #loading images
    app.cloudBackground = app.loadImage('Images/tiles/fog/fog_tile.png')
    app.cloudBackground = app.scaleImage(app.cloudBackground, app.squareLength/100)
    app.grassBackground = app.loadImage('Images/tiles/grassland/grassland_tile.png')
    app.grassBackground = app.scaleImage(app.grassBackground, app.squareLength/100)
    app.waterBackground = app.loadImage('Images/tiles/ocean/water_tile.png')
    app.waterBackground = app.scaleImage(app.waterBackground, app.squareLength/100)
    app.mountainBackground = app.loadImage('Images/tiles/mountains/mountain_tile.png')
    app.mountainBackground = app.scaleImage(app.mountainBackground, app.squareLength/100)
    app.baseK = app.loadImage('Images/tiles/bases/baseK.png')
    app.baseK = app.scaleImage(app.baseK, app.squareLength/100)
    app.baseT = app.loadImage('Images/tiles/bases/baseT.png')
    app.baseT = app.scaleImage(app.baseT, app.squareLength/100)
    app.outpostK = app.loadImage('Images/tiles/outposts/kosbie_outpost.png')
    app.outpostK = app.scaleImage(app.outpostK, app.squareLength/100)
    app.outpostT = app.loadImage('Images/tiles/outposts/taylor_outpost.png')
    app.outpostT = app.scaleImage(app.outpostT, app.squareLength/100)
    app.outpost = app.loadImage('Images/tiles/outposts/outpost.png')
    app.outpost = app.scaleImage(app.outpost, app.squareLength/100)
    app.farmK = app.loadImage('Images/tiles/farm/kosbie_farm.png')
    app.farmK = app.scaleImage(app.farmK, app.squareLength/100)
    app.farmT = app.loadImage('Images/tiles/farm/taylor_farm.png')
    app.farmT = app.scaleImage(app.farmT, app.squareLength/100)
    app.farm = app.loadImage('Images/tiles/farm/farm.png')
    app.farm = app.scaleImage(app.farm, app.squareLength/100)

    app.archerK = app.loadImage('Images/TA sprites/archers/alex_archer.png')
    app.archerK = app.scaleImage(app.archerK, app.squareLength/100)
    app.archerT = app.loadImage('Images/TA sprites/archers/asad_archer.png')
    app.archerT = app.scaleImage(app.archerT, app.squareLength/100)
    app.knightK = app.loadImage('Images/TA sprites/horseriders/anita_horserider.png')
    app.knightK = app.scaleImage(app.knightK, app.squareLength/100)
    app.knightT = app.loadImage('Images/TA sprites/horseriders/kian_horserider.png')
    app.knightT = app.scaleImage(app.knightT, app.squareLength/100)
    app.warriorK = app.loadImage('Images/TA sprites/warriors/warriorben.png')
    app.warriorK = app.scaleImage(app.warriorK, app.squareLength/100)
    app.warriorT = app.loadImage('Images/TA sprites/warriors/zhara_warrior.png')
    app.warriorT = app.scaleImage(app.warriorT, app.squareLength/100)

    app.game_background = app.loadImage('Images/game_background.png')
    app.game_background = app.scaleImage(app.game_background, 1/3)

    app.game_lore = app.loadImage('Images/game_lore.png')

    app.win_screen = app.loadImage('Images/winscreen.png')
    app.win_screen = app.scaleImage(app.win_screen, 3/5)

    app.lose_screen = app.loadImage('Images/losescreen.png')
    app.lose_screen = app.scaleImage(app.lose_screen, 3/5)

    app.help_screen = app.loadImage('Images/helpscreen.png')
    #app.help_screen = app.scaleImage(app.help_screen, 3/5)


def gameMode_timerFired(app):
    if app.gameState == 1:
        app.mode = "winScreen"
    elif app.gameState == 2:
        app.mode = "loseScreen"
    elif app.turn == 1:
        getGold(app)
        getMove(app)
        app.turn = 1 - app.turn
    
def getGold(app):
    app.gold0 += 1
    for i in app.board:
            app.gold0 += i.count('FarmKosbie')
    

    app.gold1 += 1
    for i in app.board:
            app.gold1 += i.count('FarmTaylor')
    
def gameMode_mousePressed(app,event):
    row = getDim(app,event.y)
    col = getDim(app,event.x)
    options_center = (2 * app.border +  app.squareLength * len(app.board))
    options_center = options_center + (app.width - options_center) // 2 
    
    #click help menu
    if (event.x > options_center - 100 and event.x < options_center + 100 and
        event.y > 620 and event.y < 680):
        app.mode = "helpScreen"
    
    if app.turn == 0:
        if (row >= 0 and row < len(app.board) and
            col >= 0 and col < len(app.board)):

            #check if there is a piece selected
            if app.selected != None and type(app.selected) != tuple and app.selected.owner == 'Kosbie':
                if (row,col) in app.moveable:
                    app.selected.move(app,row,col)
                    app.turn = 1 - app.turn
                
                clearSelection(app)

            #if nothing is selected, then tries to select a piece or structure
            else:
                #check if piece there
                soldier = soldierSelected(app,row,col)
                if soldier != None and soldier.owner == 'Kosbie':
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

def clearSelection(app):
    app.selected = None
    app.moveable = []
    app.createable = 0

def generateCreateable(app):
    if app.gold0 >= 9:
        return 3
    elif app.gold0 >= 6:
        return 2
    elif app.gold0 >= 4:
        return 1 
    else:
        return 0



def getDim(app,dim):
    return (dim - app.border) // app.squareLength

def soldierSelected(app,row,col):
    for character in app.characters:
        if character.x == col and character.y == row:
            return character
    return None

        
    
def gameMode_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,800,800, fill = 'blue')
    drawBoard(app,canvas)
    drawCharacters(app,canvas)
    drawCreateOptions(app,canvas)
    drawMovesAllowed(app,canvas)
    drawFog(app, canvas)

def drawFog(app, canvas):
    for row in range(len(app.visibility)):
        for col in range(len(app.visibility)):
            if app.visibility[col][row] % 2 != 1:
                canvas.create_image(row * app.squareLength + app.border + app.squareLength // 2,
                                    col * app.squareLength + app.border + app.squareLength //2,
                                    image=ImageTk.PhotoImage(app.cloudBackground))


def drawMovesAllowed(app,canvas):
    for (row,col) in app.moveable:
        circleCenterX = col * app.squareLength + app.border + app.squareLength // 2
        circleCenterY = row * app.squareLength + app.border + app.squareLength //2

        canvas.create_oval(circleCenterX - 10, circleCenterY - 10, circleCenterX + 10,
                           circleCenterY + 10, fill = 'brown')


def drawCreateOptions(app,canvas):
    options_center = (2 * app.border +  app.squareLength * len(app.board))
    options_center = options_center + (app.width - options_center) // 2 

    canvas.create_text(options_center, 50, text = "Create Menu", font = 'Arial 40 underline')

    if app.createable > 2:
        canvas.create_rectangle(options_center - 150, 280, options_center + 150, 340)
        canvas.create_text(options_center, 310, text = 'Knight\t\t9G', font = 'Arial 20')
    
    if app.createable > 1:
        canvas.create_rectangle(options_center - 150, 200, options_center + 150, 260)
        canvas.create_text(options_center, 230, text = 'Archer\t\t6G', font = 'Arial 20')
    
    if app.createable > 0:
        canvas.create_rectangle(options_center - 150, 120, options_center + 150, 180)
        canvas.create_text(options_center, 150, text = 'Soldier\t\t4G', font = 'Arial 20')
    

    canvas.create_rectangle(options_center - 100, 620, options_center + 100, 680, fill = 'gray')
    canvas.create_text(options_center, 650, text = 'Help', font = 'Arial 30')
    canvas.create_text(options_center, 500, text = f'Player Gold: {app.gold0}', font = 'Arial 30')
    canvas.create_text(options_center, 400,text = f'Player Turn: {app.turn + 1}', font = 'Arial 30')





        

def drawCharacters(app,canvas):
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
            
           





def winScreen_redrawAll(app,canvas):
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.win_screen))

def loseScreen_redrawAll(app,canvas):
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.lose_screen))

def helpScreen_redrawAll(app,canvas):
    canvas.create_image(app.width//2, app.height//2 - 50,
                        image=ImageTk.PhotoImage(app.help_screen))
    canvas.create_rectangle(app.width // 2 - 100, app.height // 2 + 265, app.width // 2 + 100, 
                            app.height // 2 + 335, fill = 'red')
    canvas.create_text(app.width//2, app.height//2 + 300, text = "Return", font = 'Arial 40', fill = 'white')

def helpScreen_mousePressed(app,event):
    if (event.x > app.width // 2 - 100 and event.x < app.width // 2 + 100 and
        event.y > app.height // 2 + 265 and event.y < app.height // 2 + 335):
            app.mode = 'gameMode'


def titleScreen_redrawAll(app,canvas):
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.game_background))\

    canvas.create_rectangle(app.width // 2 - 100, app.height // 2 + 165, app.width // 2 + 100, 
                            app.height // 2 + 235, fill = 'red')
    canvas.create_text(app.width//2, app.height//2 + 200, text = "Start", font = 'Arial 40', fill = 'white')

    

    

def titleScreen_mousePressed(app,event):
    if (event.x > app.width // 2 - 100 and event.x < app.width // 2 + 100 and
        event.y > app.height // 2 + 165 and event.y < app.height // 2 + 235):
            app.mode = 'LoreScreen'


def LoreScreen_redrawAll(app,canvas):
    canvas.create_image(app.width//2, app.height//2 - 75,
                        image=ImageTk.PhotoImage(app.game_lore))
    
    canvas.create_rectangle(app.width // 2 - 100, app.height // 2 + 260, app.width // 2 + 100, 
                            app.height // 2 + 330, fill = 'gray')
    canvas.create_text(app.width//2, app.height//2 + 295, text = "Next", font = 'Arial 40', fill = 'white')

def LoreScreen_mousePressed(app,event):
    if (event.x > app.width // 2 - 100 and event.x < app.width // 2 + 100 and
        event.y > app.height // 2 + 260 and event.y < app.height // 2 + 330):
            app.mode = 'gameMode'


runApp(width = 1200, height = 800)
