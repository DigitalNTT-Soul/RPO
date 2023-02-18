# Overview

{Important!  Do not say in this section that this is college assignment.  Talk about what you are trying to accomplish as a software engineer to further your learning.}

First and foremost, this project is the result of a series of pipe-dreams and much self-imposed learning of the Kivy framework so that I can continue developing my skills as a software engineer and game developer. My goal, as a software engineer, in making this software, is to learn a plethora of new skills, including (but obviously not limited to) how to explore new software frameworks from scratch, how to begin planning and wrapping my head around large projects, and also how to design the graphical layout of a game (such as its UI).

The app is not nearly complete at the moment and has merely a few UI elements (that will eventually be much more interactive than they currently are) and an image in the center of the screen that can be moved with either the arrow keys or WADS as an experiment and test of the included keybinding system and also a test of object movement on the screen.

While my goals as a software engineer developing this software have already been discussed, The primary purpose of this software itself is to eventually offer the app as an online, multi-platform game-service and storefront. Seeing as the Software's currently-planned end state includes:
* having its own storefront,
* where users can download games and other game-like software,
* each of which specifically utilizes the app's specific UI layout,

This software is almost more of a virtual game console/platform than it will be an actual game itself. The only significant differences between RPO and PS5 would be custom hardware and portability.

[Here's a link to my Youtube demonstration.](https://youtu.be/kLo1uO4On8M) It includes a demo of the current functionality level of the game as well as a walkthrough of all the code being used so far.



# Development Environment

At time of writing, the project is built using Python 3.10.9 in addition to Kivy 2.1.0, and the only tool used in its development (up until the end of the desktop-only phase of development, at least) was Visual Studio Code
# Useful Websites

A list of websites that I found helpful in this project:
* [Kivy Documentation Pages](https://kivy.org/doc/stable/)
* [Stack Overflow](https://stackoverflow.com/) where many of my questions had already been asked and answered for the public to see.
* [Beginner youtube series on Kivy, by Tech With Tim](https://youtube.com/playlist?list=PLzMcBGfZo4-kSJVMyYeOQ8CXJ3z1k7gHn)
* [Beginner youtube series on Kivy, by Codemy.com](https://youtube.com/playlist?list=PLCC34OHNcOtpz7PJQ7Tv7hqFBP_xDDjqg)

# Future Work

A list of things that I plan to fix, improve, and add in the future.
* Ensuring that neither child widgets of the main_screen widget, nor any part of those child widgets, can be displayed outside the bounds of the main_screen widget's borders. Any texture that crosses the border of the main_screen widget should be (at least partially) unrendered as not to cover any of the Pillar Buttons
* Add mouse and touch support
* After implementing touch support, port the software to a mobile app