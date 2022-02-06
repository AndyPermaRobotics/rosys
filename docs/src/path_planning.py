#!/usr/bin/env python3
from nicegui import ui
import rosys
import rosys.ui
from rosys.automations import drive_path
from rosys.pathplanning import Planner
from rosys.world import Pose

# setup
runtime = rosys.Runtime()
planner = Planner(runtime.world)
rosys.ui.configure(ui, runtime)


async def handle_click(msg):
    for hit in msg.hits:
        yaw = runtime.world.robot.prediction.point.direction(hit.point)
        path = planner.search(goal=Pose(x=hit.point.x, y=hit.point.y, yaw=yaw), timeout=3.0)
        path3d.update(path)
        runtime.automator.replace(drive_path(runtime.world, runtime.hardware, path))
        await runtime.resume()


# 3d scene
with ui.scene(on_click=handle_click, width=800) as scene:
    robot = rosys.ui.robot_object()
    path3d = rosys.ui.path_object()

ui.label('click into the scene to drive the robot')
rosys.ui.cpu_usage().classes('h-64').style('width:800px')

# start
ui.run(title='RoSys', port=8080)
