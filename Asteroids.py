from cmu_graphics import *
import tkinter as tk
import random
import math

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

app.width = width
app.height = height


gameInfo = open("Files/AsteroidsStats.txt", "r+")
fullInfoList = [] 
for thing in gameInfo:
    thing = thing.strip()
    if thing != '':
        fullInfoList.append((int)(thing))
hi = fullInfoList[2]

app.score = 0
app.generalSpeed = 8
app.play = True
screen = Rect(0,0,app.width, app.height)
asteroidBase = Rect(-400, -400, app.width+400, app.height+400)
score = Label("Score: %09d" %app.score, 5, 20, size = 20, fill='white', align = 'left')
hiScore = Label("High Score: %09d" %hi, app.width-2, score.centerY, size =20, fill='white', align='right')

app.asteroidspeed = (1/80)*app.width
app.stepsPerSecond = 30
app.decel= 1/4
app.Yspeed = 0
app.Xspeed = 0
app.rotationSpeed = 0
app.timer = 0
app.asteroidTimer = app.stepsPerSecond*6
app.ballSpeed = 10
app.launchSpeed = 5
app.timeSince = 0
app.asteroidSpeed = 5
head = Circle(app.width/2, app.height/2,7, fill = 'white')
ship = Group(head, Polygon(app.width/2,app.height/2, (81/160)*app.width,(21/40)*app.height, app.width/2,(81/160)*app.height, (79/160)*app.width,(21/40)*app.height, app.width/2,app.height/2, fill='white'))
ship.health = 3
health = Label("Health: %1d" %ship.health, app.width/2, score.centerY, fill='white', size = 20)
balls = Group()
asteroids = Group()
visibleScores = Group()
explosion = Group()

def update_high_score():
    if app.score>fullInfoList[0]:
        fullInfoList[2] = app.score
        hiScore.value = "High Score: %09d" %fullInfoList[2]


def update_stats():
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")  


def get_speed(speed):
    if(speed<0):
        return speed + app.decel
    elif(speed>0):
        return speed - app.decel
    return 0

def spawn_balls(x,y,angle):
    new = Circle(x,y,3, fill='white', rotateAngle = angle)
    new.next = getPointInDir(x,y,angle,app.ballSpeed)
    balls.add(new)
    fullInfoList[0]+=1
    
def create_scores(x,y,val):
    visibleScores.add(Label("+ %3d" %val, x, y, fill=None, border = 'white', size = 14))
    
def remove_scores():
    for score in visibleScores:
        if(score.opacity<=0):
            visibleScores.remove(score)
        else:
            score.opacity-=5
            score.size+=2
    
def small(x, y):
    r = angleTo(x, y, randrange((int)(app.width/4),(int)((3/4)*app.width)), randrange((int)(app.height/4),(int)((3/4)*app.height)))
    new = Polygon(10, 15, 24, 8, 34, 10, 31, 21, 41, 25, 38, 35, 30, 35, 25, 42, 13, 36, 8, 26, 10, 15, fill = None, border = 'white', opacity = 0)
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
    return new

def med(x,y):
    r = angleTo(x, y, randrange((int)(app.width/4),(int)((3/4)*app.width)), randrange((int)(app.height/4),(int)((3/4)*app.height)))
    new = Polygon(21, 30, 48, 16, 68, 21, 62, 42, 82, 50, 76, 70, 60, 70, 50, 84, 26, 72, 15, 52, 21, 30, fill = None, border = 'white', opacity = 0)
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
    return new

def big(x,y):
    r = angleTo(x, y, randrange((int)(app.width/4),(int)((3/4)*app.width)), randrange((int)(app.height/4),(int)((3/4)*app.height)))
    new = Polygon(42, 60, 96, 32, 134, 42, 124, 84, 164, 100, 154, 140, 120, 140, 102, 168, 52, 144, 30, 104, 42, 60, fill = None, border = 'white', opacity = 0)
    new.centerX = x
    new.centerY = y
    new.opacity = 100
    new.score = 75
    new.rotateAngle = r
    new.size = "big"
    new.health = 3
    new.hasHit = False
    new.speed = app.asteroidSpeed*(3/4)
    new.next = getPointInDir(new.centerX, new.centerY, r, new.speed)
    return new    

def massive(x,y):
    r = angleTo(x, y, randrange((int)(app.width/4),(int)((3/4)*app.width)), randrange((int)(app.height/4),(int)((3/4)*app.height)))    
    new = Polygon(84, 120, 192, 64, 268, 84, 248, 168, 328, 200, 308, 280, 240, 280, 204, 336, 104, 288, 60, 208, 84, 120, fill = None, border = 'white', opacity = 0)
    new.centerX = x
    new.centerY = y
    new.opacity = 100
    new.score = 100
    new.rotateAngle = r
    new.size = "massive"
    new.health = 4
    new.hasHit = False
    new.speed = app.asteroidSpeed/2
    new.next = getPointInDir(new.centerX, new.centerY, r, new.speed)
    return new   

def move_asteroids():
    for ast in asteroids:
        if(not(asteroidBase.containsShape(ast))):
            asteroids.remove(ast)
        ast.centerX, ast.centerY = ast.next
        ast.next = getPointInDir(ast.centerX, ast.centerY, ast.rotateAngle, ast.speed)
    
    
    
def spawn_asteroids(num):
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
            if(randX<=0):
                randX = -400
            if(randX>=app.width):
                randX = app.width+400
            if(randY<=0):
                randY = -400
            if(randY>=app.height):
                randY = app.height+400
            asteroids.add(massive(randX, randY))
        
    
def move_balls():
    for ball in balls:
        ball.centerX, ball.centerY = ball.next
        ball.next = getPointInDir(ball.centerX,ball.centerY,ball.rotateAngle, app.ballSpeed)
        if(not(screen.containsShape(ball))):
            balls.remove(ball)

def ship_vs_asteroids():
    for ast in asteroids:
        if(ast.hitsShape(ship) and ast.hasHit == False):
            decrease_health_ship()
            ast.hasHit = True

def decrease_health_ship():
    if ship.health <=1:
        ship.health = 0
        app.play = False
        update_stats()
    else:
        ship.health-=1
    health.value = "Health %1d" %ship.health

def decrease_health_asteroid(ast):
    if ast.health<=1:
        create_scores(ast.centerX, ast.centerY, ast.score)
        if(ast.size == 'massive'):
            asteroids.add(big(ast.centerX, ast.centerY))
            asteroids.add(big(ast.centerX, ast.centerY))
        if(ast.size == 'big'):
            asteroids.add(med(ast.centerX, ast.centerY))
            asteroids.add(med(ast.centerX, ast.centerY))
        if(ast.size == 'med'):
            asteroids.add(small(ast.centerX, ast.centerY))
            asteroids.add(small(ast.centerX, ast.centerY))
        app.score+=ast.score
        asteroids.remove(ast)
    else:
        ast.health-=1
        
def blow_up_balls():
    for ball in explosion:
        if ball.opacity<=0:
            explosion.remove(ball)
        else:
            ball.opacity -=10
            ball.radius+=1
    
    
def balls_vs_asteroids():
    for ast in asteroids:
        for ball in balls:
            if(ast.hitsShape(ball)):
                explosion.add(Circle(ball.centerX, ball.centerY, 3, fill=None, border = 'white'))
                balls.remove(ball)
                fullInfoList[1]+=1
                decrease_health_asteroid(ast)
                

def asteroids_vs_space():
    for ast in asteroids:
        if(ast.centerX>asteroidBase.right):
            asteroids.remove(ast)
        elif(ast.centerX< asteroidBase.left):
            asteroids.remove(ast)
        elif(ast.centerY<asteroidBase.top):
            asteroids.remove(ast)        
        elif(ast.centerY>asteroidBase.bottom):
            asteroids.remove(ast)
            
def hit_detection():
    ship_vs_asteroids()
    balls_vs_asteroids()
    asteroids_vs_space()


def onKeyHold(keys):
    if('a' in keys or "A" in keys):
        app.Xspeed = -app.generalSpeed 
    if('w' in keys or "W" in keys):
        app.Yspeed = -app.generalSpeed
    if('d' in keys or "D" in keys):
        app.Xspeed = app.generalSpeed 
    if('s' in keys or "S" in keys):
        app.Yspeed = app.generalSpeed
    if('left' in keys):
        app.rotationSpeed = -app.generalSpeed
    if('right' in keys):
        app.rotationSpeed = app.generalSpeed
    if('space' in keys):
        if(app.timeSince == 0):
            spawn_balls(head.centerX, head.centerY, ship.rotateAngle%360)
            app.timeSince = app.launchSpeed
        
def onStep():
    if(app.play==True):
        if(app.timeSince>0):
            app.timeSince -=1
        app.timer+=1
        app.Xspeed = get_speed(app.Xspeed)
        ship.centerX+=app.Xspeed
        app.Yspeed = get_speed(app.Yspeed)
        ship.centerY+=app.Yspeed
        app.rotationSpeed = get_speed(app.rotationSpeed)
        ship.rotateAngle+=app.rotationSpeed
        app.score+=1
        score.value = "Score: %09d" %app.score
        if(app.timer%app.asteroidTimer==0):
            spawn_asteroids(randrange(4,10))
        wrap_around()
        move_balls()
        move_asteroids()
        hit_detection()
        remove_scores()
        blow_up_balls()
        update_high_score()
        update_stats()
        

def wrap_around():
    if not(screen.containsShape(ship)):
        if(ship.centerX>=app.width):
            ship.centerX = 0
        elif(ship.centerX<0):
            ship.centerX = app.width-1
        if(ship.centerY<0):
            ship.centerY = app.height-1
        elif(ship.centerY>app.height):
            ship.centerY = 0
            
fullInfoList[4]+=1
fullInfoList[3]+=1     
    

app.run()