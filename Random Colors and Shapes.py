from cmu_graphics import *
import tkinter as tk
import random

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.destroy()

app.width = width
app.height = height

app.background = rgb(randrange(256), randrange(256), randrange(256))

def make_shape_random_place_color_points(points, size, borderWidth):
    '''
    Takes 3 args for points size and borderWidth of the shape it will create
    Returns no values
    Points refers to the points on the star or polygon, size refers to radius, and borderWidth refers to thickness
    '''
    star_or_poly = randrange(2)
    if(star_or_poly ==0):
        Star(randrange(app.width), randrange(app.height), size, points, fill = rgb(randrange(256), randrange(256), randrange(256)), border = rgb(randrange(256), randrange(256), randrange(256)), borderWidth = borderWidth)
    else:
        RegularPolygon(randrange(app.width), randrange(app.height), size, points, fill = rgb(randrange(256), randrange(256), randrange(256)), border = rgb(randrange(256), randrange(256), randrange(256)), borderWidth = borderWidth)

for i in range(1800):
    make_shape_random_place_color_points(randrange(3,30), randrange(5, 50), randrange(1,4))

app.run()