# Getting Started

First [install RoSys](installation.md) with pip or Docker.
Then create a directory to host your code and put it under version control.
Name your entry file `main.py` and add the following content:

```Python
{!getting_started_01.py!}
```

If you launch the program, a webbrowser will open the url http://0.0.0.0:8080/ and show you the robot's incrementing system time.

## Interaction

Let's add a 3D view and joystick control to move the robot around:

```Python hl_lines="5  13-16"
{!getting_started_02.py!}
```

You can drive the robot by dragging the mouse inside the top left square:

![Screenshot](getting_started_02.png)