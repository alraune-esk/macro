# macro


A set of python scripts that will execute macros onto the currently running desktop.
e.g. Combinations of mouse-clicks, key presses.


Template matching is used to detect when certain elements of the application in use appear/change.

The objective is to automate tedious tasks such as repetitive mouse clicks with the added flexibility to write individual scripts for tasks.
These scripts can be seamlessly incorporated into the application by copy and pasting a .py file into the profiles folder.
This flexibility allows for quick and easy scripts to be made and accessed all in one GUI. 


Features:
Control GUI to select, execute, pause and change macro profiles.
Flexibility in code design to allow for drag and drop macro profiles that adhere to a simple structure.
Support to run indefinite macros. 
All the functionality of win32gui and other input device libraries that allow for options such as selection of window, focus, sending of input to minimised windows etc.


<h3>To Run:</h3>
Install requirements in requirements.txt
Run macro.py in either a terminal or ide.

Or 

Use Pyinstaller to create an executable that runs the GUI.



Current profiles:
A simple "auto-battler" for the Steam game "Limbus Company" with 2 profiles:
"Always foreground" which assumes that game window will always be in focus, so the inputs will be directly sent through.
"Tab Back" for each macro iteration it tabs into the game window while also saving the window id of the previous window the user was on (if there was one), after the macro fully executes it tabs the user back to the window they were on previously. Useful for multi-tasking on a single monitor.


