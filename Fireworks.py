## App Settings ##

from cmu_graphics import *
import tkinter as tk
import random

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()


gameInfo = open("Files/FireworksFinalStats.txt", "r+")
fullInfoList = [] ## Key infomation can be found in MinesweeperStatsKeys.txt
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))


app.width = width
app.height = height
app.mode = "manual"
app.up = 1
app.play = True 
app.count = 1 
app.starryNight = False
app.twinkleMode = False 
app.stepsPerSecond = 30  
app.setMaxShapeCount(1000000)
app.autoClickSpeed = 90 
app.autoTwinkleSpeed = 90 
app.autoUntwinkleSpeed = 3 
app.timer = 0 
flareMove = (1/80) *app.height
expansion = (1/100) *app.width
maxFireworkSize = (9/20) * app.width

## App Settings

## Main Screen Settings

Rect(0,0,app.width,app.height) 
allColors = ["white", "pink", "red", "yellow", "orange", "green", "cyan", "blue", "magenta"]
title = Label("Fireworks", app.width/2, (7/80)*app.height, fill = "white", size = (1/8)*app.width)
instructions = Label("Select colors & settings for the firework show" , app.width/2, (9/40)*app.height, fill = "pink", size = (1/25)*app.width)
white = Rect((3/40 *app.width), (2/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "white") 
pink = Rect((3/8 *app.width), (2/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "deepPink") 
red = Rect((27/40 *app.width), (2/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "red") 
yellow = Rect((3/40 *app.width), (3/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "yellow") 
orange = Rect((3/8 *app.width), (3/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "darkOrange") 
green = Rect((27/40 *app.width), (3/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "lime") 
cyan = Rect((3/40 *app.width), (4/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "cyan") 
blue = Rect((3/8 *app.width), (4/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "blue") 
magenta = Rect((27/40 *app.width), (4/5 *app.height), (1/4 *app.width), (7/40 *app.height), fill = "magenta") 
goButton = Rect((17/40)*app.width, (3/10)*app.height, (3/20)*app.width, (3/40)*app.height, fill = 'limeGreen', border = 'green', borderWidth = 3) 
goLabel = Label("GO!", app.width/2, (27/80)*app.height, fill = "white", size = (1/20)*app.width, font = "monospace", bold = True)
colorButtons = Group(white, pink, red, yellow, orange, green, cyan, blue, magenta)  ## places all color buttons in a group
colorButtons.active = True
warningLabel = Label("Please Select at Least 1 Color to Continue", app.width/2, (11/40)*app.height, fill = "limeGreen", size = (1/40)*app.width, bold = True, visible = False)
screenSaverButton = Rect(0, (1/15 * app.height), (1/7) * app.width,(1/20)* app.height, border = 'gray', fill = None)
screenSaverLabel = Label("Screensaver Mode Inactive", screenSaverButton.centerX, screenSaverButton.centerY, fill = "gray", size = (1/100)*app.width, bold = True)
starryNightButton = Rect((6/7)*app.width, (1/15 * app.height), (1/7) * app.width,(1/20)* app.height, border = 'gray', fill = None)
starryNightLabel = Label("starry Night Mode Inactive", starryNightButton.centerX, starryNightButton.centerY, fill = "gray", size = (1/100)*app.width, bold = True)
twinkleButton = Rect((6/7)*app.width, (2/15 * app.height), (1/7) * app.width,(1/20)* app.height, border = 'gray', fill = None)
twinkleLabel = Label("Twinkle Mode Inactive", twinkleButton.centerX, twinkleButton.centerY, fill = "gray", size = (1/100)*app.width, bold = True)
clearStarsButton = Rect(0, (2/15 * app.height), (1/7) * app.width,(1/20)* app.height, border = 'gray', fill = None)
clearStarsLabel = Label("Remove All Stars", clearStarsButton.centerX, clearStarsButton.centerY, fill = "gray", size = (1/100)*app.width, bold = True)
selectAllButton = white = Rect((3/40 *app.width), (3/10 *app.height), (1/4 *app.width), (3/40 *app.height), fill = None, border = 'gray') 
deselectAllButton = white = Rect((27/40 *app.width), (3/10 *app.height), (1/4 *app.width), (3/40 *app.height), fill = None, border = 'gray')
selectAllLabel = Label("Select All Colors", selectAllButton.centerX, selectAllButton.centerY, fill = 'grey', size = (1/50) * app.width)
deselectAllLabel = Label("Deselect All Colors", deselectAllButton.centerX, deselectAllButton.centerY, fill = 'grey', size = (1/50) * app.width)
helpButton = Rect(0, 0, (1/7) * app.width,(1/20)* app.height, border = 'gray', fill = None)
helpLabel = Label("Help", helpButton.centerX, helpButton.centerY, fill = "gray", size = (1/40)*app.width, bold = True)
speedButtonHolder = Rect((5/7)*app.width, 0, (2/7) * app.width,(1/20)* app.height, border = 'gray', fill = None)
speedDecreaseButton = Rect(speedButtonHolder.left+(4/49)*app.width, speedButtonHolder.top, (2/49)*app.width, (1/20)*app.height, border = "gray", fill = None)
speedIncreaseButton = Rect(speedButtonHolder.left+(8/49)*app.width, speedButtonHolder.top, (2/49)*app.width, (1/20)*app.height, border = "gray", fill = None)
speedDecreaseLabel = Label('-', speedDecreaseButton.centerX, speedDecreaseButton.centerY, size = (1/40)*app.width, fill = 'gray')
speedIncreaseLabel = Label('+', speedIncreaseButton.centerX, speedIncreaseButton.centerY, size = (1/40)*app.width, fill = 'gray')
speedDecrease10Button = Rect(speedButtonHolder.left+(2/49)*app.width, speedButtonHolder.top, (2/49)*app.width, (1/20)*app.height, border = "gray", fill = None)
speedIncrease10Button = Rect(speedButtonHolder.left+(10/49)*app.width, speedButtonHolder.top, (2/49)*app.width, (1/20)*app.height, border = "gray", fill = None)
speedDecrease10Label = Label('<<', speedDecrease10Button.centerX, speedDecrease10Button.centerY, size = (1/40)*app.width, fill = 'gray')
speedIncrease10Label = Label('>>', speedIncrease10Button.centerX, speedIncrease10Button.centerY, size = (1/40)*app.width, fill = 'gray')
speedDecreaseMaxButton = Rect(speedButtonHolder.left, speedButtonHolder.top, (2/49)*app.width, (1/20)*app.height, border = "gray", fill = None)
speedIncreaseMaxButton = Rect(speedButtonHolder.left+(12/49)*app.width, speedButtonHolder.top, (2/49)*app.width, (1/20)*app.height, border = "gray", fill = None)
speedDecreaseMaxLabel = Label('Min', speedDecreaseMaxButton.centerX, speedDecreaseMaxButton.centerY, size = (1/60)*app.width, fill = 'gray')
speedIncreaseMaxLabel = Label('Max', speedIncreaseMaxButton.centerX, speedIncreaseMaxButton.centerY, size = (1/60)*app.width, fill = 'gray')
speedLabel = Label(20, speedButtonHolder.centerX, speedButtonHolder.centerY, size = (1/40)*app.width, fill = "gray")

## Main Screen Settings ##

## Help Menu

helpBackground = Rect((1/10)*app.width, (1/10)*app.height, (4/5)*app.width, (4/5)*app.height, fill = 'grey', border = 'lightGray')
helpTitle = Label("Help Menu", helpBackground.centerX, helpBackground.top + (1/20)*app.height, size = (1/40)*app.width, fill = "white")
helpText0 = Label("After selecting color(s), and pressing go, click the screen anywhere. This will launch a firework towards that location.", helpBackground.left+2, helpBackground.top + (1/10)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText1 = Label("Screensaver Mode causes the program to act as a screensaver, picking places at random to launch fireworks.", helpBackground.left+2, helpBackground.top + (3/20)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText2 = Label("starry Night Mode causes remnants of the firework rocket to remain, over time creating a colorful starry night.", helpBackground.left+2, helpBackground.top + (1/5)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText3 = Label("Twinkle Mode can only be active alongside starry Night mode, and it will allow random twinkling of the firework remnants.", helpBackground.left+2, helpBackground.top + (1/4)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText4 = Label("You can reselect colors and settings at any time by pressing escape outside of the help menu.", helpBackground.left+2, helpBackground.top + (3/10)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText4a = Label("Returning to the menu will retain your stars if you were in starry night mode but delete fireworks that have been spawned or are exploding.", helpBackground.left+2, helpBackground.top + (7/20)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText5 = Label("You can clear your stars at any time by pressing 'c' or by returning to the settings screen and pressing the clear stars button.", helpBackground.left+2, helpBackground.top + (2/5)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText6 = Label("Disabling starry Night Mode will not remove your stars unless you additionally choose to clear them.", helpBackground.left+2, helpBackground.top + (9/20)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText7 = Label("Access this menu anytime by pressing 'h'. This will pause your game and retain your stars and active fireworks upon closing the menu.", helpBackground.left+2, helpBackground.top + (1/2)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText8 = Label("Firework launch frequency can be altered using the speed selector on the main page (top right), only while in screensaver mode", helpBackground.left+2, helpBackground.top + (11/20)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText8a = Label("Please note that frequency is measured in 'Fireworks per Minute,' ranges from 1 to 100, The dafault, 20, launches 1 firework every 3 seconds", helpBackground.left+2, helpBackground.top + (3/5)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
helpText9 = Label("Access to settings and program features are disabled in this menu. To close this menu, press escpape or the X in the top left of this window", helpBackground.left+2, helpBackground.top + (13/20)*app.height, size = (1/80)*app.width, fill = "white", align = "left")
closeHelpMenuButton = Rect(helpBackground.left+2, helpBackground.top+2, (1/40)*app.width, (1/40)*app.width, fill = "red")
closeHelpMenuLabel = Label("X", closeHelpMenuButton.centerX, closeHelpMenuButton.centerY, size = (1/40)*app.width)

##  Help Menu

## Creation of Groups and Lists

filteredFireworkColorList = [] 
flares = Group()
placedFireworks = Group() 
explodingFirework = Group()
stars = Group()
speedSwitches = Group(speedButtonHolder, speedDecreaseButton, speedDecreaseLabel, 
                      speedIncreaseButton, speedIncreaseLabel, speedLabel, speedDecrease10Button, speedIncrease10Button, speedIncrease10Label, 
                      speedDecrease10Label, speedDecreaseMaxButton, speedDecreaseMaxLabel, speedIncreaseMaxButton, speedIncreaseMaxLabel)
starterScreen = Group(colorButtons, title, instructions, goButton, goLabel, screenSaverButton, screenSaverLabel, starryNightButton, 
                      starryNightLabel, twinkleButton, twinkleLabel, clearStarsButton, clearStarsLabel, selectAllButton, selectAllLabel, 
                      deselectAllButton, deselectAllLabel, helpButton, helpLabel)
starterScreen.add(speedSwitches)
helpMenu = Group(helpBackground, helpTitle, closeHelpMenuButton, closeHelpMenuLabel, helpText0, helpText1, helpText2, helpText3, 
                 helpText4, helpText4a, helpText5, helpText6, helpText7, helpText8, helpText8a, helpText9)
helpMenu.visible = False

## Creation of Groups and Lists

## Screensaver Autoclick Speed Change Settings ##

def increase_speed_max():
    if(app.mode=="screensaver"):
        speedLabel.value = 100
        app.autoClickSpeed = (60*app.stepsPerSecond)/speedLabel.value

def decrease_speed_max():
    if(app.mode=="screensaver"):
        speedLabel.value = 1
        app.autoClickSpeed = (60*app.stepsPerSecond)/speedLabel.value

def increase_speed_10():
    if(app.mode =="screensaver"):
        if speedLabel.value <91:
            speedLabel.value = speedLabel.value + 10
        else:
            speedLabel.value = 100
        app.autoClickSpeed = (60*app.stepsPerSecond)/speedLabel.value

def decrease_speed_10():
    if(app.mode =="screensaver"):
        if speedLabel.value >10:
            speedLabel.value = speedLabel.value - 10
        else:
            speedLabel.value = 1
        app.autoClickSpeed = (60*app.stepsPerSecond)/speedLabel.value

def increase_speed():
    if(app.mode=="screensaver"):
        if speedLabel.value<100:
            speedLabel.value = speedLabel.value + 1
            app.autoClickSpeed = (60*app.stepsPerSecond)/speedLabel.value

def decrease_speed():
    if(app.mode=="screensaver"):
        if speedLabel.value>1:
            speedLabel.value = speedLabel.value - 1
            app.autoClickSpeed = (60*app.stepsPerSecond)/speedLabel.value
            
def check_speed(x,y):
    if(speedDecreaseButton.contains(x, y)):
        decrease_speed()
    if(speedIncreaseButton.contains(x, y)):
        increase_speed()
    if(speedDecrease10Button.contains(x, y)):
        decrease_speed_10()
    if(speedIncrease10Button.contains(x, y)):
        increase_speed_10()
    if(speedDecreaseMaxButton.contains(x, y)):
        decrease_speed_max()
    if(speedIncreaseMaxButton.contains(x, y)):
        increase_speed_max()

## Screensaver Autoclick Speed Change Settings ##

## Main Screen Settings Changes ##

def deselect_all_colors():
    for button in colorButtons:
        button.border = button.fill

def select_all_colors():
    for button in colorButtons:
        button.border = "darkGreen"
        
def color_activation_check(locX, locY):
    for button in colorButtons: 
        button.borderWidth = (1/200)*app.width
        if(button.contains(locX, locY)): 
            if(button.border == "darkGreen"): 
                button.border = button.fill 
            else: 
                button.border = "darkGreen"        
        
def toggle_screensaver_mode():
    if (app.mode == "manual"):
        app.mode = "screensaver"
        screenSaverButton.border = "white"
        screenSaverButton.borderWidth +=3
        screenSaverLabel.fill = "white"
        screenSaverLabel.value = "Screensaver Mode Active"
        for item in speedSwitches:
            if type(item) == Label:
                item.fill='white'
            else:
                item.border = "white"
    else:
        app.mode = "manual"
        screenSaverButton.border = "gray"
        screenSaverButton.borderWidth -=3
        screenSaverLabel.fill = "gray"
        screenSaverLabel.value = "Screensaver Mode Inactive"
        for item in speedSwitches:
            if type(item) == Label:
                item.fill='gray'
            else:
                item.border = 'gray'  
        
def toggle_starry_night_mode():
    if(app.starryNight == True):
        if(app.twinkleMode == True):
            toggle_twinkle()
        app.starryNight = False
        starryNightButton.border = "gray"
        starryNightButton.borderWidth -=3
        starryNightLabel.fill = "gray"
        starryNightLabel.value = "starry Night Mode Inactive"
    else:
        app.starryNight = True
        starryNightButton.border = "white"
        starryNightButton.borderWidth +=3
        starryNightLabel.fill = "white"
        starryNightLabel.value = "starry Night Mode Active"
        
def toggle_twinkle():
    if(app.starryNight == True):
        if(app.twinkleMode == True):
            app.twinkleMode = False
            twinkleButton.border = "gray"
            twinkleButton.borderWidth -=3
            twinkleLabel.fill = "gray"
            twinkleLabel.value = "Twinkle Mode Inactive"
        else:
            app.twinkleMode = True
            twinkleButton.border = "white"
            twinkleButton.borderWidth +=3
            twinkleLabel.fill = "white"
            twinkleLabel.value = "Twinkle Mode Active"       
        
def press_button(mouseX, mouseY): 
    filteredFireworkColorList.clear() 
    if(app.play == True):
        if(screenSaverButton.contains(mouseX, mouseY)):
            toggle_screensaver_mode()
        if(starryNightButton.contains(mouseX, mouseY)):
            toggle_starry_night_mode()
        if(twinkleButton.contains(mouseX, mouseY)):
            toggle_twinkle()
        if(clearStarsButton.contains(mouseX, mouseY)):
            stars.clear()
        if(selectAllButton.contains(mouseX, mouseY)):
            select_all_colors()
        if(deselectAllButton.contains(mouseX, mouseY)):
            deselect_all_colors()
        if(helpButton.contains(mouseX, mouseY)):
            spawn_help_menu()
        if(speedButtonHolder.contains(mouseX, mouseY)):
            check_speed(mouseX, mouseY)   
        if(goButton.contains(mouseX, mouseY)): 
            for button in colorButtons:
                if(button.border == "darkGreen"): 
                    filteredFireworkColorList.append(button.fill) 
            if(len(filteredFireworkColorList) == 0): 
                warningLabel.visible = True 
            else: 
                warningLabel.visible = False
                starterScreen.visible = False
                colorButtons.active = False
        else: 
            color_activation_check(mouseX, mouseY) 
    else:
        if(closeHelpMenuButton.contains(mouseX, mouseY)):
            despawn_help_menu()        


def despawn_help_menu():
    helpMenu.visible = False
    app.play = True

def spawn_help_menu():
    helpMenu.visible = True
    app.play = False  

## Main Screen Settings Changes ##

## Motion of Rockets, Fireworks, and Leftover Stars ##

def move_flare():
    for flare in flares:
        flare.centerY -= flareMove

def cause_twinkle():
    if(app.twinkleMode == True):
        for star in stars:
            if randrange(10) <=4:
                star.radius = 5

def un_twinkle():
    for star in stars:
        star.radius = 3
        
def expand_fireworks():
    for shine in explodingFirework:
        if(shine.opacity >0): 
            shine.radius +=(expansion) 
            if(shine.radius>=(maxFireworkSize)):
                shine.opacity -=5 
        else:
            explodingFirework.remove(shine)
                
## Motion of Rockets, Fireworks, and Leftover Stars ##

## Collision and Creation of Fireworks ##

def create_firework_shape(locX, locY, fireworkColor, vis, points, num, givenAngle, poly): 
    if (vis == 100): 
        radius = 1
        starPoints = points
        angle = givenAngle
        for i in range(len(allColors)):
            if fireworkColor == allColors[i]:
                fullInfoList[i] += 1
    else: 
        radius = 31 - 15*poly
        starPoints = randrange(5, 30) 
        angle = randrange(360)
    if(poly == 0):
        new = Star(locX, locY, radius, starPoints, fill = None, border = fireworkColor, opacity = vis, borderWidth = 5, dashes = True, rotateAngle = angle) 
        new.poly = 0
    else:
        new = RegularPolygon(locX, locY, radius, starPoints, fill = None, border = fireworkColor, opacity = vis, borderWidth = 5, dashes = True, rotateAngle = angle) 
        new.poly = 1
    new.num = num
    return new

def create_flare(locX, flareColor, num): 
    new = Circle (locX, app.height + 50, 4, fill = flareColor) 
    new.num = num
    return new

def create_firework_circle(x,y,borderColor, visibility, num, givenAngle):
    if(visibility == 100):
        radius = 1
    else:
        radius = 16
    new = Circle(x,y,radius, fill = None, border = borderColor, borderWidth = 5, opacity = visibility, dashes = True, rotateAngle = givenAngle)
    new.num = num
    return new        
    
def create_firework(x, y, borderColor, visibility, points, num, angle, poly):
    if points>=3:
        if(poly != None):
            star_or_poly = poly
        else:
            star_or_poly = randrange(2)
        return create_firework_shape(x, y, borderColor, visibility, points, num, angle, star_or_poly)
    else:
        return create_firework_circle(x,y, borderColor, visibility, num, angle)

def explosion_check(): 
    for flare in flares: 
        for explosion in placedFireworks: 
            if((flare.hitsShape(explosion) or (flare.centerY <= explosion.centerY)) and flare.num == explosion.num): 
                fullInfoList[9]+=1
                if (type(explosion)!= Circle):
                    explodingFirework.add(create_firework(explosion.centerX, explosion.centerY, explosion.border, 100, explosion.points, flare.num, explosion.rotateAngle, explosion.poly))
                else:
                    explodingFirework.add(create_firework_circle(explosion.centerX,explosion.centerY,explosion.border, 100, flare.num, explosion.rotateAngle))
                explodingFirework.add(explosion) 
                explosion.opacity = 100 
                if(app.starryNight == True):
                    stars.add(Circle(explosion.centerX, explosion.centerY, 3, fill = explosion.border))
                flares.remove(flare)
                
## Collision and Creation of Fireworks ##


def update_stats():
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")


def onKeyPress(key):
    if(key == "escape"):
        if(app.play == True):
            app.up = 1
            app.count = 1
            starterScreen.visible = True
            colorButtons.active = True
            flares.clear()
            placedFireworks.clear()
            explodingFirework.clear()
        else:
            despawn_help_menu()
    if(key == 'c' or key == 'C'):
        stars.clear()
    if(key == 'h' or key =='H'):
        spawn_help_menu()
            
def onMousePress(x, y): 
    if colorButtons.active == False:
        if(app.play == True):
            color = filteredFireworkColorList[randrange(len(filteredFireworkColorList))] 
            placedFireworks.add(create_firework(x, y, color, 0, randrange(2,6), app.count, randrange(360), None)) 
            flares.add(create_flare(x, color, app.count)) 
            app.count +=1
        else:
            if(closeHelpMenuButton.contains(x,y)):
                despawn_help_menu()
            
    else:
        press_button(x,y)  

def onStep(): 
    if(app.play == True):
        if(app.mode == "screensaver"):
            app.up +=1
        if (colorButtons.active == False):
            if(app.up >= app.autoClickSpeed):
                app.up = 0
                onMousePress(randrange(app.width), randrange(app.height))
            if(app.up% app.autoTwinkleSpeed == 0):
                app.timer = app.up
                cause_twinkle()
            if(app.up >= app.timer + app.autoUntwinkleSpeed):
                un_twinkle()
            move_flare() 
            explosion_check() 
            expand_fireworks() 
            update_stats()

fullInfoList[10]+=1
update_stats()


app.run()
