For members of the code review team, this document and the README.md documents are necessary to read

To run some of the automated tests, you must have pyautogui installed. You can use pip install pyautogui or pip3 install pyautogui for windows and mac respectively. 

All instructions for setup are included in the README.

This file will give you instructions for running tests

There are 2 types of tests for this project:

1. Automatic GUI tests: You run a file testLauncher.py and tests will commence.

2. Manual GUI tests: You will run a file for each game (explained below) which will give you instructions to complete in the game window and you will select yes or no based on if the tests passed or not. The results will be saved to a txt file which you will submit as part of milestone 4 (There will be several files all in a folder, so juust submit the whole TESTSRESULTS FOLDER)


## Automatic GUI Tests

### Run testLauncher.py

#### What should happen:

##### The Launcher will open, followed by a short delay, then an opening of the first game, then the game will close. This exact process will repeat for all game files in the known games category (So testing files, and fruit ninja are excluded) There will be a print of "The Launcher has opened each time the launcher opens, followed by a print of "Launching gameName.py" and a print of "gameName.py has opened" where gameName.py is replaced by whatever game is being opened. Both instances of gameName.py should be the same. It should only change upon the next launch of the launcher and subsequent game.

##### Consider this a pass if all games launch and the pattern of Launcher -> game -> game prints holds for each launch. "DONE" will be printed upon cmpletion of this test

#### Note that mac users may be required to grant permissions for cmu graphics to run at all (via allowing all developers apps to run), as well as grant control permissions to vscode or terminal to allow pyautogui to actually control the mouse and keyboard. These options will pop up on mac with Apple's instructions and you should follow those instructions. 

## MANUAL GUI TESTS

#### Each Game will have files called GameName.py, GameNameTestOnly.py, and GameNameUserTests.py It is imperative that you run the gameNameTestsOnly.py file. It will launch the UserTests file on its own and you will interact with both windows after they open. For example, There will be Asteroids.py, AsteroidsTestOnly.py and AsteroidsUserTests.py and you should run AsteroidsTestOnly.py to conduct these tests. Instructions are pre loaded into each UserTests file and as long as you follow the instructions, the tests are straightforward. The results will be compiled in a text file for each game in the TESTSRESULTS folder. Submit that folder for Milestone 4 after conducting all tests. 


