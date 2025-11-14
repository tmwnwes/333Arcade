import pyautogui
import time
import subprocess
import os
import platform

system = platform.system()
closeGameKeys = []
if(system == "Darwin"):
    closeGameKeys+=["command", "w"]
if(system == "Windows"):
    closeGameKeys+=['alt', 'f4']

size = pyautogui.size()
width = size[0]
height = size[1]




launcher = subprocess.Popen(["python3.13", "PretendLauncher.py"])
time.sleep(5)
## OPEN GAME 1
pyautogui.click(1*(width/8), width/8) 
time.sleep(3)
for key in closeGameKeys:
    pyautogui.keyDown(key)
for key in closeGameKeys:
    pyautogui.keyUp(key)
time.sleep(3)

launcher = subprocess.Popen(["python3.13", "PretendLauncher.py"])
time.sleep(5)
## OPEN GAME 2
pyautogui.click(3*(width/8), width/8) 
time.sleep(3)
for key in closeGameKeys:
    pyautogui.keyDown(key)
for key in closeGameKeys:
    pyautogui.keyUp(key)
time.sleep(3)

launcher = subprocess.Popen(["python3.13", "PretendLauncher.py"])
time.sleep(5)
## OPEN GAME 3
pyautogui.click(5*(width/8), width/8) 
time.sleep(3)
for key in closeGameKeys:
    pyautogui.keyDown(key)
for key in closeGameKeys:
    pyautogui.keyUp(key)
time.sleep(3)

launcher = subprocess.Popen(["python3.13", "PretendLauncher.py"])
time.sleep(5)
## OPEN GAME 4
pyautogui.click(7*(width/8), width/8) 
time.sleep(3)
for key in closeGameKeys:
    pyautogui.keyDown(key)
for key in closeGameKeys:
    pyautogui.keyUp(key)
time.sleep(3)


launcher = subprocess.Popen(["python3.13", "PretendLauncher.py"])
time.sleep(5)
pyautogui.moveTo(width-5, height-50)
pyautogui.click()
time.sleep(1)
## OPEN GAME 5
pyautogui.click(1*(width/8), width/8) 
time.sleep(3)
for key in closeGameKeys:
    pyautogui.keyDown(key)
for key in closeGameKeys:
    pyautogui.keyUp(key)
time.sleep(3)

launcher = subprocess.Popen(["python3.13", "PretendLauncher.py"])
time.sleep(5)
pyautogui.moveTo(width-5, height-50)
pyautogui.click()
time.sleep(1)
## OPEN GAME 6
pyautogui.click(3*(width/8), width/8) 
time.sleep(3)
for key in closeGameKeys:
    pyautogui.keyDown(key)
for key in closeGameKeys:
    pyautogui.keyUp(key)
time.sleep(3)

launcher = subprocess.Popen(["python3.13", "PretendLauncher.py"])
time.sleep(5)
pyautogui.moveTo(width-5, height-50)
pyautogui.click()
time.sleep(1)
## OPEN GAME 7
pyautogui.click(5*(width/8), width/8) 
time.sleep(3)
for key in closeGameKeys:
    pyautogui.keyDown(key)
for key in closeGameKeys:
    pyautogui.keyUp(key)
time.sleep(3)

launcher = subprocess.Popen(["python3.13", "PretendLauncher.py"])
time.sleep(5)
pyautogui.moveTo(width-5, height-50)
pyautogui.click()
time.sleep(1)
## OPEN GAME 8
pyautogui.click(7*(width/8), width/8) 
time.sleep(3)
for key in closeGameKeys:
    pyautogui.keyDown(key)
for key in closeGameKeys:
    pyautogui.keyUp(key)
time.sleep(3)

print("DONE")

# pyautogui.click(x=200, y=200) 

# Perform a right-click
# pyautogui.rightClick(x=300, y=400)

# Double-click
# pyautogui.doubleClick(x=500, y=600)

# pyautogui.typewrite("Hello, World!")
# pyautogui.press("enter")
