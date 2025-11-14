import pyautogui
import time
import subprocess
import os
import sys
import platform

system = platform.system()
closeGameKeys = []
call=None
if(system == "Darwin"):
    closeGameKeys+=["command", "w"]
    call = 'python3.13'
if(system == "Windows"):
    closeGameKeys+=["altleft", "f4"]
    call = sys.executable

size = pyautogui.size()
width = size[0]
height = size[1]
knownGames = ["Asteroids", "ColorGame", "Fireworks", "Hangman", "Minesweeper", "SubGame", "MissileCommand", "FlappyBat", "Simon"]

file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(file_path)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)

def mac_open_page_1(num):
    launcher = subprocess.Popen([call, "PretendLauncher.py"])
    time.sleep(5)
    pyautogui.click((num*2 + 1)*(width/8), width/8) 
    time.sleep(3)
    for key in closeGameKeys:
        pyautogui.keyDown(key)
    for key in closeGameKeys:
        pyautogui.keyUp(key)
    time.sleep(3)

def mac_open_page_2(num):
    launcher = subprocess.Popen([call, "PretendLauncher.py"])
    time.sleep(5)
    pyautogui.click(width-10, height-50)
    pyautogui.click((num*2 + 1)*(width/8), width/8) 
    time.sleep(3)
    for key in closeGameKeys:
        pyautogui.keyDown(key)
    for key in closeGameKeys:
        pyautogui.keyUp(key)
    time.sleep(3)

def mac_open_page_3(num):
    launcher = subprocess.Popen([call, "PretendLauncher.py"])
    time.sleep(5)
    pyautogui.click(width-10, height-50)
    time.sleep(2)
    pyautogui.click(width-10, height-50)
    time.sleep(2)
    pyautogui.click((num*2 + 1)*(width/8), width/8) 
    time.sleep(3)
    for key in closeGameKeys:
        pyautogui.keyDown(key)
    for key in closeGameKeys:
        pyautogui.keyUp(key)
    time.sleep(3)

if(system=="Darwin"):
    for i in range(4):
        mac_open_page_1(i)
    for i in range(4):
        mac_open_page_2(i)
    for i in range(1):
        mac_open_page_3(i)


def windows_open_page_1(num):
    subprocess.Popen([call, "PretendLauncher.py"])
    time.sleep(5)
    pyautogui.click((num*2 + 1)*(width/8), width/8)
    time.sleep(3)
    active = []
    for i in range(len(knownGames)):
        a = pyautogui.getWindowsWithTitle(knownGames[i])
        if(a!=[]):
            active.append(a)
    for thing in active:
        thing[0].close()
    time.sleep(3)

def windows_open_page_2(num):
    subprocess.Popen([call, "PretendLauncher.py"])
    time.sleep(5)
    pyautogui.click(width-10, height-50)
    time.sleep(2)
    pyautogui.click((num*2 + 1)*(width/8), width/8)
    time.sleep(3)
    active = []
    for i in range(len(knownGames)):
        a = pyautogui.getWindowsWithTitle(knownGames[i])
        if(a!=[]):
            active.append(a)
    for thing in active:
        thing[0].close()
    time.sleep(3)

def windows_open_page_3(num):
    subprocess.Popen([call, "PretendLauncher.py"])
    time.sleep(5)
    pyautogui.click(width-10, height-50)
    time.sleep(2)
    pyautogui.click(width-10, height-50)
    time.sleep(2)
    pyautogui.click((num*2 + 1)*(width/8), width/8)
    time.sleep(3)
    active = []
    for i in range(len(knownGames)):
        a = pyautogui.getWindowsWithTitle(knownGames[i])
        if(a!=[]):
            active.append(a)
    for thing in active:
        thing[0].close()
    time.sleep(3)

if(system == "Windows"):
    for i in range(4):
        windows_open_page_1(i)
    for i in range(4):
        windows_open_page_2(i)
    for i in range(1):
        windows_open_page_3(i)

print("DONE")

