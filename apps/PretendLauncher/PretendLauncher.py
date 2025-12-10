import os
import sys
import subprocess
import zipfile
import shutil

try:
    import pyautogui
    import requests
except ImportError as e:
    os.system("pip3 install -r requirements.txt")
    import pyautogui
    import requests

file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(file_path)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
lib_path = os.path.join(rootPath, "libraries")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

def download_zip_file(url, destination_folder, filename):
    '''
    Takes 3 args, a url for the file, a destination folder, and a name to give the file
    Downloads the file found at url, gives it filename as a name and places it in the destination folder
    '''
    file_path = os.path.join(destination_folder, filename)
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
def unzip_all(zip_file_path, destination_directory):
    """
    Takes 2 args, a path to a zip file and a path to the destination folder
    """
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_directory)

try:
    from cmu_graphics import *
except ImportError as e:
    zip_url = 'https://s3.amazonaws.com/cmu-cs-academy.lib.prod/desktop-cmu-graphics/cmu_graphics_installer.zip'  
    output_directory = "../../libraries"
    output_filename = "cmu_graphics_installer.zip"
    download_zip_file(zip_url, output_directory, output_filename)
    unzip_all(output_directory+'/cmu_graphics_installer.zip', output_directory)
    shutil.move(output_directory+"/cmu_graphics_installer/cmu_graphics", "../../libraries")
    os.remove("../../libraries/"+output_filename)
    shutil.rmtree("../../libraries/cmu_graphics_installer")
    from cmu_graphics import *


size = pyautogui.size()
width = size[0]
height = size[1]

app.autofs = 0

shownStats = Group()

app.width = width
app.height = height
app.advanced = False
app.recentDir = None
app.lastX = app.width/2
app.slider = False
app.dragSpeed = (1/80)*width

unknownStats = Group()
knownGames = ["Asteroids.py", "ColorGame.py", "Fireworks.py", "Hangman.py", "Minesweeper.py", "SubGame.py", "MissileCommand.py", "FlappyBat.py", "Simon.py", "Typespeed.py"]
thumbnails = ["../../libraries/Thumbnails/AsteroidsImage.png", "../../libraries/Thumbnails/ColorGameImage.png", "../../libraries/Thumbnails/FireworksImage.png", "../../libraries/Thumbnails/FlappyBatImage.png", "../../libraries/Thumbnails/HangmanImage.png", "../../libraries/Thumbnails/MinesweeperImage.png", "../../libraries/Thumbnails/MissileCommandImage.png", "../../libraries/Thumbnails/SimonImage.png", "../../libraries/Thumbnails/SubGameImage.png", "../../libraries/Thumbnails/TypespeedImage.png"]
images = Group()
unknownGames = []

UnknownGameKeys = ["Unknown Game"]

### Default Values, Keys, Simple Stat Display Keys, Display Values, and General Info about each known and created game. Must update for each additional game made. Add to the known game list and create the necessary values below
SubGameDefault = [0,0,0,0,0,0,0,0,0]
SubGameKeys = ["HighScore", "GamesPlayed", "YellowSubAch", "MinesBlownUp", "TorpsFired", "TorpsHit" ,"PowerUpsCollected", "TimesLaunched", "HideStartScreen"] 
SubGameDisplay = ["High Score", "Games Played", "Mines Destroyed" , "Accuracy", "Powerups Collected"] 
SubGameStatsDisplay = []
SubGameInfoFull = [0,0,0,0,0,0,0,0,0]
HangmanDefault = [0,0,0,0,0,0,0]
HangmanKeys = ["Solved", "Attempted", "ShortestLengthWordSolved", "ShortestLengthWordFailed", "LongestLengthWordSolved", "LongestLengthWordFailed", "TimesLaunched"]
HangmanDisplay = ["Solved", "Attempted", "Success Rate"]
HangmanStatsDisplay = []
HangmanInfoFull =[0,0,0,0,0,0,0]
MinesweeperDefault = [0,0,0,0,0,0,0,0,0,0,0,0,0]
MinesweeperKeys = ["WonEasy", "AttemptedEasy", "WonMedium", "AttemptedMedium", "WonHard", "AttemptedHard" ,"WonTotal", "AttemptedTotal", "Achievement1", "FlagsUsed", "TimesLaunched", "WonCrazy", "AttemptedCrazy"]
MinesweeperDisplay = ["Total Wins", "Total Attempts", "Total Flags Used"]
MinesweeperStatsDisplay = []
MinesweeperInfoFull = [0,0,0,0,0,0,0,0,0,0,0,0,0]
FireworksDefault = [0,0,0,0,0,0,0,0,0,0,0]
FireworksColors = ["White", "Pink", "Red", "Yellow", "Orange", "Green", "Cyan", "Blue", "Magenta"]
FireworksKeys = ["white", "pink", "red", "yellow", "orange", "green", "cyan", "blue", "magenta", "totalPopped", "TimesLaunched"]
FireworksDisplay = ["Favorite Color", "Total Popped", "Times Launched"]
FireworksStatsDisplay = []
FireworksInfoFull =[0,0,0,0,0,0,0,0,0,0,0]
ColorGameDefault = [0,0,0,0,0,0]
ColorGameKeys = ["Correct", "TotalAttempts", "LongestStreak", "GamesPlayed", "TimesLaunched", "HighScore"]
ColorGameDisplay = ["Accuracy", "Longest Streak", "High Score"]
ColorGameStatsDisplay = []
ColorGameInfoFull =[0,0,0,0,0,0]
AsteroidsDefault = [0,0,0,0,0]
AsteroidsKeys = ["Shots", "Hits", "HighScore", "GamesPlayed", "TimesLaunched"]
AsteroidsDisplay = ["Accuracy", "High Score"]
AsteroidsStatsDisplay = []
AsteroidsInfoFull =[0,0,0,0,0]
MissileCommandDefault = [0,0,0,0,0,0,0,0]
MissileCommandKeys = ["HighScore", "GamesPlayed", "Shots", "Hits", "EnemiesDestroyed", "CitiesLost", "TimesLaunched", "HighestLevel"] 
MissileCommandDisplay = ["High Score", "Enemies Destroyed" , "Accuracy", "Cities Lost", "Highest Level"] 
MissileCommandStatsDisplay = []
MissileCommandInfoFull = [0,0,0,0,0,0,0,0]
FlappyBatDefault = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
FlappyBatKeys = ["TimesLaunched", "GamesPlayed", "GamesEasy", "GamesMed", "GamesHard", "HighScoreEasy", "HighScoreMed", "HighScoreHard", "OverallHighScore", "TotalPoints", "AvgEasy", "AvgMed", "AvgHard", "TotalEasy", "TotalMed", "TotalHard"]
FlappyBatDisplay = ["Highest Score", "Favorite Mode", "Average Score"]
FlappyBatStatsDisplay = []
FlappyBatInfoFull = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
SimonDefault = [0,0,0]
SimonKeys = ["HighScore", "GamesPlayed", "TimesLaunched"]
SimonDisplay = ["High Score"]
SimonStatsDisplay = []
SimonInfoFull = [0,0,0]
TypespeedDefault = [0,0,0,0,0,0,0]
TypespeedKeys = ["WordsTyped", "LongestStreak", "HighScore", "GamesPlayed", "TimesLaunched", "WordsMissed", "Mistakes"]
TypespeedDisplay = ["High Score", "Words Typed", "Longest Streak"]
TypespeedStatsDisplay = []
TypespeedInfoFull = [0,0,0,0,0,0,0]
### Default Values, Keys, Simple Stat Display Keys, Display Values, and General Info about each known and created game. Must update for each additional game made. Add to the known game list and create the necessary values above

def file_checking(path, default, gameInfo, game):
    '''
    Takes 3 args, path for which file to look for, 
    default is the default info for the game, 
    gameInfo is a list to put the values from the file into
    returns no values but does update lists
    Looks for necessary game files. Creates and populates the files if they are not found in the expected directory
    Takes the values from the files, whether already existing or new and puts the values into a list for use later
    '''
    counter = 0
    directory = path[:-len(game)]
    if(not os.path.exists(directory)):
        os.makedirs(directory, exist_ok=True)
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
                gameInfo[counter] = ((int)(info))
                counter+=1
 
def find_files_by_extension(directory, extension):
    '''
    Takes 2 args, directory and extension, which are self-explanatory
    Returns a list of strings representing files of the requested extension in the requested directory
    '''
    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            _, file_extension = os.path.splitext(file)
            if file_extension.lower() == extension.lower():
                found_files.append(file)
    return found_files

targetDirectory = "../"
targetExtension = ".py"
games = find_files_by_extension(targetDirectory, targetExtension)

for file in games[:]:
    if file == currentFile:
        games.remove(file)
    elif not (file in knownGames):
        unknownGames.append(file)
        games.remove(file)

app.games = len(games)

def find_favorite_firework_color():
    '''
    Takes no arguments and returns a string representing the most often used color in the fireworks game
    '''
    fav = 0
    for i in range(len(FireworksColors)):
        if FireworksInfoFull[i] > FireworksInfoFull[fav]:
            fav = i
    return FireworksColors[fav]

def find_favorite_game_mode_flappy_bat():
    fav = "Easy"
    if FlappyBatInfoFull[2]>FlappyBatInfoFull[3]:
        if FlappyBatInfoFull[2]>FlappyBatInfoFull[4]:
            fav = 'Easy'
        else:
            fav = "Hard"
    elif FlappyBatInfoFull[3]>FlappyBatInfoFull[4]:
        fav = 'Medium'
    else:
        fav = "Hard"
    return fav

dataPaths = []
keyPaths = []
buttons = []
gameLabels = Group()
default = []
realGameInfoPaths = []
displays = []
realKeys = []
statsDisplay = []

tempList = [SubGameStatsDisplay, HangmanStatsDisplay, MinesweeperStatsDisplay, FireworksStatsDisplay, ColorGameStatsDisplay, AsteroidsStatsDisplay, MissileCommandStatsDisplay, FlappyBatStatsDisplay, SimonStatsDisplay, TypespeedStatsDisplay]

def accuracy_check(indexYes, indexTotal, source, destination, destIndex):
    '''
    Takes 5 args and returns no values, does ipdate lists
    source = list containing raw game info
    destination = list containing abbreviated info
    indexYes = index in source containing hits
    indexTotal = index in source containing attempts
    destIndex = index in destination to store accuracy value
    This function us used to display updated accuracy and avoid division by 0
    '''
    if(source[indexTotal] == 0):
        destination[destIndex] = "0%"
    else:
        destination[destIndex] = ((str)((int)(source[indexYes])*100/ (int)(source[indexTotal]))+"%")
        
def create_all_paths_and_game_buttons(gamesAvailable):
    '''
    Takes 1 argument and returns no values but updates many lists
    gamesAvailable should be a list of strings representing available known games
    This function will iterate through that list and create file paths for stats and keys, 
    create clickable buttons for later launching of the games, and ensure that all lists representing stats are filled in the right order
    '''
    for i in range(len(gamesAvailable)):
        gamePath = gamesAvailable[i]
        data = gamePath[:-3]
        dataPath = data+"Stats.txt"
        keyPath = data+"Keys.txt"
        dataPaths.append("../"+data+"/Files/"+dataPath)
        keyPaths.append("../"+data+"/Files/"+keyPath)
        newButton = Rect(app.left + (i/4)*app.width, app.top, app.width/4,3*(app.width/10), fill = 'gray', border = 'black')
        newButton.game = "../"+data+"/"+gamePath
        buttons.append(newButton)
        for j in range(len(thumbnails)):
            if(data in thumbnails[j]):
                gameImage = Image(thumbnails[j], newButton.left, newButton.top)
                gameImage.width = (int)(width/4)
                gameImage.height = (int)(width/4)
                images.add(gameImage)
        newLabel = Label("Launch "+ data, newButton.centerX, newButton.bottom - 20, bold = True, size = app.width/60, align = 'bottom')
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
        file_checking(dataPaths[i], default[i], realGameInfoPaths[i], dataPath)
        file_checking(keyPaths[i], realKeys[i], [], keyPath)

create_all_paths_and_game_buttons(games)

## Simple Stats
SubGameStatsDisplay+=[SubGameInfoFull[0], SubGameInfoFull[1], SubGameInfoFull[3], 0, SubGameInfoFull[6]]
HangmanStatsDisplay+=[HangmanInfoFull[0], HangmanInfoFull[1], 0]
MinesweeperStatsDisplay+=[MinesweeperInfoFull[6],MinesweeperInfoFull[7],MinesweeperInfoFull[9]]
FireworksStatsDisplay+=[find_favorite_firework_color(), FireworksInfoFull[9], FireworksInfoFull[10]]
ColorGameStatsDisplay+=[0, ColorGameInfoFull[2], ColorGameInfoFull[5]]
AsteroidsStatsDisplay+=[0, AsteroidsInfoFull[2]]
MissileCommandStatsDisplay+=[MissileCommandInfoFull[0], MissileCommandInfoFull[4], 0, MissileCommandInfoFull[5], MissileCommandInfoFull[7]]
FlappyBatStatsDisplay+=[FlappyBatInfoFull[8], find_favorite_game_mode_flappy_bat(), (0 if FlappyBatInfoFull[9]==0 else FlappyBatInfoFull[9]/FlappyBatInfoFull[1])]
SimonStatsDisplay+=[SimonInfoFull[0]]
TypespeedStatsDisplay+=[TypespeedInfoFull[2], TypespeedInfoFull[0], TypespeedInfoFull[1]]
## Simple Stats

accuracy_check(5, 4, SubGameInfoFull, SubGameStatsDisplay, 3)
accuracy_check(0,1,HangmanStatsDisplay, HangmanStatsDisplay, 2)
accuracy_check(0,1,ColorGameInfoFull, ColorGameStatsDisplay, 0)
accuracy_check(1, 0, AsteroidsInfoFull, AsteroidsStatsDisplay, 0)
accuracy_check(3,2, MissileCommandInfoFull, MissileCommandStatsDisplay, 2)

def create_buttons_for_unknown_games():
    '''
    Takes no args and returns no values
    For any .py files found in the diractory that are not known games, 
    this function will create a clickable button to run that file, and a label with the name of the file
    Since it is an unknown file, there are no available stats for it so this launcher will display that the game is unknown in place of stats
    '''
    for i in range(len(unknownGames)):
        gamePath = unknownGames[i]
        data = gamePath[:-3]
        newButton = Rect(app.left + ((i+app.games)/4)*app.width, app.top, app.width/4,app.width/4, fill = 'gray', border = 'black')
        newButton.game = gamePath
        buttons.append(newButton)
        newLabel = Label("Launch "+ data, newButton.centerX, newButton.centerY, size = app.width/55, bold = True)
        gameLabels.add(newLabel)
        unknownLabel = Label(UnknownGameKeys[0], newButton.left, (1/4)*app.width+10, size = 20, align = 'left')
        unknownStats.add(unknownLabel)

create_buttons_for_unknown_games()

statsButton = Rect(0,app.bottom-40, app.width/10, 20, fill = None, border = 'black')
statsLabel = Label("Show Advanced Stats", statsButton.centerX, statsButton.centerY)
sliderLine = Line(0,app.height-10, app.width, app.height-10, fill='grey', lineWidth = 20)
slider = Rect(0, statsButton.bottom, (4/(app.games+len(unknownGames)))*app.width, 20) 
escapeButton = Rect(app.width, app.bottom-40, app.width/10, 20, fill=None, border = "black", align = 'top-right')
excapeLabel = Label("ExitLauncher", escapeButton.centerX, escapeButton.centerY)
nextPage = Rect(app.width, app.bottom-60, app.width/10, 20, fill=None, border = "black", align = 'top-right')
nextPageLabel = Label("Next Page", nextPage.centerX, nextPage.centerY)
prevPage = Rect(0, app.bottom-60, app.width/10, 20, fill=None, border = "black")
nextPageLabel = Label("Prev Page", prevPage.centerX, prevPage.centerY)

def post_advanced_stats():
    '''
    Takes no args, returns no values, but does update a group of shapes
    Displays all stats stored for each known game, under the games clickable launch button, exactly according to the keys
    Does not beautufy or simplify the stats in any way
    '''
    for i in range(len(realGameInfoPaths)):
        for j in range(len(realGameInfoPaths[i])):
            new = Label(realKeys[i][j] + ":", buttons[i].left, buttons[i].bottom + 10 + j*20, align = 'left', size = 20) ## Used to be realKeys[i][j]
            new2 = Label(realGameInfoPaths[i][j], new.right + 5, new.centerY, align = 'left', size = new.size) ## Used to be realGameInfoPaths[i][j]
            shownStats.add(new, new2)

def post_simple_stats():
    '''
    Takes no args, returns no values, but does update a group of shapes
    Displays simplified stats stored for each known game, under the games clickable launch button
    Makes the stats prettier, more polished, and readable. Default option in the launcher
    '''
    for i in range(len(displays)):
        for j in range(len(displays[i])):
            new = Label(displays[i][j] + ":", buttons[i].left, buttons[i].bottom + 10 + j*20, align = 'left', size = 20)
            new2 = Label(statsDisplay[i][1][j], new.right + 5, new.centerY, align = 'left', size = new.size)
            shownStats.add(new, new2)

def onMousePress(x,y):
    '''
    CMU built in function to accept mouse press coordinates
    For this script, a press either toggles stats or launches a game, or simply does nothing if no buttons were pressed
    '''
    if(nextPage.contains(x,y)):
        if(slider.right<app.width):
            for button in buttons:
                button.centerX-=app.width
            shownStats.centerX-=app.width
            gameLabels.centerX-=app.width
            unknownStats.centerX-=app.width
            images.centerX-=app.width
            slider.centerX+=(4/(app.games+len(unknownGames)))*(app.width)
    if(prevPage.contains(x,y)):
        if(slider.left>0):
            for button in buttons:
                button.centerX+=app.width
            shownStats.centerX+=app.width
            gameLabels.centerX+=app.width
            unknownStats.centerX+=app.width
            images.centerX+=app.width
            slider.centerX-=(4/(app.games+len(unknownGames)))*(app.width)        
    if (statsButton.contains(x,y)):
        toggle_stats()
    if (escapeButton.contains(x,y)):
        sys.exit(0)
    for button in buttons:
        if button.contains(x,y):
            subprocess.Popen([sys.executable, button.game])
            sys.exit(0)
          
def onMouseDrag(x,y):
    '''
    Built in CMU function to accept mouse dragging action and coordinates
    For this script, it is used exclusively to control the slider at the bottom of the screen.
    '''
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
                images.centerX+=app.dragSpeed
                slider.centerX-=(4/(app.games+len(unknownGames)))*(app.dragSpeed)
        if(app.recentDir == "right"):
            if(not(buttons[len(buttons)-1].right<=app.width)):
                for button in buttons:
                    button.centerX-=app.dragSpeed
                shownStats.centerX-=app.dragSpeed
                gameLabels.centerX-=app.dragSpeed
                unknownStats.centerX-=app.dragSpeed
                images.centerX-=app.dragSpeed
                slider.centerX+=(4/(app.games+len(unknownGames)))*(app.dragSpeed)
    app.lastX = x
        
def onMouseRelease(x,y):
    '''
    Built in CMU function to accept coordinates of a mouse release
    For this script, used as a disjointed helper for onMouseDrag for slider use
    '''
    app.lastX = x
    app.recentDir = None
    app.slider = False

def toggle_stats():
    '''
    Takes no args and returns no values
    If the simple stats are visible, remove and show advanced stats
    Same is true in reverse
    '''
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

def onStep(): ### Forces Full screen on mac
    if(app.autofs<=4):
        app.autofs += 1
    if(app.autofs == 3):
        pyautogui.keyDown("command")
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        pyautogui.keyUp("command")
        pyautogui.keyUp("ctrl")
    
post_simple_stats()
images.toFront()
gameLabels.toFront()

app.run()