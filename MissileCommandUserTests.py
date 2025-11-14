from cmu_graphics import *
import pyautogui

size = pyautogui.size()

width = size[0]
height = size[1]

app.width = 3*(width//10)
app.height = height


app.run()