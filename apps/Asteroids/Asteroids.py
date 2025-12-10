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

app.width = width
app.height = height
app.autofs = 0

default = [0,0,0,0,0]
keys = ["Shots", "Hits", "HighScore", "GamesPlayed", "TimesLaunched"]
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

app.failed = False
gameInfo = open("Files/AsteroidsStats.txt", "r+")

app.score = 0
app.generalSpeed = 14
app.play = True
screen = Rect(0,0,app.width, app.height)
asteroidBase = Rect(-400, -400, app.width+800, app.height+800)
score = Label("Score: %09d" %app.score, 5, 20, size = 20, fill='white', align = 'left')
hiScore = Label("High Score: %09d" %fullInfoList[2], app.width-2, score.centerY, size =20, fill='white', align='right')

outerPause = Rect(app.width/2, app.height/2, app.width/5, app.width/10, fill=None, border = 'yellow', borderWidth = 2, align = 'center')
pauseLabel = Label("Game Paused", app.width/2, app.height/2 -15, size = 30, fill= 'white')
closeGameButton = Rect(outerPause.left, outerPause.centerY, outerPause.width//2, outerPause.height//2, fill=None, border = 'red')
closeGameButton.words = Label("Close Game", closeGameButton.centerX, closeGameButton.centerY, size = 15, fill = 'white')
backToLauncher = Rect(closeGameButton.right+1, closeGameButton.top, outerPause.width//2, outerPause.height//2, fill=None, border = 'gray')
backToLauncher.game = "PretendLauncher/PretendLauncher.py"
backToLauncher.words = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 15, fill='white')
pauseScreen = Group(outerPause, pauseLabel, closeGameButton, backToLauncher, backToLauncher.words, closeGameButton.words)
pauseScreen.visible = False
shooting = [Sound("../../libraries/Audio/Shooting1.mp3"), Sound("../../libraries/Audio/Shooting2.mp3"), Sound("../../libraries/Audio/Shooting3.mp3")]

app.muted = False
app.asteroidspeed = (1/80)*app.width
app.stepsPerSecond = 30
app.decel= 1/4
app.forwardSpeed = 0
app.leftwardSpeed = 0
app.rotationSpeed = 0
app.timer = 1
app.multiplier = 1
app.asteroidTimer = app.stepsPerSecond*4.5
app.ballSpeed = 16 ## Player shots
app.shotSpeed = 25 ## Enemy shots
app.launchSpeed = 5
app.enemyLaunchSpeed = app.stepsPerSecond*4
app.timeSince = 0
app.saucerTime = app.stepsPerSecond*15
app.saucerSpawn = 0
app.asteroidSpeed = 5
app.enemy = False
head = Circle(app.width/2, app.height/2,7, fill = 'white')
ship = Group(head, Polygon(app.width/2,app.height/2, (81/160)*app.width,(21/40)*app.height, app.width/2,(81/160)*app.height, (79/160)*app.width,(21/40)*app.height, app.width/2,app.height/2, fill='white'))
ship.health = 3
health = Label("Health: %1d" %ship.health, app.width/2, score.centerY, fill='white', size = 20)
balls = Group()
asteroids = Group()
visibleScores = Group()
explosion = Group()
gameOver = Group()
shots = Group()
saucers = Group()
trail = Group()

def update_high_score():
    ''' 
    Takes no args and returns no values
    Updates high score if current score is higher than high score
    Forces stats update in that case
    
    '''
    if app.score>fullInfoList[2]:
        fullInfoList[2] = app.score
        hiScore.value = "High Score: %09d" %fullInfoList[2]
        update_stats()


def update_stats():
    '''
    Takes no arguments and returns no values
    Updates stores stats in the associated text file
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")  
        
def shots_vs_asteroids():
    '''
    No args, no returns
    Handles collision between enemy shots and asteroids
    '''
    for shot in shots:
        for ast in asteroids:
            if(shot.hitsShape(ast) or ast.containsShape(shot)):
                decrease_health_asteroid(ast, False)
                shots.remove(shot)


def get_speed(speed):
    '''
    Takes 1 arg, and returns 1 value
    speed should be a number representing the speed of some shape
    returns the next speed of the item
    '''
    if(speed<0):
        return speed + app.decel
    elif(speed>0):
        return speed - app.decel
    return 0

def spawn_balls(x,y,angle):
    '''
    Takes 3 args, 2 positional, and 1 directional
    Returns no values but does add a shape to a relevant group    
    '''
    new = Circle(x,y,4, fill='white', rotateAngle = angle)
    new.next = getPointInDir(x,y,angle,app.ballSpeed)
    balls.add(new)
    fullInfoList[0]+=1
    
def spawn_shots(x,y,angle):
    '''
    Takes 3 args, 2 positional, and 1 directional
    Returns no values but does add shapes to a relevant group    
    '''
    new = Oval(x,y,2,20, fill='white', rotateAngle = angle)
    new.next = getPointInDir(x,y,angle,app.shotSpeed)
    new2 = Oval(x,y,2,20, fill='white', rotateAngle = angle+10)
    new2.next = getPointInDir(x,y,angle+10,app.shotSpeed)
    new3 = Oval(x,y,2,20, fill='white', rotateAngle = angle-10)
    new3.next = getPointInDir(x,y,angle-10,app.shotSpeed)
    new4 = Oval(x,y,2,20, fill='white', rotateAngle = angle+5)
    new4.next = getPointInDir(x,y,angle+5,app.shotSpeed)
    new5 = Oval(x,y,2,20, fill='white', rotateAngle = angle-5)
    new5.next = getPointInDir(x,y,angle-5,app.shotSpeed)
    if(app.muted == False):
        Sound("../../libraries/Audio/UFO_shots.mp3").play(restart = True)
        Sound("../../libraries/Audio/UFO_shots.mp3").play(restart = True)
        Sound("../../libraries/Audio/UFO_shots.mp3").play(restart = True)
    shots.add(new, new2, new3, new4, new5)
    
def create_scores(x,y,val):
    '''
    Takes 3 args, 2 positional and 1 value to display
    Returns no values but does create a shape and add it to a relevant group    
    '''
    visibleScores.add(Label("+ %3d" %val, x, y, fill=None, border = 'white', size = 14))
    
def remove_scores():
    '''
    no args, no returns
    slowly grows and fades scores from destroying asteroids, then removes once invisible
    '''
    for score in visibleScores:
        if(score.opacity<=0):
            visibleScores.remove(score)
        else:
            score.opacity-=5
            score.size+=2
    
### The following 4 functions are used to create asteroids of different sizes, aim them, set their hp, and score values    
    
def small(x, y):
    r = angleTo(x, y, randrange((int)(app.width/4),(int)((3/4)*app.width)), randrange((int)(app.height/4),(int)((3/4)*app.height)))
    new = Polygon(10, 15, 24, 8, 34, 10, 31, 21, 41, 25, 38, 35, 30, 35, 25, 42, 13, 36, 8, 26, 10, 15, fill = None, border = 'white', opacity = 0, borderWidth = 3)
    new.centerX = x
    new.centerY = y
    new.opacity = 100
    new.rotateAngle = r
    new.size = "small"
    new.health = 1
    new.score = 25
    new.hasHit = False
    new.speed = (3/2)*app.asteroidSpeed
    new.next = getPointInDir(new.centerX, new.centerY, r, new.speed)
    new.note = Sound("../../libraries/Audio/Asteroid_Destroy.mp3")
    return new

def med(x,y):
    r = angleTo(x, y, randrange((int)(app.width/4),(int)((3/4)*app.width)), randrange((int)(app.height/4),(int)((3/4)*app.height)))
    new = Polygon(21, 30, 48, 16, 68, 21, 62, 42, 82, 50, 76, 70, 60, 70, 50, 84, 26, 72, 15, 52, 21, 30, fill = None, border = 'white', opacity = 0, borderWidth = 3)
    new.centerX = x
    new.centerY = y
    new.opacity = 100
    new.rotateAngle = r
    new.size = "med"
    new.health = 2
    new.score = 50
    new.hasHit = False
    new.speed = app.asteroidSpeed
    new.next= getPointInDir(new.centerX, new.centerY, r, new.speed)
    new.note = Sound("../../libraries/Audio/Asteroid_Destroy.mp3")
    return new

def big(x,y):
    r = angleTo(x, y, randrange((int)(app.width/4),(int)((3/4)*app.width)), randrange((int)(app.height/4),(int)((3/4)*app.height)))
    new = Polygon(42, 60, 96, 32, 134, 42, 124, 84, 164, 100, 154, 140, 120, 140, 102, 168, 52, 144, 30, 104, 42, 60, fill = None, border = 'white', opacity = 0, borderWidth = 3)
    new.centerX = x
    new.centerY = y
    new.opacity = 100
    new.score = 75
    new.rotateAngle = r
    new.size = "big"
    new.health = 3
    new.hasHit = False
    new.speed = app.asteroidSpeed*(7/8)
    new.next = getPointInDir(new.centerX, new.centerY, r, new.speed)
    new.note = Sound("../../libraries/Audio/Asteroid_Destroy.mp3")
    return new    

def massive(x,y):
    r = angleTo(x, y, randrange((int)(app.width/4),(int)((3/4)*app.width)), randrange((int)(app.height/4),(int)((3/4)*app.height)))    
    new = Polygon(84, 120, 192, 64, 268, 84, 248, 168, 328, 200, 308, 280, 240, 280, 204, 336, 104, 288, 60, 208, 84, 120, fill = None, border = 'white', opacity = 0, borderWidth = 3)
    new.centerX = x
    new.centerY = y
    new.opacity = 100
    new.score = 100
    new.rotateAngle = r
    new.size = "massive"
    new.health = 4
    new.hasHit = False
    new.speed = app.asteroidSpeed*(3/4)
    new.next = getPointInDir(new.centerX, new.centerY, r, new.speed)
    new.note = Sound("../../libraries/Audio/Asteroid_Destroy.mp3")
    return new   

### The preceding 4 functions are used to create asteroids of different sizes, aim them, set their hp, and score values   

def move_asteroids():
    '''
    no args, no returns
    moves the asteroids based on their aim points, sets next point based on aiming direction
    also deletes asteroids if they are off of the screen
    '''
    for ast in asteroids:
        if(not(asteroidBase.containsShape(ast))):
            asteroids.remove(ast)
        ast.centerX, ast.centerY = ast.next
        ast.next = getPointInDir(ast.centerX, ast.centerY, ast.rotateAngle, ast.speed)
    
def create_saucer(left, top, right, bottom):
    '''
    Takes 4 args relating to acceptable spawning zone for the saucer
    Creates a saucer group and places it in the acceptable spawning zone
    returns the saucer group
    '''
    new = Group()
    new.health = app.multiplier
    new.score = 500*app.multiplier
    saucerTop = Arc(100,100, 80, 40, 270, 180, fill=None, border = 'white')
    saucerMid = Rect(55, 100, 90, 10, fill="gray")
    saucerBottom = Arc(100, 110, 90, 20, 90, 180, fill='white')
    randX = randrange((int)(left), (int)(right))
    randY = randrange((int)(top), (int)(bottom))
    new.add(saucerTop, saucerMid, saucerBottom)
    new.centerX = randX
    new.centerY = randY
    app.saucerSpawn = 0
    return new 
    
    
def shots_vs_ship():
    '''
    no args, no returns
    handles collisions between enemy shots and the player ship
    '''
    for shot in shots:
        if(shot.hitsShape(ship)):
            shots.remove(shot)
            decrease_health_ship()
    
def spawn_enemy_saucer():
    '''
    no args, no returns, adds a new saucer to the saucers group after selecting spawning zone
    '''
    location = randrange(4)
    saucer = None
    if(location == 0):
        saucer = create_saucer(0,0,app.width/8, app.height/8)
    elif(location == 1):
        saucer = create_saucer(7* app.width/8, 0, app.width, app.height/8)
    elif(location == 2):
        saucer = create_saucer(0,7*app.height/8, app.width/8, app.height)
    else:
        saucer = create_saucer(7*app.width/8, 7*app.height/8, app.width, app.height)
    saucers.add(saucer)
    app.enemy = True
    
def enemy_firing(saucer):
    '''
    takes 1 argument representing a shape group of a saucer
    returns no values but will spawn shots aimed at the player ship
    '''
    if(app.enemy == True and app.timer%app.enemyLaunchSpeed == 0):
        spawn_shots(saucer.centerX, saucer.centerY, angleTo(saucer.centerX, saucer.centerY, ship.centerX, ship.centerY))
    
    
def move_enemy_shots():
    '''
    no args, no returns
    move enemy shots based on chosen aiming points. 
    Remove if they are outside of the screen
    '''
    for shot in shots:
        shot.centerX, shot.centerY = shot.next
        shot.next = getPointInDir(shot.centerX,shot.centerY,shot.rotateAngle, app.shotSpeed)
        if(not(screen.containsShape(shot))):
            shots.remove(shot)
    
    
def decrease_health_saucer(saucer):
    '''
    Takes 1 argument, representing a saucer shape group
    Meant to be called when a saucer is shot. Will remove a saucer if health has depleted
    '''
    if saucer.health<=1:
        if(app.muted == False):
            Sound("../../libraries/Audio/nuke.mp3").play(restart = True)
        create_scores(saucer.centerX, saucer.centerY, saucer.score*app.multiplier)
        app.score+=saucer.score*app.multiplier
        explosion.add(Star(saucer.centerX, saucer.centerY, 12, 12, fill = None, border = 'white'))
        explosion.add(Star(saucer.centerX, saucer.centerY, 8, 12, fill = None, border = 'white'))
        explosion.add(Star(saucer.centerX, saucer.centerY, 4, 12, fill = None, border = 'white'))
        saucers.remove(saucer)
        if(len(saucers) ==0):
            app.enemy = False
            app.multiplier+=1
    else:
        saucer.health-=1
    
def balls_vs_enemy():
    '''
    no args, no returns
    handles collision between player fired shots and enemy saucers
    '''
    for saucer in saucers:
        for ball in balls:
            if(saucer.hitsShape(ball)):
                explosion.add(Circle(ball.centerX, ball.centerY, 3, fill=None, border = 'white'))
                balls.remove(ball)
                fullInfoList[1]+=1
                decrease_health_saucer(saucer)
    
    
def spawn_asteroids(num):
    '''
    Takes 1 argument, num, representing how many asteroids to spawn
    Makes own choices about size and location
    no return values, but shapes added to appropriate groups    
    '''
    for i in range(num):
        size = randrange(0,4)
        randX = randrange(asteroidBase.left, asteroidBase.right)
        randY = randrange(asteroidBase.top, asteroidBase.bottom)
        while(screen.contains(randX, randY)):
            randX = randrange(asteroidBase.left, asteroidBase.right)
            randY = randrange(asteroidBase.top, asteroidBase.bottom)
        if(size == 0):
            asteroids.add(small(randX, randY))
        if(size == 1):
            asteroids.add(med(randX, randY))
        if(size == 2):
            asteroids.add(big(randX, randY))
        if(size ==3):
            asteroids.add(massive(randX, randY))
        
def reset():
    '''
    no args, no returns
    Full reset of the games variables and parameters to start a new game
    Should only be called if the player has had their run end.
    '''
    app.timer = 1
    app.saucerSpawn = 0
    shots.clear()
    asteroids.clear()
    balls.clear()
    saucers.clear()
    visibleScores.clear()
    explosion.clear()
    gameOver.clear()
    trail.clear()
    app.score = 0
    app.play = True
    fullInfoList[3]+=1
    score.value = "Score: %09d" %app.score
    ship.centerX = app.width/2
    ship.centerY = app.height/2
    ship.rotateAngle = 0
    app.leftwardSpeed = 0
    app.forwardSpeed = 0
    app.rotationSpeed = 0
    app.multiplier = 1
    ship.health = 3
    health.value = "Health: %1d" %ship.health
    app.enemy = False
    app.failed = False
    pauseScreen.visible = False
    pauseScreen.centerX = app.width/2
    update_stats()

    
    
    
def move_balls():
    '''
    no args, no returns
    moves shots fired by the player based on their aiming point.
    removes them if they eave the screen.
    '''
    for ball in balls:
        ball.centerX, ball.centerY = ball.next
        ball.next = getPointInDir(ball.centerX,ball.centerY,ball.rotateAngle, app.ballSpeed)
        if(not(screen.containsShape(ball))):
            balls.remove(ball)

def ship_vs_asteroids():
    '''
    no args, no returns
    handles collision between ship and asteroids
    '''
    for ast in asteroids:
        if(ast.hitsShape(ship) and ast.hasHit == False):
            decrease_health_ship()
            ast.hasHit = True

def decrease_health_ship():
    '''
    no args, no returns
    Only called when the ship has impacted another object
    Can end the game depending on ship health
    '''
    if ship.health <=1:
        update_stats()
        ship.health = 0
        app.play = False
        app.failed = True
        offer_replay()
    else:
        ship.health-=1
    health.value = "Health %1d" %ship.health

def move_trail():
    '''
    Takes no args and returns no values
    Slowly dissipates missile trails until they are invisbile
    Subsequently removes the trail peices as they are fully invisible
    '''
    for trailRemnants in trail:
        if(trailRemnants.opacity>0):
            trailRemnants.opacity -=1
        else:
            trail.remove(trailRemnants)

def decrease_health_asteroid(ast, scoring):
    '''
    Takes 2 args, 1 representing an asteroid shape, the other a boolean determining whether a hit counts for scoring
    Returns no values but adds and removes shapes from approrpate groups. 
    Increases score based on asteroid size and whether or not the player was the destroyer
    '''
    if ast.health<=1:
        if(app.muted == False):
            ast.note.play(restart = True)
        if(scoring == True):
            create_scores(ast.centerX, ast.centerY, ast.score*app.multiplier)
            app.score+=ast.score * app.multiplier
        else:
            create_scores(ast.centerX, ast.centerY, 0)
        if(ast.size == 'massive'):
            asteroids.add(big(ast.centerX, ast.centerY))
            asteroids.add(big(ast.centerX, ast.centerY))
        if(ast.size == 'big'):
            asteroids.add(med(ast.centerX, ast.centerY))
            asteroids.add(med(ast.centerX, ast.centerY))
        if(ast.size == 'med'):
            asteroids.add(small(ast.centerX, ast.centerY))
            asteroids.add(small(ast.centerX, ast.centerY))
        asteroids.remove(ast)
    else:
        ast.health-=1
        
def offer_replay():
    '''
    No args, no returns, but adds shapes to approproate group
    Should only be called if the game is over. 
    provides replay instructions
    '''
    gameOver.add(Rect(app.width/2, app.height/2, app.width, app.height, align = 'center', fill=None, border = 'white'))  
    gameOver.add(Label("Game Over", app.width/2, app.height/2-50, fill='white', size = app.width/20)) 
    gameOver.add(Label("Press Enter To Play Again", app.width/2, app.height/2 + 50, fill='white', size = app.width/30))  
    pauseScreen.visible = True
    pauseScreen.left = 0
        
def blow_up_balls():
    '''
    no args, no returns
    expands and fades balls until invisble, then removes them from the game
    Only impacted balls are those which have collided with a game object
    '''
    for ball in explosion:
        if ball.opacity<=0:
            explosion.remove(ball)
        else:
            ball.opacity -=10
            ball.radius+=1
    
    
def balls_vs_asteroids():
    '''
    no args, no returns
    handles collisions between player shots and asteroids
    '''
    for ast in asteroids:
        for ball in balls:
            if(ast.hitsShape(ball) or ast.containsShape(ball)):
                explosion.add(Circle(ball.centerX, ball.centerY, 3, fill=None, border = 'white'))
                balls.remove(ball)
                fullInfoList[1]+=1
                decrease_health_asteroid(ast, True)
                

def asteroids_vs_space():
    '''
    no args, no returns
    removes asteroids that exit the screen
    '''
    for ast in asteroids:
        if(ast.centerX>asteroidBase.right+100):
            asteroids.remove(ast)
        elif(ast.centerX< asteroidBase.left-100):
            asteroids.remove(ast)
        elif(ast.centerY<asteroidBase.top-100):
            asteroids.remove(ast)        
        elif(ast.centerY>asteroidBase.bottom+100):
            asteroids.remove(ast)
            
def hit_detection():
    '''
    no args and no returns
    Handles all collisions
    '''
    ship_vs_asteroids()
    balls_vs_asteroids()
    asteroids_vs_space()
    balls_vs_enemy()
    shots_vs_ship()
    shots_vs_asteroids()


def onKeyHold(keys):
    '''
    Built in CMU function which takes a list of currently held keys as an argument
    In this script, it is used to move the ship and fire shots
    '''
    if('a' in keys or "A" in keys):
        if(abs(app.leftwardSpeed) <= app.generalSpeed):
            app.leftwardSpeed += 2*app.decel
    if('w' in keys or "W" in keys):
        if(abs(app.forwardSpeed) <= app.generalSpeed):
            app.forwardSpeed += 3*app.decel
    if('d' in keys or "D" in keys):
        if(abs(app.leftwardSpeed) <= app.generalSpeed):
            app.leftwardSpeed -= 2*app.decel 
    if('s' in keys or "S" in keys):
        if(abs(app.forwardSpeed) <= app.generalSpeed):
            app.forwardSpeed -= 3*app.decel
    if('left' in keys):
        if(abs(app.rotationSpeed) <= app.generalSpeed):
            app.rotationSpeed -= 3*app.decel
    if('right' in keys):
        if(abs(app.rotationSpeed) <= app.generalSpeed):
            app.rotationSpeed += 3*app.decel
    if('space' in keys):
        if(app.timeSince == 0):
            spawn_balls(head.centerX, head.centerY, ship.rotateAngle%360)
            if(app.muted == False):
                shooting[randrange(3)].play(restart = True)
            app.timeSince = app.launchSpeed
        
def toggle_mute():
    '''
    Takes no args and returns no values
    When called, if sound is on, it will mute audio
    Else, sound will turn on
    '''
    if(app.muted == True):
        app.muted = False
    else:
        app.muted = True

def spawn_trail(x, y, color):
    '''
    Takes 3 args and returns no values
    Creates a shape and adds it to the appropriate shape group
    The trails in this program will represent missile streaks and rocket burns
    '''
    trail.add(Circle(x, y, 2, fill =  color, opacity = 90))

def onStep():  
    '''
    Built in CMU function
    All code in this function is run app.stepsPerSecond many times every second
    In this script, it causes all motion
    '''
    if(app.autofs<=4):
        app.autofs += 1
    if(app.autofs == 3):
        pyautogui.keyDown("command")
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        pyautogui.keyUp("command")
        pyautogui.keyUp("ctrl")
    if(app.play==True):
        move_trail()
        app.timer+=1
        if(app.timer%(app.stepsPerSecond*app.multiplier*60) == 0):
                spawn_enemy_saucer()
                app.saucerSpawn= 0
        if(app.timeSince>0):
            app.timeSince -=1
        angle = ship.rotateAngle + angleTo(ship.centerX,ship.centerY, ship.centerX-app.leftwardSpeed, ship.centerY-app.forwardSpeed)
        dist = (app.forwardSpeed**2 + app.leftwardSpeed**2)**0.5
        ship.centerX, ship.centerY = getPointInDir(ship.centerX, ship.centerY, angle, dist)
        app.forwardSpeed = get_speed(app.forwardSpeed)
        app.leftwardSpeed = get_speed(app.leftwardSpeed)
        spawn_trail(ship.centerX, ship.centerY, 'white')

        app.rotationSpeed = get_speed(app.rotationSpeed)
        ship.rotateAngle+=app.rotationSpeed
        app.score+=app.multiplier
        score.value = "Score: %09d" %app.score
        if(app.timer%app.asteroidTimer==0 and app.enemy==False):
            spawn_asteroids(randrange(4,10))
        elif(app.timer%app.asteroidTimer==0 and app.enemy == True):
            spawn_asteroids(randrange(1,4))
        for saucer in saucers:
            enemy_firing(saucer)
        app.saucerSpawn+=1
        if(app.saucerSpawn >= app.saucerTime and app.enemy == True):
            app.saucerSpawn = 0
            spawn_enemy_saucer()
            if(app.muted == False):
                Sound("../../libraries/Audio/eerie.mp3").play(restart = True)
        wrap_around()
        move_balls()
        move_asteroids()
        hit_detection()
        remove_scores()
        blow_up_balls()
        move_enemy_shots()
        shots_vs_ship()
        update_high_score()
        update_stats()
        
def toggle_pause():
    '''
    Takes no args and returns no values
    If game is paused, this will unpause it, 
    If game is unpaused, this will pause it
    Entails changing opacity of pause screen features and changing app setting
    '''
    if(app.failed == False):
        if app.play == False:
            app.play = True
            pauseScreen.visible = False
        else:
            app.play = False
            pauseScreen.visible = True
def onMousePress(x,y):
    if(pauseScreen.visible == True):
        if(closeGameButton.contains(x,y)):
            update_stats()
            sys.exit(0)
        if(backToLauncher.contains(x,y)):
            update_stats()
            os.chdir("../")
            subprocess.Popen([sys.executable, backToLauncher.game])
            sys.exit(0)

def onKeyPress(key):
    '''
    Built-in CMU function
    Takes are argument each key press
    In this script, used to reset the game after a run ends
    '''
    if(key=='enter'):
        if(app.play == False):
            reset()
    if(key == "p" or key == "P" or key == "escape"):
        toggle_pause()
    if(key =='m' or key =='M'):
        toggle_mute()
        

def wrap_around():
    '''
    no args and no returns
    Moves the ship to the other side of the screen if it flies off of the edge
    Such that you pop up on the left if you flew off of the right side, at the top if you exited at the bottom, etc.
    Deterministic relocation, not randomized. Speed is retained
    '''
    if not(screen.containsShape(ship)):
        if(ship.centerX>=app.width):
            ship.centerX = 0
        elif(ship.centerX<0):
            ship.centerX = app.width-1
        if(ship.centerY<0):
            ship.centerY = app.height-1
        elif(ship.centerY>app.height):
            ship.centerY = 0
            
score.toFront()
hiScore.toFront()
fullInfoList[4]+=1
fullInfoList[3]+=1     


app.run()