# 333Arcade
 Repository for COMP333 Fall Semester Project
________

This is the Milestone 4 Branch. Please read the entire README.md file and entire ForCodeReiewers.md file

# Python 3.14 is not currently supported. Please use Python 3.13*

*You may download Python 3.13.9 at https://www.python.org/downloads/release/python-3139/ and then navigating to your specific platform and downloading the installer.


This project is built using the Carnegie Mellon University graphics library. In order to run the launcher and games in their current state, the cmu_graphics folder must be in the same directory as the launcher and games. For your safety, you must download the graphics library yourself. The installer package for this library can be found at the following link: https://academy.cs.cmu.edu/desktop

# How to play

Regardless of platform, please download or clone this entire project repository from the "Milestone-4-Code-Review-Branch-(Never-Merge)" branch. This can be accomplised by navigting to the named branch, and then clicking the green "code" button and either downloading as zip or copying the shown link and cloning via your favorite IDE with git cloning functionality, such as VS Code and then switching to the approprate branch. Then download the CMU graphics library mentioned above directly from the source. Take the "cmu_graphics" folder from that download (not the entire installer folder, just the cmu_graphics folder. Please take special mention of this. It is the most common error) and put it in the same directory as the files from this repository. Then make sure you have pyautogui installed. This can be accomplished on Windows and Mac with pip or pip3 just by opening a terminal / command prompt and typing pip install pyautogui or pip3 pyautogui. If this function fails, instead type python3 -m pip install pyautogui or python3 -m pip3 install pyautogui. Then follow the platform dependent instructions below for the ability to play the games (This is to actually play the games, not necessarily run the tests): 

## MacOS Instructions
If you are on MacOS, you have 3 options for running the launcher:

1. Open with VS code, and run through the play button at the top right  
or  
2. Open in Python Launcher (NOT IDLE) and run the script  
or  
3. Open a terminal window, navigate to the directory the launcher is in and run the launcher*


```bash
cd path/to/this/repository
python3 PretendLauncher.py
```
Note that if you have multiple versions of python3 installed, (such as 3.6.4, 3.9.3, 3.13.7, 3.14.2), you may need to specify version in your command as shown below:

To check installed version, simply run 

```bash
which -a python3
```
or 

```bash
python3 --vesion
```
____
For example, if you have vesion 3.13.7, you would run:

```bash
cd path/to/this/repository
python3.13 PretendLauncher.py
```
____

## Windows Instructions

If you are on Windows you have 2 simple options to run the launcher:

1. Double click the PretendLauncher.py file as if it were an executable  
or  
2. Open the repository folder through VS code and click the play button at the top right while having the launcher file selected
____

For Automatic tests, you will need to run the testing files which exist with names relating to each test being run. For example:

launcherTest.py will run the launcher, then a game, then close the game and open the launcher again and open the next game, repeatedly, for all games. 
 
 You should consider this test a pass if every game opens and each print lines up in the order:
 
 "The Launcher has opened"

 "Launching [some game]"

 "[Some game] has opened" 

 for each game
You should ignore these messages in your terminal for this test:

You are running cmu-graphics version 1.1.43, but a newer version 1.1.44 is available.
Visit https://academy.cs.cmu.edu/desktop to upgrade.




                         (
                    (    (
                    ((  (*(
                    (*( (*/
                    (**.***,
                    (***************((((((((((((((((
                    (********************************
                    (*******************************(
                    (*******************************(
                    (*******************************(
                    /*******************************(
                    (/******************(((((((     ((
                (*****(****************,
                /**********(************(
            ((***************(*********
                (*****(/*********(*****(
                    (**********/(/***(*/
                    (****************(
                        (/***********(
                            (*******(
                            (**(

 ** To run your animation, add cmu_graphics.run() to the bottom of your file **

We run the animations with a different function call so this will always pop up though it is irrelevant


 There will then be tests for each game individually separate from this which is better explained in ForCodeReviewers.md 

# Included in this Repository

## Files

#### This folder will come populated with a slightly altered version of the words_alpha.txt file available at https://github.com/dwyl/english-words/blob/master/words_alpha.txt. The alterations are just the removal of words that are 4 letters or fewer, but you can feel free to look at the source or replace the file attached in this repository with that file instead. Upon running the launcher, Files will become populated with stats and key files for use by the game included with this project.

## Audio

#### This folder comes populated with mp3 files used in some of the games. Deleting this folder or files within the folder may cause game crashes as audio files are attempted to be played.

## Images

#### This folder contains thumbnail images for each of the created games as well as images for fruit ninja

## PretendLauncher.py

#### This file acts as the launcher file for all of the games released with this project. It will make and maintain stats and key files for all of the included games. If you wish to know what stats are kept, you may check the keys files which should make it clear what game events are being tracked. In an upcoming release planned for November 7th, 2025, you will be able to automatically delete and recreate the stats files, or update them to match new game updates without necessitating the manual deletion of the files in the Files folder.

#### If you delete the files or the entire Files folder, then the launcher will remake the files the next time it is run. The files are necessary for the games to work, and the games will crash on launch if the files are missing. This is solved by running the launcher again. If you delete the stats file for a specific game, your progress is erased for that game (or all games if you delete the Files folder)

## Asteroids.py

#### This is a remake of the classic arcade game, Asteroids. In this version of the game, you have 3 HP instead of 1 so you will not die immediately to one hit. Additionally, you can move in 4 directions, relative to ship rotation instead of only forward in the direction you face, like in the original. Please note that "W" will accelerate the ship forward from the ship's perspective, not up or down according to your perspective, though those perspectives may occasionally overlap. Use WASD to accelerate in the following directions (Forward, Left, Back, Right) in relation to the ship. Use Left and Right arrow keys to accelerate your ship's rotation in those direcitons, and use spacebar to fire projectiles from the front of your ship in the direction you face. The asteroids have HP relating to their size, with the smallest asteroids exploding after one hit and the largest taking 4 shots to destroy, but point values are scaled with this in mind. All sizes of asteroids except the smallest will spawn 2 asteroids of the next size down at its location upon destruction. You will also encounter enemy saucers which will fire at you and call allies in to assist if you don't destroy them fast enough. Enemy saucer health scales with time played and destroying all enemy saucers on screen will result in an increased score multiplier. Enemy saucers can destroy asteroids but you will not receive score credit for asteroids destroyed by enemy saucers. You may pause and unpause with 'p', and restart the game after a game over by pressing enter.

## ColorGame.py

#### This is an attention test described in a few psychology courses. Words will pop up at the top of the screen, and those words will be written in a certain color. To score, you must select and click the color of the word from your options. Those options are the 15 colored buttons at the bottom of the screen. The color buttons are placed in a frustrating order, on purpose, and some of the words are themselves colors. Example: You may receive the word "orange", written in the color cyan, and you will be correct if you click the cyan button, not the orange button. You will receive a time bonus of 1 second added to your countdown clock for every correct guess. You are granted 2 seconds per guess. This means that you can gain time if you answer correctly in under 1 second but you will lose time overall if you average longer time between guesses. Additionally, an incorrect guess will subtract time from your overall time, and no guess is treated as an incorrect guess, so you'll lose the 2 seconds it took to not guess and be penalized on top of that. You lose when you run out of time overall. 

## Fireworks.py

#### This is a mindless stress relief style of "game", where you click on the screen and watch fireworks shoot up from the ground and explode where you clicked. This project has several features, such as screensaver mode, which handles clicking for you so you can put it up as a screensaver if you wish. You can still make manual clicks in screensaver mode and you can also control the rate of firework launches in screensaver mode from the main menu. Additional features include Starry Night mode which leaves small circles at the point of explosion which, overtime lead to a night sky-like background populated with colorful "stars". This mode is compatibale with manual clicks and with screensaver mode. Finally, there is also twinkle mode which will select "stars" at random to twinkle. This mode can only be activated if Starry Night mode is also active, and is compatible with manual clicks and screensaver mode. The available colors are the 9 on the main menu. Select colors by clicking on them, or alternatively using the select all or deselect all buttons. The game will prevent you from continuing if you fail to select a color on the main screen. 

## FlappyBat.py

#### This is a knockoff of flappy bird, a popular phone app from the early 2010s. There are aspects of the game that set it apart, however. The creator of this game was bitten by a bat at Wesleyan and so chose to model a bat at the player character for this game. The game also takes place at night with a starry background, and the cities in the distance are generated from the same model that generates the cities in MissileCommand.py which is mentioned later in this document. You will select your difficulty from the main menu. Difficulty is relating to the speed at which the pipes move in the beginning. In all difficulty modes, speed will increase over time. Your bat is affected by gravity and you flap by pressing spacebar which will send you upwarards. Be careful to avoid the green pipes, the ground, and flying too high into the sky, as your bat will crash and your round will end. You may pause and unpause at any point with 'p' and you may reselect difficulty upon failure by pressing escape, or simply replay at the same difficulty upon failure with enter.

## FruitNinja.py

#### This game is more of a joke than a real project. You can "slice" fruit that is launched from the bottom of the screen. You slice with the use of a mouse drag (meaning clicking, holding down, and moving, not just moving). There are 2 powerup types, freeze and double points, activated by special bananas. The countdown time is represented by a circular timer towards the top left of the screen visible when the powerups are active. Freeze will freeze all whole fruits powerups and bombs on the screen and still allow sliced items to fall away. Double points will score all slices as double (including negative point bombs). No combo system or fail system has been implemented at the time of this README but it is anticipated in the future, but it considered low priority as this game is just a joke inclusion.

## Hangman.py

#### To guess a letter, you can either type the letter using your keyboard or click the box surrounding the letter on the screen. This game is similar to the standard Hangman experience, but with a few key differnces. Internal development reffered to this game as Hangman Hard Mode becase it is significantly harder than standard hangman. To provide balance, you only fail after 9 incorrect letter guesses. The difficulty is a result of the following design choices. 

#### 1. The word list is 365k words long and contains words from past and present english dictionaries. This means that there are hundreds of old english words with weird spellings.  

#### 2. The game will operate as normal hangman until you have selected a correct letter, which it will show and reveal as correct. Subsequent guesses after choosing your first correct letter will function in a different manner, as the program attempts to find a word matching all previous characteristics, (length, what letters are not present, what letters are present and in what specific locations) but without your most recent guess. It collects all words meeting those criteria and picks one randomly to be the new word. If it cannot find a word with those characteristics, you are granted that letter as a correct guess. This continues in a cycle until you figure out the word or guess incorrectly 9 times. You may try to guess a new word by clicking the try again button opon winning or losing the round

## Minesweeper.py

#### This game is the standard minesweeper experience. You select a difficulty and click on the board. The numbers in each square represent how many its adjacent 8 squares are bombs. You can place flags with right click on physical mice, or the two-finger click on trackpads. Flags should be used to help you remember places that you think are bombs. Rates of bomb placement scale up with difficulty, as does the size of the board. There is also a system in place which will automatically clear all squares adjacent to a square containing a 0 once it is discovered, since it is the case that a 0 means that all adjacent squares are safe. This is a quality of life feature which speeds up each game since you do not have to manually clear all squares adjacent to a 0. You may pause and see help info with either 'p' or 'h'. Upon winning the game or failing, you may return to the main menu with escape and select difficulty to play another round. Your first click will reveal information about the square you click and all adjacent squares, at minimum, and will automatically flag bombs in that subset of squares. More information will be revelaed if a zero happens to fall in the subset cleared by your first click.

## MissileCommand.py

#### Basic Information: This is a modern remake of an arcade game, Missile Command. In this game, you control 3 missile batteries tasked with protecting 6 cities during an overnight attack. If you wish to manually switch which missile battery you are controlling at any time, you may do so by using the left and right arrow keys. Additionally, upon firing, the game will automatically select the next missile battery in rotation. You shoot by clicking your mouse on the screen at the place you want to fire a missile towards. The missile will fire from whichever missile battery you have selected, which will be outlined in white. Once reaching its target destination, your missile will explode and the explosion will remain for a few seconds as a fireball, able to destroy incoming enemies, allowing you to score. If you hit an enemy with a missile directly, instead of via the explosion, you will earn a 5x score bonus

####  More Gameplay: Each missile battery must reload after firing, and it has its own ammo which cannot be moved to other missile batteries. If an enemy hits any missile battery, it is damaged for a set amount of time and cannot fire or be selected during that time. This damaged state will result in a red highlight around the missile battery. This damage time is determined based on the type of enemy which caused the damage. Repair time after a large enemy hit is 25 seconds, and repair time after a small enemy hit is 10 seconds. This time is cumulative, meaning that subsequent hits extend repair time. This a a change from the original aracde game, where a single hit to a missile battery resulted in total destruction of the missile battery for the level, with repair immediate upon survival of the level. In order to balance this feature of repair time instead of destruction, repair time will carry over between levels. If a large enemy hits a city, it is immediately destroyed in its entirety. If a small enemy hits a city, the building(s) hit by the small enemy will be destroyed and the city overall will take damage. If the city takes damage in this way 3 times, it will be wholly destroyed. You will receive extra ammo each level, on top of the ammo you retained, but the number of enemies scales faster than the ammount of new ammo granted at later levels, so pick your targets carefully, and keep as much ammo as possible. All enemies can be destroyed in 1 shot

#### Enemies: You will face tougher enemies as you advance in the game. You begin by defending against basic missiles will travel directly down and with a constant speed. The next enemy type is a bomber plane which will drop bombs across the map, but can be destroyed before dropping all bombs. The next enemy type are missiles with horizontal velocity which are affected by gravity, so they will move faster as they travel. The next enemy is a "multi-bomb" which will explode well above the ground and launch multiple smaller bombs, but it can be destroyed before reaching that unknown height. The next enemy is a smart missile which will manuever to avoid fireballs. It is affected by gravity and will speed up as it falls, and has limited angles to avoid fireballs, but it is best to try and hit this enemy directly or nearly directly. The final enemy type is the UFO. You absolutely can not afford to let this enemy reach the space above your middle missile battery, because it will launch devestating strikes of smaller bombs towards your cities and missile batteries. This is the most dangerous enemy and should be your primary target if you spot one. 

#### There are certain score milestones which enable you to unlock bonus cities, which will replace a destroyed city at the start of the next level in the event that you were unable to protect it. Bonus cities will only spawn if you survived the level, by keeping at least one city alive. Since you gain points for destruction, including a 5x muliplier on direct hit, and bonus points for unspent ammo, and cities kept alive, you will earn bonus cities faster the better you are at the game. Cities will spawn at the start of a new level if you ahve space for a new city. If ypu do not have space, you will retain your bonus city until you reach the start of a level and have space for the city. Bonus cities stack, so it is possible to have several bonus cities, and therfore multiple cities created at the start of a level. There is no win condition for this game, as eventually, you will be unable to protect all of your cities, despite your best efforts.

## SubGame.py

#### This game places you as the commander of a submarine in an underwater minefield, targeted by mines, depth charges, and (in an upcoming update in december, other submarines.) It is your job to survive as long as possible. You have torpedoes to preotect yourself against mines fired with left arrow key (front of sub) and right arrow key (back of sub). Torpedoes can cause a chain reaction of mine explosions You may also angle your submarine counterclockwise with Q or clockwise with E. Finally, actually moving your submarine is accomplished with WASD keys, where W and S move the submarine upwards and downwards with respect to the screen and general notions of up and down while A and D move the ship forward or backwards relative to its rotation. Periodically, you willbe targeted with depth charges which will target your general location within the ocean and explode near your last known coordinates. Depth charges can also start a chain reaction, blowing up nearby mines. You will earn score for all depth charges avoided and mines destroyed by your torpedoes, depth charges or chain reactions. There is no win condition in this game, your goal is to survive as long as possible. 


# For each game, there are 2 other files, a TestOnly file and a UserTests file. 

### ForCodeReviewers will explain what to do with these files but if you are only interested in playing the games, then ignore those files and just use the main branch. It is assumed that anybody on this branch is here for Comp 333 Milestone 4


