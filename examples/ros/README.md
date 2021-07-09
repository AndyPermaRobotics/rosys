# ROS Example

This example shows how to start [ROS](https://www.ros.org/) on the [Zauberzeug Robot Brain](https://zauberzeug.com/product-robot-brain.html).
For simplicity we use [NiceGUI](https://nicegui.io/) to present a website with control elements:

<img src="https://raw.githubusercontent.com/zauberzeug/rosys/main/examples/ros/screenshot.png" width="800">

The build in NVIDIA Jetson is running a rather old Ubuntu LTS 18.04.
Therefore it's best to start ROS in a docker container.
We created a small helper script `docker.sh` for simplicity. Run

```bash
./docker.sh build
./docker.sh run
```

to build and start the image in a new container.
You should then be able to open the user interface on http://localhost.

## ROS Nodes

The example constists of two ROS nodes `esp` and `ui`.
The first handles the communication with the ESP32 within the Robot Brain for sending speed commands to the wheels.
The latter is just a demonstration of a seperate node which generates Twist messages through a web interface with [NiceGUI](https://nicegui.io/). You can replace this with any other node as needed.

## Configure ESP32 Low Level API

By sending the `/configure` message to the `esp`node the ESP32 will receive the configuration of the attached devices (two wheels thorugh a RoboClaw Controller) stored in the `config.txt`. The configuration is stored persitent on the ESP32. So you only need to save it once.

In the example the web page provides a button to trigger the `/configure` message. In a real scenario you would do it when deploying the robot.