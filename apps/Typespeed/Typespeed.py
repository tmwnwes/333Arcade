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
gameName = currentFile[:-3]
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
closeGameButton = Rect(0,app.height, (1/10)*app.width, (1/10)*app.height, fill=None, border = 'black', align = 'bottom-left')
launcherButton = Rect(app.width,app.height, (1/10)*app.width, (1/10)*app.height, fill=None, border = 'black', align = 'bottom-right')
launcherButton.game = "PretendLauncher/PretendLauncher.py"
closeGameLabel = Label("Close game", closeGameButton.centerX, closeGameButton.centerY, fill='red', size = 15)
launcherLabel = Label("Return to Launcher", launcherButton.centerX, launcherButton.centerY, fill='black', size = 15)


default = [0,0,0,0,0,0,0]
keys = ["WordsTyped", "LongestStreak", "HighScore", "GamesPlayed", "TimesLaunched", "WordsMissed", "Mistakes"]
fullInfoList = []

words = open("../../libraries/words_alpha.txt", "r", -1)
wordList = []
for thing in words:
    thing = thing.strip()
    wordList.append(thing)




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
    if("Stats" in properPath):
        with open(properPath, "r+") as gameInfo:
            for thing in gameInfo:
                thing = thing.strip()
                if thing != '':
                    fullInfoList.append((int)(thing))
            if(len(default)>len(fullInfoList)):
                keysFile = open("Files/"+gameName+"Keys.txt", "r+")
                start = len(fullInfoList)
                for i in range(start,len(default)):
                    fullInfoList.append(default[i])
                    gameInfo.seek(0,2)
                    gameInfo.write((str)(fullInfoList[i])+"\n")
                    keysFile.seek(0,2)
                    keysFile.write(keys[i] + "\n")

file_checking(gameName+"Stats.txt", default)
file_checking(gameName+"Keys.txt", keys)

app.failed = False
gameInfo = open("Files/TypespeedStats.txt", "r+")


app.score = 0
yourScore = Label("Score: %d" %app.score, 10, (1*(app.height/20)), size = app.width/50, align = 'top-left')
app.hiScore = fullInfoList[2]
yourHiScore = Label("High Score: %d" %app.hiScore, app.width-10, (1*(app.height/20)), size = app.width/50, align = 'top-right')

def move_words(speed):
    '''
    Takes 1 arg: speed which is a number (float or int is fine)
    Moves all words to the right by that number of pixels every call
    Returns no values
    '''
    for word in activeStrings:
        word.centerX += speed
        if(word.left>width):
            activeStrings.remove(word)
            fullInfoList[5]+=1
            app.runAway += 1
            

def check_loss():
    '''
    Takes no args and returns no values
    When called, check if too many words have passed to the side of the screen
    If so, decrease multiplier. If that is impossible, the round is over.
    '''
    if(app.runAway >= app.level*5):
        if(app.level == 1):
            app.failed = True
            background = Rect(0,0,app.width, app.height)
            gameOverLabel = Label("Game Over", app.width/2, app.height/4, fill='white', size = app.width/30)
            retryLabel = Label("Press Space to Play Again", gameOverLabel.centerX, gameOverLabel.centerY + app.height/8, fill = 'white', size = app.width/30)
            lastScore = Label("Last Score: %d" %(app.score), retryLabel.centerX, retryLabel.centerY+app.height/8, fill='white', size=app.width/30)
            hiScore = Label("High Score: %d" %app.hiScore, lastScore.centerX, lastScore.centerY+app.height/8, fill='white', size = app.width/30)
            gameOver.add(background, gameOverLabel, retryLabel, lastScore, hiScore)
        else:
            app.runAway = 0
            app.level -= 1

def onStep():
    '''
    Built in CMU function which calls body code app.stepsPerSecond many times every second
    Used in this game to spawn and move words, update score, check for losing status
    '''
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
    '''
    Takes are arg a number, howMany, which must be an int
    Returns no values, but does create howMany random words, up to 8 maximum
    '''
    for i in range(howMany):
        if(i<=8):
            newWord = wordList[randrange(len(wordList))]
            newLabel = Label(newWord, -100, randrange((1*app.height//10), (9*app.height//10)), fill = colors[randrange(len(colors))], size = app.width/40)
            activeStrings.add(newLabel)
            yourScore.left = 10
            yourHiScore.right = app.width-10
    update_stats()
    
def check_word(word):
    '''
    Takes are argument a string called word
    Returns no values, but checks if that string matches any strings on the screen. 
    If it matches, score incremented and other checks are made
    Else, end streak and derease multiplier
    
    '''
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
        fullInfoList[6]+=1
        if(app.level>=4):
            app.level-=3
            app.runAway = 0
        else:
            app.level = 1
    else:
        app.streak+=1
    if(app.streak%5 == 0 and app.streak != 0):
        app.level+=1
    update_stats()

def reset_game():
    '''
    Takes no args and returns no values
    Should only be called if player has lost the round
    Resets all game variables to default values and begins again
    '''
    app.runAway = 0
    app.currentWord = ''
    gameOver.clear()
    app.level = 1
    app.score = 0
    fullInfoList[3] += 1
    activeStrings.clear()
    app.yourWord.value = app.currentWord
    app.failed = False
    update_stats()

def update_stats():
    '''
    Takes no arguments and returns no values
    Updates stores stats in the associated text file
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")         
        
def onKeyPress(key):
    '''
    CMU built in funciton which takes a pressed key as an argument
    Used on this game to allow for word typing, checking, and resetting the game
    '''
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

def onMousePress(x,y):
    '''
    Built in CMU function taking coordinates of a mouse press as argument
    Used in this game to close the game or return to launcher
    '''
    if closeGameButton.contains(x,y):
        update_stats()
        sys.exit(0)
    if(launcherButton.contains(x,y)):
        update_stats()
        os.chdir("../")
        subprocess.Popen([sys.executable, launcherButton.game])
        sys.exit(0)


fullInfoList[3]+=1
fullInfoList[4]+=1
update_stats()
app.run()