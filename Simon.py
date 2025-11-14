from cmu_graphics import *
import sys
import subprocess
import random
import os
import pyautogui

size = pyautogui.size()
width = size[0]
height = size[1]

app.autofs = 0

default = [0,0,0]
keys = ["HighScore", "GamesPlayed", "TimesLaunched"] 

file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(file_path)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)
gameName = currentFile[:-3]

print(currentFile + " has opened")

def file_checking(path, default):
    '''
    Takes 2 args, path for which file to look for, 
    default is the default info for the game, 
    returns no values but creates text files
    Looks for necessary game files. Creates and populates the files if they are not found in the expected directory
    Takes the values from the files, whether already existing or new and puts the values into a list for use later
    '''
    directory = "Files"
    properPath = os.path.join(directory, path)
    if(not os.path.exists(directory)):
        os.makedirs(directory, exist_ok=True)
    if (not os.path.exists(properPath)):
        with open(properPath, 'w') as f:
            f.seek(0)
            for i in range(len(default)):
                f.write((str)(default[i])+"\n")

file_checking(gameName+"Stats.txt", default)
file_checking(gameName+"Keys.txt", keys)

gameInfo = open("Files/SimonStats.txt", "r+")
fullInfoList = []
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))
hi = fullInfoList[0]

app.width = width
app.height = height
app.level = 1
app.stepsPerSecond = 30
app.hiScore = fullInfoList[0]
app.waiting = app.stepsPerSecond * 0.5
app.timer = 0
app.counter = 0
app.turnOffTimer = 10
app.playerButtonTimer = 7
app.playerSelectionTimer = app.stepsPerSecond*2
app.timeBetweenComputerAndPlayer = app.stepsPerSecond
app.mode = 'computer'
app.lastMode = None
app.failed = False
order_game = []
order_player = []

greenButton = Rect(1/8*app.width, 1/8*app.height, 3/8*app.width, 3/8*app.height, fill='green', border = 'black', borderWidth = 3)
greenButton.note = Sound("Audio/C4.mp3")
redButton = Rect(4/8*app.width, 1/8*app.height, 3/8*app.width, 3/8*app.height, fill='red', border = 'black', borderWidth = 3)
redButton.note = Sound("Audio/D#4.mp3")
yellowButton = Rect(1/8*app.width, 4/8*app.height, 3/8*app.width, 3/8*app.height, fill='yellow', border = 'black', borderWidth = 3)
yellowButton.note = Sound("Audio/F#4.mp3")
blueButton = Rect(4/8*app.width, 4/8*app.height, 3/8*app.width, 3/8*app.height, fill='blue', border = 'black', borderWidth = 3)
blueButton.note = Sound("Audio/A4.mp3")
colors = ['green', 'red', 'yellow', 'blue']
buttons = Group(greenButton, redButton, yellowButton, blueButton)
level = Label("Level %d" %app.level, app.width/2, app.height/16, size = app.width/40)
timer = Label("Your Turn in: %1.1f" %(app.timeBetweenComputerAndPlayer/app.stepsPerSecond), (15/16)*app.width, app.height/2)
yourGuessTime = Label("", (1/16)*app.width, app.height/2)
postGame = Group()

closeGameButton = Rect(greenButton.centerX, 7/8 * app.height, 3/16*app.width, 1/8 * app.height, fill = None, border = 'grey')
closeGameLabel = Label("Close Game", closeGameButton.centerX, closeGameButton.centerY, size = 1/100*app.width, fill='red')
backToLauncher = Rect(closeGameButton.right, 7/8 * app.height, 3/16*app.width, 1/8 * app.height, fill = None, border = 'grey')
backToLauncherLabel = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 1/100*app.width, fill='red')


def toggle_on():
    '''
    Takes no arguments and returns no values
    Activate highlighting of button if "clicked" by computer
    '''
    if(app.timer%app.waiting == 0 and app.counter< len(order_game)):
        for button in buttons:
            if(button.fill == order_game[app.counter]):
                button.border = 'lime'
                app.turnOffTimer = 10
                button.note.play(restart = True)
        app.counter+=1

def toggle_off():
    '''
    Takes no args and returns no values
    Disables highlighting at appropriate time
    If computer has clicked all buttons in order, prepare player's turn
    '''
    if(app.turnOffTimer <= 0):
        for button in buttons:
            button.border = 'black'
        if(app.counter == len(order_game)):
            app.timeBetweenComputerAndPlayer = app.stepsPerSecond
            app.counter = 0
            app.lastMode = app.mode
            app.mode = 'delay'

def end_round_win():
    '''
    Takes no args and returns no values
    Should only be called if player wins the round
    Advance level, reset timers and add new color to order
    '''
    app.level+=1
    level.value = "Level: %d" %app.level
    yourGuessTime.value = ''
    order_player.clear()
    order_game.append(colors[randrange(4)])

def offer_replay():
    '''
    Takes no args and returns no values
    Should only be called if player has lost the round
    Display instructions and add shapes to appropriate group
    '''
    if(app.level-1 > app.hiScore):
        app.hiScore = app.level-1
    fullInfoList[0] = app.hiScore
    background = Rect(0,0,app.width, app.height)
    gameOverLabel = Label("Simon Says... You Lost", app.width/2, app.height/4, fill='white', size = app.width/30)
    retryLabel = Label("Press Enter to Play Again", gameOverLabel.centerX, gameOverLabel.centerY + app.height/8, fill = 'white', size = app.width/30)
    lastScore = Label("Last Score: %d" %(app.level-1), retryLabel.centerX, retryLabel.centerY+app.height/8, fill='white', size=app.width/30)
    hiScore = Label("High Score: %d" %app.hiScore, lastScore.centerX, lastScore.centerY+app.height/8, fill='white', size = app.width/30)
    postGame.add(background, gameOverLabel, retryLabel, lastScore, hiScore)
    

def reset_game():
    '''
    Takes no args and returns no values
    Should only be called if the player has chosen to begin new round
    Reset all values and clear lists.
    '''
    order_game.clear()
    order_game.append(colors[randrange(4)])
    order_player.clear()
    postGame.clear()
    app.level = 1
    app.mode = 'computer'
    app.score = 0
    app.playerSelectionTimer = app.stepsPerSecond*2
    app.timeBetweenComputerAndPlayer = app.stepsPerSecond
    yourGuessTime.value = ''
    level.value = "Level %d" %app.level
    app.failed = False

def end_round_fail():
    '''
    Takes no args and returns no values
    Should only be called if the player has clicked the wrong button
    Offer a chance to replay and update stats
    '''
    app.failed = True
    offer_replay()
    update_stats()

def check_accuracy():
    '''
    Takes no args and returns no values
    Checks the order of colors created by the game against the order created by player clicks. 
    If there is a discrepency, fail the round
    If there are no discrpencies and the orders have the same length, win the round and advance
    Otherwise do nothing other than update stats
    '''
    for i in range(len(order_player)):
        if(order_player[i] != order_game[i]):
            end_round_fail()
        if(i == len(order_game)-1):
            end_round_win()
            app.timeBetweenComputerAndPlayer = app.stepsPerSecond
            app.lastMode = app.mode
            app.mode = "delay"
    update_stats()

def onStep():
    '''
    Built in CMU function which calls body code app.stepsPerSecond many times every second
    Used to create the motion and highlighting/unhighlighting of the buttons
    '''
    if(app.autofs<=1):
        app.autofs += 1
    if(app.autofs == 1):
        pyautogui.keyDown("command")
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        pyautogui.keyUp("command")
        pyautogui.keyUp("ctrl")
    if(app.failed == False):
        if(app.playerSelectionTimer<=0):
            end_round_fail()
        if(app.mode == 'computer'):
            app.timer+=1
            toggle_on()
            app.turnOffTimer -=1
            toggle_off()
        elif(app.mode == 'player'):
            app.playerSelectionTimer -=1
            yourGuessTime.value = "Guess Time Remaining: %1.1f" %(app.playerSelectionTimer/app.stepsPerSecond)
        elif(app.mode == 'delay'):
            app.timeBetweenComputerAndPlayer -=1
            if(app.lastMode == 'computer'):
                timer.value = "Your Turn In: %1.1f" %(app.timeBetweenComputerAndPlayer/app.stepsPerSecond)
                if(app.timeBetweenComputerAndPlayer <=0):
                    app.mode = 'player'
                    timer.value = "Your Turn Now"
                    app.playerSelectionTimer = app.stepsPerSecond*2
                    yourGuessTime.value = "Guess Time Remaining: %1.1f" %(app.playerSelectionTimer/app.stepsPerSecond)
            if(app.lastMode == 'player'):
                timer.value = "Computer's Turn In: %1.1f" %(app.timeBetweenComputerAndPlayer/app.stepsPerSecond)
                if(app.timeBetweenComputerAndPlayer <=0):
                    app.mode = 'computer'
                    timer.value = "Computer's Turn Now"
                    yourGuessTime.value = ''
        
def onMousePress(x,y):
    '''
    Built in CMU function which takes as argument the coordinates of a mouse press
    Checks which button contains the mouse press
    Does the approprate action    
    '''
    if(closeGameButton.contains(x,y)):
        sys.exit(0)
    if(backToLauncher.contains(x,y)):
        subprocess.Popen(['python3', "PretendLauncher.py"])
        sys.exit(0)
    if(app.mode == 'player'):
        for button in buttons:
            if(button.contains(x,y)):
                button.border = 'lime'
                order_player.append(button.fill)
                app.playerSelectionTimer = app.stepsPerSecond*2
                button.note.play(restart = True)
    check_accuracy()
            

        
def onMouseRelease(x,y):
    '''
    Built in CMU function which takes as argument the coordinates of a mouse being let go
    Coordinates for this function are pointless in this game but need to be included as this is a built in function
    Upon call, all buttons are in an unclicked state
    '''
    if(app.mode == 'player' or app.mode == 'delay'):
        for button in buttons:
            button.border = 'black'

def onKeyPress(key):
    '''
    Built in CMU function which takes a key press as argument
    Used in this game to reset after a round is over
    '''
    if(key == 'enter' and app.failed == True):
        fullInfoList[1]+=1
        update_stats()
        reset_game()
        
def update_stats():
    '''
    Takes no arguments and returns no values
    Updates values relating to stored stats outside of the program
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")
        
order_game.append(colors[randrange(4)])
fullInfoList[1]+=1
fullInfoList[2]+=1
update_stats()

app.run()

