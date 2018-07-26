# Updater

This project now merges the build framework for creating Windows installers with the Updater project.

### Windows x64

Anything declared with ```!define``` is a macro; to use it, you must dereference it with ```${<NAME>}```.
Note the use of ```{``` and ```}```.
If you want to use a constant, you omit the ```{``` and ```}```.
If its a variable, you need to declare it first with the keyword ```Var```, then you can use ```StrCpy``` to write to it.
You can then dereference the variable as with constants.

### OSX

For OSX, simply execute `updater/updater.py` as I'm currently lacking an  up-to-date solution for OSX.
The old `py2appp` solution *may* still work, but it has not been tested in a long time.

@author Daniel J. Finnegan  
@date September 2017
