from cmu_graphics import *
import tkinter as tk
import random
import math

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.wm_attributes('-fullscreen', True) ## This line is a workaround for macOs devices with no ill effects for Windows users. It forces a new window to open in fullscreen and focus on it, before destroying it on the next line. The main canvas is then created and players will see it. Players must still maximise this window manually however
root.destroy()
fruits = Group()
powerups = Group()
bombs = Group()
app.width = width
app.height = height
app.stepsPerSecond = 30
app.setMaxShapeCount(10000000)
app.timer = 0
app.num = 0
app.score = 0
app.startingYspeed = 35
app.powerUpTimer = app.stepsPerSecond*randrange(20)
app.bombTimer = app.stepsPerSecond*randrange(60)
app.mult = 1
app.frozen = False
app.freezeTimer = app.stepsPerSecond * 3
app.doubleTimer = app.stepsPerSecond * 5
splits = Group()
app.bombs = 0
app.doubled = False

doubleTime = Arc(20, 20, 40, 40, 0, 360, fill='lime', opacity = 0)
freezeTime = Arc(20, 70, 40, 40, 0, 360, fill='cyan', opacity = 0)

background = Image("Images/FruitNinjaBackground.png", 0,0) ### Give proper credit
background.width = app.width
background.height = app.height

scoreLabel = Label("%d" %app.score, app.width/2, app.height/10, fill='white', bold = True, border = 'black', size = 50)

particles = []
partLines = []
deleteShapes = Group()
app.angle = None
head = RegularPolygon(-500,-500,12, 3, fill='white', rotateAngle = 90, visible = False)
app.lastX, app.lastY = 0,0


## The above lines import the image of the background and stretch it to fit the window

def update_score():
    scoreLabel.value = "%d" %app.score
    
def remove_particles():
    for part in particles:
        part.life-=1
        if(part.life<=0):
            particles.remove(part)
            deleteShapes.add(part)
    for line in partLines:
        line.life-=1
        if(line.life<=0):
            partLines.remove(line)
            deleteShapes.add(line)    

def particles_helper():
    for i in range(len(particles)-1):
        if(particles[i].num == particles[i+1].num):
            new = Line(particles[i].centerX, particles[i].centerY, particles[i+1].centerX, particles[i+1].centerY, lineWidth = 12, fill='white')
            new.life = particles[i].life
            partLines.append(new)
            

def decrease_timers(timer, maxSteps):
    if(timer.sweepAngle>5):
        timer.sweepAngle -= 360/maxSteps
    else: 
        timer.sweepAngle = 360
        timer.opacity = 0

def spawn_particle_effects(x,y):
    new = Circle(x,y, 5, fill = None)
    new.life = app.stepsPerSecond*(1/3)
    new.num = app.num
    particles.append(new)
    particles_helper()
    
    
def move_fruit(type):
    for fruit in type:
        fruit.Yspeed -=0.55
        fruit.centerX += fruit.Xspeed
        fruit.centerY -= fruit.Yspeed
        fruit.rotateAngle+=fruit.Xspeed/2
        fruit.hitbox.centerX, fruit.hitbox.centerY = fruit.centerX, fruit.centerY
        fruit.hitbox.rotateAngle = fruit.rotateAngle
        if(fruit.Yspeed<0 and fruit.top>=app.height):
            type.remove(fruit)

def move_splits():
    for half in splits:
        half.centerX += half.Xspeed
        half.centerY -= half.Yspeed
        half.Yspeed -= 0.3
        half.rotateAngle += half.Xspeed/2
        if(half.top> app.height):
            splits.remove(half)

def onMousePress(x,y):
    head.centerX, head.centerY,  = x,y
    app.num +=1
    app.lastX, app.lastY = x,y

def slice_it(fruit):
    for i in range(len(fruit_names)):
        if fruit.name == fruit_names[i]:
            new = Image(fruit_splits[(i*2)], fruit.centerX +randrange(-10, 11, 1), fruit.centerY + randrange(-20, 0, 1))
            new2 = Image(fruit_splits[(i*2)+1], fruit.centerX +randrange(-10, 11, 1), fruit.centerY + randrange(0, 10, 1))
    for i in range(len(powerups_names)):
        if fruit.name == powerups_names[i]:
            new = Image(powerupSplits[(i*2)], fruit.centerX +randrange(-10, 11, 1), fruit.centerY + randrange(-20, 0, 1))
            new2 = Image(powerupSplits[(i*2)+1], fruit.centerX +randrange(-10, 11, 1), fruit.centerY + randrange(0, 10, 1))
            if(i==0):
                new.width/=3
                new.height/=3
                new2.width/=3
                new2.height/=3
    for i in range(len(bomb_names)):
        if fruit.name == bomb_names[i]:
            new = Image(bomb_splits[(i*2)], fruit.centerX +randrange(-10, 11, 1), fruit.centerY + randrange(-20, 0, 1))
            new2 = Image(bomb_splits[(i*2)+1], fruit.centerX +randrange(-10, 11, 1), fruit.centerY + randrange(0, 10, 1))
            
    new.Xspeed = randrange(-5, 0)
    new2.Xspeed = randrange(6)
    new.Yspeed = fruit.Yspeed + randrange(-2,3)
    new2.Yspeed = fruit.Yspeed + randrange(-2,3)
    new.rotateAngle = fruit.rotateAngle
    new2.rotateAngle = fruit.rotateAngle
    splits.add(new, new2)

            
def hit_bomb():
    app.bombs +=1

def fruit_slicing(type):
    for fruit in type:
        for line in partLines:
            if(fruit.hitbox.hitsShape(line) and line.life>app.stepsPerSecond*(1/4) and fruit.sliced == False):
                fruit.sliced = True
                app.score+=fruit.score * app.mult
                if(fruit.name == 'x2'):
                    app.mult = 2
                    app.doubled = True
                    app.doubleTimer = app.stepsPerSecond * 5
                    doubleTime.opacity = 100
                if(fruit.name == 'freeze'):
                    app.frozen = True
                    app.freezeTimer = app.stepsPerSecond * 3
                    freezeTime.opacity = 100
                if(fruit.name == 'bomb'):
                    hit_bomb()
                deleteShapes.add(fruit.hitbox)
                type.remove(fruit)
                slice_it(fruit)
                

def hit_detection():
    fruit_slicing(fruits)
    fruit_slicing(powerups)
    fruit_slicing(bombs)

def onMouseDrag(x,y):
    app.angle = angleTo(app.lastX, app.lastY, x,y)
    head.centerX, head.centerY = x,y
    head.rotateAngle = app.angle
    app.lastX, app.lastY = x,y
    spawn_particle_effects(x,y)
    
    
def onMouseRelease(x,y):
    app.angle = 90
    head.centerX, head.centerY = x,y
    
def onStep():
    if(app.frozen == False):
        move_fruit(fruits)
        move_fruit(bombs)
        move_fruit(powerups)
        if(app.timer%app.stepsPerSecond*4 == 0):
            spawn_fruit()
        if(app.powerUpTimer <=0):
            app.powerUpTimer = randrange(app.stepsPerSecond*20)
            spawn_powerup()
        if(app.bombTimer <=0):
            app.bombTimer = randrange(app.stepsPerSecond*60)
            spawn_bomb()
    else:
        decrease_timers(freezeTime, app.stepsPerSecond*3)
    if(app.freezeTimer <=0):
        app.frozen = False
    if(app.doubleTimer <=0):
        app.doubled = False
        app.mult = 1
    if(app.doubled == True):
        decrease_timers(doubleTime, app.stepsPerSecond * 3)
    deleteShapes.clear()
    remove_particles()
    app.timer += 1
    app.powerUpTimer -=1
    app.bombTimer -=1
    app.freezeTimer -=1
    app.doubleTimer-=1
    hit_detection()
    move_splits()
    update_score()
    
def spawn_fruit():
    howMany = randrange(1,9)
    for i in range(howMany):
        rndSpeed = randrange(-5, 6, 1)
        pick = randrange(len(fruit_urls))
        fruit = Image(fruit_urls[pick], randrange(app.width), randrange((int)(app.height+100), (int)(app.height+300)))
        fruit.Yspeed = app.startingYspeed + rndSpeed
        fruit.startX = fruit.centerX
        fruit.targetX = randrange((app.width//10), 9*(app.width//10))
        fruit.Xspeed = (fruit.targetX - fruit.centerX)/ 180
        fruit.hitbox = Polygon(0,0,-1, -1,-2,0) ## Have to create a random useless polygon to replace
        fruit.hitbox.pointList = fruit_hitboxes[pick].pointList
        fruit.hitbox.centerX, fruit.hitbox.centerY = fruit.centerX, fruit.centerY
        fruit.hitbox.rotateAngle = fruit.rotateAngle
        fruit.hitbox.toBack()
        fruit.sliced = False
        fruit.score = 1
        fruit.name = fruit_names[pick]
        if fruit.targetX<= fruit.centerX:
            fruit.dir = 'left' 
        else:
            fruit.dir = 'right'
        fruits.add(fruit)

fruit_splits = ["Images/Splits/Banana1.png", "Images/Splits/Banana2.png", "Images/Splits/Cherry1.png", "Images/Splits/Cherry2.png","Images/Splits/Coconut1.png", "Images/Splits/Coconut2.png", "Images/Splits/Dragonfruit1.png", "Images/Splits/Dragonfruit2.png", "Images/Splits/Greenapple1.png", "Images/Splits/Greenapple2.png", "Images/Splits/Kiwi1.png", "Images/Splits/Kiwi2.png", "Images/Splits/Lemon1.png", "Images/Splits/Lemon2.png", "Images/Splits/Lime1.png", "Images/Splits/Lime2.png", "Images/Splits/Mango1.png", "Images/Splits/Mango2.png", "Images/Splits/Orange1.png", "Images/Splits/Orange2.png", "Images/Splits/Passionfruit1.png", "Images/Splits/Passionfruit2.png", "Images/Splits/Peach1.png", "Images/Splits/Peach2.png", "Images/Splits/Pear1.png", "Images/Splits/Pear2.png", "Images/Splits/Pineapple1.png", "Images/Splits/Pineapple2.png", "Images/Splits/Plum1.png", "Images/Splits/Plum2.png", "Images/Splits/Pomegranate1.png", "Images/Splits/Pomegranate2.png", "Images/Splits/Red_Apple1.png", "Images/Splits/Red_Apple2.png", "Images/Splits/Strawberry1.png", "Images/Splits/Strawberry2.png", "Images/Splits/Tomato1.png", "Images/Splits/Tomato2.png", "Images/Splits/Watermelon1.png", "Images/Splits/Watermelon2.png"]
fruit_urls = ["Images/Banana.png","Images/Cherry.png","Images/Coconut.png","Images/Dragonfruit.png","Images/Greenapple.png","Images/Kiwi.png","Images/Lemon.png","Images/Lime.png","Images/Mango.png","Images/Orange.png","Images/Passionfruit.png","Images/Peach.png","Images/Pear.png","Images/Pineapple.png","Images/Plum.png","Images/Pomegranate.png","Images/Red_Apple.png","Images/Strawberry.png","Images/Tomato.png","Images/Watermelon.png"]
fruit_hitboxes = []
cut_fruit_urls = []
powerupSplits = ["Images/Splits/Score_2x_Banana1.png", "Images/Splits/Score_2x_Banana2.png" ,"Images/Splits/Freeze_Banana2.png", "Images/Splits/Freeze_Banana1.png"]
powerups_urls = ["Images/Score_2x_Banana.png", "Images/Freeze_Banana.png"]
powerups_hitboxes = []
bomb_splits = ["Images/Splits/Bomb1.png", "Images/Splits/Bomb2.png", "Images/Splits/bomb101.png", "Images/Splits/bomb102.png"]
bomb_urls = ["Images/Bomb.png", "Images/bomb10.png"]
bomb_hitboxes = []
fruit_names = ['Banana', 'Cherry', 'Coconut', 'Dragonfruit', 'Greenapple', 'Kiwi', 'Lemon', 'Lime', 'Mango', 'Orange', 'Passionfruit', 'Peach', 'Pear', 'Pineapple', 'Plum', 'Pomegranate', 'Red_Apple', 'Strawberry', 'Tomato', 'Watermelon']
powerups_names = ['x2', 'freeze']  
bomb_names=['bomb', '-10']  

splits.toFront()
fruits.toFront()
bombs.toFront()
powerups.toFront()
doubleTime.toFront()
freezeTime.toFront()

def spawn_powerup():
    pick = randrange(len(powerups_urls))
    new = Image(powerups_urls[pick], randrange(app.width), randrange((int)(app.height+100), (int)(app.height+300)))
    if(pick == 0):
        new.width /=3
        new.height/=3
        new.name = 'x2'
        new.score = 10
    else:
        new.name = 'freeze'
        new.score = 10
    new.Yspeed = app.startingYspeed
    new.startX = new.centerX
    new.targetX = randrange((app.width//10), 9*(app.width//10))
    new.Xspeed = (new.targetX - new.centerX)/ 180
    new.hitbox = powerups_hitboxes[pick]
    new.hitbox.centerX, new.hitbox.centerY = new.centerX, new.centerY
    new.hitbox.rotateAngle = new.rotateAngle
    new.hitbox.toBack()
    new.sliced = False
    if new.targetX<= new.centerX:
        new.dir = 'left' 
    else:
        new.dir = 'right'
    powerups.add(new)
    
def spawn_bomb():
    pick = randrange(len(bomb_urls))
    new = Image(bomb_urls[pick], randrange(app.width), randrange((int)(app.height+100), (int)(app.height+300)))
    if pick == 0:
        new.name = 'bomb'
        new.score = 0
    else:
        new.name = '-10'
        new.score = -10
    new.Yspeed = app.startingYspeed
    new.startX = new.centerX
    new.targetX = randrange((app.width//10), 9*(app.width//10))
    new.Xspeed = (new.targetX - new.centerX)/ 180
    new.hitbox = bomb_hitboxes[pick]
    new.hitbox.centerX, new.hitbox.centerY = new.centerX, new.centerY
    new.hitbox.rotateAngle = new.rotateAngle
    new.hitbox.toBack()
    new.sliced = False
    if new.targetX<= new.centerX:
        new.dir = 'left' 
    else:
        new.dir = 'right'
    bombs.add(new)


fruit_hitboxes.append(Polygon(264, 202, 273, 201, 277, 209, 279, 215, 282, 226, 284, 228, 283, 263, 272, 286, 258, 303, 244, 316, 225, 325, 201, 324, 201, 315, 226, 277, 251, 236, 263, 214, 263, 200))
fruit_hitboxes.append(Polygon(216, 229, 234, 206, 245, 200, 275, 201, 275, 211, 270, 212, 257, 221, 246, 232, 241, 241, 248, 246, 259, 259, 263, 269, 258, 290, 253, 302, 241, 310, 222, 310, 206, 299, 199, 286, 200, 264, 205, 256, 215, 245, 223, 243, 234, 241, 239, 233, 246, 223, 234, 227, 226, 227))
fruit_hitboxes.append(Polygon(249, 203, 276, 203, 287, 207, 299, 216, 309, 227, 312, 234, 315, 246, 318, 246, 317, 269, 310, 284, 301, 297, 288, 306, 273, 312, 271, 315, 245, 313, 226, 308, 211, 296, 203, 281, 200, 268, 202, 253, 205, 238, 211, 227, 218, 221, 228, 212, 240, 205, 249, 201, 246, 203))
fruit_hitboxes.append(Polygon(202, 325, 207, 315, 210, 296, 209, 280, 213, 291, 233, 249, 235, 244, 237, 225, 237, 220, 247, 236, 251, 236, 256, 224, 254, 207, 262, 217, 255, 248, 255, 250, 274, 244, 279, 241, 283, 240, 293, 225, 295, 214, 297, 226, 303, 235, 347, 209, 351, 223, 367, 210, 355, 257, 385, 247, 365, 264, 354, 285, 358, 298, 362, 297, 369, 281, 374, 298, 367, 303, 368, 310, 413, 302, 379, 321, 355, 349, 332, 380, 330, 384, 352, 388, 359, 391, 351, 390, 330, 394, 284, 409, 257, 406, 238, 407, 228, 394, 211, 372, 202, 330))
fruit_hitboxes.append(Polygon(236, 307, 227, 304, 217, 291, 205, 271, 201, 262, 201, 246, 212, 229, 219, 222, 235, 216, 244, 214, 247, 214, 252, 203, 255, 204, 253, 212, 254, 216, 263, 215, 278, 220, 288, 227, 292, 232, 296, 240, 297, 251, 298, 265, 295, 273, 290, 283, 284, 292, 277, 302, 267, 308, 260, 308, 238, 307))
fruit_hitboxes.append(Polygon(230, 202, 250, 202, 259, 206, 268, 211, 275, 220, 281, 230, 281, 247, 281, 260, 275, 273, 263, 283, 252, 287, 231, 287, 212, 279, 206, 267, 201, 262, 201, 238, 206, 222, 214, 212, 223, 206, 230, 201))
fruit_hitboxes.append(Polygon(201, 276, 201, 267, 204, 261, 204, 246, 212, 230, 221, 219, 235, 209, 254, 203, 277, 202, 284, 203, 297, 211, 305, 211, 309, 217, 309, 227, 307, 246, 302, 255, 296, 268, 273, 283, 269, 283, 259, 289, 229, 290, 217, 283, 211, 279, 202, 279))
fruit_hitboxes.append(Polygon(204, 226, 212, 216, 220, 208, 233, 202, 248, 203, 259, 207, 274, 219, 280, 226, 282, 241, 284, 256, 275, 269, 265, 278, 252, 285, 235, 285, 220, 278, 210, 270, 202, 255, 202, 239, 204, 229, 216, 214))
fruit_hitboxes.append(Polygon(202, 256, 201, 231, 208, 218, 219, 208, 228, 204, 237, 202, 254, 202, 259, 202, 274, 212, 281, 216, 298, 241, 297, 249, 291, 258, 283, 270, 275, 277, 263, 281, 261, 283, 231, 282, 217, 276, 210, 270, 203, 260, 201, 257))
fruit_hitboxes.append(Polygon(221, 209, 239, 203, 262, 202, 270, 205, 279, 211, 284, 217, 295, 232, 296, 266, 282, 288, 268, 294, 257, 300, 240, 300, 231, 297, 218, 292, 211, 282, 206, 274, 202, 269, 202, 256, 201, 244, 202, 236, 207, 230, 211, 219, 218, 212, 221, 210))
fruit_hitboxes.append(Polygon(238, 217, 239, 201, 244, 201, 243, 208, 244, 216, 264, 222, 272, 232, 276, 239, 278, 249, 278, 263, 276, 272, 276, 278, 266, 287, 259, 292, 247, 295, 233, 294, 219, 290, 208, 281, 202, 272, 201, 255, 202, 247, 204, 236, 209, 231, 216, 224, 222, 220, 229, 218, 237, 217))
fruit_hitboxes.append(Polygon(231, 282, 211, 265, 202, 250, 202, 227, 204, 222, 209, 210, 221, 201, 239, 200, 246, 202, 254, 205, 259, 200, 262, 202, 261, 206, 274, 212, 283, 217, 290, 224, 293, 234, 293, 249, 290, 259, 286, 267, 279, 272, 267, 280, 252, 281, 241, 281, 231, 281, 222, 272, 210, 262, 205, 254, 201, 247, 203, 228, 208, 213, 221, 201))
fruit_hitboxes.append(Polygon(251, 230, 253, 201, 258, 202, 254, 231, 265, 235, 267, 241, 271, 257, 278, 272, 285, 284, 286, 301, 286, 316, 276, 325, 269, 331, 254, 332, 232, 331, 212, 326, 202, 312, 202, 289, 206, 276, 211, 270, 221, 260, 227, 249, 236, 240, 240, 232, 249, 230))
fruit_hitboxes.append(Polygon(256, 267, 249, 219, 268, 250, 274, 238, 271, 204, 281, 220, 283, 235, 296, 208, 296, 237, 324, 224, 322, 231, 330, 227, 313, 247, 322, 244, 320, 247, 323, 248, 316, 255, 338, 257, 306, 269, 291, 285, 298, 294, 300, 301, 300, 316, 294, 335, 281, 354, 274, 364, 258, 378, 234, 377, 201, 353, 202, 328, 216, 290, 221, 283, 243, 270, 255, 268))
fruit_hitboxes.append(Polygon(252, 229, 255, 215, 258, 202, 264, 201, 263, 214, 258, 232, 282, 245, 285, 255, 283, 291, 262, 320, 234, 321, 206, 306, 202, 293, 202, 276, 207, 258, 214, 243, 225, 233, 238, 231, 250, 229))
fruit_hitboxes.append(Polygon(344, 219, 353, 202, 367, 211, 375, 228, 396, 236, 411, 248, 401, 250, 389, 257, 398, 265, 397, 273, 402, 275, 408, 285, 411, 301, 411, 325, 416, 339, 412, 353, 406, 368, 398, 381, 390, 393, 382, 401, 369, 412, 361, 413, 314, 427, 308, 425, 279, 421, 261, 413, 242, 400, 223, 382, 210, 360, 206, 334, 205, 320, 202, 307, 209, 286, 214, 272, 221, 259, 233, 246, 245, 235, 266, 225, 283, 220, 301, 217, 317, 217, 330, 220, 341, 222))
fruit_hitboxes.append(Polygon(255, 203, 265, 208, 270, 211, 277, 219, 282, 226, 286, 233, 286, 242, 286, 253, 283, 262, 279, 269, 271, 275, 263, 279, 256, 285, 251, 288, 233, 289, 223, 284, 216, 280, 208, 272, 204, 262, 201, 255, 203, 245, 203, 234, 204, 225, 209, 215, 218, 208, 228, 202, 240, 202, 256, 202))
fruit_hitboxes.append(Polygon(214, 213, 231, 216, 245, 201, 253, 217, 270, 213, 264, 222, 272, 228, 278, 237, 279, 249, 279, 261, 274, 269, 266, 278, 258, 289, 252, 295, 247, 298, 229, 299, 207, 273, 200, 258, 201, 239, 207, 227, 217, 219))
fruit_hitboxes.append(Polygon(235, 204, 250, 204, 254, 200, 257, 204, 261, 208, 267, 212, 279, 212, 275, 216, 280, 220, 286, 225, 291, 236, 294, 240, 292, 257, 288, 269, 280, 283, 266, 287, 256, 292, 242, 292, 218, 281, 201, 260, 202, 246, 204, 232, 209, 223, 214, 215, 224, 211, 233, 205))
fruit_hitboxes.append(Polygon(201, 290, 201, 259, 205, 251, 212, 239, 220, 228, 230, 222, 238, 213, 248, 209, 258, 204, 265, 200, 277, 202, 289, 202, 301, 209, 307, 216, 316, 226, 322, 235, 320, 248, 321, 264, 314, 280, 307, 289, 295, 302, 282, 312, 269, 320, 261, 319, 247, 319, 234, 320, 217, 311, 202, 290))

powerups_hitboxes.append(Polygon(244, 208, 251, 203, 258, 217, 266, 228, 270, 249, 269, 267, 263, 282, 255, 295, 247, 303, 239, 311, 230, 315, 217, 317, 208, 317, 202, 311, 204, 306, 217, 287, 226, 267, 233, 254, 238, 242, 244, 227, 247, 219, 242, 207))
powerups_hitboxes.append(Polygon(235, 206, 245, 202, 248, 211, 254, 220, 258, 232, 258, 244, 258, 259, 248, 272, 243, 281, 235, 286, 231, 291, 219, 294, 209, 294, 202, 292, 214, 278, 223, 263, 228, 249, 234, 234, 238, 220, 239, 215, 237, 207))

bomb_hitboxes.append(Polygon(218, 201, 234, 201, 235, 216, 246, 217, 245, 226, 257, 233, 264, 247, 262, 264, 254, 276, 238, 283, 228, 282, 218, 280, 209, 273, 201, 259, 204, 245, 213, 231, 208, 221, 218, 218))
bomb_hitboxes.append(Polygon(223, 204, 240, 201, 238, 216, 249, 217, 246, 229, 258, 238, 262, 249, 262, 259, 259, 266, 253, 274, 247, 278, 232, 281, 217, 278, 208, 271, 204, 259, 203, 248, 206, 237, 216, 230, 219, 229, 215, 219, 225, 216))

for thing in fruit_hitboxes:
    thing.opacity = 0
    thing.centerX = app.width *2
    thing.centerY = app.height *2
for thing in powerups_hitboxes:
    thing.opacity = 0
    thing.centerX = app.width *2
    thing.centerY = app.height *2
for thing in bomb_hitboxes:
    thing.opacity = 0
    thing.centerX = app.width *2
    thing.centerY = app.height *2

    
app.run()