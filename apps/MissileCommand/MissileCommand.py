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

app.setMaxShapeCount(100000000)
app.autofs = 0

default = [0,0,0,0,0,0,0,0]
keys = ["HighScore", "GamesPlayed", "Shots", "Hits", "EnemiesDestroyed", "CitiesLost", "TimesLaunched", "HighestLevel"] 
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


gameInfo = open("Files/MissileCommandStats.txt", "r+")
app.hiscore = fullInfoList[0]
allEnemies = Group()
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
app.multiBombSpeed = ((width*height)**0.5)/261 ### Roughly around 6 on standard macbook screen, but it is now relative to screen size
app.planeSpeed = (1/280) * width ### Only horizontal so more simple calculation
app.spawnTimer = app.stepsPerSecond * 4
app.enemiesLeftToSpawn = (app.level*7) + 5
app.bombSpeed = (1/210) * height ### Mostly vertical (some horizontal but not alot) so simpler calculation
app.flakSpeed = ((width*height)**0.5)/25 ## Roughly around 63 on a standard macbook, but is now relative to screen size
app.gravity = 0.05
app.saucerSpeed = (1/560) * width ### Only horizontal so more simple calculation
app.ufoProjectileSpeed = ((width*height)**0.5)/142 ### Roughly round 11 on standard macbook screen, but now relative to screen size
app.infoTimer = app.stepsPerSecond*5
app.infoShowing = False
app.pause = False
app.muted = False
app.planeSound = Sound("../../libraries/Audio/planeflying.mp3")
app.plane = 0
app.flakNum = 0
app.maxSize = (1/125)*app.width
app.sizeToShortenTime = (1/200)*app.width
app.xRange = 68 # Maximum horizontal dispersion for flak shots
app.yRange = 50 #Maximum vertical dispersion for flak shots

outerPause = Rect(app.width/2, app.height/2, app.width/5, app.width/10, fill=None, border = 'yellow', borderWidth = 2, align = 'center')
pauseLabel = Label("Game Paused", app.width/2, app.height/2 -15, size = 30, fill= 'white')
closeGameButton = Rect(outerPause.left, outerPause.centerY, outerPause.width//2, outerPause.height//2, fill=None, border = 'red')
closeGameButton.words = Label("Close Game", closeGameButton.centerX, closeGameButton.centerY, size = 15, fill = 'white')
backToLauncher = Rect(closeGameButton.right+1, closeGameButton.top, outerPause.width//2, outerPause.height//2, fill=None, border = 'gray')
backToLauncher.game = "PretendLauncher/PretendLauncher.py"
backToLauncher.words = Label("Return to Launcher", backToLauncher.centerX, backToLauncher.centerY, size = 15, fill='white')
pauseScreen = Group(outerPause, pauseLabel, closeGameButton, backToLauncher, backToLauncher.words, closeGameButton.words)
pauseScreen.visible = False

leftBattery = Rect((1/40)*app.width, (19/20)*app.height, (1/12) * app.width, (1/20)*app.height)
midBattery = Rect(app.width/2, (19/20)*app.height, (1/12) * app.width, (1/20)*app.height, align = 'top')
rightBattery = Rect((39/40)*app.width, (19/20)*app.height, (1/12) * app.width, (1/20)*app.height, align = 'top-right')
batteries = [leftBattery, midBattery, rightBattery]
targets = Group()
defense = Group()
explosion = Group()
cities = Group()
bubbles = Group()
gameOver = Group()
fakes = Group()
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
    label2 = Label("You have unlocked a bonus city", 5, box.top, fill='white', align = 'top-left', size = 15)
    label3 = Label("Survive this wave to spawn your bonus city", 5, label2.bottom+2, fill='white', align = 'top-left', size = 15)
    info.add(box, label2, label3)
    app.infoTimer = app.stepsPerSecond*4

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
    for i in range(14):
        tall = randrange(5,80)
        wide = randrange(4,15)
        lastWidth = wide
        building = Rect(x+lastWidth+ i*(app.width/200), app.height-tall, wide, tall, border = 'white')
        building.note = Sound("../../libraries/Audio/explosion.mp3")
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
    app.spawnTimer = app.stepsPerSecond * 4
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
            Sound("../../libraries/Audio/eerie.mp3").play(restart = True)
    if(app.score> app.hiscore):
        app.hiscore = app.score
    score.value = "Score: %05d" %app.score
    hiscore.value = "High Score: %05d" %app.hiscore
    fullInfoList[0] = app.hiscore
    update_stats()

    
def update_stats():
    '''
    Takes no args and returns no values
    Updates game stats stored in an external txt file
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")

def move_enemies():
    '''
    Takes no args and returns no values
    Handles all movement for all enemies
    '''
    for enemy in allEnemies:
        if(enemy.type!="ufo"):
            spawn_trail(enemy.centerX, enemy.centerY, enemy.fill)
        enemy.centerX, enemy.centerY = enemy.next
        if(enemy.type == 'plane'):
            if(enemy.bombs>0 and enemy.centerX>= enemy.dropZones[0]):
                enemy.dropZones.pop(0)
                spawn_bombs(enemy.centerX, enemy.centerY)
                enemy.bombs-=1
            elif(enemy.left > app.width):
                allEnemies.remove(enemy)
                app.plane -=1
                if(app.plane<1):
                    app.planeSound.play(restart=True)
                    app.planeSound.pause()
        if(enemy.type == 'fun'):
            enemy.gravity+=app.gravity/2
            enemy.centerY+=enemy.gravity
        if(enemy.type == 'multi'):
            if(enemy.centerY>enemy.detHeight):
                spawn_small_bombs((int)(enemy.centerX), (int)(enemy.centerY), enemy.bombs)
                allEnemies.remove(enemy)
        if(enemy.type == 'smart'):
            enemy.gravity+=app.gravity/5
            enemy.centerY+=enemy.gravity
            enemy.how_far = []
            for shape in explosion:
                dist = distance(enemy.centerX, enemy.centerX, shape.centerX, shape.centerY)
                if(shape.bottom> enemy.centerY and dist<250):
                    enemy.how_far.append((dist, (angleTo(enemy.centerX, enemy.centerY, shape.centerX, shape.centerY)), shape))
            for shape in flak:
                dist = distance(enemy.centerX, enemy.centerX, shape.centerX, shape.centerY)
                if(shape.bottom> enemy.centerY and dist<250):
                    enemy.how_far.append((dist, (angleTo(enemy.centerX, enemy.centerY, shape.centerX, shape.centerY)), shape))
            if(len(enemy.how_far)>0):
                lowestDistaceExplosionInfo = min(enemy.how_far, key=lambda t: t[0])
                scaryAngle = lowestDistaceExplosionInfo[1]
                if(enemy.angle <= scaryAngle and enemy.angle>130):
                    enemy.angle -= 5
                    enemy.speed -= (app.gravity/2)
                elif(enemy.angle> scaryAngle and enemy.angle<230):
                    enemy.angle +=5
                    enemy.speed -= (app.gravity/2)
        if(enemy.type=='ufo'):
            if(enemy.centerX>=app.width+200):
                allEnemies.remove(enemy)
            if(enemy.centerX<=-200):
                allEnemies.remove(enemy)
            if(enemy.centerX>= (15/32)*app.width and enemy.centerX <= (17/32)*app.width and enemy.firing>=1):
                angle = angleTo(enemy.centerX, enemy.bottom, randrange(((int)(app.width/10)), (int)((app.width*(9/10)))), app.height)
                spawn_shots(enemy.centerX, enemy.bottom, angle)
                enemy.firing-=1
        enemy.next = getPointInDir(enemy.centerX, enemy.centerY, enemy.angle, enemy.speed)
                

def spawn_plane(y):
    '''
    Takes one positional arg and returns no values
    y represents the height on the screen that the shape will be spawned
    Creates a shape with certain attributes
    Then adds that shape to an appropriate group
    '''
    hitbox = Oval(-20, y, 40, 10, border = 'white', fill='gray')
    hitbox.bombs = app.level//2+1 if app.level <= 48 else 25
    hitbox.dropZones = []
    hitbox.flakHP = hitbox.bombs//2 + 10 ### Only relevant for city flak hits 
    hitbox.type = 'plane'
    hitbox.speed = app.planeSpeed
    hitbox.importance = 0.55 + app.level/100 if app.level<50 else 1.05
    hitbox.gravity=0
    hitbox.score = 625
    spacing = app.width// hitbox.bombs
    for i in range(hitbox.bombs):
        hitbox.dropZones.append(spacing * (i) + randrange(-50, 51, 1))
    app.plane += 1
    hitbox.hitIDs = []
    if(app.muted == False):
        app.planeSound.play(restart = True)
    hitbox.angle = angleTo(hitbox.centerX, y, app.width, y)
    hitbox.next = getPointInDir(hitbox.centerX, hitbox.centerY, hitbox.angle, hitbox.speed)
    allEnemies.add(hitbox)

def get_next_index(list, current):
    '''
    Takes 2 args, a list and an index in that list, returns an index in the given list
    This function specifially provides the index directly after the given index
    Will return 0 in the case that the next index would be out of bounds
    '''
    return 0 if current == len(list)-1 else current + 1

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
    return len(list) -1 if current == 0 else current - 1

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

def spawn_bombs(x,y):
    '''
    Takes 2 positional arguments, x and y for horizontal and vertical spawning respectively
    Creates a shape with specific attributes anf adds it to a shape group, returns no values
    Typicallt used to drop bombs from bomber planes
    '''
    bomb = Oval(x,y,2,8, fill = 'white')
    bomb.speed = app.bombSpeed
    bomb.targetX = bomb.centerX + randrange(30, 80)        
    bomb.rotateAngle = angleTo(bomb.centerX, bomb.centerY, bomb.targetX, app.height)
    bomb.angle = bomb.rotateAngle
    bomb.importance = 0.5 + app.level/100 if app.level<50 else 1
    bomb.next = getPointInDir(bomb.centerX, bomb.centerY, bomb.rotateAngle, bomb.speed)
    bomb.flakHP = 1 ### Only relevant for city flak hits 
    bomb.score = app.level * 50
    bomb.hitIDs = []
    bomb.gravity = 0
    bomb.type = 'bomb'
    bomb.willHit = False
    possible_loc = (x,y)
    fakeShape = Oval(x,y,2,8, fill='orange', rotateAngle = bomb.rotateAngle)
    fakes.add(fakeShape)
    while(bomb.willHit == False and fakeShape.top<app.height):
        fakeShape.centerX, fakeShape.centerY = possible_loc
        if(fakeShape.bottom>=cities.top):
            for bat in batteries:
                if bat.hitsShape(fakeShape):
                    bomb.willHit = True
            if(cities.hitsShape(fakeShape)):
                bomb.willHit = True
        possible_loc = getPointInDir(fakeShape.centerX, fakeShape.centerY, bomb.angle, bomb.speed*3)
    fakes.remove(fakeShape)
    allEnemies.add(bomb)

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
    app.level+=1
    if(app.muted == False):
        Sound("../../libraries/Audio/levelup.mp3").play(restart = True)
    stage.value = "Level: %1d" %app.level
    app.mult = app.level   
    app.enemiesLeftToSpawn = (app.level*7) + 5
    newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    app.xRange = 68 - app.level*2 if app.level<12 else 44
    app.yRange = 50 - app.level if app.level<8 else 42
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
        object.opacity-=1
        if(object.radius<=app.maxSize): 
            object.radius+=1
        if object.opacity == 0:
            explosion.remove(object)
    for flakShot in flak:
        if(flakShot.time <= 0):
            flakShot.opacity-=20
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
    new = Circle(shape.centerX, shape.centerY, 6, fill='yellow', border = 'orange')
    new.willScore = causedByPlayer
    explosion.add(new)

def move_player_shots():
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

def spawn_basic_missile(x,y):
    '''
    Takes 2 args and returns no values
    Adds new shape with special attributes to shape group
    This function creates the most basic enemy in the game, a basic missile, no horizontal motion, not affected by gravity
    '''
    new = Circle(x,y, 6, fill = 'limeGreen')
    new.type = "basic"
    new.gravity = 0
    new.importance = 0.7 + app.level/100 if app.level<50 else 1.2
    new.score = 100
    new.flakHP = 14 ### Only relevant for city flak hits 
    new.hitIDs = []
    new.speed = app.basicMissileSpeed
    new.angle = angleTo(x,y,x,app.height)
    new.next = getPointInDir(x,y,new.angle, new.speed)
    allEnemies.add(new)

def spawn_trail(x, y, color):
    '''
    Takes 3 args and returns no values
    Creates a shape and adds it to the appropriate shape group
    The trails in this program will represent missile streaks and rocket burns
    '''
    bubbles.add(Circle(x, y, 2, fill =  color))
                
def explosion_vs_enemies():
    '''
    Takes no args and returns no values
    checks if objects in the allEnemies shape group hit objects in the explosion shape group
    Crucial function, withouth this function, explosions will not affect enemies
    '''
    for shape in explosion:
        for bomb in allEnemies:
            if(shape.hitsShape(bomb)):
                if(app.muted == False): 
                    Sound("../../libraries/Audio/medium.mp3").play(restart = True)
                if(shape.willScore == True):
                    points = bomb.score * app.mult
                    app.score+= points
                    create_scores(bomb.centerX, bomb.centerY, points)
                    fullInfoList[3]+=1
                explode_object(bomb, shape.willScore)
                allEnemies.remove(bomb)
                fullInfoList[4]+=1
                if(bomb.type == 'plane'):
                    app.plane-=1
                    if(app.plane<1):
                        app.planeSound.play(restart = True)
                        app.planeSound.pause()
                update_score()               
                
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
    new.speed = app.saucerSpeed
    return new                 
                
def enemies_vs_bat():
    '''
    Takes no args and returns no values
    checks for contact between missile batteries and all enemy types
    Crucial function, withouth this function, enemies will not affect player missile batteries
    '''
    for bat in batteries:
        for enemy in allEnemies:
            if(enemy.hitsShape(bat) or bat.containsShape(enemy)):
                explode_object(enemy, False)
                allEnemies.remove(enemy)
                bat.broken = True
                if(enemy.type=='bomb'):
                    bat.repairTimer += 10*app.stepsPerSecond
                else:
                    bat.repairTimer += 25*app.stepsPerSecond
                if(app.muted == False):
                    Sound("../../libraries/Audio/explosion.mp3").play(restart = True)
                if bat == app.bat: app.bat = select_next_bat(app.bat)
                bat_color_update()
                update_score()


def missiles_vs_ground():
    '''
    Takes no args and returns no values
    Checks if enemies impacted the ground
    Important for realism and also preventing lag since it forces deletion of shapes that would be below the screen
    '''
    for enemy in allEnemies:
        if enemy.bottom>= height: ## using height here, not app.height because height is the actual size, and app.height is the window size
            explode_object(enemy, False)
            if(app.muted == False):
                Sound("../../libraries/Audio/medium.mp3").play(restart = True)
            allEnemies.remove(enemy)

def enemies_vs_cities():
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against hitting the cities
    Crucial function, withouth this function, enemies will not affect cities and the game could never end
    '''
    for city in cities:
        for enemy in allEnemies:
            if(enemy.hitsShape(city)):
                if(enemy.type!='bomb' or city.health<=1):
                    try: ## Fixing a near impossible crash which can only occur during testing when 2 enemies hit the same city on the same frame (only happens in testing when 50+ enemies are launched from the same place at the same time)
                        cityids.remove(city.id)
                    except:
                        pass
                    for building in city.children:
                        if(app.muted == False):
                            building.note.play(restart = True)
                        explode_object(building, False)
                    explode_object(enemy, False)
                    allEnemies.remove(enemy)
                    cities.remove(city)
                    app.cities-=1
                    fullInfoList[5]+=1
                    update_score()
                else:
                    for building in city:
                        if(enemy.hitsShape(building)):
                            if(app.muted == False):
                                building.note.play(restart = True)
                            explode_object(building, False)
                            allEnemies.remove(enemy)
                            city.remove(building)
                            city.health-=1

def missiles_vs_anti_missiles():
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against being hit directly by player munitions
    Crucial function, withouth this function, player munitions would phase through enemies and only explosions would affect enemies
    Also rewards players with a 5x bonus for direct impacts, to provide some risk-reward motivaiton
    '''
    for anti in defense:
        for enemy in allEnemies:    
            if(enemy.hitsShape(anti)):
                for target in targets:
                    if(target.num == anti.num):
                        targets.remove(target)
                explode_object(enemy, True)
                if(app.muted == False):
                    Sound("../../libraries/Audio/uwexplosion.mp3").play(restart = True)
                points = enemy.score*app.mult*5
                app.score+=points
                create_scores(enemy.centerX, enemy.centerY, points)
                allEnemies.remove(enemy)
                defense.remove(anti)
                fullInfoList[3]+=1
                fullInfoList[4]+=1
                update_score()
       
def decrease_health(item, x2):
    '''
    Takes 2 arguments:
    item, which is a shape
    x2 is a boolean such that True means the score should get a 2x multiplier
    Returns no values
    Decreases the hp of the item and destroys it if appropriate, removing it from the allEnemies group
    In destruction case, adds appropriate score to player score
    '''
    if(x2 == True):
        item.flakHP-=2
    else:
        item.flakHP-=1 
    if(item.flakHP<=0):
        points = item.score * app.mult
        if(x2 == True):
            points = points * 2
            if(app.muted == False):
                Sound("../../libraries/Audio/uwexplosion.mp3").play(restart = True)
        else:
            if(app.muted == False):
                Sound("../../libraries/Audio/medium.mp3").play(restart = True)
        if(item.type == "plane"):
            app.plane-=1
            if(app.plane<1):
                app.planeSound.play(restart = True)
                app.planeSound.pause()
        app.score+= points
        create_scores(item.centerX, item.centerY, points)
        explode_object(item, True)  
        allEnemies.remove(item) 
        update_score()   
       
def flak_vs_enemies():
    '''
    Takes no args and returns no values
    Checks if flak explosions hit any of the shapes in the allEnemies group
    '''
    for enemy in allEnemies:
        for exp in flak:
            if(exp.hitsShape(enemy)):
                if(not exp.id in enemy.hitIDs):
                    enemy.hitIDs.append(exp.id)
                    decrease_health(enemy, False)
        for thing in flakShots:
            if(thing.hitsShape(enemy)):
                if(not thing.id in enemy.hitIDs):
                    enemy.hitIDs.append(thing.id)
                    decrease_health(enemy, True) 
                for target in flakTargets:
                    if(thing.id == target.id):
                        new = Circle(target.centerX, target.centerY, 3, fill='grey', border = 'yellow', borderWidth = 0.5)
                        new.time = app.stepsPerSecond//2
                        new.id = target.id
                        flak.add(new)
                        flakTargets.remove(target)
                        flakShots.remove(thing)
                        
def hit_detection():
    '''
    Takes no args and returns no values
    Calls all functions related to impacts
    Possibly the most crucial function as scoring, destruction failing would be impossible without it
    '''
    missiles_vs_anti_missiles()
    enemies_vs_bat()
    explosion_vs_enemies()
    missiles_vs_ground()
    flak_vs_enemies()
    enemies_vs_cities()

def move_trail():
    '''
    Takes no args and returns no values
    Slowly dissipates missile trails until they are invisbile
    Subsequently removes the trail peices as they are fully invisible
    '''
    for bubble in bubbles:
        if(bubble.opacity>0):
            bubble.opacity -=4
        else:
            bubbles.remove(bubble)

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
        flak.clear()
        flakShots.clear()
        flakTargets.clear()
        explosion.clear()
        cities.clear()
        bubbles.clear()
        allEnemies.clear()
        targets.clear()
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
        
def spawn_small_bombs(x,y,num):
    '''
    Takes 3 args, x and y for position, num for counting how many to spawn
    Spawns num many small bombs at the specified location
    adds them all to the appropriate shape group
    '''
    for i in range(num):
        new = Circle(x,y,2, fill='cyan')
        new.targetX = randrange(x-(app.width//10), x+(app.width//10))
        new.angle = angleTo(x,y,new.targetX, app.height)
        new.next = getPointInDir(x,y,new.rotateAngle, app.bombSpeed)
        new.gravity = app.gravity
        new.type = 'bomb'
        new.score = 100
        new.speed = app.bombSpeed
        new.flakHP = 1
        new.hitIDs = []
        new.importance = 0.5 + app.level/100 if app.level<50 else 1
        new.willHit = False
        possible_loc = (x,y)
        fakeShape = Circle(x,y,2, fill='orange', rotateAngle = new.rotateAngle)
        fakes.add(fakeShape)
        while(new.willHit == False and fakeShape.top<app.height):
            fakeShape.centerX, fakeShape.centerY = possible_loc
            if(fakeShape.bottom>=cities.top):
                for bat in batteries:
                    if bat.hitsShape(fakeShape):
                        new.willHit = True
                if(cities.hitsShape(fakeShape)):
                    new.willHit=True
            possible_loc = getPointInDir(fakeShape.centerX, fakeShape.centerY, new.angle, new.speed*3)
        allEnemies.add(new)
        fakes.remove(fakeShape)
    if(app.muted == False):
        Sound("../../libraries/Audio/pop.mp3").play(restart = True)
    
def spawn_multi_bomb(x, detHeight):
    '''
    Takes 2 args, x for horizontal location and detHeight for when the bomb should explode
    Returns no values but adds a shaoe with special attributes to the appropriate shape group
    This is a special enemy type which will reach a designated height, and then spawn several smaller faster bombs which are nearly impossible to shoot down
    Players should shoot this enemy down quickly
    '''
    new = Circle(x,-10, 8, fill = 'cyan')
    new.detHeight = detHeight
    new.bombs = app.level//2 + 2 if app.level <= 18 else 20
    new.importance = 1.3 + app.level/100 if app.level < 50 else 1.8
    new.type = 'multi'
    new.score = 750 + (125 * new.bombs)
    new.speed = app.multiBombSpeed
    new.angle = angleTo(new.centerX,new.centerY,randrange(app.width//4, 3*(app.width//4)),detHeight)
    new.gravity = app.gravity
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, new.speed)
    new.flakHP = new.bombs+1 ### Only relevant for city flak hits 
    new.hitIDs = []
    allEnemies.add(new)
        
def spawn_shots(x, y, angle):
    '''
    Takes 3 args, x and y for horizontal and vertical positioning, and angle for direction
    Returns no values but does add shapes to appropriate shape groups
    '''
    new = Oval(x,y,2,20, fill='white', rotateAngle = angle)
    new.angle = angle
    new.importance = 0.7 + app.level/100 if app.level<50 else 1.2
    new.speed = app.ufoProjectileSpeed
    new.gravity = 0
    new.type = 'bomb'
    new.next = getPointInDir(x,y,angle,new.speed)
    new2 = Oval(x,y,2,20, fill='white', rotateAngle = angle+10)
    new2.angle = angle+10
    new2.importance = 0.7 + app.level/100 if app.level<50 else 1.2
    new2.speed = app.ufoProjectileSpeed
    new2.gravity = 0
    new2.type = 'bomb'
    new2.next = getPointInDir(x,y,angle+10,new.speed)
    new3 = Oval(x,y,2,20, fill='white', rotateAngle = angle-10)
    new3.angle = angle-10
    new3.importance = 0.7 + app.level/100 if app.level<50 else 1.2
    new3.speed = app.ufoProjectileSpeed
    new3.gravity = 0
    new3.type = 'bomb'
    new3.next = getPointInDir(x,y,angle-10,new.speed)
    new.score = 1000
    new2.score = 1000
    new3.score = 1000
    if(app.muted == False):
        Sound("../../libraries/Audio/UFO_shots.mp3").play(restart = True)
    new.flakHP = 2 ### Only relevant for city flak hits 
    new2.flakHP = 2 ### Only relevant for city flak hits 
    new3.flakHP = 2 ### Only relevant for city flak hits 
    new.hitIDs = []
    new2.hitIDs = []
    new3.hitIDs = []
    new.willHit = False
    new2.willHit = False
    new3.willHit = False
    possible_loc1 = (x,y)
    possible_loc2 = (x,y)
    possible_loc3 = (x,y)
    fakeShape1 = Oval(x,y,2,20, fill='orange', rotateAngle = new.rotateAngle)
    fakeShape2 = Oval(x,y,2,20, fill='orange', rotateAngle = new2.rotateAngle)
    fakeShape3 = Oval(x,y,2,20, fill='orange', rotateAngle = new3.rotateAngle)
    fakes.add(fakeShape1, fakeShape2, fakeShape3)
    while(new.willHit == False and fakeShape1.top<app.height):
        fakeShape1.centerX, fakeShape1.centerY = possible_loc1
        if(fakeShape1.bottom >= cities.top):
            for bat in batteries:
                if bat.hitsShape(fakeShape1):
                    new.willHit = True
            if(cities.hitsShape(fakeShape1)):
                new.willHit = True
        possible_loc1 = getPointInDir(fakeShape1.centerX, fakeShape1.centerY, new.angle, new.speed*3)
    while(new2.willHit == False and fakeShape2.top<app.height):
        fakeShape2.centerX, fakeShape2.centerY = possible_loc2
        if(fakeShape2.bottom>= cities.top):
            for bat in batteries:
                if bat.hitsShape(fakeShape2):
                    new2.willHit = True
            if(cities.hitsShape(fakeShape2)):
                new2.willHit = True
        possible_loc2 = getPointInDir(fakeShape2.centerX, fakeShape2.centerY, new2.angle, new2.speed*3)
    while(new3.willHit == False and fakeShape3.top<app.height):
        fakeShape3.centerX, fakeShape3.centerY = possible_loc3
        if(fakeShape3.bottom>= cities.top):
            for bat in batteries:
                if bat.hitsShape(fakeShape3):
                    new3.willHit = True
            if(cities.hitsShape(fakeShape3)):
                new3.willHit = True
        possible_loc3 = getPointInDir(fakeShape3.centerX, fakeShape3.centerY, new3.angle, new3.speed*3)
    fakes.remove(fakeShape1)
    fakes.remove(fakeShape2)
    fakes.remove(fakeShape3)
    allEnemies.add(new, new2, new3)        

def spawn_fun_missile():
    '''
    Takes no args and returns no values
    Creates a shape with specific attributes and adds it to the appropriate shape group
    This enemy type is affected by horizontal motion and gravity
    '''
    new = Circle(randrange((app.width//10), (9*app.width//10)), -100, 6, fill='red')
    new.score = 1000
    new.num = app.munitionCounter
    new.importance = 1 + app.level/100 if app.level<50 else 1.5
    new.speed = app.basicMissileSpeed
    new.gravity = app.gravity
    new.angle = angleTo(new.centerX, new.centerY, randrange(3*(app.width//40), 37*(app.width//40)), app.height)
    new.next = getPointInDir(new.centerX, new.centerY, new.angle, new.speed)
    new.flakHP = 6 ### Only relevant for city flak hits 
    new.type = 'fun'
    new.hitIDs = []
    possible_loc = (new.centerX, new.centerY)
    new.willHit = False
    i = 0
    fakeShape = Circle(new.centerX, new.centerY, 6, fill='orange')
    fakes.add(fakeShape)
    while(new.willHit == False and fakeShape.top<=app.height):
        fakeShape.centerX, fakeShape.centerY = possible_loc
        for bat in batteries:
            if bat.hitsShape(fakeShape):
                new.willHit = True
        if(cities.hitsShape(fakeShape)):
            new.willHit = True
        nextPoint = getPointInDir(possible_loc[0], possible_loc[1], new.angle, new.speed)
        possible_loc = (nextPoint[0], nextPoint[1]+ new.gravity + (app.gravity/2)*(i+1))
        i+=1
    fakes.remove(fakeShape)
    allEnemies.add(new)       

def spawn_smart_bomb():
    '''
    Takes no args and returns no values
    Creates a shape with specific attributes and adds to appropriate shape group
    '''
    new = Circle(randrange(app.width), -100, 6, fill='white')
    new.speed = 3
    new.type = 'smart'
    new.importance = 1 + app.level/100 if app.level<50 else 1.5
    new.gravity = 1
    new.howFar = []
    new.score = 1225
    new.angle = angleTo(new.centerX, new.centerY, randrange((int)((1/5)*app.width), (int)((4/5)*app.width)), app.height)
    new.next = getPointInDir(new.centerX, new.centerY, new.angle, new.speed)
    new.flakHP = 12
    new.hitIDs = []
    allEnemies.add(new)
                
def spawn_ufo():
    '''
    Takes no args and returns no values
    Creates shape and decides location for spawning, adding to appropriate shape group
    '''
    location = randrange(2)
    saucer = create_saucer(0, (app.height//10), location)
    saucer.score = 0   
    saucer.firing = app.level//10 + 1 if app.level <= 50 else 6
    saucer.score = 1450
    saucer.hitIDs =[]
    saucer.type = 'ufo'
    saucer.importance = 1 ## Avoids a crash relating to flak but ufos should never get shot by flak anyway
    saucer.gravity = 0
    allEnemies.add(saucer)              
                
def spawn_handling():
    '''
    Takes no args and returns no values
    Handles spawning enemies, based on current game level
    '''
    app.spawnTimer = app.stepsPerSecond * 4
    app.enemiesLeftToSpawn-=1
    if(app.level == 1): ## Just straight missiles
        spawn_basic_missile(randrange(0,app.width), -10)
    elif(app.level <= 3): ## missiles and bomber planes
        if(app.enemiesLeftToSpawn %8 ==0):
            spawn_plane(randrange(app.height//4, app.height//2))
        else:
            spawn_basic_missile(randrange(0,app.width), -10)
    elif(app.level <= 6): ## missiles, bomber planes higher up, non straight missiles
        if(app.enemiesLeftToSpawn%8 == 0):
            spawn_plane(randrange(20, app.height//4))
        elif(app.enemiesLeftToSpawn%7 == 0):
            spawn_fun_missile()
        else:
            spawn_basic_missile(randrange(0,app.width), -10)
    elif(app.level <= 9): ## missiles, bomber planes higher up, non straight missiles, multi bombs
        if(app.enemiesLeftToSpawn% 9 == 0):
            spawn_multi_bomb(randrange(app.width), randrange(5*app.height//8, 7*app.height//8))
        elif(app.enemiesLeftToSpawn%8 == 0):
            spawn_plane(randrange(20, 3*app.height//4))
        elif(app.enemiesLeftToSpawn%7 == 0):
            spawn_fun_missile()
        else:
            spawn_basic_missile(randrange(0,app.width), -10)
    elif(app.level <=12 ): ## all of the above, plus smart bombs
        if(app.enemiesLeftToSpawn%11 == 0):
            spawn_smart_bomb()
        elif(app.enemiesLeftToSpawn% 9 == 0):
            spawn_multi_bomb(randrange(app.width), randrange(5*app.height//8, 7*app.height//8))
        elif(app.enemiesLeftToSpawn%8 == 0):
            spawn_plane(randrange(20, app.height//4))
        elif(app.enemiesLeftToSpawn%7 == 0):
            spawn_fun_missile()
        else:
            spawn_basic_missile(randrange(0,app.width), -10)
    else:
        if(app.enemiesLeftToSpawn%23 == 0): ##Rare event, on purpose
            spawn_ufo()
        elif(app.enemiesLeftToSpawn%11 == 0):
            spawn_smart_bomb()
        elif(app.enemiesLeftToSpawn% 9 == 0):
            spawn_multi_bomb(randrange(app.width), randrange(5*app.height//8, 7*app.height//8))
        elif(app.enemiesLeftToSpawn%8 == 0):
            spawn_plane(randrange(20, app.height//4))
        elif(app.enemiesLeftToSpawn%7 == 0):
            spawn_fun_missile()
        else:
            spawn_basic_missile(randrange(0,app.width), -10)
    newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn

def find_valuable_enemy(x,y, range):
    '''
    Takes 2 positional args, x and y and returns the location of the shape closest to that point considered an enemy
    Takes 1 distance argument, range, representing the limit of the search area
    Returns None if no such shape exists. 
    Intended to be used in conjunction with fire_flak() to aim the flak being fired
    '''
    options = []
    willHit = []
    for enemy in allEnemies:
        dist = distance(x,y,enemy.centerX, enemy.centerY)
        if(dist<range):
            if(enemy.type == 'basic'):
                for city in cities:
                    willHit.append((city.left-7, city.right+7))
                for bat in batteries:
                    willHit.append((bat.left-7, bat.right+7))
            else:
                willHit.append((batteries[0].left-7, batteries[2].right+7))
            for tuple in willHit:
                if(enemy.type != 'bomb' and enemy.type!='fun'):
                    if(enemy.centerX>tuple[0] and enemy.centerX<tuple[1]):
                        options.append((enemy.centerX, enemy.centerY, dist, ((1000)/dist+1)*enemy.importance, enemy.importance, enemy.type))
                else:
                    if(enemy.willHit == True):
                        options.append((enemy.centerX, enemy.centerY, dist, ((1000)/dist+1)*enemy.importance, enemy.importance, enemy.type))
    if(len(options)==0):
        return None
    for item in options[:]:
        if(item[1]>y):
            options.remove(item)
    if(len(options)>0):    
        return max(options, key = lambda t: t[3])
    return None

def fire_flak(building, xRange, yRange):
    '''
    Takes no args and returns no values
    For every building on the screen, creates a tiny explosion acting like cities firing flak at incoming enemies
    The range is limited and some enemies take more hits to destroy and there is a short delay between shots
    flak will sometimes manage to save a city or a building but it is not powerful enough to rely heavily on
    Cities are no longer defenseless
    '''
    rangeBoost = app.level if app.level<75 else 75
    target = find_valuable_enemy(building.centerX, building.top, (((width/4)**2 + (height/4)**2)**0.5)+rangeBoost)
    if(target!=None):
        building.flakTimer = app.stepsPerSecond//target[4]
        if(target[5] == 'plane'):
            offsetX = randrange(xRange, 2*xRange)
        else:
            offsetX = randrange(-xRange, xRange, 1)
        offsetY = randrange(-yRange, yRange, 1)
        while target[1]+offsetY > building.top:
            offsetY-=10
        create_flak_target(target[0] + offsetX, target[1] + offsetY, app.flakNum)
        new = Circle(building.centerX, building.top, 2, fill = 'white')
        new.target = (target[0] + offsetX, target[1] + offsetY)
        new.id = app.flakNum
        new.rotateAngle = angleTo(new.centerX, new.centerY, new.target[0], new.target[1])
        new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, app.flakSpeed)
        flakShots.add(new)
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
                    new = Circle(target.centerX, target.centerY, 4, fill='grey', border = 'yellow', borderWidth = 0.5)
                    new.time = app.stepsPerSecond//2
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
    if(app.play == True and app.pause == False):
        app.spawnTimer-=1
        if(app.spawnTimer<=0):
            spawn_handling()
        for city in cities:
            for building in city:
                building.flakTimer-=1
                if(building.flakTimer<=0):
                    fire_flak(building, app.xRange, app.yRange)
        hit_detection()
        move_player_shots()
        reload_all()
        move_trail()
        move_flak_shots()
        check_loss()
        check_win()
        kaboom_all()
        remove_scores()
        move_enemies()
        if(app.infoTimer>0):               
            app.infoTimer-=1
        if(app.plane < 1):
            app.planeSound.play(restart = True)
            app.planeSound.pause()
        else:
            info.clear()

def onMousePress(x,y):
    '''
    CMU built in function
    Takes mouse press locations as arguments
    In this project, used to aim munitions
    '''
    if(app.pause == False):
        app.munitionCounter+=1
        if(app.bat.broken == False and app.bat.reloadTimer == 0 and app.bat.ammoCount>=1 and y<=app.bat.top):
            app.bat.ammoCount -= 1
            app.bat.reloadTimer = app.generalReload
            fullInfoList[2]+=1
            make_target(x,y)
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
            update_score()
            app.bat = select_next_bat(app.bat)
            bat_color_update()
    if(pauseScreen.visible == True):
        if(closeGameButton.contains(x,y)):
            update_stats()
            sys.exit(0)
        if(backToLauncher.contains(x,y)):
            update_stats()
            os.chdir("../")
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
            if(app.plane>=1):
                if(app.muted == False):
                    app.planeSound.play()
        else:
            app.pause = True
            pauseScreen.visible = True
            if(app.plane>=1):
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
allEnemies.toFront()
flak.toFront()
fakes.toBack()
update_stats()

app.run()