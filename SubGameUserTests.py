from cmu_graphics import *
import pyautogui
import os
import sys

size = pyautogui.size()

width = size[0]
height = size[1]

app.width = 3*(width//10)
app.height = (19*(height//20))
app.counter = 0

keys = ["W Moves Up", "A Moves Left", "S Moves Down", "D Moves Right", "Left Shoots Torp Left", "Right Shoots Torp Right", "Shots Hit", "Damage Is Taken", "Pausing Works", "Q Rotates Counter Clockwise (Bow Down)", "E rotates Clockwise (Bow Up)", "WASD Keys Move Relative To Rotation", "Shots Fire In Faced Direction", "Cannot travel through floor", "Cannot travel above top of ocean", "Cannot shoot with no ammo", "Powerups disappear"]
questions1 = ["Press and Hold W key", "Press and Hold the A key", "Press and Hold S Key", "Press and Hold D key" , "Press Left Arrow key", "Press Right Arrow key", "Fire torpedoes at mines", "Purposefully bump into a mine or let a depth charge hit you" , "Press P", "Unpause the Game/Play Again if you died. Press and Hold Q", "Press and Hold E", "Rotate your sub to a high angle and then Use WASD keys to move", "Rotate your sub to a high angle (may already be there) and fire torpedoes", "Try to move through the bottom of the ocean in any way you can think of", "Try to come up above the surface of the water", "Fire torpedoes aimlessly just to get rid of them until the top left says Ammo: 0. Then try to keep firing", "Purposefully do not collect a powerup when it spawns and watch the timer tick down"]
questions2 = ["Did you move Up", "Did you move Left", "Did you move Down", "Did you move Right" , "Did you shoot a torpedo to the Left", "Did you shoot a torpedo to the Right", "Did the shots explode on contact or travel a long distance before exploding?", "Did you take damage (Health bar at the top right of the screen, default 3 health)", "Did the Pause Menu Appear", "Did the submarine slowly rotate counterclockwise?", "Did the submarine slowly rotate clockwise", "Click Yes if W and S moved the sub Up and Down while A and D moved it relative to rotation", "Do torpedoes fire based on the rotation of the ship?", "Click Yes if you stayed in the water and could not travel through the floor", "Click Yes if you stayed in the water and could not travel into the air", "Click yes if you could not fire with 0 ammo", "Upon reaching 0, did the powerup disappear"]

instructions = Label("If at any point, you fail the round or due, please follow the on screen game instructions to restart", app.width/2, app.height/5, fill='black', bold = True, size = app.width/60)
instruct2 = Label("Also, you will need to click into this window each time before being able to click yes or no", instructions.centerX, instructions.bottom + 20)
instruct2 = Label("Also, you will need to click into the game window each time before being able to follow instructions", instructions.centerX, instruct2.bottom + 20)
instruct3 = Label("Make sure to move the windows such that you can see this test answer window and the game window", instructions.centerX, instructions.top -20)
shownQuestion1 = Label(questions1[0], app.width/2, 2*app.height/5)
shownQuestion2 = Label(questions2[0], app.width/2, shownQuestion1.bottom+15)

yesButton = Rect(app.width/2, app.height/2, app.width/2, app.height/10, fill='green', border = 'black', align = 'center')
noButton = Rect(yesButton.left, yesButton.bottom+5, app.width/2, app.height/10, fill='red', border = 'black')

yesLabel = Label("Yes", yesButton.centerX, yesButton.centerY, fill='white', bold = True)
noLabel = Label("No", noButton.centerX, noButton.centerY, fill='white', bold = True)

file_path = os.path.abspath(__file__)
directory_path = os.path.dirname(file_path)
os.chdir(directory_path)
currentFile =  os.path.basename(__file__)
gameName = currentFile[:-3]

print(currentFile + " has opened")

def file_checking(path, keys):
    '''
    Takes 2 args, path for which file to look for, 
    default is the default info for the game, 
    returns no values but creates text files
    Looks for necessary game files. Creates and populates the files if they are not found in the expected directory
    Takes the values from the files, whether already existing or new and puts the values into a list for use later
    '''
    directory = "TESTSRESULTS"
    properPath = os.path.join(directory, path)
    if(not os.path.exists(directory)):
        os.makedirs(directory, exist_ok=True)
    if (not os.path.exists(properPath)):
        with open(properPath, 'w') as f:
            f.seek(0)
            for i in range(len(keys)):
                f.write((str)((str)(keys[i])+ " :\n"))

file_checking(gameName+"TestResults.txt", keys)

fullInfoListResults = []

def update_stats():
    '''
    Takes no arguments and returns no values
    Updates stores stats in the associated text file
    '''
    gameInfo = open("TESTSRESULTS/" +gameName+"TestResults.txt", "w")
    gameInfo.seek(0)
    for i in range(len(fullInfoListResults)):
        gameInfo.write(keys[i] + " : " + fullInfoListResults[i]+"\n")

def onMousePress(x,y):
    if(yesButton.contains(x,y)):
        fullInfoListResults.append("PASS")
        app.counter+=1
    if(noButton.contains(x,y)):
        fullInfoListResults.append("FAIL")
        app.counter += 1
    if(app.counter>=len(questions1)):
        update_stats()
        shownQuestion1.value =  "Thank you. You may close this test"
        shownQuestion2.value = "Please Review the file and submit for milestone 4"
        yesButton.visible = False
        noButton.visible = False
    else:
        shownQuestion1.value = questions1[app.counter]
        shownQuestion2.value = questions2[app.counter]

app.run()