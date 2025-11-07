from cmu_graphics import *
import tkinter as tk
import sys
import subprocess
import random


### STATS integration coming next week

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.wm_attributes('-fullscreen', True) ## This line is a workaround for macOs devices with no ill effects for Windows users. It forces a new window to open in fullscreen and focus on it, before destroying it on the next line. The main canvas is then created and players will see it. Players must still maximise this window manually however
root.destroy()

app.width = width
app.height = height
app.level = 1
app.stepsPerSecond = 30
app.hiScore = 0 ## Change later with introduction of stats
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
    if(app.timer%app.waiting == 0 and app.counter< len(order_game)):
        for button in buttons:
            if(button.fill == order_game[app.counter]):
                button.border = 'lime'
                app.turnOffTimer = 10
                button.note.play(restart = True)
        app.counter+=1

def toggle_off():
    if(app.turnOffTimer <= 0):
        for button in buttons:
            button.border = 'black'
        if(app.counter == len(order_game)):
            app.timeBetweenComputerAndPlayer = app.stepsPerSecond
            app.counter = 0
            app.lastMode = app.mode
            app.mode = 'delay'

def end_round_win():
    app.level+=1
    level.value = "Level: %d" %app.level
    yourGuessTime.value = ''
    order_player.clear()
    order_game.append(colors[randrange(4)])
    

def offer_replay():
    background = Rect(0,0,app.width, app.height)
    gameOverLabel = Label("Simon Says... You Lost", app.width/2, app.height/4, fill='white', size = app.width/30)
    retryLabel = Label("Press Enter to Play Again", gameOverLabel.centerX, gameOverLabel.centerY + app.height/8, fill = 'white', size = app.width/30)
    lastScore = Label("Last Score: %d" %(app.level-1), retryLabel.centerX, retryLabel.centerY+app.height/8, fill='white', size=app.width/30)
    hiScore = Label("High Score: %d" %app.hiScore, lastScore.centerX, lastScore.centerY+app.height/8, fill='white', size = app.width/30)
    postGame.add(background, gameOverLabel, retryLabel, lastScore, hiScore)
    

def reset_game():
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
    app.failed = True
    offer_replay()

def check_accuracy():
    for i in range(len(order_player)):
        if(order_player[i] != order_game[i]):
            end_round_fail()
        if(i == len(order_game)-1):
            end_round_win()
            app.timeBetweenComputerAndPlayer = app.stepsPerSecond
            app.lastMode = app.mode
            app.mode = "delay"

def onStep():
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
    if(app.mode == 'player' or app.mode == 'delay'):
        for button in buttons:
            button.border = 'black'

def onKeyPress(key):
    if key == 'enter':
        reset_game()
        
order_game.append(colors[randrange(4)])


app.run()

