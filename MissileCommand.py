from cmu_graphics import *
import random
import sys
import subprocess
import os
import pyautogui

size = pyautogui.size()
width = size[0]
height = size[1]
app.setMaxShapeCount(100000000)
app.autofs = 0

default = [0,0,0,0,0,0,0,0]
keys = ["HighScore", "GamesPlayed", "Shots", "Hits", "EnemiesDestroyed", "CitiesLost", "TimesLaunched", "HighestLevel"] 
fullInfoList = []

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


gameInfo = open("Files/MissileCommandStats.txt", "r+")

app.hiscore = fullInfoList[0]

app.width = width
app.height = height
app.play = True
app.munitionCounter = 0 
app.score = 0
nightSky = Rect(0,0,app.width, app.height)
app.cities = 6
app.gate = 3500
app.generalReload = app.stepsPerSecond*2.5
app.level = 1 
app.mult = app.level
app.shotSpeedLR = ((width*height)**0.5)/88 ### Roughly around 15 on standard macbook screen, but it is now relative to screen size
app.shotSpeedMid = ((width*height)**0.5)/66 ### Roughly around 20 on standard macbook screen, but it is now relative to screen size
app.basicMissileSpeed = (1/525) * height ### Only vertical so more simple calculation
app.multiBombSpeed = ((width*height)**0.5)/522 ### Roughly around 3 on standard macbook screen, but it is now relative to screen size
app.planeSpeed = (1/280) * width ### Only horizontal so more simple calculation
app.spawnTimer = app.stepsPerSecond * 5
app.enemiesLeftToSpawn = (app.level*7) + 5
app.bombSpeed = (1/210) * height ### Mostly vertical (some horizontal but not alot) so simpler calculation
app.flakSpeed = ((width*height)**0.5)/25 ## Roughly around 63 on a standard macbook, but is now relative to screen size
app.gravity = 0.05
app.saucerSpeed = (1/560) * width ### Only horizontal so more simple calculation
app.ufoProjectileSpeed = ((width*height)**0.5)/142 ### Roughly round 11 on standard macbook screen, but now relative to screen size
app.timeToDropBombs = app.width//app.planeSpeed
app.infoTimer = app.stepsPerSecond*5
app.infoShowing = False
app.pause = False
app.muted = False
specialWarningInfo = Group()
app.warningTimer = 0
app.planeSound = Sound("Audio/planeflying.mp3")
app.plane = False
app.flakNum = 0

outerPause = Rect(app.width/2, app.height/2, app.width/5, app.width/10, fill=None, border = 'yellow', borderWidth = 2, align = 'center')
pauseLabel = Label("Game Paused", app.width/2, app.height/2 -15, size = 30, fill= 'white')
closeGameButton = Rect(outerPause.left, outerPause.centerY, outerPause.width//2, outerPause.height//2, fill=None, border = 'red')
closeGameButton.words = Label("Close Game", closeGameButton.centerX, closeGameButton.centerY, size = 15, fill = 'white')
backToLauncher = Rect(closeGameButton.right+1, closeGameButton.top, outerPause.width//2, outerPause.height//2, fill=None, border = 'gray')
backToLauncher.game = "PretendLauncher.py"
backToLauncher.words = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 15, fill='white')
pauseScreen = Group(outerPause, pauseLabel, closeGameButton, backToLauncher, backToLauncher.words, closeGameButton.words)
pauseScreen.visible = False

leftBattery = Rect((1/40)*app.width, (19/20)*app.height, (1/12) * app.width, (1/20)*app.height)
midBattery = Rect(app.width/2, (19/20)*app.height, (1/12) * app.width, (1/20)*app.height, align = 'top')
rightBattery = Rect((39/40)*app.width, (19/20)*app.height, (1/12) * app.width, (1/20)*app.height, align = 'top-right')
batteries = [leftBattery, midBattery, rightBattery]
targets = Group()
defense = Group()
basicMissiles = Group()
explosion = Group()
cities = Group()
bubbles = Group()
planes = Group()
bombs = Group()
multiBombs = Group()
multiBombPostSplit = Group()
nonbasicMissiles = Group()
smartMissiles = Group()
ufos = Group()
ufoShots = Group()
gameOver = Group()
info = Group()
visibleScores = Group()
flakTargets = Group()
flakShots = Group()
flak = Group()
score = Label("Score: %05d" %app.score, leftBattery.centerX, (1/40)*app.height, size = 20, fill='white')
stage = Label("Level: %1d" %app.level, app.width*1/3 , (1/40)*app.height, size = 20, fill = 'white')
newLevelWarning = Label("Enemies until next level: %d" % app.enemiesLeftToSpawn, app.width * 2/3, (1/40)*app.height, size = 20, fill='white')
hiscore = Label("High Score: %05d" %app.hiscore, rightBattery.centerX, (1/40)*app.height, size = 20, fill='white')

def create_scores(x,y,val):
    '''
    Takes 3 args, 2 positional and 1 value to display
    Returns no values but does create a shape and add it to a relevant group    
    '''
    visibleScores.add(Label("+ %3d" %val, x-10, y, fill=None, border = 'white', size = 14))
    
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

def display_reward_extra_city():
    '''
    Takes no args and returns no values, but adds shapes to an approprate group
    Used to relay information regarding a score milestone and unlocking a bonus city
    '''
    box = Rect(0, score.centerY * 2, app.width/8, app.height/10, fill=None)
    label2 = Label("You have unlocked a bonus city", 5, box.top, fill='white', align = 'top', size = 15)
    label3 = Label("Survive this wave to spawn your bonus city", 5, label2.bottom+2, fill='white', align = 'top-left', size = 15)
    info.add(box, label2, label3)
    app.infoTimer = app.stepsPerSecond*5

def make_city(x, j):
    '''
    Takes 2 args, a starting position and a value meant to be used as an id
    x will be the leftmost position of the city and j will be the id
    Returns a shape group representing a city
    Used to create cities on the game screen
    '''
    city = Group()
    lastWidth = 0
    city.id = j
    city.health = 5
    cityids.append(city.id)
    for i in range(12):
        tall = randrange(5,80)
        wide = randrange(4,15)
        lastWidth = wide
        building = Rect(x+lastWidth+ i*(app.width/200), app.height-tall, wide, tall, border = 'white')
        building.note = Sound("Audio/explosion.mp3")
        building.flakTimer = randrange(app.stepsPerSecond, 3*app.stepsPerSecond) ## Mostly for when a new city is added, such that all buildings do not weirdly fire at the same time
        city.add(building)
    return city

city_coords = [(15/60)*app.width, (41/60)*app.width, (21/60)*app.width, (35/60)*app.width, (47/60)*app.width, (9/60)*app.width]
cityids = []

def make_all_cities_new_level():
    '''
    Takes no args and returns no values but adds shape groups to an appropriate group
    Should only be used at the start of each level
    If used at the appropriate time, existing cities will remain and new cities will fill in empty spots if the user has extra cities
    '''
    for i in range(app.cities):
        if(app.cities> len(cities)):
            if not(i in cityids):
                if(i<6):
                    cities.add(make_city(city_coords[i], i))

def reset():
    '''
    Takes no args and returns no values
    Should only be called if the game has ended and the player initiates another round
    Resets all important app values, scores, ammo, health, level, spawning, and cities
    '''
    info.clear()
    fullInfoList[1]+=1
    app.spawnTimer = app.stepsPerSecond * 5
    app.enemiesLeftToSpawn = 10
    app.score = 0
    score.value = "Score: %05d" %app.score
    app.munitionCounter = 0
    app.gate = 3500
    app.generalReload = app.stepsPerSecond*2.5
    app.level = 1
    app.mult = app.level
    app.cities = 6
    app.flakNum = 0
    stage.value = "Level %1d" %app.level
    newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    app.pause = False
    gameOver.clear()
    for bat in batteries:
        bat.reloadTimer = 0
        bat.repairTimer = 0
        bat.ammoCount = 10
        bat.border = 'grey'
        app.bat = batteries[0]
        bat.repairLabel.value = "Repaired in %1.1f" %bat.repairTimer
        reload_all()
    make_all_cities_new_level()
    app.play = True
    pauseScreen.centerX = app.width/2
    pauseScreen.visible = False
    update_stats()

def starting_bat():
    '''
    Takes no args and returns no values
    Should only be called at the start of a new round
    Initiates important keys and labels and values for the missile batteries
    '''
    for bat in batteries:
        bat.repairTimer = 0
        bat.reloadTimer = 0
        bat.ammoCount = 10
        bat.repairLabel = Label("Repaired in %1.1f" %bat.repairTimer, bat.centerX, bat.centerY, fill='white', size= 12)
        bat.timer = Label("Ready in: %1.1f" %bat.reloadTimer, bat.centerX, bat.top+5, fill='white', size = 12, align = 'top')
        bat.ammo = Label("Ammo: %1d" %bat.ammoCount, bat.centerX, bat.bottom-5, fill='white', size = 12, align = 'bottom')
        bat.fill=None
        bat.border = 'gray'
        bat.broken = False
        bat.borderWidth = 3

def get_index(list, item):
    '''
    Takes 2 args (list and item) and returns the first index of the item in that list, -1 if it isn't in the list
    In this program, lists sent to this function will never have duplicates so it will return the one and only occurance of the item
    '''
    for i in range(len(list)):
        if list[i] == item:
            return i
    return -1

def update_score():
    '''
    Takes no args and returns no values
    Updates high score if current score is higher, 
    Updates the displayed current score to reflect actual score
    '''
    if (app.score>=app.gate):
        app.cities+=1
        app.gate*=2
        display_reward_extra_city()
        if(app.muted == False):
            Sound("Audio/eerie.mp3").play(restart = True)
    if(app.score> app.hiscore):
        app.hiscore = app.score
    score.value = "Score: %05d" %app.score
    hiscore.value = "High Score: %05d" %app.hiscore
    fullInfoList[0] = app.hiscore
    
def update_stats():
    '''
    Takes no args and returns no values
    Updates game stats stored in an external txt file
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")

def spawn_plane(y, canScore):
    '''
    Takes one positional arg and returns no values
    y represents the height on the screen that the shape will be spawned
    Creates a shape with certain attributes
    Then adds that shape to an appropriate group
    '''
    hitbox = Oval(-20, y, 40, 10, border = 'white', fill='gray')
    hitbox.bombs = app.level//2+1
    hitbox.angle = angleTo(hitbox.centerX, hitbox.centerY, app.width+30, hitbox.centerY)
    hitbox.next = getPointInDir(hitbox.centerX, hitbox.centerY, hitbox.angle, app.planeSpeed)
    hitbox.dropZones = []
    hitbox.flakHP = 5 ### Only relevant for city flak hits 
    if(canScore == True):
        hitbox.score = 625
    else:
        hitbox.score = 0
    spacing = app.width// hitbox.bombs
    for i in range(hitbox.bombs):
        hitbox.dropZones.append(spacing * (i+1) + randrange(-50, 51, 1))
    app.plane = True
    hitbox.hitIDs = []
    planes.add(hitbox)
    
def move_fun_missiles():
    '''
    Takes no args and returns no values
    Moves shapes across the screen based on specific attributes the shapes possess
    Makes decisions about speed and next location for each shape    
    Shapes controlled by this function are such missiles that have trails, horizontal motion, and are affected by gravity 
    '''
    for missile in nonbasicMissiles:
        missile.centerX, missile.centerY = missile.next
        missile.centerY += missile.gravSpeed
        missile.gravSpeed += app.gravity
        spawn_trail(missile.centerX, missile.centerY, missile.fill)
        if(missile.rotateAngle<270):
            missile.rotateAngle+=2
        else:
            missile.rotateAngle-=2
        missile.rotateAngle 
        missile.next = getPointInDir(missile.centerX, missile.centerY, missile.rotateAngle, missile.speed)
    
def move_bombs(type):
    '''
    Takes 1 arg and retuns no values
    type in this case is a shape group, representing a type of projectile
    Shapes controlled by this function are bombs with horizontal motion that are affected by gravity
    '''
    for bomb in type:
        bomb.centerX, bomb.centerY = bomb.next
        bomb.speed = bomb.speed + app.gravity
        bomb.next = getPointInDir(bomb.centerX, bomb.centerY, bomb.rotateAngle, bomb.speed)   
    
def move_planes():
    '''
    Takes no args and returns no values
    Moves shapes across the screen
    Shapes controlled by this function are bomber planes
    '''
    for plane in planes:
        plane.centerX, plane.centerY = plane.next 
        plane.next = getPointInDir(plane.centerX, plane.centerY, plane.angle, app.planeSpeed)
        if(plane.centerX>=app.width+plane.width):
            planes.remove(plane)

def get_next_index(list, current):
    '''
    Takes 2 args, a list and an index in that list, returns an index in the given list
    This function specifially provides the index directly after the given index
    Will return 0 in the case that the next index would be out of bounds
    '''
    if  current == len(list) -1:
        return 0
    else:
        return current + 1

def select_next_bat(bat):
    '''
    takes 1 arg and retuns 1 value
    the argument is the currently selcted missile battery, and the return is the next possible missile battery
    Attempts to get the next battery and will, unless it is broken or out of ammo.
    In that case, it tries again to get the next battery. If that one is also broken or empty, return current battery
    In this program there can never be more than 3 batteries, so this function will work only on this number of batteries
    This function will be called based on user input of requesting the next battery, or directly after firing to auto sequence the batteries
    '''
    index = get_index(batteries, bat)
    nextIndex = get_next_index(batteries, index)
    if(batteries[nextIndex].broken == False and batteries[nextIndex].ammoCount >= 1):
        return batteries[nextIndex]
    else:
        nextIndex = get_next_index(batteries, nextIndex)  
    if(batteries[nextIndex].broken == False and batteries[nextIndex].ammoCount >= 1):
        return batteries[nextIndex]
    else:
        return bat

def get_prev_index(list, current):
    '''
    Takes 2 args, a list and an index in that list, returns an index in the given list
    This function specifially provides the index directly prior to the given index
    Will return maximum index in the array in the case that the previous index would be out of bounds
    '''
    if  current == 0:
        return len(list) - 1 
    else:
        return current - 1

def select_prev_bat(bat):
    '''
    takes 1 arg and retuns 1 value
    the argument is the currently selcted missile battery, and the return is the previous possible missile battery
    Attempts to get the previous battery and will, unless it is broken or out of ammo.
    In that case, it tries again to get the previous battery. If that one is also broken or empty, return current battery
    In this program there can never be more than 3 batteries, so this function will work only on this number of batteries
    '''
    index = get_index(batteries, bat)
    prevIndex = get_prev_index(batteries, index)
    
    if(batteries[prevIndex].broken == False and batteries[prevIndex].ammoCount >= 1):
        return batteries[prevIndex]
    else:
        prevIndex = get_prev_index(batteries, prevIndex)  
    if(batteries[prevIndex].broken == False and batteries[prevIndex].ammoCount >= 1):
        return batteries[prevIndex]
    else:
        return bat

def spawn_bombs(x,y, canScore):
    '''
    Takes 2 positional arguments, x and y for horizontal and vertical spawning respectively
    Creates a shape with specific attributes anf adds it to a shape group, returns no values
    Typicallt used to drop bombs from bomber planes
    '''
    bomb = Oval(x,y,2,8, fill = 'white')
    bomb.speed = app.bombSpeed
    bomb.rotateAngle = angleTo(bomb.centerX, bomb.centerY, bomb.centerX + randrange(30, 80), app.height)
    bomb.next = getPointInDir(bomb.centerX, bomb.centerY, bomb.rotateAngle, bomb.speed)
    bomb.flakHP = 1 ### Only relevant for city flak hits 
    if(canScore == True):
        bomb.score = app.level * 50
    else:
        bomb.score = 0
    bomb.hitIDs = []
    bombs.add(bomb)

def bat_color_update():
    '''
    Takes no args and returns no values
    Used to make it obvious to the player which missile batteries are broken, and which is the currently selected battery
    Acheives this goal by changing border color on the batteries
    '''
    for bat in batteries:
        if(bat.broken == True):
            bat.border = 'red'
        elif app.bat == bat:
            bat.border = 'white'
        else:
            bat.border = 'gray'

def make_target(x,y):
    '''
    Takes 2 positional args, x and y for horizontal and vertical position respectively
    Returns no values, but does add a shape to the appropriate group
    The target is what the player fired munitions use to determine when to automatically explode
    The target will be placed at the spot of a player mouse click    
    '''
    new = Circle(x,y,1)
    new.num = app.munitionCounter
    targets.add(new)
    
def advance_stage():
    '''
    Takes no args and returns no values
    should only be called when a level is over, however, this function will still work if called at other times, (not recommended)
    Grants extra score based on certain game conditions
    '''
    app.score+=len(cities)*25*app.mult
    sum = 0
    for bat in batteries:
        sum+= bat.ammoCount
        if(bat.broken == False):
            sum += 20
    app.score+=sum*app.mult
    app.level+=1
    if(app.muted == False):
        Sound("Audio/levelup.mp3").play(restart = True)
    stage.value = "Level: %1d" %app.level
    app.mult = app.level   
    app.enemiesLeftToSpawn = (app.level*7) + 5
    app.spawnTimer = app.stepsPerSecond*4
    newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    if(app.level>fullInfoList[7]):
        fullInfoList[7]+=1
        update_stats()
    
def kaboom_all():
    '''
    Takes no args and returns no values
    Expands explosions to a particular size
    Then removes them from view after a certain amound of time
    This function is crucial to ensuring that explosions can disrupt or destroy enemies
    '''
    for object in explosion:
        if(object.time <= 0):
            object.opacity-=10
        if(object.radius<=(1/125)*app.width): 
            object.radius+=1
        if object.radius >=(1/200)*app.width:
            object.time -= 1
        if object.opacity == 0:
            explosion.remove(object)
    for flakShot in flak:
        if(flakShot.time <= 0):
            flakShot.opacity-=10
        else:
            flakShot.time-=1
        if flakShot.opacity == 0:
            flak.remove(flakShot)
        

def explode_object(shape, causedByPlayer):
    '''
    Takes a shape and bool as arguments, and returns no values
    adds a new shape to an appropriate shape group
    New shape is based on the location of the given shape
    '''
    new = Circle(shape.centerX, shape.centerY, 3, fill='yellow', border = 'orange')
    new.time = app.stepsPerSecond * 3
    new.willScore = causedByPlayer
    explosion.add(new)

def display_mac_window_warning():
    '''
    Takes no args and returns no values
    Creates 2 labels and adds them to a mac warning
    sets a timer for how long to display the message
    '''
    specialWarningInfo.add(Label("Your window is not maximised", app.width/2, app.height/2, fill = 'white', size = 80))
    specialWarningInfo.add(Label("Maximise your window to play the game", app.width/2, app.height/2 + 50, fill = 'white', size = 80))
    app.warningTimer = app.stepsPerSecond * 3

def hide_mac_window_warning():
    '''
    Takes no args and returns no values
    Handles lowering of timer for mac warning
    removes the message when the timer has reached zero
    '''
    app.warningTimer -= 1
    if(app.warningTimer<=0):
        specialWarningInfo.clear()

def move_shots():
    '''
    Takes no args and returns no values
    Moves the player fired munitions towards their intended location. 
    Crucial function. Game will not work without this function.
    Forces an explosion if the target is hit ot bypassed
    '''
    for shot in defense:
        spawn_trail(shot.centerX, shot.centerY, shot.fill)
        shot.centerX, shot.centerY = shot.next
        if(shot.loc == 'mid'):
            shot.next = getPointInDir(shot.centerX, shot.centerY, shot.rotateAngle, app.shotSpeedMid)
        else:
            shot.next = getPointInDir(shot.centerX, shot.centerY, shot.rotateAngle, app.shotSpeedLR)
        if shot.centerY <= shot.target[1]:
            for target in targets:
                if shot.num == target.num:
                    explode_object(target, True)
                    targets.remove(target)
            defense.remove(shot)
            
def onKeyPress(key):
    '''
    CMU built in funciton which takes a pressed key as input
    used in this function to select firing batteries and to restart the game upon loss
    '''
    if(app.pause == False):
        if(key == 'right'):
            app.bat = select_next_bat(app.bat)
        if(key == 'left'):
            app.bat = select_prev_bat(app.bat)
        bat_color_update()
    if(app.play == False):
        if(key == 'enter'):
            reset()
    if(key == "escape" or key =='p' or key =='P'):
        toggle_pause() 
    if(key == 'm' or key == "M"):
        toggle_mute()

def reload_all():
    '''
    Takes no args and returns no values
    Ensures that reloading, ammo counts, repair times are all accurate for each missile battery
    '''
    sum_not_broken = 0
    for bat in batteries:
        bat.ammo.value = "Ammo: %1d" %(bat.ammoCount)
        if(bat.reloadTimer>0):
            bat.reloadTimer-=1
            bat.timer.value = "Ready in: %1.1f" %(bat.reloadTimer / app.stepsPerSecond)
        if(bat.repairTimer>0):
            bat.repairTimer-=1
            bat.repairLabel.value = "Repaired in: %1.1f" %(bat.repairTimer / app.stepsPerSecond)
        else: 
            bat.broken = False
            sum_not_broken += 1
    if(sum_not_broken == 1 and app.bat.broken == True):
        app.bat = select_next_bat(app.bat)
    bat_color_update()        

def bombing_logic():
    '''
    Takes no args and returns no values
    This function controls the dropping of bombs from bomber planes
    '''
    for plane in planes:
        if plane.bombs>=1:
            if(plane.centerX>= plane.dropZones[0]):
                plane.dropZones.pop(0)
                if(plane.score == 0):
                    spawn_bombs(plane.centerX, plane.centerY, False)
                else:
                    spawn_bombs(plane.centerX, plane.centerY, True)
                plane.bombs-=1

def spawn_basic_missile(x,y, canScore):
    '''
    Takes 2 args and returns no values
    Adds new shape with special attributes to shape group
    This function creates the most basic enemy in the game, a basic missile, no horizontal motion, not affected by gravity
    '''
    new = Circle(x,y, 6, fill = 'limeGreen')
    new.num = app.munitionCounter
    if(canScore == True):
        new.score = 100
    else:
        new.score = 0
    new.rotateAngle = angleTo(x,y,x,app.height)
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, app.basicMissileSpeed)
    new.flakHP = 15 ### Only relevant for city flak hits 
    new.hitIDs = []
    basicMissiles.add(new)

def spawn_trail(x, y, color):
    '''
    Takes 3 args and returns no values
    Creates a shape and adds it to the appropriate shape group
    The trails in this program will represent missile streaks and rocket burns
    '''
    bubbles.add(Circle(x, y, 2, fill =  color, opacity = 90))
                
def explosion_vs_bombs(type):
    '''
    Takes 1 arg and returns no values
    type represents the shape group whose children are being checked against explosion hits
    Crucial function, withouth this function, explosions will not affect enemies
    '''
    for shape in explosion:
        for bomb in type:
            if(shape.hitsShape(bomb)):
                if(app.muted == False): 
                    Sound("Audio/medium.mp3").play(restart = True)
                if(shape.willScore == True):
                    points = bomb.score * app.mult
                    app.score+= points
                    create_scores(bomb.centerX, bomb.centerY, points)
                    fullInfoList[3]+=1
                explode_object(bomb, shape.willScore)
                type.remove(bomb)
                fullInfoList[4]+=1
                
def move_ufo_shots():
    '''
    Takes no args and returns no values
    Controls the motion of shots fired by ufos by 
    1. moving them to their next location and 
    2. calculating the new next location
    '''
    for shot in ufoShots:
        shot.centerX, shot.centerY = shot.next 
        shot.next = getPointInDir(shot.centerX, shot.centerY, shot.rotateAngle, app.ufoProjectileSpeed)                
                
def create_saucer(top, bottom, lr):
    '''
    Takes 3 args relating to acceptable spawning zone for the saucer
    top, bottom are the bounds of height for the ufo
    lr represents whether it should spawn on the left of right of the screen
    Creates a saucer group and places it in the acceptable spawning zone
    returns the saucer group
    '''
    new = Group()
    saucerTop = Arc(100,100, 80, 40, 270, 180, fill=None, border = 'white')
    saucerMid = Rect(55, 100, 90, 10, fill="gray")
    saucerBottom = Arc(100, 110, 90, 20, 90, 180, fill='white')
    randX = 0
    randY = randrange((int)(top), (int)(bottom))
    if lr == 0:
        randX = -100
    else:
        randX = app.width+100
    new.add(saucerTop, saucerMid, saucerBottom)
    new.centerX = randX
    new.centerY = randY
    new.angle = angleTo(new.centerX, new.centerY, app.width/2, new.centerY)
    new.next = getPointInDir(new.centerX, new.centerY, new.angle, app.saucerSpeed)
    return new                 
                
def missiles_vs_bat(type):
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against hitting the missile batteries
    Crucial function, withouth this function, enemies will not affect player missile batteries
    '''
    for missile in type:
        for bat in batteries:
            if(missile.hitsShape(bat) or bat.containsShape(missile)):
                explode_object(missile, False)
                type.remove(missile)
                bat.broken = True
                bat.repairTimer += 25*app.stepsPerSecond
                if(app.muted == False):
                    Sound("Audio/explosion.mp3").play(restart = True)
                if bat == app.bat: app.bat = select_next_bat(app.bat)
                bat_color_update()
                
def bombs_vs_bat(type):
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against hitting the missile batteries
    Crucial function, withouth this function, enemies will not affect player missile batteries
    This function differs from missiles_vs_bat in that it shortens the impact as it is only meant to be used regarding smaller enemy munitions
    '''
    for missile in type:
        for bat in batteries:
            if(missile.hitsShape(bat) or bat.containsShape(missile)):
                explode_object(missile, False)
                type.remove(missile)
                bat.broken = True
                bat.repairTimer += 10*app.stepsPerSecond
                if(app.muted == False):
                    Sound("Audio/medium.mp3").play(restart = True)
                if bat == app.bat: app.bat = select_next_bat(app.bat)
                bat_color_update()

def missile_vs_ground(type):
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against hitting the ground
    Important for realism and also preventing lag since it forces deletion of shapes that would be below the screen
    '''
    for missile in type:
        if missile.bottom>= height: ## using height here, not app.height because height is the actual size, and app.height is the window size
            explode_object(missile, False)
            if(app.muted == False):
                Sound("Audio/medium.mp3").play(restart = True)
            type.remove(missile)

def missiles_vs_cities(type):
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against hitting the cities
    Crucial function, withouth this function, enemies will not affect cities and the game could never end
    '''
    for missile in type:
        for city in cities:
            if(missile.hitsShape(city)):
                cityids.remove(city.id)
                for building in city.children:
                    if(app.muted == False):
                        building.note.play(restart = True)
                    explode_object(building, False)
                explode_object(missile, False)
                type.remove(missile)
                cities.remove(city)
                app.cities-=1
                fullInfoList[5]+=1
                
def bombs_vs_cities(type):
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against hitting the cities
    Crucial function, withouth this function, enemies will not affect cities and the game could never end
    This function differs from missiles_vs_cities in that it does small damage to cities instead of full damage, to reflect the smaller munitions
    '''
    for bomb in type:
        for city in cities:
            if(city.health<=1):
                if(bomb.hitsShape(city)):
                    for building in city.children:
                        explode_object(building, False)
                        if(app.muted == False):
                            building.note.play(restart = True)
                    explode_object(bomb, False)
                    type.remove(bomb)
                    cityids.remove(city.id)
                    cities.remove(city)
                    app.cities-=1
                    fullInfoList[5]+=1    
            else:
                for building in city:
                    if(bomb.hitsShape(building)):
                        if(app.muted == False):
                            building.note.play(restart = True)
                        explode_object(building, False)
                        explode_object(bomb, False)
                        type.remove(bomb)
                        city.remove(building)
                        city.health-=1

    
def missiles_vs_anti_missiles(type):
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against being hit directly by player munitions
    Crucial function, withouth this function, player munitions would phase through enemies and only explosions would affect enemies
    Also rewards players with a 5x bonus for direct impacts, to provide some risk-reward motivaiton
    '''
    for missile in type:
        for anti in defense:
            if(missile.hitsShape(anti)):
                for target in targets:
                    if(target.num == anti.num):
                        targets.remove(target)
                explode_object(missile, True)
                if(app.muted == False):
                    Sound("Audio/uwexplosion.mp3").play(restart = True)
                points = missile.score*app.mult*5
                app.score+=points
                create_scores(missile.centerX, missile.centerY, points)
                type.remove(missile)
                defense.remove(anti)
                fullInfoList[3]+=1
                fullInfoList[4]+=1
       
       
def decrease_health(item, group, x3):
    '''
    Takes 3 arguments:
    item, which is a shape
    group, which is the group the shape belongs to
    x3 is a boolean such that True means the score should get a 3x multiplier
    Returns no values
    Decreases the hp of the item and destroys it if appropriate, removing it from the group
    In destruction case, adds appropriate score to player score
    '''
    if(x3 == True):
        item.flakHP-=3
    else:
        item.flakHP-=1 
    if(item.flakHP<=0):
        points = item.score * app.mult
        if(x3 == True):
            points = points * 3
            if(app.muted == False):
                Sound("Audio/uwexplosion.mp3").play(restart = True)
        else:
            if(app.muted == False):
                Sound("Audio/medium.mp3").play(restart = True)
        app.score+= points
        create_scores(item.centerX, item.centerY, points)
        explode_object(item, True)  
        group.remove(item)    
       
def flak_vs_group(group):
    '''
    Takes 1 arg, group, which represents a shape group
    Checks if flak explosions hit any of the shapes in that group and handles decrememnting health
    Returns no values
    '''
    for item in group:
        for flakExplosion in flak:
            if(item.hitsShape(flakExplosion)):
                if(not flakExplosion.id in item.hitIDs):
                    item.hitIDs.append(flakExplosion.id)
                    decrease_health(item, group, False)

def direct_flak_vs_group(group):
    '''
    Takes 1 arg, group, which represents a shape group
    Checks if direct flak shots hit any of the shapes in that group and handles decrememnting health
    Returns no values
    '''
    for item in group:
        for flakBullet in flakShots:
            if(item.hitsShape(flakBullet)):
                if(not flakBullet.id in item.hitIDs):
                    item.hitIDs.append(flakBullet.id)
                    decrease_health(item, group, True) 
                for target in flakTargets:
                    if(flakBullet.id == target.id):
                        new = Circle(target.centerX, target.centerY, 3, fill='grey', border = 'yellow', borderWidth = 0.5)
                        new.time = app.stepsPerSecond
                        new.id = target.id
                        flak.add(new)
                        flakTargets.remove(target)
                        flakShots.remove(flakBullet)
    
                        

def hit_detection():
    '''
    Takes no args and returns no values
    Calls all functions related to impacts
    Possibly the most crucial function as scoring, destruction failing would be impossible without it
    '''
    missiles_vs_bat(basicMissiles)
    bombs_vs_bat(bombs)
    missiles_vs_bat(ufoShots)
    missiles_vs_bat(nonbasicMissiles)
    bombs_vs_bat(multiBombPostSplit)
    missiles_vs_cities(basicMissiles) 
    bombs_vs_cities(bombs) 
    bombs_vs_cities(ufoShots)
    bombs_vs_cities(multiBombPostSplit)
    missiles_vs_cities(smartMissiles)
    missiles_vs_bat(smartMissiles)
    missiles_vs_cities(nonbasicMissiles)
    missiles_vs_anti_missiles(basicMissiles)
    missiles_vs_anti_missiles(ufoShots)
    missiles_vs_anti_missiles(ufos)
    missiles_vs_anti_missiles(multiBombs)
    missiles_vs_anti_missiles(multiBombPostSplit)
    missiles_vs_anti_missiles(nonbasicMissiles)
    missiles_vs_anti_missiles(planes)
    missiles_vs_anti_missiles(smartMissiles)
    explosion_vs_bombs(bombs)
    explosion_vs_bombs(basicMissiles)
    explosion_vs_bombs(nonbasicMissiles)
    explosion_vs_bombs(planes)
    explosion_vs_bombs(ufos)
    explosion_vs_bombs(multiBombs)
    explosion_vs_bombs(multiBombPostSplit)
    explosion_vs_bombs(ufoShots)
    explosion_vs_bombs(smartMissiles)
    missile_vs_ground(basicMissiles)
    missile_vs_ground(bombs)
    missile_vs_ground(ufoShots)
    missile_vs_ground(multiBombPostSplit)
    missile_vs_ground(nonbasicMissiles)
    missile_vs_ground(smartMissiles)
    flak_vs_group(basicMissiles)
    flak_vs_group(planes)
    flak_vs_group(bombs)
    flak_vs_group(nonbasicMissiles)
    flak_vs_group(multiBombs)
    flak_vs_group(multiBombPostSplit)
    flak_vs_group(ufoShots)
    flak_vs_group(smartMissiles)
    direct_flak_vs_group(basicMissiles)
    direct_flak_vs_group(planes)
    direct_flak_vs_group(bombs)
    direct_flak_vs_group(nonbasicMissiles)
    direct_flak_vs_group(multiBombs)
    direct_flak_vs_group(multiBombPostSplit)
    direct_flak_vs_group(ufoShots)
    direct_flak_vs_group(smartMissiles)
    
    
def move_trail():
    '''
    Takes no args and returns no values
    Slowly dissipates missile trails until they are invisbile
    Subsequently removes the trail peices as they are fully invisible
    '''
    for bubble in bubbles:
        if(bubble.opacity>0):
            bubble.opacity -=1
        else:
            bubbles.remove(bubble)

def move_basic_missiles():
    '''
    Takes no args and returns no values
    Moves the most common and basic enemy type, the basic missile
    No horizontal movement, no gravity
    '''
    for thing in basicMissiles:
        spawn_trail(thing.centerX, thing.centerY, thing.fill)
        thing.centerX, thing.centerY = thing.next
        thing.next = getPointInDir(thing.centerX, thing.centerY, thing.rotateAngle, app.basicMissileSpeed)
        if(thing.centerY>=app.height):
            basicMissiles.remove(thing)

def check_loss():
    '''
    Takes no args and returns no values
    Checks if the player has met the conditions to lose the game
    Will clear all enemies and create a game over screen in that case
    '''
    if(len(cities) == 0):
        app.play = False
        targets.clear()
        defense.clear()
        basicMissiles.clear()
        flak.clear()
        flakShots.clear()
        flakTargets.clear()
        explosion.clear()
        cities.clear()
        bubbles.clear()
        planes.clear()
        bombs.clear()
        multiBombs.clear()
        multiBombPostSplit.clear()
        nonbasicMissiles.clear()
        smartMissiles.clear()
        ufos.clear()
        ufoShots.clear()
        targets.clear()
        defense.clear()
        gameOver.add(RegularPolygon(app.width/2, app.height/2, app.width/2, 4, fill=None))
        gameOver.add(Label("All Cities Lost", app.width/2, app.height/4, fill='white', size = 30))
        gameOver.add(Label("Final Score: %d" %app.score, app.width/2, 3*app.height/8, fill='white', size = 30))
        gameOver.add(Label("High Score: %d" %app.hiscore, app.width/2, app.height/2, fill='white', size = 30))
        gameOver.add(Label("Press Enter to Restart", app.width/2, 5*app.height/8, fill='white', size = 30))
        pauseScreen.visible = True
        pauseScreen.left = 0

def check_win():
    '''
    Takes no args and returns no values
    Checks whether or not the player has met the requirements to advance in the game
    Forces progress in that case
    '''
    if (app.enemiesLeftToSpawn == 0):
        advance_stage()
        make_all_cities_new_level()
        for bat in batteries:
            bat.ammoCount+=(10 + app.level*2) 
        
def spawn_small_bombs(x,y,num, canScore):
    '''
    Takes 3 args, x and y for position, num for counting how many to spawn
    Spawns num many small bombs at the specified location
    adds them all to the appropriate shape group
    '''
    for i in range(num):
        new = Circle(x,y,2, fill='cyan')
        new.rotateAngle = angleTo(x,y,randrange(x-(app.width//10), x+(app.width//10)), app.height)
        new.next = getPointInDir(x,y,new.rotateAngle, app.bombSpeed)
        if(canScore == True):
            new.score = 100
        else:
            new.score = 0
        new.speed = app.bombSpeed
        new.flakHP = 1
        new.hitIDs = []
        multiBombPostSplit.add(new)
    if(app.muted == False):
        Sound("Audio/pop.mp3").play(restart = True)
    
def spawn_multi_bomb(x, detHeight, canScore):
    '''
    Takes 2 args, x for horizontal location and detHeight for when the bomb should explode
    Returns no values but adds a shaoe with special attributes to the appropriate shape group
    This is a special enemy type which will reach a designated height, and then spawn several smaller faster bombs which are nearly impossible to shoot down
    Players should shoot this enemy down quickly
    '''
    new = Circle(x,-10, 12, fill = 'cyan')
    new.num = app.munitionCounter
    new.detHeight = detHeight
    new.bombs = app.level//2 + 2
    if(canScore == True):
        new.score = 750 + (125 * new.bombs)
    else:
        new.score = 0
    new.speed = app.multiBombSpeed
    new.rotateAngle = angleTo(new.centerX,new.centerY,randrange(app.width//4, 3*(app.width//4)),detHeight)
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, new.speed)
    new.flakHP = 4 ### Only relevant for city flak hits 
    new.hitIDs = []
    multiBombs.add(new)
    
def move_multi_bomb():
    '''
    Takes no args and retuens no values
    Controls the motion of the multi bomb enemy
    The primary enemy is affected by horizontal motion and gravity
    Ppon reaching a specific height, bursts and spreads smaller bombs which are harder to track
    '''
    for bomb in multiBombs:
        bomb.centerX, bomb.centerY = bomb.next 
        bomb.speed += app.gravity
        bomb.next = getPointInDir(bomb.centerX, bomb.centerY, bomb.rotateAngle, bomb.speed)
        spawn_trail(bomb.centerX, bomb.centerY, bomb.fill)
        if bomb.centerY >= bomb.detHeight:
            if(bomb.score == 0):
                spawn_small_bombs((int)(bomb.centerX), (int)(bomb.centerY), bomb.bombs, False)
            else:
                spawn_small_bombs((int)(bomb.centerX), (int)(bomb.centerY), bomb.bombs, True)
            multiBombs.remove(bomb)
        
def spawn_shots(x, y, angle, canScore):
    '''
    Takes 3 args, x and y for horizontal and vertical positioning, and angle for direction
    Returns no values but does add shapes to appropriate shape groups
    '''
    new = Oval(x,y,2,20, fill='white', rotateAngle = angle)
    new.next = getPointInDir(x,y,angle,app.ufoProjectileSpeed)
    new2 = Oval(x,y,2,20, fill='white', rotateAngle = angle+10)
    new2.next = getPointInDir(x,y,angle+10,app.ufoProjectileSpeed)
    new3 = Oval(x,y,2,20, fill='white', rotateAngle = angle-10)
    new3.next = getPointInDir(x,y,angle-10,app.ufoProjectileSpeed)
    if(canScore == True):
        new.score = 1000
        new2.score = 1000
        new3.score = 1000
    else:
        new.score = 0
        new2.score = 0
        new3.score = 0
    if(app.muted == False):
        Sound("Audio/UFO_shots.mp3").play(restart = True)
    new.flakHP = 1 ### Only relevant for city flak hits 
    new2.flakHP = 1 ### Only relevant for city flak hits 
    new3.flakHP = 1 ### Only relevant for city flak hits 
    new.hitIDs = []
    new2.hitIDs = []
    new3.hitIDs = []
    ufoShots.add(new, new2, new3)        

def move_ufo():
    '''
    Takes no args and returns no values
    Moves the ufo enemy type
    Players should shoot it down before it reaches the middle of the screen
    A single ufo can destroy a ton of cities in one fell swoop in later levels
    '''
    for saucer in ufos:
        if(saucer.centerX>=app.width+200):
            ufos.remove(saucer)
        if(saucer.centerX<=-200):
            ufos.remove(saucer)
        saucer.centerX, saucer.centerY = saucer.next 
        saucer.next = getPointInDir(saucer.centerX, saucer.centerY, saucer.angle, app.saucerSpeed)
        if(saucer.centerX>= (15/32)*app.width and saucer.centerX <= (17/32)*app.width and saucer.firing>=1):
            angle = angleTo(saucer.centerX, saucer.centerY, randrange(((int)(app.width/10)), (int)((app.width*(9/10)))), app.height)
            if(saucer.score == 0):
                spawn_shots(saucer.centerX, saucer.centerY, angle, False)
            else:
                spawn_shots(saucer.centerX, saucer.centerY, angle, True)
            saucer.firing-=1

def spawn_fun_missile(canScore):
    '''
    Takes no args and returns no values
    Creates a shape with specific attributes and adds it to the appropriate shape group
    This enemy type is affected by horizontal motion and gravity
    '''
    new = Circle(randrange(app.width), -100, 6, fill='red')
    if(canScore == True):
        new.score = 1000
    else:
        new.score = 0
    new.num = app.munitionCounter
    new.speed = app.basicMissileSpeed - 1
    new.gravSpeed = app.gravity
    new.rotateAngle = angleTo(new.centerX, new.centerY, randrange(5*(app.width//40), 35*(app.width//40)), app.height)
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, new.speed)
    new.flakHP = 3 ### Only relevant for city flak hits 
    new.hitIDs = []
    nonbasicMissiles.add(new)
    
def move_smart_bombs():
    '''
    Takes no args and returns no values
    Controls the motion of the smart bombs enemy type. 
    Smart bombs will try to evade explosions
    Can only be destroyed via a direct hit or an explosion so close that it has no time to adjust
    '''
    for bomb in smartMissiles:
        bomb.how_far = []
        bomb.centerX, bomb.centerY = bomb.next 
        spawn_trail(bomb.centerX, bomb.centerY, bomb.fill)
        bomb.speed += app.gravity
        for shape in explosion:
            if(shape.centerY> bomb.centerY):
                bomb.how_far.append(((distance(bomb.centerX, bomb.centerX, shape.centerX, shape.centerY)), (angleTo(bomb.centerX, bomb.centerY, shape.centerX, shape.centerY)), shape))
        for shape in flak:
            if(shape.centerY>bomb.centerY):
                bomb.how_far.append(((distance(bomb.centerX, bomb.centerX, shape.centerX, shape.centerY)), (angleTo(bomb.centerX, bomb.centerY, shape.centerX, shape.centerY)), shape))
        if(len(bomb.how_far)>0):
            lowestDistaceExplosionInfo = min(bomb.how_far, key=lambda t: t[0])
            scaryAngle = lowestDistaceExplosionInfo[1]
            if(bomb.rotateAngle <= scaryAngle and bomb.rotateAngle>130):
                bomb.rotateAngle -= 5
                bomb.speed -= (app.gravity/2)
            elif(bomb.rotateAngle> scaryAngle and bomb.rotateAngle<230):
                bomb.rotateAngle +=5
                bomb.speed -= (app.gravity/2)
        bomb.next = getPointInDir(bomb.centerX, bomb.centerY, bomb.rotateAngle, bomb.speed)           

def spawn_smart_bomb(canScore):
    '''
    Takes no args and returns no values
    Creates a shape with specific attributes and adds to appropriate shape group
    '''
    new = Circle(randrange(app.width), -100, 6, fill='white')
    new.speed = 3
    new.howFar = []
    if(canScore == True):
        new.score = 1225
    else:
        new.score = 0
    new.rotateAngle = angleTo(new.centerX, new.centerY, randrange((int)((1/5)*app.width), (int)((4/5)*app.width)), app.height)
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, new.speed)
    new.flakHP = 2 ### Only relevant for city flak hits and low health because in the lore, it is a delicate complicated device such that damage messes it up quickly
    new.hitIDs = []
    smartMissiles.add(new)
                
def spawn_ufo(canScore):
    '''
    Takes no args and returns no values
    Creates shape and decides location for spawning, adding to appropriate shape group
    '''
    location = randrange(2)
    saucer = create_saucer(0, (app.height//10), location)
    if(canScore == True):
        saucer.score = 1450
    else:
        saucer.score = 0   
    saucer.firing = app.level//10 + 1
    ufos.add(saucer)              
                
def spawn_handling():
    '''
    Takes no args and returns no values
    Handles spawning enemies, based on current game level
    '''
    if(app.bat.top<=app.height):
        canScore = True
    else:
        canScore = False
    if(app.level == 1): ## Just straight missiles
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer <= 0):
                spawn_basic_missile(randrange(0,app.width), -10, canScore)
                app.spawnTimer = app.stepsPerSecond * 4
                if(app.bat.top<=app.height):
                    app.enemiesLeftToSpawn -=1
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    elif(app.level <= 3): ## missiles and bomber planes
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer <= 0):
                if(app.enemiesLeftToSpawn %8 ==0):
                    if(app.muted == False):
                        app.planeSound.play(restart = True)
                    spawn_plane(randrange(app.height//4, app.height//2), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                else:
                    spawn_basic_missile(randrange(0,app.width), -10, canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                app.spawnTimer = app.stepsPerSecond * 4
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    elif(app.level <= 6): ## missiles, bomber planes higher up, non straight missiles
            if(app.enemiesLeftToSpawn >=1):
                if(app.spawnTimer <= 0):
                    if(app.enemiesLeftToSpawn%8 == 0):
                        if(app.muted == False):
                            app.planeSound.play(restart = True)
                        spawn_plane(randrange(20, app.height//4), canScore)
                        if(app.bat.top<=app.height):
                            app.enemiesLeftToSpawn -=1
                    elif(app.enemiesLeftToSpawn%7 == 0):
                        spawn_fun_missile(canScore)
                        if(app.bat.top<=app.height):
                            app.enemiesLeftToSpawn -=1
                    else:
                        spawn_basic_missile(randrange(0,app.width), -10, canScore)
                        if(app.bat.top<=app.height):
                            app.enemiesLeftToSpawn -=1
                    app.spawnTimer = app.stepsPerSecond * 4
                    newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    elif(app.level <= 9): ## missiles, bomber planes higher up, non straight missiles, multi bombs
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer <= 0):
                if(app.enemiesLeftToSpawn% 9 == 0):
                    spawn_multi_bomb(randrange(app.width), randrange(6*app.height//8, 7*app.height//8), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                elif(app.enemiesLeftToSpawn%8 == 0):
                    if(app.muted == False):
                        app.planeSound.play(restart = True)
                    spawn_plane(randrange(20, 3*app.height//4), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                elif(app.enemiesLeftToSpawn%7 == 0):
                    spawn_fun_missile(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                else:
                    spawn_basic_missile(randrange(0,app.width), -10, canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                app.spawnTimer = app.stepsPerSecond * 4
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    elif(app.level <=12 ): ## all of the above, plus smart bombs
            if(app.enemiesLeftToSpawn >=1):
                if(app.spawnTimer <= 0):
                    if(app.enemiesLeftToSpawn%11 == 0):
                        spawn_smart_bomb(canScore)
                        if(app.bat.top<=app.height):
                            app.enemiesLeftToSpawn -=1
                    elif(app.enemiesLeftToSpawn% 9 == 0):
                        spawn_multi_bomb(randrange(app.width), randrange(6*app.height//8, 7*app.height//8), canScore)
                        if(app.bat.top<=app.height):
                            app.enemiesLeftToSpawn -=1
                    elif(app.enemiesLeftToSpawn%8 == 0):
                        if(app.muted == False):
                            app.planeSound.play(restart = True)
                        spawn_plane(randrange(20, app.height//4), canScore)
                        if(app.bat.top<=app.height):
                            app.enemiesLeftToSpawn -=1
                    elif(app.enemiesLeftToSpawn%7 == 0):
                        spawn_fun_missile(canScore)
                        if(app.bat.top<=app.height):
                            app.enemiesLeftToSpawn -=1
                    else:
                        spawn_basic_missile(randrange(0,app.width), -10, canScore)
                        if(app.bat.top<=app.height):
                            app.enemiesLeftToSpawn -=1
                    app.spawnTimer = app.stepsPerSecond * 4
                    newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    elif(app.level<=16):
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer <= 0):
                if(app.enemiesLeftToSpawn%23 == 0): ##Rare event, on purpose
                    spawn_ufo(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                elif(app.enemiesLeftToSpawn%11 == 0):
                    spawn_smart_bomb(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                elif(app.enemiesLeftToSpawn% 9 == 0):
                    spawn_multi_bomb(randrange(app.width), randrange(6*app.height//8, 7*app.height//8), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                elif(app.enemiesLeftToSpawn%8 == 0):
                    if(app.muted == False):
                        app.planeSound.play(restart = True)
                    spawn_plane(randrange(20, app.height//4), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                elif(app.enemiesLeftToSpawn%7 == 0):
                    spawn_fun_missile(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                else:
                    spawn_basic_missile(randrange(0,app.width), -10, canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                app.spawnTimer = app.stepsPerSecond * 4
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    elif(app.level<=24): ## All of the above, but now multiple enemies at the same time. (certain pairings can spawn at the same time, not all)
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer <= 0):
                if(app.enemiesLeftToSpawn%23 == 0): ##Rare event, on purpose
                    spawn_ufo(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                elif(app.enemiesLeftToSpawn%11 == 0):
                    spawn_smart_bomb(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn% 9 == 0):
                    spawn_multi_bomb(randrange(app.width), randrange(6*app.height//8, 7*app.height//8), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                elif(app.enemiesLeftToSpawn%8 == 0):
                    if(app.muted == False):
                        app.planeSound.play(restart = True)
                    spawn_plane(randrange(20, app.height//4), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn%7 == 0):
                    spawn_fun_missile(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                else:
                    spawn_basic_missile(randrange(0,app.width), -10, canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                app.spawnTimer = app.stepsPerSecond * 4
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    else: ## All of the above, but now multiple enemies at the same time (no limit on which can spawn at the same time.).
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer == 0):
                if(app.enemiesLeftToSpawn%23 == 0): ##Rare event, on purpose
                    spawn_ufo(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn% 9 == 0):
                    spawn_multi_bomb(randrange(app.width), randrange(6*app.height//8, 7*app.height//8), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn%8 == 0):
                    if(app.muted == False):
                        app.planeSound.play(restart = True)
                    spawn_plane(randrange(20, app.height//4), canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn%7 == 0):
                    spawn_fun_missile(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn%11 == 0):
                    spawn_smart_bomb(canScore)
                    if(app.bat.top<=app.height):
                        app.enemiesLeftToSpawn -=1
                spawn_basic_missile(randrange(0,app.width), -10, canScore)
                if(app.bat.top<=app.height):
                    app.enemiesLeftToSpawn -=1
                app.spawnTimer = app.stepsPerSecond * 4
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn

def find_closest_of_group(x,y,range, group, importance):
    '''
    Takes 5 args
    x, y are positional args representing the first set of coordinates of a distance pair calculated in this function
    range is the max distance to check for
    group is the shape group to search through for finding closest shape of that group
    importance is an int which will later act as a multiplier for how valuable a target is
    Returns a tuple containing the coordinates of the shape closest to given x, y, the distance from x,y to the shape, and a calculation representing how valuable the target is, and the importance value itself
    '''
    info = []
    for shape in group:
        dist = distance(x,y, shape.centerX, shape.centerY)
        if(dist<range):
            info.append((shape.centerX, shape.centerY, dist, ((1000/dist))*importance, importance))
    if(len(info)>0):
        return min(info, key= lambda t: t[2])
    else:
        return None


def find_valuable_enemy(x,y, range):
    '''
    Takes 2 positional args, x and y and returns the location of the shape closest to that point considered an enemy
    Takes 1 distance argument, range, representing the limit of the search area
    Returns None if no such shape exists. 
    Intended to be used in conjunction with fire_flak() to aim the flak being fired
    '''
    options = []
    basic = find_closest_of_group(x,y,range, basicMissiles, 0.75)
    bomb = find_closest_of_group(x,y,range, bombs, 0.6)
    multiBomb = find_closest_of_group(x,y,range, multiBombs, 1)
    smart = find_closest_of_group(x,y,range, smartMissiles, 0.3)
    fun = find_closest_of_group(x,y,range, nonbasicMissiles, 0.85)
    plane = find_closest_of_group(x,y,range, planes, 0.2)
    tiny = find_closest_of_group(x,y,range, multiBombPostSplit, 0.6)
    ufoBullets = find_closest_of_group(x,y,range, ufoShots, 0.6)
    options+=[basic, bomb, multiBomb, smart, fun, plane, tiny, ufoBullets]
    for item in options[:]:
        if(item == None or item[1]>y):
            options.remove(item)
    if(len(options)>0):    
        bestTarget = max(options, key = lambda t: t[3])
        return bestTarget
    else:
        return None    

def fire_flak():
    '''
    Takes no args and returns no values
    For every building on the screen, creates a tiny explosion acting like cities firing flak at incoming enemies
    The range is limited and some enemies take more hits to destroy and there is a short delay between shots
    flak will sometimes manage to save a city or a building but it is not powerful enough to rely heavily on
    Cities are no longer defenseless
    '''
    for city in cities:
        for building in city:
            if(building.flakTimer>0):
                building.flakTimer -=1
            if(building.flakTimer == 0):
                target = find_valuable_enemy(building.centerX, building.top, ((width/4)**2 + (height/4)**2)**0.5)
                if(target!=None):
                    accuracyX = app.width/90
                    accuracyY = target[1]/12 
                    offsetX = randrange((int)(-(1/accuracyX)*app.width)-1, (int)((1/accuracyX)*app.width)+1, 1)
                    offsetY = randrange((int)((4/accuracyY)*app.height)+1)
                    while(target[1] + offsetY>= city.top -5):
                        offsetY -= 10
                    create_flak_target(target[0] + offsetX, target[1] + offsetY, app.flakNum)
                    new = Circle(building.centerX, building.top, 2, fill = 'white')
                    new.target = (target[0] + offsetX, target[1] + offsetY)
                    new.id = app.flakNum
                    new.rotateAngle = angleTo(new.centerX, new.centerY, new.target[0], new.target[1])
                    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, app.flakSpeed)
                    flakShots.add(new)
                    building.flakTimer = app.stepsPerSecond//target[4]
                    app.flakNum+=1

def move_flak_shots():
    '''
    Takes no args and returns no values
    Moves the player fired munitions towards their intended location. 
    Crucial function. Game will not work without this function.
    Forces an explosion if the target is hit ot bypassed
    '''
    for shot in flakShots:
        shot.centerX, shot.centerY = shot.next
        shot.next = getPointInDir(shot.centerX, shot.centerY, shot.rotateAngle, app.flakSpeed)
        if shot.centerY <= shot.target[1]:
            for target in flakTargets:
                if shot.id == target.id:
                    new = Circle(target.centerX, target.centerY, 3, fill='grey', border = 'yellow', borderWidth = 0.5)
                    new.time = app.stepsPerSecond
                    new.id = shot.id
                    flak.add(new)
                    flakTargets.remove(target)
            flakShots.remove(shot)
        

def create_flak_target(x,y, id):
    new = Circle(x,y,3,fill = 'black')
    new.id = id
    flakTargets.add(new)

def onStep():
    '''
    CMU built in function
    All code in this body is executed app.stepsPerSecond many times every second
    Used to show motion in this project
    '''
    if(app.autofs<=5):
        app.autofs += 1
    if(app.autofs == 4):
        pyautogui.keyDown("command")
        pyautogui.keyDown('ctrl')
        pyautogui.press('f')
        pyautogui.keyUp("command")
        pyautogui.keyUp("ctrl")
    if(app.play == True):
        if(app.pause == False):
            if(app.warningTimer>=0):
                hide_mac_window_warning()
            if(app.plane == True and len(planes) == 0):
                app.plane = False
                app.planeSound.play(restart = True) ## To avoid a crash
                app.planeSound.pause()                
            app.infoTimer-=1
            app.spawnTimer -= 1
            update_score()
            reload_all()
            move_shots()
            move_smart_bombs()
            move_ufo()
            move_ufo_shots()
            kaboom_all()
            move_basic_missiles()
            hit_detection()
            move_trail()
            remove_scores()
            move_bombs(bombs)
            move_bombs(multiBombPostSplit)
            check_loss()
            check_win()
            spawn_handling()
            move_planes()
            bombing_logic()
            move_multi_bomb()
            move_fun_missiles()
            fire_flak()
            move_flak_shots()
            if(app.infoTimer ==0):
                info.clear()
            update_stats()

def onMousePress(x,y):
    '''
    CMU built in function
    Takes mouse press locations as arguments
    In this project, used to aim munitions
    '''
    if(app.pause == False):
        realX, realY = x,y ## This fixed an error where the player should shoot when entering fullscreen on macOs devices
        app.munitionCounter+=1
        if(app.bat.broken == False):
            if(app.bat.reloadTimer == 0 and app.bat.ammoCount>=1):
                if(app.bat.top<= app.height):
                    if(realY<=app.bat.top):
                        app.bat.ammoCount -= 1
                        app.bat.reloadTimer = app.generalReload
                        fullInfoList[2]+=1
                        make_target(realX,realY)
                        defender = Circle(app.bat.centerX, app.bat.top+5, 3, fill='white')
                        defender.rotateAngle = angleTo(defender.centerX, defender.centerY, x, y)
                        defender.target = (x,y)
                        defender.num = app.munitionCounter
                        if(app.bat == batteries[1]):
                            defender.next = getPointInDir(defender.centerX, defender.centerY, defender.rotateAngle, app.shotSpeedMid)
                            defender.loc = "mid"
                        else:
                            defender.next = getPointInDir(defender.centerX, defender.centerY, defender.rotateAngle, app.shotSpeedLR)
                            defender.loc = "edge"
                        defense.add(defender)
                        app.bat = select_next_bat(app.bat)
                        bat_color_update()
                else:
                    display_mac_window_warning()
    if(pauseScreen.visible == True):
        if(closeGameButton.contains(x,y)):
            update_stats()
            sys.exit(0)
        if(backToLauncher.contains(x,y)):
            update_stats()
            subprocess.Popen([sys.executable, backToLauncher.game])
            sys.exit(0)
            
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
            
def toggle_pause():
    '''
    Takes no args and returns no values
    If game is paused, this will unpause it, 
    If game is unpaused, this will pause it
    Entails changing opacity of pause screen features and changing app setting
    '''
    if(app.play == True):
        if app.pause == True:
            app.pause = False
            pauseScreen.visible = False
            if(app.plane == True):
                if(app.muted == False):
                    app.planeSound.play()
        else:
            app.pause = True
            pauseScreen.visible = True
            if(app.plane == True):
                app.planeSound.play()
                app.planeSound.pause()
                
starting_bat()
app.bat = batteries[0]
app.bat.border = 'white'
make_all_cities_new_level()
fullInfoList[1]+=1
fullInfoList[6]+=1
pauseScreen.toFront()
flakTargets.toBack()
flak.toFront()
update_stats()

app.run()