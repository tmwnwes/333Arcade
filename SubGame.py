## Creating the screen and wide-scoped variables/groups/labels/objects ##

import sys
from cmu_graphics import *
import tkinter as tk

gameInfo = open("Files/SubGameStats.txt", "r+")
fullInfoList = [] ## Key infomation can be found in MinesweeperStatsKeys.txt
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))
hi = fullInfoList[0]

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

app.width = width
app.height = height

app.failed = False
app.pause = False
app.achShowing = False
app.timer = 0
app.stepsPerSecond=30
app.powerCounter = 0
app.explosionCounter = 0
app.removeAchTimer = 200
app.yellow = False

powerUps=Group()
powerUpTimers = Group()
depthCharges = Group()
mines=Group()
allTorpedoes = Group()
explosion = Group()
bubbles = Group()
AcheivementNote = Group()


safetyShield=Circle((app.width/2),(app.height/2),80, fill="white")
ocean=Rect(0,app.height/10,app.width,(17/20)*app.height, fill=rgb(100,100,200))
seaFloor = Rect(0,ocean.bottom, app.width, 1/20*app.height, fill = 'saddleBrown')
sky = Rect(0,0,app.width, ocean.top, fill='lightSkyBlue')
propUp = Oval(235, 197, 2,8)
propDown = Oval(235, 202, 2, 8)
sub=Group(Oval(200,200,70,20), Line(185,200, 185, 180, lineWidth = 4), Line(185,182, 180,182, lineWidth = 4), Circle(235,200,2), propUp, propDown,  Circle(215, 200, 3, fill='white', borderWidth = 0.5, border = 'black'), Circle(200,200,3, fill='white', borderWidth = 0.5, border = 'black'), Circle(185,200,3,fill='white', borderWidth = 0.5, border = 'black'))
sub.centerX = safetyShield.centerX
sub.centerY = safetyShield.centerY

hsLabel = Label('High Score:', (17/20)*app.width, seaFloor.centerY, fill='white', size=25, bold=True)
ysLabel = Label('Your Score:', (1/20)*app.width, seaFloor.centerY, fill='white', size=25, bold=True)

score=Label(0,(3/20)*app.width, seaFloor.centerY, size=25, fill='white', bold=True)
gameOverScore=Label(0, 300, 120, bold=True, size=25, visible=False)
warning = Label("Depth Charges Incoming", seaFloor.centerX, seaFloor.centerY, fill="red", size = app.width/40, visible = False)
gameOverHighScore=Label(hi, 300, 150, bold=True, size=25, visible=False)
gameOverStuff=Group(Rect(50, 100, 300, 100, fill='lightCyan', border='red', borderWidth=5), Label('High Score:', 150, 150, size=30, bold=True), Label('Your Score:', 150, 120, size=30, bold=True), Label('Press ENTER to play again', 200, 180, size=20, bold=True))
gameOverStuff.visible=False
highScore=Label(hi, (19/20)*app.width, seaFloor.centerY, fill='white', size=25, bold=True)
torpSpeed = 150 / app.stepsPerSecond
bubbleSpeed = 100 / app.stepsPerSecond
maxRange = app.width/3
mines.count = 0
minesAtStart = 80
sub.health = 3

ammo = Label("Ammo:", sky.left+30, 10, size = 20)
torpedoes=Label(30, ammo.centerX, ammo.centerY+20, bold=True, size=20)
health = Label("Health:", sky.right-30, 10, size = 20)
hp=Label(sub.health, health.centerX, health.centerY+20, bold=True, size=20)

pauseScreen = Group(Rect(app.width/2, app.height/2, app.width/5, app.width/10, fill=None, border = 'yellow', borderWidth = 2, align = 'center', opacity = 0), Label("Game Paused", app.width/2, app.height/2, size = 30, opacity = 0))

## Creating the screen and wide-scoped variables/groups/labels/objects ##

## Object Motion ##

def move_charges():
    '''
    Takes no arguments and returns no values
    Moves depth charges down until they hit their target depth
    At that point, they explode
    '''
    for charge in depthCharges:
        charge.centerY+=3
        if charge.centerY>=charge.depth:
            explode_object(charge)
            depthCharges.remove(charge)
            score.value +=3

def move_bubbles():
    '''
    Takes no arguments and returns no values
    Moves all objects in the bubbles group, slowly makes them less visible and deletes them
    Intended to create the illusion of bubbles coming from moving torpedoes
    '''
    for bubble in bubbles:
        if(bubble.opacity>0):
            bubble.opacity -=4
        else:
            bubbles.remove(bubble)
        if(bubble.centerY>= ocean.top):
            bubble.centerY -= bubbleSpeed
        else:
            bubbles.remove(bubble)

def kaboom_all():
    '''
    Takes no arguments and returns no values, controls graphics only
    Kaboom handles the explosion effects for all objects that are exploding
    It will expand the explosion and remove it once it has reached the appropriate size
    Additionally, since explosions are supposed to harm the submarine, this function holds a hitcheck
    If the explosion touches the submarine, health is decreased
    '''
    for object in explosion:
        object.radius+=2
        if object.radius >=(1/50)*app.width:
            object.opacity -= 25
        if object.opacity ==0:
            explosion.remove(object)
        if (object.hitsShape(sub) and object.fill == 'red'):
            explosion.remove(object)
            decrease_health()

def propeller_motion():
    '''
    Takes no arguments and returns no values
    Provides a facsimile of propellers spinning on the sub    
    '''
    if(propDown.opacity == 0):
        propUp.opacity = 0
        propDown.opacity = 100
    else:
        propUp.opacity = 100
        propDown.opacity = 0

def move_torps():
    '''
    Takes no arguments and returns no values
    Moves all activeTorpedoes
    '''
    for torp in allTorpedoes:
        if torp.dir == 'left':
            torp.centerX -= torpSpeed
            spawn_bubbles(torp.right, torp.centerY, randrange(3), "left")
        else:
            torp.centerX += torpSpeed
            spawn_bubbles(torp.left, torp.centerY, randrange(3), "right")
            
## Object Motion ##

## Object Spawning ##

def create_depth_charge(x, y):
    '''
    Takes 2 positional arguments, x and y, returns a shape group
    x should be the horizontal value to create a charge at
    y should be the vertical value to send the charge to (not creation height)
    '''
    newCharge = Group()
    middle = RegularPolygon(x,ocean.top, 2, 4, )
    topCap = Circle(middle.left, middle.centerY, 2)
    bottomCap = Circle(middle.right, middle.centerY, 2)
    newCharge.add(middle, topCap, bottomCap)
    newCharge.depth = y
    newCharge.rotateAngle+=90
    return newCharge

def spawn_depth_charges(x, y):
    '''
    Takes 2 positional arguments, x and y, returns no values, but adds shapes to appropriate groups
    x and y should represent a general location that a depth charge should be sent towards
    This will launch a depth charge aimed in the vicinity of the (x,y) coordinated provided
    '''
    left  = (int)(x-200)
    right = (int)(x+200)
    top = (int)(y-50)
    bottom = (int)(y+100)
    if left<=10: left = 15
    if right>=app.width-10: right = (int)(app.width-15)
    if top<=ocean.top+5: top = (int)(ocean.top+10)
    if bottom>=ocean.bottom-10: right = (int)(ocean.bottom-15)
    randX = randrange(left, right)
    randY = randrange(top, bottom)
    charge = create_depth_charge(randX, randY)
    depthCharges.add(charge)
    
def spawn_mine():
    '''
    Takes no arguments and returns no values
    Spawns a mine at a random location in the ocean
    If that location is too close to the sub, it will pick another location    
    '''
    spawnX=randrange(10, app.width - 10, 10)
    spawnY=randrange(ocean.top+12, (int)(ocean.bottom) -10, 10)
    new = Star(spawnX, spawnY , 8, 12, fill='darkGray')
    while safetyShield.hitsShape(new):
        new.centerX = randrange(10, app.width - 10, 10)
        new.centerY = randrange(ocean.top+12, (int)(ocean.bottom) -10, 10)
    mines.add(new)
    mines.count+=1

def launch_torpedo(x,y, dir):
    '''
    Takes 3 arguments, x, y, and a direction, returns no values but adds shapes to appropriate groups
    x and y are positional arguments, direction entails which side of the sub to create the shape
    direction also determines the way the shapes should move
    '''
    if app.yellow == True:
        col = "yellow"
    else:
        col = "black"
    if(dir == "right"):
        new = Oval(x+10, y+4, 20, 6, fill=col)
        new.dist = new.centerX + maxRange
        new.dir = dir
        allTorpedoes.add(new)
    if(dir == "left"):
        new = Oval(x-10, y+4, 20, 6, fill=col)
        new.dir = dir
        new.dist = new.centerX - maxRange
        allTorpedoes.add(new)

def starter_mines():
    '''
    Takes no arguments and returns no values
    Creates minesAtStart many mines
    Intended to be used at the beginner of the game as well as upon restarting
    '''
    for i in range (minesAtStart):
        spawn_mine()

def spawn_powerup():
    '''
    Takes no arguments and returns no values
    Randomly decides what powerup to spawn on the map
    The powerups have weighted chances based on how powerful they are
    Makes sure not to put it directly next to the submarine so it is actually a bit of a trek to reach the powerup
    '''
    randX= randrange(20,app.width - 20,10)
    randY= randrange((int)(ocean.top)+10 ,(int)(ocean.bottom) - 10,10)
    if(not(safetyShield.hits(randX, randY))):
        powerUps.power=randrange(100)
        if(powerUps.power>=70):
            newPowerUp = Circle(randX, randY, 8, fill=rgb(255, 0, 0))
            newPowerUp.time = 20
            newPowerUp.num = app.powerCounter
            newTimer = Label(newPowerUp.time, randX, randY, size = 15, fill = 'black')
            newTimer.num = app.powerCounter
            powerUps.add(newPowerUp)
            powerUpTimers.add(newTimer)
        elif(powerUps.power>=25):
            newPowerUp = Circle(randX, randY, 8, fill=rgb(0, 0, 255))
            newPowerUp.time = 20
            newPowerUp.num = app.powerCounter
            newTimer = Label(newPowerUp.time, randX, randY, size = 15, fill = 'white')
            newTimer.num = app.powerCounter
            powerUps.add(newPowerUp)
            powerUpTimers.add(newTimer)
        elif(powerUps.power>=1):
            newPowerUp = Circle(randX, randY, 8, fill=rgb(0, 255, 0))
            newPowerUp.time = 20
            newPowerUp.num = app.powerCounter
            newTimer = Label(newPowerUp.time, randX, randY, size = 15, fill = 'black')
            newTimer.num = app.powerCounter
            powerUps.add(newPowerUp)
            powerUpTimers.add(newTimer)
        elif(powerUps.power>=0):
            newPowerUp = Circle(randX, randY, 8, fill="purple", border = 'yellow')
            newPowerUp.time = 30
            newPowerUp.num = app.powerCounter
            newTimer = Label(newPowerUp.time, randX, randY, size = 15, fill = 'white')
            newTimer.num = app.powerCounter
            powerUps.add(newPowerUp)
            powerUpTimers.add(newTimer)
    else:
        spawn_powerup()
        
def spawn_bubbles(x,y, num, dir):
    '''
    Takes 4 arguments, x and y for position, num for how many bubbles to create, 
    dir for which way the torp is moving and where the bubbles should be spawned
    Can be used for non torp bubbles, should use None as direction in that case
    Returns no values but adds created shapes to a pre-defined group, bubbles,
    Will create bubbles in the close vicinity of the given location
    '''
    for i in range(num):
        offsetX = randrange(5)
        if(dir == 'left'):
            new = Circle(x + offsetX, y, randrange(1,5), fill = None, border = 'white')
        else:
            new = Circle(x - offsetX, y, randrange(1,5), fill = None, border = 'white')
        bubbles.add(new)

def spawn_handling():
    '''
    Takes no arguments and returns no values
    Handles all of the spawning events for depth charges, mines, warning labels, and powerups
    '''
    if(app.timer%(app.stepsPerSecond*25) == 0):
        for i in range(7):
            spawn_depth_charges(sub.centerX, sub.centerY)
    if(app.timer%(app.stepsPerSecond*25) == (app.stepsPerSecond*20)): 
        spawn_warning()
    if(app.timer%(app.stepsPerSecond*25) == (app.stepsPerSecond*4)):
        despawn_warning()
    if((int)(app.timer%(app.stepsPerSecond*(2/3))) == 0):  
        spawn_mine()
    if((int)(app.timer%(app.stepsPerSecond*17) == 0)):
        app.powerCounter+=1
        spawn_powerup()

def spawn_warning():
    '''
    Takes no arguements and returns no values
    Adds the depth charge warning
    '''
    warning.visible = True

## Object Spawning ##

## Timing, Scoring, Collisions, and Destruction ##

def depth_charge_check():
    '''
    Takes no arguments and returns no values
    Handles the case of depth charges hitting the submarine directly
    '''
    for charge in depthCharges:
        if charge.hitsShape(sub):
            explode_object(charge)
            depthCharges.remove(charge)

def explode_object(shape):
    '''
    Takes a shape as an argument, returns no values, but adds shapes to an explosion group
    Explosion effects created at the location of the exploding object
    3 shapes are created for the explosion, to mimic a gradient while also allowing removal of the effect slowly
    '''
    inner = Star(shape.centerX, shape.centerY, 5, 12, fill = "yellow")
    middle = Star(shape.centerX, shape.centerY, 8, 12, fill = "orange")
    outer = Star(shape.centerX, shape.centerY, 12, 12, fill = 'red')
    explosion.add(outer, middle, inner)

def power_timing(num, time):
    '''
    Takes 2 arguments, num and time, returns no values, but can both update and remove shapes from game
    num enables a check that the timer is the correctly related object, and time is the value the timer should be set to
    time is also the trigger for removal of the time at value 0
    '''
    for timer in powerUpTimers:
        if num == timer.num:
            timer.value = time
            if time<=0:
                powerUpTimers.remove(timer)


def unlockAcheivement(type):
    app.achShowing = True
    box = Rect(app.width/2, sky.centerY, 1/2*app.width, sky.height, fill = None, border = 'black', align = 'center')
    app.removeAchTimer = 200
    name = Label("You unlocked the" + type + " Acheivement", box.centerX, box.centerY-10, size = app.width/75)
    instruction = Label("Press y to toggle your " + type, name.centerX, name.centerY + 25, size = app.width/75)
    AcheivementNote.add(box, name, instruction)
                
def power_ups_time_management_and_collision():
    '''
    Takes no arguments and returns no values
    Handles updating powerup timers
    Handles despawning of powerups in the case of time running out
    Handles implementation of rewarding powerUps to the player if they collect the powerup
    '''
    for power in powerUps:
        if(app.timer%app.stepsPerSecond == 0):
            power.time -= 1
            power_timing(power.num, power.time)
            if(power.time <= 0):
                powerUps.remove(power)
        if(power.hitsShape(sub)):
            fullInfoList[6]+=1
            power_timing(power.num, 0)
            if(power.fill==rgb(0, 0, 255)):
                score.value+=15
            if(power.fill==rgb(0, 255, 0)):
                if(mines.count>=150):
                    fullInfoList[2] = 1
                    unlockAcheivement("Yellow Submarine")
                for mine in mines:
                    explode_object(mine)
                    mines.remove(mine)
                score.value+=mines.count
                fullInfoList[3]+=mines.count
                mines.count=0
            if(power.fill==rgb(255, 0, 0)):
                torpedoes.value+=25
            if(power.fill =='purple'):
                sub.health = 3
                hp.value = sub.health
                torpedoes.value+=50
                mines.clear()
                score.value += mines.count
                fullInfoList[3]+=mines.count
                score.value += 100
                mines.count = 0 
            powerUps.remove(power)

def torps_destroying_mines():
    '''
    Takes no arguments and returns no values
    Handles the case of a torpedo directly impacting a mine or exceeding their maximum range
    '''
    for torp in allTorpedoes:
        if(torp.centerX>=torp.dist and torp.dir == 'right'):
            explode_object(torp)
            allTorpedoes.remove(torp)
        if(torp.centerX<=torp.dist and torp.dir == 'left'):
            explode_object(torp)
            allTorpedoes.remove(torp)
        for mine in mines:
            if torp.hitsShape(mine):
                explode_object(mine)
                fullInfoList[3]+=1
                mines.remove(mine)
                score.value+=1
                mines.count-=1
                allTorpedoes.remove(torp)
                fullInfoList[5]+=1

def sub_against_mines():
    '''
    Takes no arguements and returns no values
    Handles the case of the submarine directly impacting mines
    '''
    for mine in mines:
        if sub.hitsShape(mine):
            explode_object(mine)
            mines.remove(mine)

def chainReaction():
    '''
    Takes no arguments and returns no values
    Implements a chain reaction for explosions to cause explosions of nearby objects
    If an explosion hits any mine, that mine will explode, causing a chain reaction to other nearby mines
    '''
    for boom in explosion:
        for mine in mines:
            if boom.hitsShape(mine):
                explode_object(mine)
                mines.remove(mine)
                score.value+=1
                fullInfoList[3]+=1

def despawn_warning():
    '''
    Takes no arguments and returns no values
    Removes the depth charge warning
    '''
    warning.visible = False 

def decrease_health():
    '''
    Takes no arguements and returns no values
    Lowers sub health upon being called. 
    If this call puts the sub at or below 0 health, the game will end
    '''
    if sub.health <= 1:
        sub.health = 0
        hp.value = sub.health
        game_over()
    else:
        sub.health -=1
        hp.value = sub.health

def hit_detection():
    '''
    Takes no arguments and returns no values
    Runs all other hit detection and collisions functions
    '''    
    sub_against_mines()
    power_ups_time_management_and_collision()
    torps_destroying_mines()
    depth_charge_check()

def update_stats():
    '''
    Takes no arguments and returns no values
    Updates values relating to stored stats outside of the program
    '''
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")

def update_high_score():
    '''
    Updates the High Score in Game if current score is higher
    Also updates high score value stored outside of the game
    
    '''
    if(score.value>highScore.value):
        highScore.value=score.value
    fullInfoList[0] = highScore.value
    update_stats()
    
def toggle_yellow_sub():
    if app.yellow == False:
        for thing in sub:
            if thing.fill == 'black':
                thing.fill = 'yellow'
        app.yellow = True
    else:
        for thing in sub:
            if thing.fill == 'yellow':
                thing.fill = 'black'
        app.yellow = False

def toggle_pause():
    if(app.failed == False):
        if app.pause == True:
            app.pause = False
            for thing in pauseScreen:
                thing.opacity = 0
        else:
            app.pause = True
            for thing in pauseScreen:
                thing.opacity = 100
## Timing, Scoring, Collisions, and Destruction ##

## Ending and Resetting ##
def game_over():
    '''
    Takes no arguments and returns no values
    Shows the fail screen, score, and high score
    Places game into fail mode
    '''
    gameOverStuff.visible=True
    gameOverScore.visible=True
    gameOverScore.toFront()
    gameOverScore.value=score.value
    gameOverHighScore.toFront()
    gameOverHighScore.value=highScore.value
    gameOverHighScore.visible=True
    app.failed=True
    update_stats()
    
def restartGame():
    '''
    Takes no arguments and retuens no values
    When called:
    -> all values are reset to initial values
    -> all groups are cleared
    -> all shapes are reset to starting locations
    -> high score remains unchanged
    -> mines are placed for the next round
    '''
    despawn_warning()
    app.powerCounter = 0
    app.timer = 0
    safetyShield.centerX=app.width/2
    safetyShield.centerY=app.height/2
    sub.centerX=safetyShield.centerX
    sub.centerY=safetyShield.centerY   
    explosion.clear()
    powerUps.clear()
    powerUpTimers.clear()
    depthCharges.clear()
    mines.clear()
    mines.count=0    
    gameOverStuff.visible=False
    gameOverScore.visible=False
    gameOverHighScore.visible=False
    gameOverScore.toFront()
    gameOverScore.value=score.value
    score.value=0
    torpedoes.value=30
    sub.health = 3
    hp.value = sub.health
    app.failed=False
    starter_mines()
    fullInfoList[1]+=1
    update_stats()

## Ending and Resetting ##
 
## CMU Built-In Functions Used for Player Motion, Controls, Handling ##

def onKeyPress(key):
    '''
    CMU Built-In Funciton
    Takes keyboard input as argument, returns no values
    Focus on presses, not holds
    Primarily used for restarting the game and lunching torpedoes
    '''
    if(key=='enter'):
        if(app.failed == True):
            restartGame()
    if(app.paused == False):
        if(torpedoes.value>0):
            if(key=='right' or key == 'left'): 
                launch_torpedo(sub.centerX, sub.centerY, key)
                fullInfoList[4]+=1
                torpedoes.value-=1
        if(key == 'y' or key == 'Y'):
            if fullInfoList[2] == 1:
                toggle_yellow_sub()
    if(key == "escape" or key =='p' or key =='P'):
        toggle_pause() 
            
def onStep():
    '''
    CMU Built-In Function
    Takes no arguments and returns no values
    Anything called in this function is called app.stepsPerSecond many times per second
    '''
    if(app.achShowing == True):
        app.removeAchTimer-=1
        if(app.removeAchTimer <=0):
            AcheivementNote.clear()
            app.achShowing = False
    if(app.pause==False):
        app.timer+=1
        if(app.timer%3 == 0):
            propeller_motion()
        update_high_score()
        hit_detection()
        kaboom_all()
        move_torps()
        move_charges()
        chainReaction()
        spawn_handling()
        move_bubbles()
        
def onKeyHold(keys):
    '''
    CMU Built-In Function
    Takes keyboard input as arguments, specifcally looking for key holds, returns no values 
    Focus is on game motion, moving the submarine, as well as the 
    '''
    if(app.failed==False and app.pause == False):
        if(sub.left>0):    
            if('a' in keys):
                sub.centerX-=(1/2+sub.health/2)  
        if(sub.right<app.width):
            if('d' in keys):
                sub.centerX+=(1/2+sub.health/2)  
        if(sub.top>ocean.top+4):
            if('w' in keys):
                sub.centerY-=(1/2+sub.health/2)  
        if(sub.bottom<ocean.bottom-5):
            if('s' in keys):
                sub.centerY+=(1/2+sub.health/2)  
        safetyShield.centerX = sub.centerX
        safetyShield.centerY = sub.centerY
        
## CMU Built-In Functions Used for Player Motion, Controls, Handling ##

## Bring All Game Object Groups to Front in a Proper Order and Spawn Mines to Start the Game ##

powerUps.toFront()
powerUpTimers.toFront()
depthCharges.toFront()
explosion.toFront()
allTorpedoes.toFront()
mines.toFront()
bubbles.toFront()
sub.toFront()
AcheivementNote.toFront()
starter_mines()
fullInfoList[7]+=1
fullInfoList[1]+=1
update_stats()
    
if(fullInfoList[2] == 1):
    unlockAcheivement("Yellow Submarine")

## Bring All Game Object Groups to Front in a Proper Order and Spawn Mines to Start the Game ##

app.run()