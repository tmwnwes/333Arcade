# 333Arcade
 Repository for COMP333 Fall Semester Project


**Python 3.14 is not currently supported. Please use Python 3.9 - 3.13**


**In order to run the launcher in its current state, the cmu_graphics folder must be in the same directory as the launcher. For convenienvce, it is included in the repository.**

 **Addititionally, since the games were built upon the cmu_graphics library, they must also be in the same directory to run**

Download this entire Repository as a zip file and unpack it in whatever directory you wish. 

If you are on MacOS, you have 3 options for running the launcher:
1. Open with VS code, and run through the play button at the top right 
2. Open in IDLE and run the script
3. Run through a terminal window, making sure to navigate to the directory the file is in, and running python3 PretendLauncher.py

If you are on Windows you have 2 simple options to run the launcher
1. Double click the PretendLauncher.py file as if it were an executable
2. Open through VS code and click the play button at the top right


 Finally, since we are using a graphics library, we are reliant on its update schedule. For now, it is up to date with Python 3.13.9.

 Any later versions will not work with this project. Confer with this document for any updates on that. 

 Please Note that the Files folder created when you first run the launcher will contain stats from all of the games attached to this project. 

The launcher will create the stats files and each game will access and maintain those files. 

If you delete the files or the entire Files folder, then the launcher will remake the files the next time it is run. The files are necessary for the games to work.

If you delete the files containing your stats, your progress is erased for that game (or all games if you delete the Files folder)

Additionally, each game script can be run on its own under the following 2 conditions:
1. The game is in the same diractory as the launcher and (more importantly) the cmu_praphics folder
2. The stats files exist and are populated (running the launcher once will accomplish this)

If both conditions are met, the game files can be run directly, bypassing the launcher.


 If you encounter issues running the launcher while being on the correct python version and following all steps, the proximal cause is likely a security issue raised regarding the cmu_graphics library. This issue is only present on MacOS. For now, there are 2 workarounds.
 
 1. Completely disabling security warnings about files from unknown developers. This comes with some risks unassociated with this program and project. This can be accomplished via first running the "sudo spctl --master-disable" command in terminal and then going to Settings -> Privacy & Security -> Security -> Allow Applications and selecting "Anywhere."

2. For users who do not wish to invite this risk, simply delete the cmu_graphics folder and download the graphics installer directly from Carnegie Mellon University. The download can be found at https://academy.cs.cmu.edu/desktop After downloading the installer (it is a zip file) extract the contents and place the cmu_graphics folder in the same directory as your launcher and games from this project. Note that it needs to be specifically the cmu_graphics folder, not the entire installer folder.

This issue was documented on the repository: https://github.com/tmwnwes/333Arcade/issues/7#issue-3518942044


