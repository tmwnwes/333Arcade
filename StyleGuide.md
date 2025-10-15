Style Guide for Arcade Style Launcher

Team Members: Tim Watson, Avinash Reddy, Jeramiah Trout

________________________________________________________________
*Please Review and make alterations/suggetsions as you see fit*
________________________________________________________________

Functions should have comment blocks directly above or docstrings inside, explaining what their purpose is as well as their general expected input(s) and output(s)

All shapes directly created prior to runtime must be named

Simple variables and low-scope variables should be one descriptive noun 

Global variables or wide-scope or app-wide variables should be camelCase and descriptive

Lists/Arrays should be pluralized nouns describing what will be in them

Functions should be snake_case verb or verb phrase with the above mentioned comment block

More complex variables like classes/groups/shapes should be camelCase with an explanatory comment at declaration

Field access should be one descriptive adjective or noun, and be camelCase when one word is not enough

____________________
If there are many variables/shapes/lists/helper functions being declared right next to eachother at once, i.e. a bunch of related terms for a math equation, all of the body parts for hangman, different lists of strings/ints, then a single comment explaining what they are and how they are related shall be sufficient instead of making a comment for each one. 

All long term variables should be a minimum of 5 letters long. Examples include variables defined before runtime that are used in serveral places in the code, while short-lived variables such as loop iterators or temp lists can be shorter in length

Branching Guidelines:

All new games/apps should start out as full feature branches, with checks to ensure that the program is stable and functional before being merged onto main. 

If there are new features to add to a game/app, then a feature branch should be made to accomodate those new featues

Bug fixes for games on main should be pushed to main branch as soon as they are confirmed to solve the problem and not introduce new bugs. No feature branch necessary for simple bug fixes.

Branches should be made to tackle issues based on priority, and then to tackle feature requests if there are no further pressing issues.