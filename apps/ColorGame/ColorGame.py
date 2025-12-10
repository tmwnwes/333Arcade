import os
import sys
import subprocess
import zipfile
import shutil

file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(file_path)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)
gameName = currentFile[:-3]
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
lib_path = os.path.join(rootPath, "libraries")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

try:
    import pyautogui
    import requests
except ImportError as e:
    os.system("pip3 install -r requirements.txt")
    import pyautogui
    import requests

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


app.width = width
app.height = height

default = [0,0,0,0,0,0]
keys = ["Correct", "TotalAttempts", "LongestStreak", "GamesPlayed", "TimesLaunched", "HighScore"]
fullInfoList =[]


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


gameInfo = open("Files/ColorGameStats.txt", "r+")

app.hi = fullInfoList[5]

app.time = 1000
app.score = 0
app.stepsPerSecond = 45
app.timeSince = app.stepsPerSecond*3
app.att = 0
app.failed = False
app.currentStreak = 0
oTime = Label("Overall Time: %1.1f" %(app.time/app.stepsPerSecond), 5, (3/80)*app.height, size = (1/40)*app.width, align = 'left')
score = Label("Score: %1d" %app.score, app.width, (3/80)*app.height, size = (1/20)*app.width, align = 'right')
hiScore = Label("High Score: %1d" %app.hi, app.width, (1/10)*app.height, size =(1/20)*app.width, align = 'right')
words = ['blue', 'cyan', 'teal', 'orange', 'red', 'magenta', 'gray', 'black', 'pink', 'purple', 'brown', 'yellow', 'lime', 'khaki', 'indigo', 'green', 'gold', 'silver', 'bronze', 'lemon', 'white', 'gray', 'olive', 'turquoise', 'crimson', 'aqua']
colors = ['blue', 'cyan', 'teal', 'orange', 'red', 'magenta', 'gray', 'black', 'pink', 'purple', 'brown', 'yellow', 'lime', 'khaki', 'indigo']

escapeButton = Rect(3*app.width/8, 0, app.width/8, app.height/10, fill=None, border = 'red')
escapeLabel = Label("Close Game", escapeButton.centerX, escapeButton.centerY, size = 15)
backToLauncher = Rect(4*app.width/8, 0, app.width/8, app.height/10, fill=None, border = 'gray')
backToLauncher.game = "PretendLauncher/PretendLauncher.py"
launcherLabel = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 15)
leaving = Group(escapeButton, escapeLabel, backToLauncher, launcherLabel)
gameOver = Group()

massiveWord = Label('word', app.width/2, (1/5)*app.height, size = (3/20)*app.width)
infoLabel = Label("Current Time: %1.1f" %(app.timeSince/app.stepsPerSecond), 5, (3/40)*app.height, size = (1/40)*app.width, align = 'left')
buttons = Group()
int = 0
for i in range(3):
    for j in range(5):
        buttons.add(Rect(i*(3/10)*app.width + (3/40)*app.width, j*(3/40)*app.height + (3/5)*app.height, (1/4)*app.width, (1/20)*app.height, fill = colors[int]))
        int += 1
        

def update_stats():
    '''
    Takes no args and returns no values
    Updates stats about the user's play session and 
    Writes that info to the external stats files
    '''
    if(app.currentStreak>fullInfoList[2]):
        fullInfoList[2] = app.currentStreak
    if app.score>fullInfoList[5]:
        fullInfoList[5] = app.score
        app.hi = app.score
        score.right = app.width
        hiScore.right = app.width
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")  

def end_game():
    '''
    Takes no args and returns no values
    Displays score and accuracy stats from the round that just ended
    Should only be called if user lost the round
    Adds shapes to appropriate group
    '''
    massiveWord.visible = False
    accuracy = (100 * (app.score / app.att))
    a = Rect(0,0,app.width,app.height, fill='white')
    b = Rect((1/5)*app.width, (1/4)*app.height, (3/5)*app.width, (9/20)*app.height, fill=None, border = 'red', borderWidth = 2)
    c = Label("Game Over", app.width/2, (2/5)*app.height, size = 30, fill='red')
    sco = Label("Score: ", (9/20)*app.width, (19/40)*app.height, size = (1/20)*app.width)
    acc = Label("Accuracy: ", (9/20)*app.width, (11/20)*app.height, size = (1/20)*app.width)
    d = Label(app.score, sco.right + (3/100)*app.width, sco.centerY, size = (1/20)*app.width)
    num = Label("%02d" %accuracy, acc.right+ (1/40)*app.width ,(11/20)*app.height, size = (1/20)*app.width)
    e = Label("%", num.right + (1/40)*app.width, (11/20)*app.height, size = (1/20)*app.width)
    f = Label("Press Enter to Restart", app.width/2, num.centerY+(1/10)*app.height, size = (1/20)*app.width)
    gameOver.add(a, b, c, d, e, f, sco, acc, num)
    app.failed = True

def reset_word():
    '''
    Takes no args and returns no values
    Resets the 
    '''
    massiveWord.value = words[randrange(len(words))]
    massiveWord.fill = colors[randrange(len(colors))]
    update_stats()
    
def check_button(colInput):
    '''
    Takes 1 arg and returns no values
    colInput is the color of the button the user pressed
    Determines if the button was the correct button to press
    '''
    app.att+=1
    if(colInput == massiveWord.fill):
        app.score += 1
        if(app.time<=app.stepsPerSecond*59):
            app.time += app.stepsPerSecond
        else:
            app.time = app.stepsPerSecond * 60
        app.currentStreak+=1
        fullInfoList[0]+=1
    else:
        app.time -= app.stepsPerSecond*3
        app.currentStreak = 0
    
def onMousePress(x,y):
    '''
    CMU built in function which takes an x,y coordinate pair of a mouse click
    In this script, used to actually play the game by clicking on the colored buttons. Also allows user to click on a button to close the game.
    '''
    for button in buttons:
        if(button.contains(x,y)):
            app.timeSince = app.stepsPerSecond*2
            check_button(button.fill)
            reset_word()
            fullInfoList[1]+=1
    if(backToLauncher.contains(x,y)):
        update_stats()
        os.chdir("../")
        subprocess.Popen([sys.executable, backToLauncher.game])
        sys.exit(0)
    if(escapeButton.contains(x,y)):
        update_stats()
        sys.exit(0)
    
def check_time():
    '''
    Takes no args and returns no values
    Uses time values to determine if the round is over or if a new word needs to be created
    '''
    if(app.time <= 0):
        end_game()
    if(app.timeSince<=0):
        app.timeSince = app.stepsPerSecond*2
        app.time -= app.stepsPerSecond*3
        app.att += 1
        reset_word()
        fullInfoList[1]+=1
        app.currentSrteak = 0
        
def full_reset():
    '''
    Takes no args and returns no values
    Should only be called if the user has lost the round and chosen to restart
    resets time, resets score, and resets counters
    '''
    fullInfoList[3]+=1
    app.score = 0
    app.time = 1000
    app.timeSince = app.stepsPerSecond*2
    app.att = 0
    gameOver.clear()
    app.failed = False
    massiveWord.visible = True
    reset_word()
    

def onKeyPress(key):
    '''
    Built in CMU function which takea a key as an argument
    Used in this script exclusively to reset the game after a round is lost    
    '''
    if(key == 'enter'):
        if(app.failed == True):
            full_reset()

def onStep():
    '''
    Built in CMU function which calls all of the body code app.stepsPerSecond many times per second
    Used in this script to descrement timeers and show scores
    '''
    if(app.autofs<=1): ## Forces mac fullscreen
        app.autofs += 1
    if(app.autofs == 1):
        pyautogui.keyDown("command")
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        pyautogui.keyUp("command")
        pyautogui.keyUp("ctrl")
    if(app.failed == False):
        check_time()
        app.time -= 1
        app.timeSince -= 1
        infoLabel.value = "Current Time: %1.1f" %(app.timeSince/app.stepsPerSecond)
        oTime.value = "Overall Time: %1.1f" %(app.time/app.stepsPerSecond)
        score.value = "Score: %1d" %app.score
        hiScore.value = "High Score: %1d" %app.hi
    
fullInfoList[3]+=1
fullInfoList[4]+=1
reset_word()
fullInfoList[1]+=1
gameOver.toFront()
leaving.toFront()

app.run()