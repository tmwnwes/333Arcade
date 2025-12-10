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
app.autofs = 0

app.typeyTime = False

app.width = width
app.height = height

wordList = open("../../libraries/words_alpha.txt", "r", -1) ### 365k words, incliuding names, places, plurals, and weird old english words like symphysy
words = []
words2 = []

default = [0,0,0,0,0,0,0]
keys = ["Solved", "Attempted", "ShortestLengthWordSolved", "ShortestLengthWordFailed", "LongestLengthWordSolved", "LongestLengthWordFailed", "TimesLaunched"]
fullInfoList = []


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

gameInfo = open("Files/HangmanStats.txt", "r+")

    
app.paused = False
app.case = 0 ## Default is case 0. This is a solution to a lack of proper update upon clicks. While in case 0, everything will run, then run again and place into case 1, then run everything, and go back to case 0
app.otherCase = 0 ## Doesn't cheat until the first letter is found, at which point this will update to 1
app.over = 0 ## Standard case is 0, will be 1 if and only if the user has won or lost the game, this exists as a way to allow a continuation without closing and restarting the program
app.minLengthWord = 5
app.mode = "easy"


## Cleaning up the list
for thing in wordList: 
    thing = thing.strip()
    words.append(thing)


word = words[randrange(len(words))] # pick a word



app.wordLength = len(word)
wordPattern = []

for i in range(app.wordLength):
    wordPattern.append('0')

wordy = [word] ## wordy is a list containing every iteration of the word, beginning obviously with the 1st word

def get_same_length(wordLength):
    '''
    Takes a number, wordLength, as an arg
    returns list of words as a subset of the words list which have the same length
    '''
    temp = []
    for wd in words:
        if len(wd) == wordLength:
            temp.append(wd) 
    return temp
     
words2 = get_same_length(app.wordLength)   

def pattern_check(list, pattern):
    '''
    Takes 2 args:
    list: Current possible words
    pattern: list containing letters in their position which must be matched to by possible words
    Returns a list containing only words which were both in the original list AND matched the pattern    
    '''
    accepted = list
    bad = []
    for wd in accepted:
        for i in range(len(pattern)):
            if(not(pattern[i] == '0')):
                if(not(wd[i] == pattern[i])):
                    bad.append(wd)
            else:
                if(wd[i] in yesLetters):
                    bad.append(wd)            
    for wd in bad:
        if wd in accepted:
            accepted.remove(wd)
    return accepted

def pick_new_word(yes, no, pattern, letter):
    '''
    Takes 4 args:
    yes: list containing included letters
    no: list containing letters not in word
    pattern: list containing revealed letters in their position that must be matched to by any other possible words
    letter: most recently guessed letter   
    Returns no values but does update lists and potentially current word 
    '''
    temp = []
    bad = []
    withit = []
    without = []
    global words2
    global wordPattern
    for wd in words2:
        if len(wd) == app.wordLength:
            temp.append(wd)
    for wd in temp:
        for i in range(len(no)):
            if (no[i] in wd):
                bad.append(wd)
    for wd in temp:
        for i in range(len(yes)):
            if not((yes[i]) in wd):
                bad.append(wd)
    for badWord in bad:
        if badWord in temp:
            temp.remove(wd)
    temp = pattern_check(temp, pattern)
    for wd in temp:
        if letter in wd:
            withit.append(wd)
        else: 
            without.append(wd)
    withoutLength = len(without)
    if(withoutLength>0):
        words2 = without
        wordy.append(words2[randrange(withoutLength)])
        noLetters.append(letter)
    else:
        words2 = withit
        yesLetters.append(letter)
        for i in range(app.wordLength):
            if wordy[len(wordy)-1][i] == letter:
                wordPattern[i] = letter
            
gameLetters = Group()

underlines = Group()

def create_Word():
    '''
    Takes no args and returns no values
    Creates the spaces for the letters in the word as well as the letters from the word
    '''
    gameLetters.clear()
    underlines.clear()
    for i in range(app.wordLength):
        new = Label(wordPattern[i], (i* ((3/80)*app.width) + (3/80 * app.width)), 0, size = (1/20)*app.width, opacity = 0) ##????
        underline = Line((i* ((15/400)*app.width) + (9/400 * app.width)), (0.17*app.height), (i * (15/400)*app.width + (21/400)*app.width), (0.17*app.height), lineWidth = (1/200)*app.width)
        new.bottom = (0.16*app.height)
        gameLetters.add(new)
        underlines.add(underline)
        for j in gameLetters:
            if j.value != '0':
                j.opacity = 100
create_Word()

rects = Group()
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x' ,'y', 'z']
letterLabels = Group()
app.wrongCount = 0        

def make_alphabet():
    '''
    Takes no args and returns no values
    Creates the set of letters on the right side of the screen
    '''
    global rects
    global letterLabels
    int = 0
    rects.clear()
    letterLabels.clear()
    for i in range (9):
        for j in range(3):
            if(i*j != 16):
                new = Rect(((j*(9/80) * app.width)+((5.0/8)*app.width) + (1/20)*app.width), (i*(9/80)* app.height), app.width/10, app.height/10, fill = 'white', border = "black", borderWidth = 3)
                new.letter = letters[int]
                rects.add(new)
                int+=1
    for rect in rects:
        letterLabels.add(Label(rect.letter, rect.centerX, rect.centerY, size = 20))
make_alphabet()


base = Rect(0, (39/40)*app.height, (3/10)*app.width, (1/40)*app.height)
pole = Rect((11/80)*app.width, (1/4)*app.height, (1/40)*app.width, (29/40)*app.height)
lever = Rect((13/80)*app.width, (1/4)*app.height, (5/16)*app.width, (1/40)*app.height)
knot = Rect((9/20)*app.width, (11/40)*app.height ,(1/40)*app.width, (1/16)*app.height)

head = Circle((37/80)*app.width, (33/80)*app.height, (3/40)*app.width, fill = None, border = 'black', borderWidth = (1/100)*app.width, opacity = 0)
head.top = knot.bottom
body = Line((37/80)*app.width,head.bottom,(37/80)*app.width,head.bottom+(1/5)*app.height, lineWidth = (1/100)*app.width, opacity = 0)
leftLeg = Line(body.x2, body.y2, head.left, body.y2+(1/10)*app.height, lineWidth = (1/100)*app.width, opacity = 0)
rightLeg = Line(body.x2, body.y2, head.right, body.y2+(1/10)*app.height, lineWidth = (1/100)*app.width, opacity = 0)
leftArm = Line(body.x1, (body.y1+ body.y2)/2, head.left, body.y1, lineWidth = (1/100)*app.width, opacity = 0)
rightArm = Line(body.x1, (body.y1+ body.y2)/2, head.right, body.y1, lineWidth = (1/100)*app.width, opacity = 0)
leftEye = Circle((35/80)*app.width, (2/5)*app.height, (1/100)*app.width, opacity = 0)
rightEye = Circle((39/80)*app.width, (2/5)*app.height, (1/100)*app.width, opacity = 0)
mouth = Arc((37/80)*app.width, (37/80)*app.height, (7/80)*app.width, (1/20)*app.height, -50, 100, fill = None, border='black', borderWidth = (1/200)*app.width, opacity = 0)
person = Group(head, body, leftArm, rightArm, rightArm, leftLeg, rightLeg, leftEye, rightEye, mouth)


yesLetters = []
noLetters = []

def validate_words():
    '''
    Takes no args and returns no values
    Updates lists with valid words
    '''
    temp = []
    global words2
    for wd in words2:
        for i in range(len(noLetters)):
            if noLetters[i] in wd:
                temp.append(wd)
    for badWord in temp:
        if badWord in words2:
            words2.remove(badWord)
            
 
 
def update_stats():
    '''
    Takes no arguments and returns no values
    Updates values relating to stored stats outside of the program
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")           
            
            
def reset_all():
    '''
    Takes no args and returns no values
    Resets all values to beginning values and picks a new starting word, updating lists to match
    Also updates stats
    '''
    global words2
    app.over = 0
    app.otherCase = 0
    app.wrongCount = 0
    for part in gameOver:
        part.opacity = 0
    for part in person:
        part.opacity = 0
    noLetters.clear()
    yesLetters.clear()
    wordPattern.clear()
    word = words[randrange(len(words))]
    wordy.clear()
    wordy.append(word)
    app.wordLength = len(word)
    for i in range(app.wordLength):
        wordPattern.append('0')
    words2 = get_same_length(app.wordLength)
    create_Word()
    make_alphabet()
    failScreen.clear()
    winScreen.clear()
    fullInfoList[1]+=1
    update_stats()       

def onMousePress(x,y):
    '''
    Built in CMU function which takes the coordinates of a mouse press as argument
    Used in this game to press buttons to guess letters, start new round or close game
    '''
    if app.over == 1:
        if button.contains(x,y):
            reset_all()
    else:
        validate_words()
        temp = wordy[len(wordy)-1]
        pattern_check(words2, wordPattern)
        for rect in rects:
            for let in letterLabels:
                if(rect.contains(x,y)):
                    if(let.value == rect.letter):
                        if(let.value in wordy[len(wordy)-1]):
                            if app.otherCase == 1:
                                pick_new_word(yesLetters, noLetters, wordPattern, let.value)
                            if (temp == wordy[len(wordy)-1]):
                                for i in range(app.wordLength):
                                    if temp[i] == let.value:
                                        wordPattern[i] = temp[i]
                                let.fill = 'lime'
                                letter_reveal(let.value)
                                app.otherCase = 1
                            else: 
                                let.fill = 'red'
                        elif(not(let.value in wordy[len(wordy)-1])):
                            noLetters.append(let.value)
                            validate_words()
                            let.fill = 'red'
                    rect.opacity = 25
        check_count()
        body_add()
        if app.case == 0:
            app.case = 1
            onMousePress(x,y)
        app.case = 0
    update_stats()
    if(closeGameButton.contains(x,y)):
        update_stats()
        sys.exit(0)
    if(backToLauncher.contains(x,y)):
        update_stats()
        os.chdir("../")
        subprocess.Popen([sys.executable, backToLauncher.game])
        sys.exit(0)

def check_count():
    '''
    Takes no args and returns no values
    Updates count of wrong letters and checks if the word has been guessed completely
    '''
    app.wrongCount = 0
    for let in letterLabels:
        if(let.fill=='red'):
            app.wrongCount+=1
    if(not("0" in wordPattern)):
        win_round()
        app.over = 1
        offer_to_play_again()

winScreen = Group()

def onKeyPress(key):
    '''
    Built in CMU function which takes a pressed key as argument
    Used in this game to press the button matching the letter pressed
    '''
    if(app.typeyTime == True):
        for letter in letterLabels:
            if key.lower() == letter.value:
                onMousePress(letter.centerX, letter.centerY)

def win_round():
    '''
    Takes no args and returns no values
    Should only be called if player has won the round
    Creates shapes and adds them to appropriate groups
    '''
    fullInfoList[0]+=1
    if(len(wordy[len(wordy)-1])>fullInfoList[4]):
        fullInfoList[4] = len(wordy[len(wordy)-1])
    if(len(wordy[len(wordy)-1])<fullInfoList[2] or fullInfoList[2] == 0):
        fullInfoList[2] = len(wordy[len(wordy)-1])
    update_stats()
    winScreen.add(Rect((1/5)*app.width, (13/20)*app.height, (1/5)*app.width, (1/10)*app.height, fill=None))
    winScreen.add(Label("You Win", (3/10)*app.width, (7/10)*app.height, size = (1/40)*app.width))


button = Rect((1/5)*app.width, (3/10)*app.height, (1/6)*app.width, (1/8)*app.height, fill = None, borderWidth = (1/200)*app.width, border = 'black', opacity = 0)
question = Label("Try Again?", button.centerX, button.centerY, size = 1/30 * app.width, opacity = 0)
gameOver = Group(button, question)

def offer_to_play_again():
    '''
    Takes no args and returns no values
    Should only be called if player has lost the round.
    Unhides game over screeen
    '''
    for part in gameOver:
        part.opacity = 100

def body_add():
    '''
    Takes no args and returns no values
    Called whenever player guesses a wrong letter
    Unhides a body part to show advancement towards failure
    '''
    if(app.wrongCount>=1):
        head.opacity = 100
    if(app.wrongCount>=2):
        body.opacity = 100
    if(app.wrongCount>=3):
        leftLeg.opacity = 100
    if(app.wrongCount>=4):
        rightLeg.opacity = 100
    if(app.wrongCount>=5):
        leftArm.opacity = 100
    if(app.wrongCount>=6):
        rightArm.opacity = 100
    if(app.wrongCount>=7):
        leftEye.opacity = 100
    if(app.wrongCount>=8):
        rightEye.opacity = 100
    if(app.wrongCount>=9):
        mouth.opacity = 100
        fail_game()
        app.over = 1
        offer_to_play_again()
        
failScreen = Group()

def fail_game():
    '''
    Takes no args and returns no values
    Creates shapes and adds them to appropriate groups
    Should only be called if player has lost the round
    Also update stats    
    '''
    failScreen.add(Rect((3/20)*app.width,(3/5)*app.height,(7/20)*app.width,(3/20)*app.height, fill=None))
    failScreen.add(Label("You failed", (13/40)*app.width, (21/32)*app.height, size = (1/30)*app.width))
    failScreen.add(Label(wordy[len(wordy)-1], (13/40)*app.width, (23/32)*app.height, size = (1/30)*app.width))
    if(len(wordy[len(wordy)-1])>fullInfoList[5]):
        fullInfoList[5] = len(wordy[len(wordy)-1])
    if(len(wordy[len(wordy)-1])<fullInfoList[3] or fullInfoList[3] == 0):
        fullInfoList[3] = len(wordy[len(wordy)-1])
    update_stats()

def letter_reveal(letter):
    '''
    Takes 1 argument, a character representing a letter in the word
    Returns no values but does show letters in the word matching the provided letter
    If called with a letter not in the word, nothing will happen
    '''
    create_Word()
    for thing in gameLetters:
        if(thing.value == letter):
            if letter in wordPattern:
                thing.opacity = 100

fullInfoList[1]+=1
fullInfoList[6]+=1

closeGameButton = Rect(base.left, base.top, pole.left, app.height//10, fill=None, border = 'red', align = 'bottom-left')
closeGameButton.words = Label("Close Game", closeGameButton.centerX, closeGameButton.centerY, size = 15)
backToLauncher = Rect(pole.right, base.top, closeGameButton.width, closeGameButton.height, fill=None, border = 'gray', align = 'bottom-left')
backToLauncher.game = "PretendLauncher/PretendLauncher.py"
backToLauncher.words = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 15)

def onStep():
    '''
    Built in CMU function with executes body code app.stepsPerSecond many times per second
    Used in this function exclusively to force fullscreen on mac devices
    '''
    if(app.autofs<=2):
        app.autofs += 1
    if(app.autofs == 1):
        pyautogui.keyDown("command")
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        pyautogui.keyUp("command")
        pyautogui.keyUp("ctrl")
    if(app.autofs ==2):
        app.typeyTime = True

app.run()