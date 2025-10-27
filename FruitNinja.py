from cmu_graphics import *
import tkinter as tk
import random
import math

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.wm_attributes('-fullscreen', True) ## This line is a workaround for macOs devices with no ill effects for Windows users. It forces a new window to open in fullscreen and focus on it, before destroying it on the next line. The main canvas is then created and players will see it. Players must still maximise this window manually however
root.destroy()

app.width = width
app.height = height
app.stepsPerSecond = 30
app.setMaxShapeCount(10000000)
app.timer = 0
app.num = 0

background = Image("Files/FruitNinjaBackground.png", 0,0) ### Give proper credit
background.width = app.width
background.height = app.height

particles = []
partLines = []
deleteShapes = Group()
app.angle = None
head = RegularPolygon(100,100,12, 3, fill='white', rotateAngle = 90, visible = False)
app.lastX, app.lastY = 0,0


## The above lines import the image of the background and stretch it to fit the window
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
            

def spawn_particle_effects(x,y):
    new = Circle(x,y, 5, fill = None)
    new.life = app.stepsPerSecond*(1/2)
    new.num = app.num
    particles.append(new)
    particles_helper()

def onMousePress(x,y):
    head.centerX, head.centerY,  = x,y
    head.visible = True
    app.num +=1
    app.lastX, app.lastY = x,y

def onMouseDrag(x,y):
    app.angle = angleTo(app.lastX, app.lastY, x,y)
    head.centerX, head.centerY = x,y
    head.rotateAngle = app.angle
    app.lastX, app.lastY = x,y
    spawn_particle_effects(x,y)
    
    
def onMouseRelease(x,y):
    app.angle = 90
    head.visible = False
    head.centerX, head.centerY = x,y
    
def onStep():
    deleteShapes.clear()
    remove_particles()
    

app.run()