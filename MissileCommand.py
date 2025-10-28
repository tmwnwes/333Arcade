from cmu_graphics import *
import tkinter as tk
import random

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.wm_attributes('-fullscreen', True) ## This line is a workaround for macOs devices with no ill effects for Windows users. It forces a new window to open in fullscreen and focus on it, before destroying it on the next line. The main canvas is then created and players will see it. Players must still maximise this window manually however
root.destroy()

gameInfo = open("Files/MissileCommandStats.txt", "r+")
fullInfoList = [] 
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))
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
app.mult = 1
app.shotSpeedLR = 15
app.shotSpeedMid = 20
app.basicMissileSpeed = 2
app.multiBombSpeed = 3
app.planeSpeed = 6
app.spawnTimer = app.stepsPerSecond * 5
app.enemiesLeftToSpawn = 10
app.bombSpeed = 8
app.gravity = 0.05
app.saucerSpeed = 3
app.ufoProjectileSpeed = 12
app.timeToDropBombs = app.width//app.planeSpeed
app.infoTimer = app.stepsPerSecond*5
app.infoShowing = False

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
    label2 = Label("You have unlocked a bonus city", box.centerX+20, box.top, fill='white', align = 'top', size = 15)
    label3 = Label("Survive this wave to spawn your bonus city", box.centerX+20, label2.bottom+2, fill='white', align = 'top', size = 15)
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
    city.health = 4
    cityids.append(city.id)
    for i in range(12):
        tall = randrange(5,80)
        wide = randrange(4,15)
        lastWidth = wide
        building = Rect(x+lastWidth+ i*(app.width/200), app.height-tall, wide, tall, border = 'white')
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
    fullInfoList[1]+=1
    app.spawnTimer = app.stepsPerSecond * 5
    app.enemiesLeftToSpawn = 10
    app.score = 0
    score.value = "Score: %05d" %app.score
    app.munitionCounter = 0
    app.gate = 3500
    app.generalReload = app.stepsPerSecond*2.5
    app.level = 1
    app.mult = 1
    app.cities = 6
    stage.value = "Level %1d" %app.level
    gameOver.clear()
    for bat in batteries:
        bat.reloadTimer = 0
        bat.repairTimer = 0
        bat.ammoCount = 10
        bat.border = 'grey'
        app.bat = batteries[0]
    make_all_cities_new_level()
    app.play = True
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

def spawn_plane(y):
    '''
    Takes one positional arg and returns no values
    y represents the height on the screen that the shape will be spawned
    Creates a shape with certain attributes
    Then adds that shape to an appropriate group
    '''
    hitbox = Rect(-20, y, 40, 10, border = 'white')
    hitbox.bombs = app.level
    hitbox.angle = angleTo(hitbox.centerX, hitbox.centerY, app.width+30, hitbox.centerY)
    hitbox.next = getPointInDir(hitbox.centerX, hitbox.centerY, hitbox.angle, app.planeSpeed)
    hitbox.dropZones = []
    hitbox.score = 625
    for i in range(hitbox.bombs+1, 1, -1):
        hitbox.dropZones.append(app.width/i)
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

def spawn_bombs(x,y):
    '''
    Takes 2 positional arguments, x and y for horizontal and vertical spawning respectively
    Creates a shape with specific attributes anf adds it to a shape group, returns no values
    Typicallt used to drop bombs from bomber planes
    '''
    bomb = Oval(x,y,2,8, fill = 'white')
    bomb.speed = app.bombSpeed
    bomb.rotateAngle = angleTo(bomb.centerX, bomb.centerY, bomb.centerX + randrange(30, 80), app.height)
    bomb.next = getPointInDir(bomb.centerX, bomb.centerY, bomb.rotateAngle, bomb.speed)
    bomb.score = app.level * 50
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
        if(object.radius<=(1/150)*app.width): 
            object.radius+=1
        if object.radius >=(1/200)*app.width:
            object.time -= 1
        if object.opacity == 0:
            explosion.remove(object)

def explode_object(shape):
    '''
    Takes a shape as an argument, and returns no values
    adds a new shape to an appropriate shape group
    New shape is based on the location of the given shape
    '''
    new = Circle(shape.centerX, shape.centerY, 3, fill='yellow', border = 'orange')
    new.time = app.stepsPerSecond * 3
    explosion.add(new)
    
def move_shots():
    '''
    Takes no args and returns no values
    Moves the player fired munitions towards their intended location. 
    Crucial function. Game will not work without this function.
    Forces an explosion if the target is hit ot bypassed
    '''
    for shot in defense:
        shot.centerX, shot.centerY = shot.next
        if(shot.loc == 'mid'):
            shot.next = getPointInDir(shot.centerX, shot.centerY, shot.rotateAngle, app.shotSpeedMid)
        else:
            shot.next = getPointInDir(shot.centerX, shot.centerY, shot.rotateAngle, app.shotSpeedLR)
        if shot.centerY <= shot.target[1]:
            explode_object(shot)
            for target in targets:
                if shot.num == target.num:
                    targets.remove(target)
            defense.remove(shot)
            
def onKeyPress(key):
    '''
    CMU built in funciton which takes a pressed key as input
    used in this function to select firing batteries and to restart the game upon loss
    '''
    if(key == 'right'):
        app.bat = select_next_bat(app.bat)
    if(key == 'left'):
        app.bat = select_prev_bat(app.bat)
    if(app.play == False):
        if(key == 'enter'):
            reset()
    bat_color_update()

def reload_all():
    '''
    Takes no args and returns no values
    Ensures that reloading, ammo counts, repair times are all accurate for each missile battery
    '''
    for bat in batteries:
        bat.ammo.value = "Ammo: %1d" %(bat.ammoCount)
        if(bat.reloadTimer>0):
            bat.reloadTimer-=1
            bat.timer.value = "Ready in: %1.1f" %(bat.reloadTimer / app.stepsPerSecond)
        if(bat.repairTimer>0):
            bat.repairTimer-=1
            bat.repairLabel.value = "Repaired in: %1.1f" %(bat.repairTimer / app.stepsPerSecond)
        else: bat.broken = False
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
                spawn_bombs(plane.centerX, plane.centerY)
                plane.bombs-=1

def spawn_basic_missile(x,y):
    '''
    Takes 2 args and returns no values
    Adds new shape with special attributes to shape group
    This function creates the most basic enemy in the game, a basic missile, no horizontal motion, not affected by gravity
    '''
    new = Circle(x,y, 6, fill = 'limeGreen')
    new.num = app.munitionCounter
    new.score = 100
    new.rotateAngle = angleTo(x,y,x,app.height)
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, app.basicMissileSpeed)
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
                points = bomb.score * app.mult
                app.score+= points
                create_scores(bomb.centerX, bomb.centerY, points)
                explode_object(bomb)
                type.remove(bomb)
                fullInfoList[3]+=1
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
                explode_object(missile)
                type.remove(missile)
                bat.broken = True
                bat.repairTimer += 30*app.stepsPerSecond
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
                explode_object(missile)
                type.remove(missile)
                bat.broken = True
                bat.repairTimer += 10*app.stepsPerSecond
                if bat == app.bat: app.bat = select_next_bat(app.bat)
                bat_color_update()

def missile_vs_ground(type):
    '''
    Takes 1 arg and returns no values
    type represents the shape group being checked against hitting the ground
    Important for realism and also preventing lag since it forces deletion of shapes that would be below the screen
    '''
    for missile in type:
        if missile.bottom>= app.height:
            explode_object(missile)
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
                    explode_object(building)
                explode_object(missile)
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
                        explode_object(building)
                    explode_object(bomb)
                    type.remove(bomb)
                    cityids.remove(city.id)
                    cities.remove(city)
                    app.cities-=1
                    fullInfoList[5]+=1    
            else:
                for building in city:
                    if(bomb.hitsShape(building)):
                        explode_object(building)
                        explode_object(bomb)
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
                explode_object(missile)
                points = missile.score*app.mult*5
                app.score+=points
                create_scores(missile.centerX, missile.centerY, points)
                type.remove(missile)
                defense.remove(anti)
                fullInfoList[3]+=1
                fullInfoList[4]+=1
       
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
    missiles_vs_cities(ufoShots)
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
        gameOver.add(RegularPolygon(app.width/2, app.height/2, app.width/2, 4, fill=None))
        gameOver.add(Label("All Cities Lost", app.width/2, app.height/4, fill='white', size = 30))
        gameOver.add(Label("Final Score: %d" %app.score, app.width/2, 3*app.height/8, fill='white', size = 30))
        gameOver.add(Label("High Score: %d" %app.hiscore, app.width/2, app.height/2, fill='white', size = 30))
        gameOver.add(Label("Press Enter to Restart", app.width/2, 5*app.height/8, fill='white', size = 30))

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
        new.rotateAngle = angleTo(x,y,randrange(x-(app.width//10), x+(app.width//10)), app.height)
        new.next = getPointInDir(x,y,new.rotateAngle, app.bombSpeed)
        new.score = 100
        new.speed = app.bombSpeed
        multiBombPostSplit.add(new)
    
def spawn_multi_bomb(x, detHeight):
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
    new.score = 750 + (125 * new.bombs)
    new.speed = app.multiBombSpeed
    new.rotateAngle = angleTo(new.centerX,new.centerY,randrange(app.width//4, 3*(app.width//4)),detHeight)
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, new.speed)
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
            spawn_small_bombs((int)(bomb.centerX), (int)(bomb.centerY), bomb.bombs)
            multiBombs.remove(bomb)
        
def spawn_shots(x, y, angle):
    '''
    Takes 3 args, x and y for horizontal and vertical positioning, and angle for direction
    Returns no values but does add shapes to appropriate shape groups
    '''
    new = Oval(x,y,2,20, fill='white', rotateAngle = angle)
    new.next = getPointInDir(x,y,angle,app.ufoProjectileSpeed)
    new.score = 1000
    new2 = Oval(x,y,2,20, fill='white', rotateAngle = angle+10)
    new2.next = getPointInDir(x,y,angle+10,app.ufoProjectileSpeed)
    new2.score = 1000
    new3 = Oval(x,y,2,20, fill='white', rotateAngle = angle-10)
    new3.next = getPointInDir(x,y,angle-10,app.ufoProjectileSpeed)
    new3.score = 1000
    new4 = Oval(x,y,2,20, fill='white', rotateAngle = angle+5)
    new4.next = getPointInDir(x,y,angle+5,app.ufoProjectileSpeed)
    new4.score = 1000
    new5 = Oval(x,y,2,20, fill='white', rotateAngle = angle-5)
    new5.next = getPointInDir(x,y,angle-5,app.ufoProjectileSpeed)
    new5.score = 1000
    ufoShots.add(new, new2, new3, new4, new5)        

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
            spawn_shots(saucer.centerX, saucer.centerY, angle)
            saucer.firing-=1

def spawn_fun_missile():
    '''
    Takes no args and returns no values
    Creates a shape with specific attributes and adds it to the appropriate shape group
    This enemy type is affected by horizontal motion and gravity
    '''
    new = Circle(randrange(app.width), -100, 6, fill='red')
    new.score = 1000
    new.num = app.munitionCounter
    new.speed = app.basicMissileSpeed - 1
    new.gravSpeed = app.gravity
    new.rotateAngle = angleTo(new.centerX, new.centerY, randrange(app.width//40, 39*app.width//40), app.height)
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, new.speed)
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
        bomb.speed += app.gravity
        for shape in explosion:
            if(shape.centerY> bomb.centerY):
                bomb.how_far.append(((distance(bomb.centerX, bomb.centerX, shape.centerX, shape.centerY)), (angleTo(bomb.centerX, bomb.centerY, shape.centerX, shape.centerY)), shape))
        if(len(bomb.how_far)>0):
            lowestDistaceExplosionInfo = min(bomb.how_far, key=lambda t: t[0])
            scaryAngle = lowestDistaceExplosionInfo[1]
            if(bomb.rotateAngle <= scaryAngle and bomb.rotateAngle>140):
                bomb.rotateAngle -= 2
                bomb.speed -= (app.gravity/2)
            elif(bomb.rotateAngle> scaryAngle and bomb.rotateAngle<220):
                bomb.rotateAngle +=2
                bomb.speed -= (app.gravity/2)
        bomb.next = getPointInDir(bomb.centerX, bomb.centerY, bomb.rotateAngle, bomb.speed)           

def spawn_smart_bomb():
    '''
    Takes no args and returns no values
    Creates a shape with specific attributes and adds to appropriate shape group
    '''
    new = Circle(randrange(app.width), -100, 6, fill='white')
    new.speed = 3
    new.howFar = []
    new.score = 1225
    new.rotateAngle = angleTo(new.centerX, new.centerY, randrange(app.width), app.height)
    new.next = getPointInDir(new.centerX, new.centerY, new.rotateAngle, new.speed)
    smartMissiles.add(new)
                
def spawn_ufo():
    '''
    Takes no args and returns no values
    Creates shape and decides location for spawning, adding to appropriate shape group
    '''
    location = randrange(2)
    saucer = create_saucer(0, (app.height//10), location)
    saucer.score = 1450     
    saucer.firing = app.level
    ufos.add(saucer)              
                
def spawn_handling():
    '''
    Takes no args and returns no values
    Handles spawning enemies, based on current game level
    '''
    if(app.level == 1): ## Just straight missiles
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer == 0):
                spawn_basic_missile(randrange(0,app.width), -10)
                app.spawnTimer = app.stepsPerSecond * 6
                app.enemiesLeftToSpawn -=1
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    elif(app.level <= 3): ## missiles and bomber planes
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer == 0):
                if(app.enemiesLeftToSpawn %4 ==0):
                    spawn_plane(randrange(app.height//4, app.height//2))
                else:
                    spawn_basic_missile(randrange(0,app.width), -10)
                app.spawnTimer = app.stepsPerSecond * 5
                app.enemiesLeftToSpawn -=1
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    elif(app.level <= 6): ## missiles, bomber planes higher up, multi-bombs, non straight missiles
            if(app.enemiesLeftToSpawn >=1):
                if(app.spawnTimer == 0):
                    if(app.enemiesLeftToSpawn% 9 == 0):
                        spawn_multi_bomb(randrange(app.width), randrange(app.height//4, 3*app.height//4))
                    if(app.enemiesLeftToSpawn%4 == 0):
                        spawn_plane(randrange(20, app.height//4))
                    if(app.enemiesLeftToSpawn%7 == 0):
                        spawn_fun_missile()
                    else:
                        spawn_basic_missile(randrange(0,app.width), -10)
                    app.spawnTimer = app.stepsPerSecond * 4
                    app.enemiesLeftToSpawn -=1
                    newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    if(app.level <=9 ): ## all of the above, plus smart bombs
            if(app.enemiesLeftToSpawn >=1):
                if(app.spawnTimer == 0):
                    if(app.enemiesLeftToSpawn% 9 == 0):
                        spawn_multi_bomb(randrange(app.width), randrange(app.height//4, 3*app.height//4))
                    if(app.enemiesLeftToSpawn%4 == 0):
                        spawn_plane(randrange(20, app.height//4))
                    if(app.enemiesLeftToSpawn%7 == 0):
                        spawn_fun_missile()
                    if(app.enemiesLeftToSpawn%11 == 0):
                        spawn_smart_bomb()
                    else:
                        spawn_basic_missile(randrange(0,app.width), -10)
                    app.spawnTimer = app.stepsPerSecond * 3
                    app.enemiesLeftToSpawn -=1
                    newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn
    else: ## all of the above, plus hovering ufos which will launch devastating strikes if they are not blown up fast enough, and basic missiles can spawn at the same time as other enemy types
        if(app.enemiesLeftToSpawn >=1):
            if(app.spawnTimer == 0):
                if(app.enemiesLeftToSpawn% 9 == 0):
                    spawn_multi_bomb(randrange(app.width), randrange(app.height//4, 3*app.height//4))
                    app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn%4 == 0):
                    spawn_plane(randrange(20, app.height//4))
                    app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn%7 == 0):
                    spawn_fun_missile()
                    app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn%11 == 0):
                    spawn_smart_bomb()
                    app.enemiesLeftToSpawn -=1
                if(app.enemiesLeftToSpawn%23): ##Rare event, on purpose
                    spawn_ufo()
                    app.enemiesLeftToSpawn -=1
                spawn_basic_missile(randrange(0,app.width), -10)
                app.spawnTimer = app.stepsPerSecond * 2
                app.enemiesLeftToSpawn -=1
                newLevelWarning.value = "Enemies until next level: %d" % app.enemiesLeftToSpawn

def onStep():
    '''
    CMU built in function
    All code in this body is executed app.stepsPerSecond many times every second
    Used to show motion in this project
    '''
    if(app.play == True):
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
        if(app.infoTimer ==0):
            info.clear()
        update_stats()

def onMousePress(x,y):
    '''
    CMU built in function
    Takes mouse press locations as arguments
    In this project, used to aim munitions
    '''
    realX, realY = x,y ## This fixed an error where the player should shoot when entering fullscreen on macOs devices
    app.munitionCounter+=1
    if(app.bat.broken == False):
        if(app.bat.reloadTimer == 0 and app.bat.ammoCount>=1):
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
            
starting_bat()
app.bat = batteries[0]
app.bat.border = 'white'
make_all_cities_new_level()
fullInfoList[1]+=1
fullInfoList[6]+=1
update_stats()

app.run()