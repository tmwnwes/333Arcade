import os
import sys
from cmu_graphics import *
import tkinter as tk
import subprocess

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(file_path)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)

shownStats = Group()

app.width = width
app.height = height
app.advanced = False
app.recentDir = None
app.lastX = app.width/2
app.slider = False
app.dragSpeed = (1/84)*app.width

unknownStats = Group()
knownGames = ["Asteroids.py", "ColorGame.py", "Fireworks.py", "Hangman.py", "Minesweeper.py", "SubGame.py"]
unknownGames = []

UnknownGameKeys = ["Unknown Game"]

SubGameDefault = [0,0,0,0,0,0,0,0,0]
SubGameKeys = ["HighScore", "GamesPlayed", "YellowSubAch", "MinesBlownUp", "TorpsFired", "TorpsHit" ,"PowerUpsCollected", "TimesLaunched", "HideStartScreen"] 
SubGameDisplay = ["High Score", "Games Played", "Mines Destroyed" , "Accuracy", "Powerups Collected"] 
SubGameStatsDisplay = []
SubGameInfoFull = []
HangmanDefault = [0,0,0,0,0,0,0]
HangmanKeys = ["Solved", "Attempted", "ShortestLengthWordSolved", "ShortestLengthWordFailed", "LongestLengthWordSolved", "LongestLengthWordFailed", "TimesLaunched"]
HangmanDisplay = ["Solved", "Attempted", "Success Rate"]
HangmanStatsDisplay = []
HangmanInfoFull =[]
MinesweeperDefault = [0,0,0,0,0,0,0,0,0,0,0]
MinesweeperKeys = ["WonEasy", "AttemptedEasy", "WonMedium", "AttemptedMedium", "WonHard", "AttemptedHard" ,"WonTotal", "AttemptedTotal", "Achievement1", "FlagsUsed", "TimesLaunched"]
MinesweeperDisplay = ["Total Wins", "Total Attempts", "Total Flags Used"]
MinesweeperStatsDisplay = []
MinesweeperInfoFull = []
FireworksDefault = [0,0,0,0,0,0,0,0,0,0,0]
FireworksColors = ["White", "Pink", "Red", "Yellow", "Orange", "Green", "Cyan", "Blue", "Magenta"]
FireworksKeys = ["white", "pink", "red", "yellow", "orange", "green", "cyan", "blue", "magenta", "totalPopped", "TimesLaunched"]
FireworksDisplay = ["Favorite Color", "Total Popped", "Times Launched"]
FireworksStatsDisplay = []
FireworksInfoFull =[]
ColorGameDefault = [0,0,0,0,0]
ColorGameKeys = ["Correct", "TotalAttempts", "Longest", "GamesPlayed", "TimesLaunched"]
ColorGameDisplay = ["Accuracy", "Longest Run"]
ColorGameStatsDisplay = []
ColorGameInfoFull =[]
AsteroidsDefault = [0,0,0,0,0]
AsteroidsKeys = ["Shots", "Hits", "HighScore", "GamesPlayed", "TimesLaunched"]
AsteroidsDisplay = ["Accuracy", "High Score"]
AsteroidsStatsDisplay = []
AsteroidsInfoFull =[]


def file_checking(path, default, gameInfo):
    if not os.path.exists(path):
        with open(path, 'w') as f:
                f.seek(0)
                for i in range(len(default)):
                    f.write((str)(default[i])+"\n")
    for info in open(path, "r+"):
        if "Keys" in path:
            None
        else:
            info = info.strip()
            if info != '':
                gameInfo.append((int)(info))
 

def find_files_by_extension(directory, extension):
    found_files = []
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path):
            _, file_extension = os.path.splitext(item)
            if file_extension.lower() == extension.lower():
                found_files.append(item)
    return found_files

targetDirectory = "."
targetExtension = ".py"
games = find_files_by_extension(targetDirectory, targetExtension)

for file in games:
    if file == currentFile:
        games.remove(file)
    elif not file in knownGames:
        unknownGames.append(file)
        games.remove(file)

app.games = len(games)


def find_favorite_firework_color():
    fav = 0
    for i in range(len(FireworksColors)):
        if FireworksInfoFull[i] > FireworksInfoFull[fav]:
            fav = i
    return FireworksColors[fav]



dataPaths = []
keyPaths = []
buttons = []
gameLabels = Group()
default = []
realGameInfoPaths = []
displays = []
realKeys = []
statsDisplay = []

tempList = [SubGameStatsDisplay, HangmanStatsDisplay, MinesweeperStatsDisplay, FireworksStatsDisplay, ColorGameStatsDisplay, AsteroidsStatsDisplay]


def accuracy_check(indexYes, indexTotal, source, destination, destIndex):
    if(source[indexTotal] == 0):
        destination[destIndex] = "0%"
    else:
        destination[destIndex] = ((str)((int)(source[indexYes])*100/ (int)(source[indexTotal]))+"%")
        
def create_all_paths_and_game_buttons(gamesAvailable):
    for i in range(len(gamesAvailable)):
        gamePath = gamesAvailable[i]
        data = gamePath[:-3]
        dataPath = "Files/"+data+"Stats.txt"
        keyPath = "Files/"+data+"Keys.txt"
        dataPaths.append(dataPath)
        keyPaths.append(keyPath)
        newButton = Rect(app.left + (i/4)*app.width, app.top, app.width/4,app.width/4, fill = 'gray', border = 'black')
        newButton.game = gamePath
        buttons.append(newButton)
        newLabel = Label("Launch "+ data, newButton.centerX, newButton.centerY)
        gameLabels.add(newLabel)
        for name, value in list(globals().items()):
            if data in name:
                if "Default" in name:
                    default.append(value)
                if "InfoFull" in name:
                    realGameInfoPaths.append(value)
                if "Keys" in name:
                    realKeys.append(value)
                if "StatsDisplay" in name:
                    statsDisplay.append((name, value))
                elif "Display" in name:
                    displays.append(value)
        file_checking(dataPaths[i], default[i], realGameInfoPaths[i])
        file_checking(keyPaths[i], realKeys[i], [])


   
create_all_paths_and_game_buttons(games)

SubGameStatsDisplay+=[SubGameInfoFull[0], SubGameInfoFull[1], SubGameInfoFull[3], 0, SubGameInfoFull[6]]
HangmanStatsDisplay+=[HangmanInfoFull[0], HangmanInfoFull[1], 0]
MinesweeperStatsDisplay+=[MinesweeperInfoFull[6],MinesweeperInfoFull[7],MinesweeperInfoFull[9]]
FireworksStatsDisplay+=[find_favorite_firework_color(), FireworksInfoFull[9], FireworksInfoFull[10]]
ColorGameStatsDisplay+=[0, ColorGameInfoFull[2]]
AsteroidsStatsDisplay+=[0, AsteroidsInfoFull[2]]


accuracy_check(5, 4, SubGameInfoFull, SubGameStatsDisplay, 3)
accuracy_check(0,1,HangmanStatsDisplay, HangmanStatsDisplay, 2)
accuracy_check(0,1,ColorGameInfoFull, ColorGameStatsDisplay, 0)
accuracy_check(1, 0, AsteroidsInfoFull, AsteroidsStatsDisplay, 0)


def create_buttons_for_unKnown_games():
    for i in range(len(unknownGames)):
        gamePath = unknownGames[i]
        data = gamePath[:-3]
        newButton = Rect(app.left + ((i+app.games)/4)*app.width, app.top, app.width/4,app.width/4, fill = 'gray', border = 'black')
        newButton.game = gamePath
        buttons.append(newButton)
        newLabel = Label("Launch "+ data, newButton.centerX, newButton.centerY)
        gameLabels.add(newLabel)
        unknownLabel = Label(UnknownGameKeys[0], newButton.left, (1/4)*app.width+10, size = 20, align = 'left')
        unknownStats.add(unknownLabel)


create_buttons_for_unKnown_games()






statsButton = Rect(0,app.bottom-40, app.width/10, 20, fill = None, border = 'black')
statsLabel = Label("Show Advanced Stats", statsButton.centerX, statsButton.centerY)
sliderLine = Line(0,app.height-10, app.width, app.height-10, fill='grey', lineWidth = 20)
slider = Rect(0, statsButton.bottom, (4/(app.games+len(unknownGames)))*app.width, 20) 













def post_advanced_stats():
    for i in range(len(realGameInfoPaths)):
        for j in range(len(realGameInfoPaths[i])):
            new = Label(realKeys[i][j] + ":", buttons[i].left, 1/4*app.width + 10 + j*20, align = 'left', size = 20) ## Used to be realKeys[i][j]
            new2 = Label(realGameInfoPaths[i][j], new.right + 5, new.centerY, align = 'left', size = new.size) ## Used to be realGameInfoPaths[i][j]
            shownStats.add(new, new2)

def post_simple_stats():
    for i in range(len(displays)):
        for j in range(len(displays[i])):
            new = Label(displays[i][j] + ":", buttons[i].left, 1/4*app.width + 10 + j*20, align = 'left', size = 20)
            new2 = Label(statsDisplay[i][1][j], new.right + 5, new.centerY, align = 'left', size = new.size)
            shownStats.add(new, new2)

def onMousePress(x,y):
    if (statsButton.contains(x,y)):
        toggle_stats()
    for button in buttons:
        if button.contains(x,y):
            subprocess.Popen(["python3", button.game])
            sys.exit(0)
          
def onMouseDrag(x,y):
    if(slider.contains(x,y)):
        app.slider = True
    if(app.slider == True):
        if(x > app.lastX):
            app.recentDir = 'right'
        if(x < app.lastX):
            app.recentDir = 'left'
        if(app.recentDir == 'left'):
            if(not(buttons[0].left>=0)):
                for button in buttons:
                    button.centerX+=app.dragSpeed
                shownStats.centerX+=app.dragSpeed
                gameLabels.centerX+=app.dragSpeed
                unknownStats.centerX+=app.dragSpeed
                slider.centerX-=(4/(app.games+len(unknownGames)))*(app.dragSpeed)
        if(app.recentDir == "right"):
            if(not(buttons[len(buttons)-1].right<=app.width)):
                for button in buttons:
                    button.centerX-=app.dragSpeed
                shownStats.centerX-=app.dragSpeed
                gameLabels.centerX-=app.dragSpeed
                unknownStats.centerX-=app.dragSpeed
                slider.centerX+=(4/(app.games+len(unknownGames)))*(app.dragSpeed)
    app.lastX = x
        
def onMouseRelease(x,y):
    app.lastX = x
    app.recentDir = None
    app.slider = False

def toggle_stats():
    if app.advanced == True:
        app.advanced = False
        shownStats.clear()
        post_simple_stats()
        statsLabel.value = "Show Advanced Stats"
    else:
        app.advanced = True
        shownStats.clear()
        post_advanced_stats()
        statsLabel.value = "Show Simple Stats"

post_simple_stats()
gameLabels.toFront()
app.run()




