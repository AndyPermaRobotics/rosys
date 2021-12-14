#!/usr/bin/env python3
from nicegui import ui
import rosys
from rosys.actors.pathplanning import Planner
from rosys.automations import drive_path
import rosys.ui

# setup
runtime = rosys.Runtime(world=rosys.World(mode=rosys.Mode.SIMULATION))
planner = Planner(runtime.world)
rosys.ui.configure(ui, runtime)


async def handle_click(msg):
    for hit in msg.hits:
        target_yaw = runtime.world.robot.prediction.point.direction(hit.point)
        planner.search(goal=rosys.Pose(x=hit.point.x, y=hit.point.y, yaw=target_yaw), timeout=3.0)
        path = [rosys.PathSegment(spline=step.spline, backward=step.backward) for step in planner.path]
        path_3d.update(path)
        runtime.automator.replace(drive_path(runtime.world, runtime.hardware, path))
        await runtime.resume()


# 3d scene
with ui.scene(on_click=handle_click) as scene:
    robot = rosys.ui.robot_object()
    ui.timer(0.05, robot.update)
    path_3d = rosys.ui.path_object()

ui.label('click into the scene to drive the robot')

# start
ui.run(title="RoSys", port=8080)
