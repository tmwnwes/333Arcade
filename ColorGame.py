from cmu_graphics import *
import random
import tkinter as tk


root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.wm_attributes('-fullscreen', True) ## This line is a workaround for macOs devices with no ill effects for Windows users. It forces a new window to open in fullscreen and focus on it, before destroying it on the next line. The main canvas is then created and players will see it. Players must still maximise this window manually however
root.destroy()

app.width = width
app.height = height

gameInfo = open("Files/ColorGameStats.txt", "r+")
fullInfoList = [] 
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))
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
words = ['blue', 'yellow', 'cow', 'dog', 'purple', 'aardvark', 'green', 'jellyfish', 'pink', 'brown', 'shark', 'black', 'piranha', 'gold', 'lime', 'lemon', 'chips', 'corkboard', 'paper', 'white', 'school', 'gray', 'magenta', 'maroon', 'orange', 'olive', 'turquoise', 'red', 'dinosuar', 'teal', 'cyan']
colors = ['blue', 'yellow', 'purple', 'darkGreen', 'pink', 'brown', 'black', 'lime', 'maroon', 'magenta', 'darkOrange', 'turquoise', 'red', 'teal', 'cyan']

thing = Label('word', app.width/2, (1/5)*app.height, size = (3/20)*app.width)
infoLabel = Label("Current Time: %1.1f" %(app.timeSince/app.stepsPerSecond), 5, (3/40)*app.height, size = (1/40)*app.width, align = 'left')
buttons = Group()
int = 0
for i in range(3):
    for j in range(5):
        buttons.add(Rect(i*(3/10)*app.width + (3/40)*app.width, j*(3/40)*app.height + (3/5)*app.height, (1/4)*app.width, (1/20)*app.height, fill = colors[int]))
        int += 1

def update_stats():
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
    accuracy = (100 * (app.score / app.att))
    Rect(0,0,app.width,app.height, fill='white')
    Rect((1/5)*app.width, (1/4)*app.height, (3/5)*app.width, (9/20)*app.height, fill=None, border = 'red', borderWidth = 2)
    Label("Game Over", app.width/2, (2/5)*app.height, size = 30, fill='red')
    sco = Label("Score: ", (9/20)*app.width, (19/40)*app.height, size = (1/20)*app.width)
    acc = Label("Accuracy: ", (9/20)*app.width, (11/20)*app.height, size = (1/20)*app.width)
    Label(app.score, sco.right + (3/100)*app.width, sco.centerY, size = (1/20)*app.width)
    num = Label("%02d" %accuracy, acc.right+ (1/40)*app.width ,(11/20)*app.height, size = (1/20)*app.width)
    Label("%", num.right + (1/40)*app.width, (11/20)*app.height, size = (1/20)*app.width)
    Label("Press Enter to Restart", app.width/2, num.centerY+(1/10)*app.height, size = (1/20)*app.width)
    app.failed = True

def reset_word():
    thing.value = words[randrange(len(words))]
    thing.fill = colors[randrange(len(colors))]
    fullInfoList[1]+=1
    update_stats()
    
def check_button(colInput):
    app.att+=1
    if(colInput == thing.fill):
        app.score += 1
        app.time += app.stepsPerSecond*1.5
        app.currentStreak+=1
        fullInfoList[0]+=1
    else:
        app.time -= app.stepsPerSecond
        app.currentStreak = 0
    
def onMousePress(x,y):
    for button in buttons:
        if(button.contains(x,y)):
            app.timeSince = app.stepsPerSecond*2
            check_button(button.fill)
            reset_word()
    
def checkTime():
    if(app.time <= 0):
        end_game()
        app.stop()
    if(app.timeSince<=0):
        app.timeSince = app.stepsPerSecond*2
        app.att += 1
        reset_word()
        app.currentSrteak = 0
        
def full_reset():
    fullInfoList[3]+=1
    app.score = 0
    app.time = 1000
    app.timeSince = app.stepsPerSecond*2
    app.att = 0
    app.failed = False

def onKeyPress(key):
    if(key =='enter'):
        if(app.failed == True):
            full_reset()

def onStep():
    if(app.failed == False):
        checkTime()
        app.time -= 1
        app.timeSince -= 1
        infoLabel.value = "Current Time: %1.1f" %(app.timeSince/app.stepsPerSecond)
        oTime.value = "Overall Time: %1.1f" %(app.time/app.stepsPerSecond)
        score.value = "Score: %1d" %app.score
        hiScore.value = "High Score: %1d" %app.hi
    
fullInfoList[3]+=1
fullInfoList[4]+=1
reset_word()



app.run()