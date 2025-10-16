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
asteroidBase = Rect(-400, -400, app.width+800, app.height+800)
score = Label("Score: %09d" %app.score, 5, 20, size = 20, fill='white', align = 'left')
hiScore = Label("High Score: %09d" %hi, app.width-2, score.centerY, size =20, fill='white', align='right')

app.asteroidspeed = (1/80)*app.width
app.stepsPerSecond = 30
app.decel= 1/4
app.Yspeed = 0
app.Xspeed = 0
app.rotationSpeed = 0
app.timer = 0
app.multiplier = 1
app.asteroidTimer = app.stepsPerSecond*4.5
app.ballSpeed = 9 ## Player shots
app.shotSpeed = 25 ## Enemy shots
app.launchSpeed = 5
app.enemyLaunchSpeed = app.stepsPerSecond*3
app.timeSince = 0
app.saucerTime = app.stepsPerSecond*9
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

def update_high_score():
    if app.score>fullInfoList[2]:
        fullInfoList[2] = app.score
        hiScore.value = "High Score: %09d" %fullInfoList[2]
        update_stats()


def update_stats():
    gameInfo.seek(0)
    for i in range(len(fullInfoList)):
        gameInfo.write((str)(fullInfoList[i])+"\n")  
        
def shots_vs_asteroids():
    for shot in shots:
        for ast in asteroids:
            if(shot.hitsShape(ast) or ast.containsShape(shot)):
                decrease_health_asteroid(ast, False)
                shots.remove(shot)


def get_speed(speed):
    if(speed<0):
        return speed + app.decel
    elif(speed>0):
        return speed - app.decel
    return 0

def spawn_balls(x,y,angle):
    new = Circle(x,y,4, fill='white', rotateAngle = angle)
    new.next = getPointInDir(x,y,angle,app.ballSpeed)
    balls.add(new)
    fullInfoList[0]+=1
    
def spawn_shots(x,y,angle):
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
    shots.add(new, new2, new3, new4, new5)
    
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
    return new   

def move_asteroids():
    for ast in asteroids:
        if(not(asteroidBase.containsShape(ast))):
            asteroids.remove(ast)
        ast.centerX, ast.centerY = ast.next
        ast.next = getPointInDir(ast.centerX, ast.centerY, ast.rotateAngle, ast.speed)
    
def create_saucer(left, top, right, bottom):
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
    for shot in shots:
        if(shot.hitsShape(ship)):
            shots.remove(shot)
            decrease_health_ship()
    
def spawn_enemy_saucer():
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
    if(app.enemy == True and app.timer%app.enemyLaunchSpeed == 0):
        spawn_shots(saucer.centerX, saucer.centerY, angleTo(saucer.centerX, saucer.centerY, ship.centerX, ship.centerY))
    
    
def move_enemy_shots():
    for shot in shots:
        shot.centerX, shot.centerY = shot.next
        shot.next = getPointInDir(shot.centerX,shot.centerY,shot.rotateAngle, app.shotSpeed)
        if(not(screen.containsShape(shot))):
            shots.remove(shot)
    
    
def decrease_health_saucer(saucer):
    if saucer.health<=1:
        create_scores(saucer.centerX, saucer.centerY, saucer.score)
        app.score+=saucer.score
        explosion.add(Star(saucer.centerX, saucer.centerY, 12, 12, fill = None, border = 'white'))
        explosion.add(Star(saucer.centerX, saucer.centerY, 8, 12, fill = None, border = 'white'))
        explosion.add(Star(saucer.centerX, saucer.centerY, 4, 12, fill = None, border = 'white'))
        saucers.remove(saucer)
        if(len(saucers) ==0):
            app.enemy = False
    else:
        saucer.health-=1
    
def balls_vs_enemy():
    for saucer in saucers:
        for ball in balls:
            if(saucer.hitsShape(ball)):
                explosion.add(Circle(ball.centerX, ball.centerY, 3, fill=None, border = 'white'))
                balls.remove(ball)
                fullInfoList[1]+=1
                decrease_health_saucer(saucer)
    
    
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
            asteroids.add(massive(randX, randY))
        
def reset():
    app.timer = 0
    app.saucerSpawn = 0
    shots.clear()
    asteroids.clear()
    balls.clear()
    saucers.clear()
    visibleScores.clear()
    explosion.clear()
    gameOver.clear()
    app.score = 0
    app.play = True
    fullInfoList[3]+=1
    score.value = "Score: %09d" %app.score
    ship.centerX = app.width/2
    ship.centerY = app.height/2
    ship.rotateAngle = 0
    app.Xspeed = 0
    app.Yspeed = 0
    app.multiplier = 1
    ship.health = 3
    health.value = "Health: %1d" %ship.health
    app.enemy = False
    update_stats()

    
    
    
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
        update_stats()
        ship.health = 0
        app.play = False
        offer_replay()
    else:
        ship.health-=1
    health.value = "Health %1d" %ship.health

def decrease_health_asteroid(ast, scoring):
    if ast.health<=1:
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
    gameOver.add(Rect(app.width/2, app.height/2, app.width, app.height, align = 'center', fill=None, border = 'white'))  
    gameOver.add(Label("Game Over", app.width/2, app.height/2-50, fill='white', size = app.width/20)) 
    gameOver.add(Label("Press Enter To Play Again", app.width/2, app.height/2 + 50, fill='white', size = app.width/30))   
        
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
                decrease_health_asteroid(ast, True)
                

def asteroids_vs_space():
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
    ship_vs_asteroids()
    balls_vs_asteroids()
    asteroids_vs_space()
    balls_vs_enemy()
    shots_vs_ship()
    shots_vs_asteroids()


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
        app.timer+=1
        if(app.timer%(app.stepsPerSecond*app.multiplier*60) == 1):
            for i in range(app.multiplier):
                if(i<=3):
                    spawn_enemy_saucer()
                    app.saucerSpawn= 0
            app.multiplier += 1
        if(app.timeSince>0):
            app.timeSince -=1
        app.Xspeed = get_speed(app.Xspeed)
        ship.centerX+=app.Xspeed
        app.Yspeed = get_speed(app.Yspeed)
        ship.centerY+=app.Yspeed
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
        
def onKeyPress(key):
    if(key=='enter'):
        if(app.play == False):
            reset()
        

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
            
score.toFront()
hiScore.toFront()
fullInfoList[4]+=1
fullInfoList[3]+=1     
    

app.run()