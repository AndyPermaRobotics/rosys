# User Interface

RoSys plays very well with [NiceGUI](https://nicegui.io/) and provides additional robot-related components through the `rosys.ui` package.
NiceGUI is a high-level web UI framework on top of [JustPy](https://justpy.io/).
This means you can write all UI code in Python.
The state is automatically reflected in the browser through websockets.
If required RoSys can also be used with other user interfaces or interaction models, for example a completely app-based control through Bluetooth LE with Flutter.