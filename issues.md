I ran into many issues and this is how I resolved them

# multiple games popping up when selecting a diffculty
* One bug that I found was clicking on the difficulty button 
multiple times will more games horizontally, which is not a desired
feature. 
* I resolved this by having a variable track that there is only one game widget on the screen. If the user decides on another difficulty, then there will be a condition to check if there is one game widget on the screen, which will remove the previous game widget on the screen and replace it with a new widget. 

# game would not respond like timer, game over, etc...
* I resolved this by making the game have the main window as well. Doing this
fixed the entire gui and made the game responsive.

# learning the module and options 
* I resolved this through documentation, stackoverflow, and some examples