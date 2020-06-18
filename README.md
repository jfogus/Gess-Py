# Gess Game

*State: Functioning*

This started as a project for the Intro to Computer Science class that I took at Oregon State University.  I
like the concept of the game, but did not like the UI necessary to fit the parameters of the assignment.  I've
chosen Qt to learn more about making GUI applications for the desktop.

If you would like to know more about the game of Gess, please find the instructions I am using at
[chessvariants.com](https://www.chessvariants.com/crossover.dir/gess.html).

**Roadmap:**
* ~~Get the game working~~
* ~~Add a notification area for tracking turn and sending error messages.~~
* ~~Add a notation sidebar for seeing a history of the game.~~
* Add pagination to the history sidebar on overflow
* Add a save button to keep the move history for posterity.
* Add a mode for reviewing/stepping through a complete or saved game.
* (maybe) Add an upload button to upload the game to a site.
* (maybe) Online matchmaker

**Possible Related Projects:**
* Site for uploading previously played games and discussing
* Browser based version of the game 
* Mobile version of the game

**Notes:**
* In part, this is for MVC practice.  I am aware that Qt uses the Model/View pattern, combining
the view and controller, but it didn't seem like a complete misuses of the framework to separate 
the controller from the view.