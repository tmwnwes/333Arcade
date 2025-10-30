from cmu_graphics import *
import tkinter as tk
import random
import sys
import subprocess

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.wm_attributes('-fullscreen', True) ## This line is a workaround for macOs devices with no ill effects for Windows users. It forces a new window to open in fullscreen and focus on it, before destroying it on the next line. The main canvas is then created and players will see it. Players must still maximise this window manually however
root.destroy()

gameInfo = open("Files/FlappyBatStats.txt", "r+")
fullInfoList = [] 
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))
        
app.hiScore = fullInfoList[8]
app.easyHi = fullInfoList[5]
app.medHi = fullInfoList[6]
app.hardHi = fullInfoList[7]
app.width = width
app.height = height
app.stepsPerSecond = 42
app.play = False
app.ready = False
app.score = 0
scoreLabel = Label("%d" %app.score, app.width/2, app.height/10, fill='white', bold = True, border = 'black', size = 50)
cities = Group()
failScreen = Group()
stars = Group()
app.pause = False

outerPause = Rect(app.width/2, app.height/2, app.width/5, app.width/10, fill=None, border = 'yellow', borderWidth = 2, align = 'center', opacity = 0)
pauseLabel = Label("Game Paused", app.width/2, app.height/2 -15, size = 30, opacity = 0, fill= 'white')
closeGameButton = Rect(outerPause.left, outerPause.centerY, outerPause.width//2, outerPause.height//2, fill=None, border = 'red', opacity = 0)
closeGameButton.words = Label("Close Game", closeGameButton.centerX, closeGameButton.centerY, size = 15, opacity = 0, fill = 'white')
backToLauncher = Rect(closeGameButton.right+1, closeGameButton.top, outerPause.width//2, outerPause.height//2, fill=None, border = 'gray', opacity = 0)
backToLauncher.game = "PretendLauncher.py"
backToLauncher.words = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 15, opacity = 0, fill='white')
pauseScreen = Group(outerPause, pauseLabel, closeGameButton, backToLauncher, backToLauncher.words, closeGameButton.words)



def make_city(x):
    '''
    Takes 2 args, a starting position and a value meant to be used as an id
    x will be the leftmost position of the city and j will be the id
    Returns a shape group representing a city
    Used to create cities on the game screen
    '''
    city = Group()
    lastWidth = 0
    for i in range(12):
        tall = randrange(5,80)
        wide = randrange(4,15)
        lastWidth = wide
        building = Rect(x+lastWidth+ i*(app.width/200), ground.top-tall, wide, tall, border = 'white')
        city.add(building)
    return city

def move_cities():
    cities.centerX -= app.speed/40
    for city in cities:
        if(city.right<=0):
            cities.remove(city)
            cities.add(make_city(app.width))
            
def make_stars():
    for i in range(200):
        stars.add(Star(randrange(app.width), randrange((int)(ground.top - 5)), randrange(1, 3), randrange(3, 30), fill='white'))

def fail():
    score_avgs()
    yourScoreLabel = Label("Last Score: %d" %app.score, (1/2)*app.width, (27/80)*app.height, fill='pink', size = 30, bold = True)
    highScoreLabel = Label("High Score: %d" %app.hiScore, (1/2)*app.width, (33/80)*app.height, fill='pink', size = 30, bold = True)
    failLabel = Label("Press ENTER to Restart", (app.width*(1/2)), (39/80)*app.height, size = 30, fill = 'pink', bold = True)
    mainMenuLabel = Label("Press ESCAPE to return to main menu", (app.width*(1/2)), (45/80)*app.height, size = 30, fill = 'pink', bold = True)
    failScreen.add(yourScoreLabel, highScoreLabel, failLabel, mainMenuLabel)
    mainScreenExit.visible = True
    app.play = False
    app.ready = False
    update_stats()

background=Rect(0,0,app.width,app.height, fill =rgb(0,0,70))
ground = Rect(-10, (7/10)*app.height, app.width+20, (3/10)*app.height, fill = rgb(49, 43, 0), border = 'darkGreen', borderWidth = 4)
choice = Label("", 0,0, visible = False, size = 50)
app.accel = 1
app.mode = None
app.speed = 0
app.ballSpeed = 0
ball = Group()
leftWing = Polygon((80/200)*app.width, (3/5)*app.height, (81/200)*app.width, (23/40)*app.height, (85/200)*app.width, (3/5)*app.height)
body = Circle((11/25)*app.width,(59/100)*app.height, (3/100)*((app.width+app.height)/2))
leftEye = Circle((43/100)*app.width, (59/100)*app.height, (1/100)*((app.width+app.height)/2), fill = gradient("black", "white", 'white'), borderWidth = 3, border = 'violet')
rightEye = Circle((45/100)*app.width, (59/100)*app.height, (1/100)*((app.width+app.height)/2), fill = gradient("black", "white", 'white'), borderWidth = 3, border = 'violet')
rightWing = Polygon((91/200)*app.width, (3/5)*app.height, (19/40)*app.width, (23/40)*app.height, (96/200)*app.width, (3/5)*app.height)
leftEar = Polygon((43/100)*app.width, (11/20)*app.height, (22/50)*app.width, (57/100)*app.height, (21/50)*app.width, (57/100)*app.height)
rightEar = Polygon((9/20)*app.width, (11/20)*app.height, (23/50)*app.width, (57/100)*app.height, (22/50)*app.width, (57/100)*app.height)
leftTooth = Polygon((43/100)*app.width, (241/400)*app.height, (22/50)*app.width, (241/400)*app.height, (87/200)*app.width, (49/80)*app.height, fill='white')
rightTooth = Polygon((22/50)*app.width, (241/400)*app.height, (9/20)*app.width, (241/400)*app.height, (89/200)*app.width, (49/80)*app.height, fill='white')
ball.add(body, leftWing, leftEye, rightEye, rightWing, leftEar, rightEar, leftTooth, rightTooth)
ball.centerX = app.width/4
ball.centerY = (7/20)*app.height

def killOpen(selection):
    mainthing.visible = False
    choice.value = selection.value
    choice.visible=True
    choice.fill = selection.fill
    choice.left = 5
    choice.top = 5
    ball.centerX = app.width/4
    ball.centerY = (7/20)*app.height
    
def resetBlocks():
    for block in Blocks:
        if(block.y1<=0):
            block.y1 = 0
            block.y2 = block.y2
        else:
            block.y1 = ground.top
            block.y2 = block.y2
        if(block.centerX<(-(1/5)*app.width)):
            block.centerX = (7/5)*app.width
            app.foo=(randrange(0, (int)((3/10)*app.height)))
            if(block == a1):
                a1.y2 = app.foo
                a2.y2 = app.foo + (3/8)*app.height
                a2.counted = False
            if(block == b1):
                b1.y2 = app.foo
                b2.y2 = app.foo + (3/8)*app.height
                b2.counted = False
            if(block == c1):
                c1.y2 = app.foo
                c2.y2 = app.foo + (3/8)*app.height
                c2.counted = False
            if(block == d1):
                d1.y2 = app.foo
                d2.y2 = app.foo + (3/8)*app.height
                d2.counted = False

def scoring():
    for block in Blocks:
        if ball.left>= block.centerX and block.counted == False:
            block.counted = True
            app.score+=1
            fullInfoList[9]+=1
            scoreLabel.value = "%d" % app.score
            if(app.mode == "easy"):
                fullInfoList[13]+=1
            if(app.mode =="medium"):
                fullInfoList[14]+=1
            if(app.mode =="hard"):
                fullInfoList[15]+=1
                
def score_avgs():
    fullInfoList[10] = (0 if fullInfoList[2] == 0 else fullInfoList[13]//fullInfoList[2])
    fullInfoList[11] = (0 if fullInfoList[3] == 0 else fullInfoList[14]//fullInfoList[3])
    fullInfoList[12] = (0 if fullInfoList[4] == 0 else fullInfoList[15]//fullInfoList[4])          

### Blocks for the game. They will move and interact with player
a1= Line((3/5)*app.width, -50, (3/5*app.width), (3/8)*app.height, fill=rgb(0,130,0), lineWidth=(1/12)*app.width)
a2=Line((3/5)*app.width, ground.top, (3/5)*app.width, 300, fill=rgb(0,130,0), lineWidth=(1/12)*app.width)
b1=Line((5/5)*app.width, -50, (5/5)*app.width, 100, fill=rgb(0,130,0), lineWidth=(1/12)*app.width)
b2=Line((5/5)*app.width, ground.top, (5/5)*app.width, 250, fill=rgb(0,130,0), lineWidth=(1/12)*app.width)
c1=Line((7/5)*app.width, -50, (7/5)*app.width, (3/8)*app.height, fill=rgb(0,130,0), lineWidth=(1/12)*app.width)
c2=Line((7/5)*app.width, ground.top, (7/5)*app.width, 300, fill=rgb(0,130,0), lineWidth=(1/12)*app.width)
d1=Line((9/5)*app.width, -50, (9/5)*app.width,125 , fill=rgb(0,130,0), lineWidth=(1/12)*app.width)
d2=Line((9/5)*app.width, ground.top, (9/5)*app.width, 325, fill=rgb(0,130,0), lineWidth=(1/12)*app.width)  
### Blocks for the game. They will move and interact with player

## Workaround for counting
a1.counted = True
a2.counted = False
b1.counted = True
b2.counted = False
c1.counted = True
c2.counted = False
d1.counted = True
d2.counted = False
## Workaround for counting

Blocks = Group(a1, a2, b1, b2, c1, c2, d1, d2)        

def update_stats():
    '''
    Takes no arguments and returns no values
    Updates values relating to stored stats outside of the program
    '''
    if(app.score>=fullInfoList[8]):
        fullInfoList[8] = app.score
        app.hiScore = fullInfoList[8]
    if(app.mode == "easy" and app.score>fullInfoList[5]):
        fullInfoList[5] = app.score
    if(app.mode == "medium" and app.score>fullInfoList[6]):
        fullInfoList[6] = app.score
    if(app.mode == "easy" and app.score>fullInfoList[7]):
        fullInfoList[7] = app.score
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")

def checkSpeed(speed):
    speed += app.accel
    ball.rotateAngle+=(3*app.accel)
    return speed

def movePipes(speed):
    Blocks.centerX -= speed

def toggle_pause():
    '''
    Takes no args and returns no values
    If game is paused, this will unpause it, 
    If game is unpaused, this will pause it
    Entails changing opacity of pause screen features and changing app setting
    '''
    if app.pause == True:
        app.pause = False
        for thing in pauseScreen:
            thing.opacity = 0
    else:
        app.pause = True
        for thing in pauseScreen:
            thing.opacity = 100

def onKeyPress(key):
    if(app.play==False):
        if(key =='escape'):
            mainthing.visible = True
            mainScreenExit.visible = True
            mainScreenExit.toFront()
            choice.visible = False
            app.mode = None
        if(app.ready == True):
            if(key == 'space'):
                app.play = True
                scoreLabel.toFront()
                app.ballSpeed = -8
                ball.rotateAngle
                if(app.mode == 'easy'):
                    fullInfoList[2]+=1
                if(app.mode == 'medium'):
                    fullInfoList[3]+=1
                if(app.mode == 'medium'):
                    fullInfoList[4]+=1
        elif(key=='enter'):
            failScreen.clear()
            ball.centerX = (1/4)*app.width
            ball.centerY = (7/20)*app.height
            reset()
            mainScreenExit.visible = False
            scoreLabel.toFront()
            scoreLabel.value = "%d" %app.score
            if(app.mode == 'easy'):
                fullInfoList[2]+=1
            if(app.mode == 'medium'):
                fullInfoList[3]+=1
            if(app.mode == 'medium'):
                fullInfoList[4]+=1
    if(key=='space' and app.play == True and app.pause == False):
        app.ballSpeed = -8
        ball.rotateAngle = -50
    if((key =='p' or key =='P') and app.play == True):
        toggle_pause()

def reset():
    app.foo=(random.randrange(0, (int)((3/10)*app.height)))
    a1.y2=app.foo-40
    b1.y2=app.foo
    c1.y2=app.foo+20
    d1.y2=app.foo-70
    a2.counted = False
    b2.counted = False
    c2.counted = False
    d2.counted = False
    a2.y2=a1.y2+(3/8)*app.height
    b2.y2=b1.y2+(3/8)*app.height
    c2.y2=c1.y2+(3/8)*app.height
    d2.y2=d1.y2+(3/8)*app.height
    a1.centerX = (3/5)*app.width
    a2.centerX = (3/5)*app.width
    b1.centerX = (5/5)*app.width
    b2.centerX = (5/5)*app.width
    c1.centerX = (7/5)*app.width
    c2.centerX = (7/5)*app.width
    d1.centerX = (9/5)*app.width
    d2.centerX = (9/5)*app.width
    app.ballSpeed = 0
    ball.rotateAngle = 0
    failScreen.clear()
    scoreLabel.toBack()
    app.score = 0
    app.ready = True
    app.pause = False

def hit_detection():
    if(ball.hitsShape(Blocks)):
        fail()
    if(ball.bottom>= ground.top):
        fail()
    if(ball.top<=0):
        fail()
    
def onStep():
    if(app.play==True and app.pause == False):
        move_cities()
        scoring()
        hit_detection()
        movePipes(app.speed)
        resetBlocks()
        ball.centerY += app.ballSpeed
        app.ballSpeed = checkSpeed(app.ballSpeed)
        update_stats()

def onMousePress(x,y):
    if(title.visible==True):
        reset()
        if(easy.contains(x,y)):
            killOpen(easy)
            app.mode = "easy"
            app.speed = (1/110)*app.width
            app.ready = True
            scoreLabel.value = "%d" %app.score
            scoreLabel.toFront()
            fullInfoList[1]+=1
            fullInfoList[2]+=1
            mainScreenExit.visible = False
        elif(intermediate.contains(x,y)):
            app.mode = "medium"
            killOpen(intermediate)
            app.speed = (1/90)*app.width
            app.ready = True
            scoreLabel.value = "%d" %app.score
            scoreLabel.toFront()
            fullInfoList[1]+=1
            fullInfoList[3]+=1
            mainScreenExit.visible = False
        elif(hard.contains(x,y)):
            app.mode = "hard"
            killOpen(hard)
            app.speed = (1/70)*app.width
            app.ready = True
            scoreLabel.value = "%d" %app.score
            scoreLabel.toFront()
            fullInfoList[1]+=1
            fullInfoList[4]+=1
            mainScreenExit.visible = False
        if(backToLauncherMain.contains(x,y)):
            update_stats()
            subprocess.Popen(["python3", backToLauncherMain.game])
            sys.exit(0)
        if(closeGameButtonMain.contains(x,y)):
            update_stats()
            sys.exit(0)
    else:
        if(backToLauncher.contains(x,y) and app.pause == True):
            update_stats()
            subprocess.Popen(["python3", backToLauncher.game])
            sys.exit(0)
        if(closeGameButton.contains(x,y) and app.pause == True):
            update_stats()
            sys.exit(0)
        if(backToLauncherMain.contains(x,y) and app.play == False):
            print("Failed and clicks launcher")
            update_stats()
            subprocess.Popen(["python3", backToLauncherMain.game])
            sys.exit(0)
        if(closeGameButtonMain.contains(x,y) and app.play == False):
            print("Failed and Closed")
            update_stats()
            sys.exit(0)
            
stars.toFront()
cities.toFront()
Blocks.toFront()
ball.toFront()
cover = Rect(0, 0, app.width, app.height, fill=rgb(0,0,70))
title = Label('FlappyBat', (app.width/2), (3/20)*app.height, fill='white', size=70)
instructions=Label('Select Difficulty', (app.width/2), (5/16)*app.height, fill='white', size=25)
box = Rect((7/20)*app.width, (2/5)*app.height, (3/10)*app.width, (2/5)*app.height, fill=None, border='white')
easy=Label('Easy', app.width/2, (9/20)*app.height, fill='green', size=50)
intermediate = Label('Normal', app.width/2, (3/5)*app.height, fill='yellow', size=50)
hard = Label('Hard', app.width/2, (3/4)*app.height, fill='red', size=50)
mainScreenExitBox = Rect(box.left, box.bottom, box.width, app.width/20, fill=None, border = 'yellow', borderWidth = 2)
closeGameButtonMain = Rect(mainScreenExitBox.left, mainScreenExitBox.top, mainScreenExitBox.width//2, mainScreenExitBox.height, fill=None, border = 'red')
closeGameButtonMain.words = Label("Close Game", closeGameButtonMain.centerX, closeGameButtonMain.centerY, size = 15, fill = 'white')
backToLauncherMain = Rect(closeGameButtonMain.right+1, closeGameButtonMain.top, mainScreenExitBox.width//2, mainScreenExitBox.height, fill=None, border = 'gray')
backToLauncherMain.game = "PretendLauncher.py"
backToLauncherMain.words = Label("Return to Launcher", backToLauncherMain.centerX, backToLauncherMain.centerY, size = 15, fill='white')
mainScreenExit = Group(mainScreenExitBox, closeGameButtonMain, closeGameButtonMain.words, backToLauncherMain, backToLauncherMain.words)
mainthing = Group(cover, title, instructions, box, easy, intermediate, hard)
failScreen.toFront()
mainScreenExit.toFront()
make_stars()
cities.add(make_city(0))
cities.add(make_city((1/10)*app.width))
cities.add(make_city((2/10)*app.width))
cities.add(make_city((3/10)*app.width))
cities.add(make_city((4/10)*app.width))
cities.add(make_city((5/10)*app.width))
cities.add(make_city((6/10)*app.width))
cities.add(make_city((7/10)*app.width))
cities.add(make_city((8/10)*app.width))
cities.add(make_city((9/10)*app.width))
cities.add(make_city(app.width))
pauseScreen.toFront()
fullInfoList[0]+=1


        
app.run()
