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
If there are many variables/shapes/lists being declared right next to eachother at once, i.e. a bunch of related terms for a math equation, all of the body parts for hangman, different lists of strings/ints, then a single comment explaining what they are and how they are related shall be sufficient instead of making a comment for each one. 

All long term variables should be a minimum of 5 letters long. Examples include variables defined before runtime that are used in serveral places in the code, while short-lived variables such as loop iterators or temp lists can be shorter in length
