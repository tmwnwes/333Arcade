from cmu_graphics import *
import tkinter as tk
import random
import sys
import subprocess

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
achievementNote = Group()
background = Rect(0,0,app.width, app.height, fill='lightGray')
colors = ['black', 'saddleBrown', 'cornflowerBlue', 'darkCyan', 'lime', 'yellow', 'darkOrange', 'red', 'magenta']
app.flagCol = 'orange'
numberLabels = Group()
buttonLabels = Group()
buttons = Group()
squares = Group()
flags = Group()
preGame = Group()
bombs = Group()
gameOverScreen = Group()
achievements = Group()
escapeButtons = Group()
helpMenu = Group()
app.help = False
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
    closeGameButton = Rect(hardButton.left, hardButton.bottom, hardButton.width//2, app.height//10, fill=None, border = 'red')
    closeGameButton.words = Label("Close Game", closeGameButton.centerX, closeGameButton.centerY, size = 15, fill='white')
    closeGameButton.game = None
    backToLauncher = Rect(closeGameButton.right, closeGameButton.top, closeGameButton.width, closeGameButton.height, fill=None, border = 'gray',)
    backToLauncher.game = "PretendLauncher.py"
    backToLauncher.words = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 15, fill='white')
    buttons.add(easyButton, mediumButton, hardButton)
    buttonLabels.add(label1, label2, label3)
    preGame.add(frontScreen, label4, label5, closeGameButton.words, backToLauncher.words)
    escapeButtons.add(closeGameButton,backToLauncher)

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
    app.squareSize = (int)((1/app.blocksWide)*width)
    app.rows = (int)(height / app.squareSize)
    app.cols = (int)(width / app.squareSize)
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
    bomb_Check_Algorithm()
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
                    
def bomb_Check_Algorithm():
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
                
def create_number_label(square): 
    '''
    Takes no arguments and returns no values
    Iterates throgh each square in the game board and accesses the 'count' attribute representing the number of nearby bombs
    Creates Labels for each square that show the number of nearby bombs    
    '''
    if square.bomb == False:
        new = Label(square.count, square.centerX, square.centerY, fill = colors[square.count], size = app.squareSize)
        new.zeroCleared = False
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
    
def unlock_achievement(type):
    app.achShowing = True
    box = Rect(app.width/2,  1/2*app.width, 8*app.squareSize, 4*app.squareSize, fill = None, border = 'black', align = 'center', borderWidth = 4)
    app.removeAchTimer = app.stepsPerSecond*10
    name = Label("You unlocked the " + type + " Achievement", box.centerX, box.centerY-10, size = app.width/60)
    instruction = Label("Press (y) to toggle flag color in future games" , name.centerX, name.centerY + 25, size = app.width/60)
    achievementNote.add(box, name, instruction)
    
def win_game():
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
        unlock_achievement("Win Without Using Flags")
    update_stats()
    app.mode = None
    app.play = False

def toggle_flags_color():
    '''
    Takes no args and returns no values
    Toggles flag color and should only be called if the user has unlocked noFlagWin achievement
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

def reset_game():
    '''
    Takes no args and retuns no values
    Resets the game position to as if it had first been launched but does update the stored stats first
    '''
    update_stats()
    app.achShowing = False
    app.removeAchTimer = 0
    achievementNote.clear()
    gameOverScreen.clear()
    achievements.clear()
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
    Takes 2 positional and 1 achievement related argument
    Toggles the relevant flag on or off 
    Also removes current game from achievement consideration if the flag was placed by the user and not by the first reveal
    '''
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
    update_stats()

def auto_clear_zeros():
    '''
    Takes no args and returns no values
    Used to clear squares adjacent to discovered zeroes. 
    This is a twin recursive function with fanc_first_click
    This function will call fancy_first_click on the location of a discovered zero 
    In turn, all adjacent squares are cleared and then this function will be called
    This recursion continues until all squares adjacent to discovered zeroes are cleared
    This will not automatically clear squares that are adjacent to a zero but manually flagged by the user
    In that case, they flagged wrong and have to realize it themselves. 
    This function is a quality of life feature    
    '''
    for num in numberLabels:
        if(num.value == 0 and num.zeroCleared == False):
            num.zeroCleared = True
            fancy_first_click(num.centerX, num.centerY)
            

def fancy_first_click(x,y):
    '''
    Takes 2 positional arguments and returns no values
    Reveals the square clicked by the user (based on coordinarea) and all adjacent (including corner) squares
    '''
    disappear_clicked_square(x,y)
    disappear_clicked_square(x, y-app.squareSize)
    disappear_clicked_square(x, y+app.squareSize)
    disappear_clicked_square(x+app.squareSize,y)
    disappear_clicked_square(x+app.squareSize, y-app.squareSize)
    disappear_clicked_square(x+app.squareSize, y+app.squareSize)
    disappear_clicked_square(x-app.squareSize,y)
    disappear_clicked_square(x-app.squareSize, y-app.squareSize)
    disappear_clicked_square(x-app.squareSize, y+app.squareSize)
    auto_clear_zeros()
    
    
    
def check_win():
    '''
    Takes no args and returns no values
    Checks if the game has been won, activates win screen if the condition was met
    '''
    if(app.numSafe == app.numCleared):
        win_game()

def disappear_clicked_square(x,y):
    '''
    Takes 2 positional arguments to locate the square to remove
    Removes the clicked square and checks to see if it was the winning move
    Also can end the game if a bomb was clicked
    Has a safeguard to plant flags instead of revealing bombs if called during the first click reveal    
    '''
    for square in squares:
        if square.contains(x,y):
            if(square.flag == False and square.revealed == False):
                create_number_label(square)
                if square.bomb == True and app.firstClick == False:
                    create_bombs_end_game()
                    app.failed = True
                elif(square.bomb == False):
                    squares.remove(square)
                    app.numCleared+=1
                    check_win()
                elif(app.firstClick == True and square.bomb == True):
                    toggle_flag(x,y, False)
                else:
                    squares.remove(square)
        
def create_help():
    '''
    Takes no args and returns a shape group
    The shape group represents the help screen which fully hides the game board while active
    Also creates buttons allowing the user to close the game or return to launcher on the help screen instead of just the main menu    
    '''
    temp = Group()
    helpBackground = Rect(0,0,width, height)
    helpLabel = Label("Help", helpBackground.centerX, helpBackground.top + app.squareSize, fill='white', size = app.squareSize)
    help1 = Label("Click on a square to reveal it. If it is a bomb, you lose", helpBackground.centerX, helpLabel.centerY + app.squareSize, fill='white', size = width//40)
    help2 = Label("Numbers in each square represent how many adjacent squres are bombs", helpBackground.centerX, help1.centerY + app.squareSize, fill='white', size = width//40)
    help3 = Label("Place (or remove) a flag on a square by right-clicking it", helpBackground.centerX, help2.centerY + app.squareSize, fill='white', size = width//40)
    help4 = Label("Flags can be used to help you keep track of squares you think may be bombs", helpBackground.centerX, help3.centerY+app.squareSize, fill='white', size = width//40)
    help5 = Label("There is no time limit and you win by clearing all non-bomb squares", helpBackground.centerX, help4.centerY + app.squareSize, fill='white', size = width//40)
    help6 = Label("You can access this menu any time with 'h' or 'p' and close with that same key", helpBackground.centerX, help5.centerY + app.squareSize, fill='white', size = width//40)
    closeGameButton = Rect(helpBackground.left, helpBackground.bottom - app.height//10, helpBackground.width//2, app.height//10, fill=None, border = 'red')
    closeGameButton.words = Label("Close Game", closeGameButton.centerX, closeGameButton.centerY, size = 15, fill='white')
    closeGameButton.game = None
    backToLauncher = Rect(closeGameButton.right, closeGameButton.top, closeGameButton.width, closeGameButton.height, fill=None, border = 'gray',)
    backToLauncher.game = "PretendLauncher.py"
    backToLauncher.words = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 15, fill='white')
    temp.add(helpBackground, helpLabel, closeGameButton.words, backToLauncher.words, help1, help2, help3, help4, help5, help6)
    escapeButtons.add(closeGameButton, backToLauncher)
    return temp        
        
def toggle_help():
    '''
    Takes no args and returns no values
    Toggles the help/pause menu so the player can better understand the object of the game
    '''
    if(app.help == False):
        app.help = True
        helpMenu.add(create_help())
        escapeButtons.toFront()
    else:
        app.help = False
        helpMenu.clear()
        escapeButtons.clear()
            
        
def onKeyPress(key):
    '''
    Built in CMU function to accept key presses
    Used to toggle flag color and reset the game after a win or loss
    '''
    if(key == "escape"):
        if(app.failed == True or app.play == False):
            reset_game()
    if(key == 'y' or key =="Y"):
        if(fullInfoList[8]==1):
            if(app.flagCol == 'orange'):
                app.flagCol = "white"
            else:
                app.flagCol = "orange"
            toggle_flags_color()
    if((key == 'h' or key == 'H' or key =='p' or key =='P') and app.mode != None):
        toggle_help()

def clean_pre_game():
    '''
    Takes no args and returns no values
    Removes all shapes related to beginning screen
    '''
    preGame.clear()
    buttons.clear()
    buttonLabels.clear()
    escapeButtons.clear()

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
        for button in escapeButtons:
            if(button.contains(x,y)):
                if(button.game == None):
                    update_stats()
                    sys.exit(0)
                else:
                    update_stats()
                    subprocess.Popen(["python3", button.game])
                    sys.exit(0)
    else:
        if(app.help == False):
            if(button == 2 and app.firstClick == False):
                toggle_flag(x,y, True)
            if(button == 0):
                if app.firstClick == True:
                    fancy_first_click(x,y)
                    app.firstClick = False
                else:
                    disappear_clicked_square(x,y)
        else:
            for button in escapeButtons:
                if(button.contains(x,y)):
                    if(button.game == None):
                        update_stats()
                        sys.exit(0)
                    else:
                        update_stats()
                        subprocess.Popen(["python3", button.game])
                        sys.exit(0)
                    
 
def onStep():
    '''
    Built in CMU function, runs the code below app.stepsPerSecond times every second. 
    Used to explode bombs in failure and hide achievement over time
    '''
    if(app.failed == True):
        explode_bombs()
    if(app.achShowing == True):
        app.removeAchTimer-=1
        if(app.removeAchTimer <=0):
            achievementNote.clear()
            app.achShowing = False

fullInfoList[10]+=1
bombs.toFront()
buttons.toFront()
buttonLabels.toFront()
gameOverScreen.toFront()
achievementNote.toFront()
escapeButtons.toFront()
helpMenu.toFront()
create_front_screen()
update_stats()



app.run()