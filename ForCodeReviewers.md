For members of the code review team, this document and the README.md documents are necessary to read

To run some of the automated tests, you must have pyautogui installed. You can use pip install pyautogui or pip3 install pyautogui for windows and mac respectively. 

All instructions for setup are included in the README.

This file will give you instructions for running tests

There are 3 types of tests for this project:

1. Automatic GUI tests: You run a file (titles specified later) and tests will commence. Details on what should happen will be specified for each file.

2. Manual GUI tests: You will run a file(titles specfied later) which will give you instructions to complete in the game window and you will select yes or no based on if the tests passed or not. The results will be saved to a txt file which you will submit as part of milestone 4 (There will be several)

3. Function tests where functions from different games are pulled out into a new file (function_tests.py) which allow you to test them directly. Some tests will be provided. For milestone 4, simply state whether they behaved as expected


## Automatic GUI Tests

### Run testLauncher.py

#### What should happen:

##### The Launcher will open, followed by a short delay, then an opening of the first game, then the game will close. This exact process will repeat for all game files in the known games category (So testing files, and fruit ninja are excluded) There will be a print of "The Launcher has opened each time the launcher opens, followed by a print of "Launching gameName.py" and a print of "gameName.py has opened" where gameName.py is replaced by whatever game is being opened. Both instances of gameName.py should be the same. It should only change upon the next launch of the launcher and subsequent game.

##### Consider this a pass if all games launch and the pattern of Launcher -> game -> game prints holds for each launch. "DONE" will be printed upon cmpletion of this test


