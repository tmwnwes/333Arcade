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
    closeGameKeys+=["alt", "f4"]
    call = sys.executable

size = pyautogui.size()
width = size[0]
height = size[1]

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

if(system=="Darwin"):
    for i in range(4):
        mac_open_page_1(i)
    for i in range(4):
        mac_open_page_2(i)

def windows_open_page_1(num):
    launcher = subprocess.Popen([call, "PretendLauncher.py"])
    time.sleep(5)
    pyautogui.click((num*2 + 1)*(width/8), width/8) 
    time.sleep(3)
    pyautogui.hotkey(closeGameKeys)
    time.sleep(3)

def windows_open_page_2(num):
    launcher = subprocess.Popen([call, "PretendLauncher.py"])
    time.sleep(5)
    ## OPEN GAME 5
    pyautogui.doubleClick(width-10, height-50)
    pyautogui.doubleClick(1*(width/8), width/8) 
    time.sleep(3)
    pyautogui.hotkey(closeGameKeys)
    time.sleep(3)

if(system == "Windows"):
    for i in range(4):
        windows_open_page_1(i)
    for i in range(4):
        windows_open_page_2(i)

print("DONE")

# pyautogui.click(x=200, y=200) 

# Perform a right-click
# pyautogui.rightClick(x=300, y=400)

# Double-click
# pyautogui.doubleClick(x=500, y=600)

# pyautogui.typewrite("Hello, World!")
# pyautogui.press("enter")
