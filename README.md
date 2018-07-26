# Updater Installer

NSIS script for creating a Windows installer for Updater.
The installer includes a copy of the CMake and git installers so the user can install each if they have not already done so.

# Notes
Anything declared with ```!define``` is a macro; to use it, you must dereference it with ```${<NAME>}```.
Note the use of ```{``` and ```}```.
If you want to use a constant, you omit the ```{``` and ```}```.
If its a variable, you need to declare it first with the keyword ```Var```, then you can use ```StrCpy``` to write to it.
You can then dereference the variable as with constants.

# TODO
This is great for the Windows solution, but I still need one for OSX.
I suppose for OSX I have two options

- Build an application with py2app and then distribute this in a zip. If going with this option, I need to write code to execute at build time that will call py2app and then zip everything up into a package
- Alternatively, just encourage folks to download the project repo and call updater.py. This is not really desirable as its not actually a deployable solution

@author Daniel J. Finnegan  
@date September 2017