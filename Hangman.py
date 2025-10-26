from cmu_graphics import *
import tkinter as tk
import random

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.wm_attributes('-fullscreen', True) ## This line is a workaround for macOs devices with no ill effects for Windows users. It forces a new window to open in fullscreen and focus on it, before destroying it on the next line. The main canvas is then created and players will see it. Players must still maximise this window manually however
root.destroy()

app.width = width
app.height = height

wordList = open("Files/words_alpha.txt", "r", -1) ### 370k words, incliuding names, places, plurals, and weird old english words like symphysy
words = []
words2 = []

gameInfo = open("Files/HangmanStats.txt", "r+")
fullInfoList = [] ## Key infomation can be found in MinesweeperStatsKeys.txt
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))
    
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



wordLength = len(word)
wordPattern = []

for i in range(wordLength):
    wordPattern.append('0')

wordy = [word] ## wordy is a list containing every iteration of the word, beginning obviously with the 1st word

def get_same_length(wordLength):
    temp = []
    for wd in words:
        if len(wd) == wordLength:
            temp.append(wd) 
    return temp
     
words2 = get_same_length(wordLength)   

def patternCheck(list, pattern):
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
    temp = []
    bad = []
    withit = []
    without = []
    global words2
    global wordPattern
    for wd in words2:
        if len(wd) == wordLength:
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
    temp = patternCheck(temp, pattern)
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
        for i in range(wordLength):
            if wordy[len(wordy)-1][i] == letter:
                wordPattern[i] = letter
            
gameLetters = Group()

underlines = Group()

def create_Word():
    gameLetters.clear()
    underlines.clear()
    for i in range(wordLength):
        new = Label(wordPattern[i], (i* ((3/80)*app.width) + (3/80 * app.width)), 0, size = (1/20)*app.width, opacity = 0) ##????
        underline = Line((i* ((15/400)*app.width) + (9/400 * app.width)), (0.17*app.height), (i * (15/400)*app.width + (21/400)*app.width), (0.17*app.height), lineWidth = (1/200)*app.width)
        new.bottom = (0.16*app.height)
        gameLetters.add(new)
        underlines.add(underline)
        for j in gameLetters:
            if j.value != '0':
                j.opacity = 100

create_Word()

def bring():
    for letter in gameLetters:
        for let in letterLabels:
            if let.fill == 'lime':
                if letter.value == let.value:
                    letter.opacity = 100

rects = Group()
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x' ,'y', 'z']
letterLabels = Group()
app.wrongCount = 0        

def make_alphabet():
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

def validate():
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
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")           
            
            
def reset_all():
    global noLetters
    global yesLetters
    global wordy
    global wordLength
    global wordPattern
    global words2
    app.over = 0
    app.otherCase = 0
    app.wrongCount = 0
    for part in gameOver:
        part.opacity = 0
    for part in person:
        part.opacity = 0
    noLetters = []
    yesLetters = []
    wordPattern = []
    word = words[randrange(len(words))]
    wordy = [word]
    wordLength = len(word)
    for i in range(wordLength):
        wordPattern.append('0')
    words2 = get_same_length(wordLength)
    create_Word()
    make_alphabet()
    failScreen.clear()
    winScreen.clear()
    fullInfoList[1]+=1
    update_stats()       

def onMousePress(x,y):
    if app.over == 1:
        if button.contains(x,y):
            reset_all()
    else:
        validate()
        temp = wordy[len(wordy)-1]
        patternCheck(words2, wordPattern)
        for rect in rects:
            for let in letterLabels:
                if(rect.contains(x,y)):
                    if(let.value == rect.letter):
                        if(let.value in wordy[len(wordy)-1]):
                            if app.otherCase == 1:
                                pick_new_word(yesLetters, noLetters, wordPattern, let.value)
                            if (temp == wordy[len(wordy)-1]):
                                for i in range(wordLength):
                                    if temp[i] == let.value:
                                        wordPattern[i] = temp[i]
                                let.fill = 'lime'
                                letterReveal(let.value)
                                app.otherCase = 1
                            else: 
                                let.fill = 'red'
                        elif(not(let.value in wordy[len(wordy)-1])):
                            noLetters.append(let.value)
                            validate()
                            let.fill = 'red'
                    rect.opacity = 25
        checkCount()
        bodyAdd()
        if app.case == 0:
            app.case = 1
            onMousePress(x,y)
        app.case = 0
    update_stats()

def checkCount():
    app.wrongCount = 0
    for let in letterLabels:
        if(let.fill=='red'):
            app.wrongCount+=1
    if(not("0" in wordPattern)):
        win()
        app.over = 1
        offer_to_play_again()

winScreen = Group()

def win():
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
    for part in gameOver:
        part.opacity = 100

def bodyAdd(): ## Move fail() and app.stop() up for harder game and down for easier game (In step 6 is for an average regular game, in step 9 for a super easy game, in 4 for mostly impossible)
    if(app.wrongCount==1):
        head.opacity = 100
    if(app.wrongCount==2):
        body.opacity = 100
    if(app.wrongCount==3):
        leftLeg.opacity = 100
    if(app.wrongCount==4):
        rightLeg.opacity = 100
    if(app.wrongCount==5):
        leftArm.opacity = 100
    if(app.wrongCount==6):
        rightArm.opacity = 100
    if(app.wrongCount==7):
        leftEye.opacity = 100
    if(app.wrongCount==8):
        rightEye.opacity = 100
    if(app.wrongCount==9):
        mouth.opacity = 100
        fail()
        app.over = 1
        offer_to_play_again()
        

failScreen = Group()

def fail():
    failScreen.add(Rect((3/20)*app.width,(3/5)*app.height,(7/20)*app.width,(3/20)*app.height, fill=None))
    failScreen.add(Label("You failed", (13/40)*app.width, (21/32)*app.height, size = (1/30)*app.width))
    failScreen.add(Label(wordy[len(wordy)-1], (13/40)*app.width, (23/32)*app.height, size = (1/30)*app.width))
    if(len(wordy[len(wordy)-1])>fullInfoList[5]):
        fullInfoList[5] = len(wordy[len(wordy)-1])
    if(len(wordy[len(wordy)-1])<fullInfoList[3] or fullInfoList[3] == 0):
        fullInfoList[3] = len(wordy[len(wordy)-1])
    update_stats()

def letterReveal(letter):
    create_Word()
    for thing in gameLetters:
        if(thing.value == letter):
            if letter in wordPattern:
                thing.opacity = 100

fullInfoList[1]+=1
fullInfoList[6]+=1
        
        
app.run()