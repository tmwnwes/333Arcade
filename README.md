# 333Arcade
 Repository for COMP333 Fall Semester Project
________

**Python 3.14 is not currently supported. Please use Python 3.9 - 3.13**

You may download Python 3.13.9 at https://www.python.org/downloads/release/python-3139/ and then navigating to your specific platform and downloading the installer.


This project is built using the Carnegie Mellon University graphics library. In order to run the launcher and games in their current state, the cmu_graphics folder must be in the same directory as the launcher and games. For your safety, you must download the graphics library yourself. The installer package for this library can be found at the following link: https://academy.cs.cmu.edu/desktop

# How to play

Regardless of platform, please download or clone this entire project repository from the "main" branch. Then download the CMU graphics library mentioned above directly from the source. Take the "cmu_graphics" folder from that download (not the entire installer folder, just the cmu_graphics folder) and put it in the same directory as the files from this repository. Then follow the platform dependent instructions below

# MacOS Instructions
If you are on MacOS, you have 3 options for running the launcher:
1. Open with VS code, and run through the play button at the top right 
2. Open in Python Launcher (NOT IDLE) and run the script
3. Open a terminal window, navigate to the directory the launcher is in and run the launcher


```bash
cd path/to/this/repository
python3 PretendLauncher.py
```

___

# Windows Instructions

If you are on Windows you have 2 simple options to run the launcher
1. Double click the PretendLauncher.py file as if it were an executable
2. Open the repository folder through VS code and click the play button at the top right while having the launcher file selected
___

## Included in this Repository

Files

This folder will come populated with a slightly altered version of the words_alpha.txt file available at https://github.com/dwyl/english-words/blob/master/words_alpha.txt. The alterations are just the removal of words that are 4 letters or fewer, but you can feel free to look at the source or replace the file attached in this repository with that file instead. Upon running the launcher, Files will become populated with stats and key files for use by the game included with this project.

PretendLauncher.py

This file acts as the launcher file for all of the games released with this project. It will make and maintain stats and key files for all of the included games. If you wish to know what stats are kept, you may check the keys files which should make it clear what game events are being tracked. In an upcoming release planned for November 7th, 2025, you will be able to automatically delete and recreate the stats files, or update them to match new game updates without necessitating the manual deletion of the files in the Files folder.

If you delete the files or the entire Files folder, then the launcher will remake the files the next time it is run. The files are necessary for the games to work, and the games will crash on launch if the files are missing. This is solved by running the launcher again. If you delete the stats file for a specific game, your progress is erased for that game (or all games if you delete the Files folder)

Asteroid.py

This is a remake of the classic arcade game, Asteroids. In this version of the game, you have 3 HP instead of 1 so you will not die immediately to one hit. Additionally, you can move in 4 directions, relative to ship rotation instead of only forward in the direction you face. Please note that "W" will accelerate the ship forward from the ship's perspective, not up accordin to your perspective, though those perspectives may occasionally overlap. Use WASD to accelerate in the following directions (Forward, Left, Back, Right) in relation to the ship. Use Left and Right arrow keys to accelerate towards rotation in those direcitons, and use spacebar to fire projectiles from the front of your ship in the direction you face. The asteroids have HP relating to their size, with the smallest asteroids exploding to one hit and the largest taking 4 shots to destroy, but point values are scaled with this in mind. You will also encounter enemy saucers which will fire at you and call allies in to assist if you don't destroy them fast enough. Enemy saucer health scales with time played and destroying all enemy saucers on screen will result in an increased score multiplier

Descriptions for other games will be posted by November 2nd 2025



