from cmu_graphics import *
import tkinter as tk
import random

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.wm_attributes('-fullscreen', True) ## This line is a workaround for macOs devices with no ill effects for Windows users. It forces a new window to open in fullscreen and focus on it, before destroying it on the next line. The main canvas is then created and players will see it. Players must still maximise this window manually however
root.destroy()

gameInfo = open("Files/MinesweeperStats.txt", "r+")
fullInfoList = [] ## Key infomation can be found in MinesweeperStatsKeys.txt
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))

app.width = width
app.height = height

app.setMaxShapeCount(100000)

app.stepsPerSecond = 30
app.blocksWide = 0
app.bombPercentage = 0
app.numSafe = 0
app.achShown = 0
app.numCleared = 0
app.firstClick = True
app.failed = False
app.play = True
app.mode = None
app.noFlags = True
app.achShowing = False
AcheivementNote = Group()
background = Rect(0,0,app.width, app.height, fill='lightGray')
colors = ['black', 'saddleBrown', 'darkGreen', 'seaGreen', 'blue', 'mediumSlateBlue', 'darkMagenta', 'darkRed', 'red']
app.flagCol = 'orange'
numberLabels = Group()
buttonLabels = Group()
buttons = Group()
squares = Group()
flags = Group()
preGame = Group()
bombs = Group()
gameOverScreen = Group()
acheivements = Group()
app.removeAchTimer = 0

def create_front_screen():
    '''
    Takes No arguments and returns no values
    When called, creates opjects and assigns them into approprate groups
    Used at the launch of the app and each time a new game begins    
    '''
    frontScreen = Rect(0,0,app.width,app.height, fill = 'black')
    easyButton = Rect((11/40)*app.width, (13/40)*app.height, (9/20)*app.width, (7/40)*app.height, fill = 'white')
    mediumButton = Rect((11/40)*app.width, (21/40)*app.height, (9/20)*app.width, (7/40)*app.height, fill = 'white')
    hardButton = Rect((11/40)*app.width, (29/40)*app.height, (9/20)*app.width, (7/40)*app.height, fill = 'white')
    easyButton.type = "easy"
    mediumButton.type = "medium"
    hardButton.type = "hard"
    label1 = Label("Easy", easyButton.centerX, easyButton.centerY, size = (3/40)*app.width)
    label2 = Label("Medium", mediumButton.centerX, mediumButton.centerY, size = (3/40)*app.width)
    label3 = Label("Hard", hardButton.centerX, hardButton.centerY, size = (3/40)*app.width)
    label4 = Label("Minesweeper", easyButton.centerX, (1/8)*app.height, size = (1/10)*app.width, fill = 'white')
    label5 = Label("* Your first click on the board is always safe *", easyButton.centerX, (9/40)*app.height, fill = 'white', size = (1/20)*app.width)
    buttons.add(easyButton, mediumButton, hardButton)
    buttonLabels.add(label1, label2, label3)
    preGame.add(frontScreen, label4, label5)

def create_board():
    '''
    Takes no argumens and returns no values
    Creates the game board and sets global values based on mode selected by player  
    Called only once per game,   
    '''
    if(app.mode == None):
        None
    if(app.mode == 'easy'):
        app.blocksWide = 16
        app.bombPercentage = 20
        fullInfoList[1]+=1
    if(app.mode == 'medium'):
        app.blocksWide = 24
        app.bombPercentage = 24
        fullInfoList[3]+=1
    if(app.mode == 'hard'):
        app.blocksWide = 40
        app.bombPercentage = 28
        fullInfoList[5]+=1
    fullInfoList[7]+=1
    app.squareSize = (int)((1/app.blocksWide)*app.width)
    app.rows = (int)(app.height / app.squareSize)
    app.cols = (int)(app.width / app.squareSize)
    for i in range(app.cols):
        for j in range(app.rows):
            if (i+j)%2 == 0:
                color = "yellowGreen"
            else:
                color = "lightGreen"
            new = Rect(i*app.squareSize, j*app.squareSize, app.squareSize, app.squareSize, fill = color)
            create_flag(new.centerX, new.centerY, i, j)
            new.i = i
            new.j = j
            new.count = 0
            new.flag = False
            new.revealed = False
            new.bomb = False
            squares.add(new)
            app.numSafe+=1
    plant_bombs(squares)
    bombCheckAlgortihm()
    update_stats()
    
def update_stats():
    '''
    Takes no arguments and returns no values
    Updates values relating to stored stats outside of the program
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")

def create_bombs_end_game():
    '''
    Takes no arguments and returns no values
    Should only be called if the player has clicked a bomb and lost the game
    Creates "bombs" on each square where a bomb was planted
    '''
    for sq in squares:
        if sq.bomb == True:
            bombs.add(Star(sq.centerX, sq.centerY, 1, 30, fill= 'red', border = 'yellow'))
            sq.bomb = False

def plant_bombs(blocks):
    '''
    Takes a group of shapes representing the game board, returns no values
    Iterates through each shape in the group and decides whether or not to plant a bomb
    Chance for planting a bomb is determined by game mode
    '''
    for square in blocks:
        bombChance = randrange(100)
        if (bombChance<=app.bombPercentage):
            square.bomb = True
            app.numSafe-=1
                    
def bombCheckAlgortihm():
    '''
    Takes no arguments and returns no values
    Iterates through every square in the game board
    Checks through all nearby squares for if they contain a bomb
    Add the given values and store in attribute of each square on the game board
    '''
    for square in squares:
        square.count+=searchLeft(square.i, square.j)
        square.count+=searchRight(square.i, square.j)
        square.count+=searchUp(square.i, square.j)
        square.count+=searchDown(square.i, square.j)
        square.count+=searchUpLeft(square.i, square.j)
        square.count+=searchDownLeft(square.i, square.j)
        square.count+=searchUpRight(square.i, square.j)
        square.count+=searchDownRight(square.i, square.j)
    create_number_labels()
                
def create_number_labels():
    '''
    Takes no arguments and returns no values
    Iterates throgh each square in the game board and accesses the 'count' attribute representing the number of nearby bombs
    Creates Labels for each square that show the number of nearby bombs    
    '''
    for square in squares:
        if square.bomb == True:
            new = Label("", square.centerX, square.centerY, size = app.squareSize)
        else:
            new = Label(square.count, square.centerX, square.centerY, fill = colors[square.count], size = app.squareSize)
        numberLabels.add(new)
                
                
###### The Following 8 Functions are helpers called by bomb_check_algorithm() and will search in the direction implied by the name, sourced from the given values ######                

def searchLeft(i,j):
    if(i>0):
        for square in squares:
            if(square.i == i-1 and square.j == j):
                if square.bomb == True:
                    return 1
    return 0

def searchRight(i,j):
    if(i<app.cols):
        for square in squares:
            if(square.i == i+1 and square.j == j):
                if square.bomb == True:
                    return 1
    return 0

def searchUp(i,j):
    if(j>0):
        for square in squares:
            if(square.i == i and square.j == j-1):
                if square.bomb == True:
                    return 1
    return 0

def searchDown(i,j):
    if(j<app.rows):
        for square in squares:
            if(square.i == i and square.j == j+1):
                if square.bomb == True:
                    return 1
    return 0

def searchUpLeft(i,j):
    if(i>0 and j>0):
        for square in squares:
            if(square.i == i-1 and square.j == j-1):
                if square.bomb == True:
                    return 1
    return 0

def searchDownLeft(i,j):
    if(i>0 and j<app.rows):
        for square in squares:
            if(square.i == i-1 and square.j == j+1):
                if square.bomb == True:
                    return 1
    return 0

def searchUpRight(i,j):
    if(i<app.cols and j>0):
        for square in squares:
            if(square.i == i+1 and square.j == j-1):
                if square.bomb == True:
                    return 1
    return 0

def searchDownRight(i,j):
    if(i<app.cols and j<app.rows):
        for square in squares:
            if(square.i == i+1 and square.j == j+1):
                if square.bomb == True:
                    return 1
    return 0

###### The Preceding 8 Functions are helpers called by bomb_check_algorithm() and will search in the direction implied by the name, sourced from the given values ######

def explode_bombs():
    '''
    Takes no arguments and returns no values
    Iterates through bombs on the game board
    Expands all bombs until a certain size, then stops
    Will reset game mode to default when bombs are finished exploding
    '''
    for bomb in bombs:
        if bomb.radius<=app.squareSize/4:
            bomb.radius +=2
        else:
            fail()
            app.mode = None
    
def fail():
    '''
    Takes no arguments and returns no values
    will update stats and create a fail message, offering a chance to play again
    '''
    update_stats()
    gameOverScreen.add(Rect(app.width/4, 2*app.height/5, app.width/2, app.height/5, fill = None, border = 'black'))
    gameOverScreen.add(Label("Press Escape to Try Again", app.width/2, app.height/2 + 20, size = 25))
    gameOverScreen.add(Label("You're a failure", app.width/2, (app.height/2)-20, size = 50))
    
def unlockAcheivement(type):
    app.achShowing = True
    box = Rect(app.width/2,  1/2*app.width, 8*app.squareSize, 4*app.squareSize, fill = None, border = 'black', align = 'center', borderWidth = 4)
    app.removeAchTimer = app.stepsPerSecond*15
    name = Label("You unlocked the" + type + " Acheivement", box.centerX, box.centerY-10, size = app.width/60)
    instruction = Label("Press (y) to toggle flag color in future games" , name.centerX, name.centerY + 25, size = app.width/60)
    AcheivementNote.add(box, name, instruction)
    
def win():
    '''
    Takes no args and returns no values
    Should only be called if the user has won the game
    '''
    if(app.mode == "easy"):
        fullInfoList[0]+=1
    if(app.mode == "medium"):
        fullInfoList[2]+=1
    if(app.mode=="hard"):
        fullInfoList[4]+=1
    fullInfoList[6]+=1
    gameOverScreen.add(Rect(app.width/4, 2*app.height/5, app.width/2, app.height/5, fill = None, border = 'black'))
    gameOverScreen.add(Label("Press Escape to Try Again", app.width/2, app.height/2 + 20, size = 25))
    gameOverScreen.add(Label("You're a Winner", app.width/2, (app.height/2)-20, size = 50))
    if(app.noFlags == True):
        fullInfoList[8] = 1
        unlockAcheivement("Win Without Using Flags")
    update_stats()
    app.mode = None
    app.play = False

def toggle_flags_color():
    '''
    Takes no args and returns no values
    Toggles flag color and should only be called if the user has unlocked noFlagWin acheivement
    '''
    for flag in flags:
        flag.fill = app.flagCol

def create_flag(x,y, i, j):
    '''
    Takes 2 positional arguments and 2 identifier arguemtns to match flags to squares
    Creates a flag on each square that can be toggled on and off by the user
    returns no values
    '''
    flag = RegularPolygon(x,y,app.squareSize/3, 3, fill=app.flagCol, rotateAngle = 90, opacity = 0)
    flag.i = i
    flag.j = j
    flags.add(flag)

def reset():
    '''
    Takes no args and retuns no values
    Resets the game position to as if it had first been launched but does update the stored stats first
    '''
    update_stats()
    gameOverScreen.clear()
    acheivements.clear()
    app.blocksWide = 0
    app.bombPercentage = 0
    app.numSafe = 0
    app.numCleared = 0
    app.firstClick = True
    app.failed = False
    app.play = True
    numberLabels.clear()
    squares.clear()
    flags.clear()
    bombs.clear()
    create_front_screen()
    app.mode = None
    app.noFlags = True

def toggle_flag(x,y, real):
    '''
    Takes 2 positional and 1 acheivement related argument
    Toggles the relevant flag on or off 
    Also removes current game from acheivement consideration if the flag was placed by the user and not by the first reveal
    '''
    update_stats()
    for square in squares:
        for flag in flags:
            if flag.i == square.i:
                if flag.j == square.j:
                    if(square.contains(x,y)):
                        if(flag.opacity == 100):
                            flag.opacity = 0
                            square.flag = False
                        else:
                            flag.opacity = 100
                            square.flag = True
                            if(real==True):
                                app.noFlags = False
                                fullInfoList[9] +=1

def fancy_first_click(x,y):
    '''
    Takes 2 positional arguments and returns no values
    Reveals the square clicked by the user (based on coordinarea) and all adjacent (including corner) squares
    '''
    disappear(x,y)
    disappear(x, y-app.squareSize)
    disappear(x, y+app.squareSize)
    disappear(x+app.squareSize,y)
    disappear(x+app.squareSize, y-app.squareSize)
    disappear(x+app.squareSize, y+app.squareSize)
    disappear(x-app.squareSize,y)
    disappear(x-app.squareSize, y-app.squareSize)
    disappear(x-app.squareSize, y+app.squareSize)
    
def checkWin():
    '''
    Takes no args and returns no values
    Checks if the game has been won, activates win screen if the condition was met
    '''
    if(app.numSafe == app.numCleared):
        win()

def disappear(x,y):
    '''
    Takes 2 positional arguments to locate the square to remove
    Removes the clicked square and checks to see if it was the winning move
    Also can end the game if a bomb was clicked
    Has a safeguard to plant flags instead of revealing bombs if called during the first click reveal    
    '''
    for square in squares:
        if square.contains(x,y):
            if(square.flag == False):
                if square.bomb == True and app.firstClick == False:
                    create_bombs_end_game()
                    app.failed = True
                elif(square.bomb == False):
                    squares.remove(square)
                    app.numCleared+=1
                    checkWin()
                elif(app.firstClick == True and square.bomb == True):
                    toggle_flag(x,y, False)
                else:
                    squares.remove(square)
        
def onKeyPress(key):
    '''
    Built in CMU function to accept key presses
    Used to toggle flag color and reset the game after a win or loss
    '''
    if(key == "escape"):
        if(app.failed == True or app.play == False):
            reset()
    if(key == 'y' or key =="Y"):
        if(fullInfoList[8]==1):
            if(app.flagCol == 'orange'):
                app.flagCol = "white"
            else:
                app.flagCol = "orange"
            toggle_flags_color()

def clean_pre_game():
    '''
    Takes no args and returns no values
    Removes all shapes related to beginning screen
    '''
    preGame.clear()
    buttons.clear()
    buttonLabels.clear()

def onMousePress(x,y,button):
    '''
    CMU built-in function to accepts coordinates and press type of given mouse press
    Used in this script to select game mode, click on squares in game, and place flags or reveal squares
    '''
    if(app.mode == None):
        for button in buttons:
            if(button.contains(x,y)):
                app.mode = button.type
                create_board()
                clean_pre_game()
    else:
        if(button == 2 and app.firstClick == False):
            toggle_flag(x,y, True)
        if(button == 0):
            if app.firstClick == True:
                fancy_first_click(x,y)
                app.firstClick = False
            else:
                disappear(x,y)
 
def onStep():
    '''
    Built in CMU function, runs the code below app.stepsPerSecond times every second. 
    Used to explode bombs in failure and hide acheivement over time
    '''
    if(app.failed == True):
        explode_bombs()
    if(app.achShowing == True):
        app.removeAchTimer-=1
        if(app.removeAchTimer <=0):
            AcheivementNote.clear()
            app.achShowing = False

fullInfoList[10]+=1
bombs.toFront()
buttons.toFront()
buttonLabels.toFront()
gameOverScreen.toFront()
AcheivementNote.toFront()
create_front_screen()
update_stats()

app.run()