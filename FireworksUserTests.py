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

keys = ["Help Button Opens Help Menu", "Select All Does Select All Colors", "Deselect All does Deselect All Colors", "Clicking a Color Button will toggle it's selection Status", "No Color Warning Works", "All setting options are toggleable", "Fireworks are created in game screen", "Can return to main menu", "Can use help menu from game screen"]
questions1 = ["Click the Help Button (Top Left)", "Close the help menu and click the Select All Colors Button", "Click Deselect All Colors Button", "Click a series of color buttons. Your choice of ordering", "Deselect All Colors and Press Go", "Click Screensaver button, starry night button, twinkle mode button, and muted button, in that order", "Disable screensaver and starry night and twinkle. Select whatever colors you want and press go. Then click on the screen", "Press Escape", "Press Go again and return to the game screen. Now press H"]
questions2 = ["Did the help menu open?", "Are all colors buttons outlined in green?" , "Are all color buttons no longer outlined?", "If a color was outlined in green, clicking it removed the outline and vice versa?", "Did you get a warning instruction you to pick at least 1 color?", "Did they all gain a white outline and change what they say (Active instead of Inactive)", "Does a shape move towards where you cicked and then explode upon reaching that point?", "Did you return to main menu?", "Did the Help Menu appear?"]
answers = []
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