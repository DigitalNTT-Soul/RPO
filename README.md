# Overview

First and foremost, this project is the result of a series of pipe-dreams and much self-imposed learning of the Kivy framework so that I can continue developing my skills as a software engineer and game developer. My goal, as a software engineer, in making this software, is to learn a plethora of new skills, including (but obviously not limited to) how to explore new software frameworks from scratch, how to begin planning and wrapping my head around large projects, and also how to design the various layouts of a game (such as its UI).

The app is not nearly complete at the moment and has merely a few UI elements (that will eventually be much more interactive than they currently are) and an image in the center of the screen that can be moved with either the arrow keys, WADS keys, or by dragging it around with mouse or touch, all as an experiment and test of the included keybinding and mouse/touch support systems and also a test of object movement on the screen.

While my goals as a software engineer developing this software have already been discussed, The primary purpose of this software itself is to eventually offer the app as an online, multi-platform game-service and storefront. Seeing as the Software's currently-planned end state includes:

* having its own storefront,
* where users can download games and other game-like software,
* each of which specifically utilizes the app's specific controls and framework,

This software will be almost more of a virtual game console/platform than it will be an actual game itself. The only significant differences between RPO and a PS5 would be portability and custom hardware.

First networking update: Networking features can be tested by running the 'rpo_server/server.py' file and then the 'rpo_client/clientTest.py' file, in that order. It is currently only a TCP approximation of a file transfer interaction, with a bit of defined client/server communication syntax thrown in for good measure and future feature addition, which currently allows the client to indicate that it is requesting a download, and indicate which file it is trying to receive.

Here's a list of links to my Youtube demonstrations about the various early phases of the project:

[First Youtube demonstration](https://youtu.be/kLo1uO4On8M) It includes a quick demo of the functionality at the *very* early, PC-Only phase of development, as well as a quick walkthrough of the code being used up to that point.

[Second Youtube demonstration](https://youtu.be/N236vxlm350) This is a demo of a *barely* better version of the software, with click/touch support and a equally functional (or *dis-functional*) .apk port.

[Third Youtube demonstration](https://youtu.be/nVaRtjcoEnE) This is a demo of some early networking features. Since one of the server's many responsibilities is going to be distribution of modules, systems, and expansions, I figured that would be the first thing I designed. The client-side networking features have not yet been implemented into the actual RPO app interface yet, but that (alongside some bug fixes and safety/sanity checks in the netcode) is the next step in the development process.

# Network Communication

The networking portions of this project are in a purely client/server relationship, and using a TCP connection over port 4606. This port was not chosen for any technical reason. It's more like an encoded acronym. If you map the (capital-only) English alphabet to Hexadecimal, with 'A' mapping to 0x0, 'P' mapping to 0xF, and 'Q' mapping to 0x10, then 'RPO' would be 0x11FE, which is 4606 in decimal.

The message format between client and server depends on which task is occurring at that time. The currently-built netcode defines a default syntax with which the client can send requests to the server (comma-separated keywords/arguments), as well as a rudimentary method of mimicking FTP via TCP, in which several back-to-back messages are sent from server to client, containing the raw binary of a requested package, to be reassembled into a zip file on the client side and then extracted.

# Development Environment

At time of writing, the project is built using Python 3.10.9 in addition to the Kivy 2.1.0 library, and the only tool used in its development (up until the end of the desktop-only phase of development, at least) was Visual Studio Code. In order to compile the software into an Android .apk file, the project used Kivy's own Buildozer tool (and its dependencies). Buildozer also only works in a Linux environment, so I used Ubuntu 20.04 via the Windows Sub-system for Linux.

# Useful Websites

A list of websites that I found helpful in this project:
* [Kivy Documentation Pages](https://kivy.org/doc/stable/)
* [Stack Overflow](https://stackoverflow.com/) where many of my questions had already been asked and answered for the public to see.
* [Beginner youtube series on Kivy, by Tech With Tim](https://youtube.com/playlist?list=PLzMcBGfZo4-kSJVMyYeOQ8CXJ3z1k7gHn)
* [Beginner youtube series on Kivy, by Codemy.com](https://youtube.com/playlist?list=PLCC34OHNcOtpz7PJQ7Tv7hqFBP_xDDjqg)

# Future Work

A list of things that I plan to fix, improve, and add in the future:
* Ensuring that neither child widgets of the main_screen widget, nor any part of those child widgets, can be displayed outside the bounds of the main_screen widget's borders. Any texture that crosses the border of the main_screen widget should be (at least partially) unrendered as not to cover any of the Pillar Buttons.
* Known bug: Pillar buttons do not un-highlight after being tapped or clicked.
* Pillar Buttons should create and slide-down Sub-Buttons of similar design, but with different labels, and tied to various actions.
    * Sub-buttons are tied to dictionary entries where the key stores the label button and the value stores the actual function the button represents
* Numerous stability improvements and bugfixes to netcode, especially:
    * Make sure that if client and server are run from different machines, client receives full package file and does not prematurely cut connection, causing server to crash
    * Make the server checks for file existence before attempting to open
        * also make sure the client awaits and properly handles this confirmation instead of automatically diving into package reception mode.
    * Handle the possibility of a failed connection between client and server