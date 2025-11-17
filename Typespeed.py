from cmu_graphics import *
import sys
import subprocess
import random
import math
import os
import pyautogui

size = pyautogui.size()
width = size[0]
height = size[1]

app.width = width
app.height = height
app.autofs = 0
app.currentWord = ''
app.level = 1
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
colors = ['blue', 'cyan', 'teal', 'orange', 'red', 'magenta', 'gray', 'black', 'pink', 'purple', 'brown', 'yellow', 'lime', 'khaki', 'indigo']
activeStrings = Group()
app.streak = 0
app.speed = app.width/1500
app.timer = 0
app.spawnTime = app.stepsPerSecond * 5
app.yourWord = Label("", app.width/2, 1*(app.height/20), size = app.width/30, align = 'top')
app.multLabel = Label("Mulitplier: %d" %app.level, (app.width/2), (19*(app.height/20)), size = app.width/80, align = 'bottom')
app.runAway = 0
gameOver = Group()


default = [0,0,0,0,0,0,0]
keys = ["WordsTyped", "LongestStreak", "HighScore", "GamesPlayed", "TimesLaunched", "WordsMissed", "Mistakes"]


words = open("Files/words_alpha.txt", "r", -1)
wordList = []
for thing in words:
    thing = thing.strip()
    wordList.append(thing)



file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(file_path)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)
gameName = currentFile[:-3]

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

app.failed = False
gameInfo = open("Files/TypespeedStats.txt", "r+")
fullInfoList = [] 
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))

app.score = 0
yourScore = Label("Score: %d" %app.score, 10, (1*(app.height/20)), size = app.width/50, align = 'top-left')
app.hiScore = fullInfoList[2]
yourHiScore = Label("High Score: %d" %app.hiScore, app.width-10, (1*(app.height/20)), size = app.width/50, align = 'top-right')

def move_words(speed):
    for word in activeStrings:
        word.centerX += speed
        if(word.left>width):
            activeStrings.remove(word)
            fullInfoList[5]+=1
            app.runAway += 1

def check_loss():
    if(app.runAway >= 30):
        app.failed = True
        background = Rect(0,0,app.width, app.height)
        gameOverLabel = Label("Game Over", app.width/2, app.height/4, fill='white', size = app.width/30)
        retryLabel = Label("Press Space to Play Again", gameOverLabel.centerX, gameOverLabel.centerY + app.height/8, fill = 'white', size = app.width/30)
        lastScore = Label("Last Score: %d" %(app.score), retryLabel.centerX, retryLabel.centerY+app.height/8, fill='white', size=app.width/30)
        hiScore = Label("High Score: %d" %app.hiScore, lastScore.centerX, lastScore.centerY+app.height/8, fill='white', size = app.width/30)
        gameOver.add(background, gameOverLabel, retryLabel, lastScore, hiScore)

def onStep():
    if(app.failed == False):
        if(app.autofs<=6):
            app.autofs +=1
        if(app.autofs ==2):
            pyautogui.keyDown("command")
            pyautogui.keyDown("ctrl")
            pyautogui.press('f')
            pyautogui.keyUp("ctrl")
            pyautogui.keyUp("command")
        if(app.autofs==3):
            app.currentWord = ''
            app.yourWord.value = ''
        app.timer+=1
        if(app.timer%app.spawnTime == 0):
            num = app.level*3
            spawn_words(num)
        move_words(app.speed)
        yourHiScore.value = "High Score: %d" %app.hiScore
        yourScore.value = "Score: %d" %app.score
        app.multLabel.value = "Multiplier: %d" %app.level
        check_loss()
        
        
def spawn_words(howMany):
    for i in range(howMany):
        if(i<=8):
            newWord = wordList[randrange(len(wordList))]
            newLabel = Label(newWord, -100, randrange((1*app.height//10), (9*app.height//10)), fill = colors[randrange(len(colors))], size = app.width/40)
            activeStrings.add(newLabel)
            yourScore.left = 10
            yourHiScore.right = app.width-10
    update_stats()
    
def check_word(word):
    if(app.streak>fullInfoList[1]):
        fullInfoList[1] = app.streak
    count = 0
    for string in activeStrings:
        if(word == string.value):
            activeStrings.remove(string)
            app.score+=len(word)*app.level
            fullInfoList[0]+=1
            app.runAway = 0
            if(app.score>app.hiScore):
                app.hiScore = app.score
                fullInfoList[2] = app.hiScore
            count+=1
    if(count == 0):
        app.streak = 0
        app.level = 1
        fullInfoList[6]+=1
    else:
        app.streak+=1
    if(app.streak%5 == 0 and app.streak != 0):
        app.level+=1
    update_stats()

def reset_game():
    app.runAway = 0
    app.currentWord = ''
    gameOver.clear()
    app.level = 1
    app.score = 0
    fullInfoList[3] += 1
    activeStrings.clear()
    app.yourWord.value = app.currentWord
    app.failed = False

def update_stats():
    '''
    Takes no arguments and returns no values
    Updates stores stats in the associated text file
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")         
        
def onKeyPress(key):
    if(key == 'enter'):
        check_word(app.currentWord)
        app.currentWord = ''
    if(key == 'backspace' and len(app.currentWord)>0):
        app.currentWord = app.currentWord[:-1]
    elif key in letters:
        app.currentWord += key
    if(app.failed == True):
        if(key == 'space'):
            reset_game()
    app.yourWord.value = app.currentWord

fullInfoList[3]+=1
fullInfoList[4]+=1
update_stats()
app.run()