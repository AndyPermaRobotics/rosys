#!/usr/bin/env python3
import rosys
from nicegui import ui
from rosys.vision import CameraServer, UsbCameraProviderHardware, UsbCameraProviderSimulation, camera_provider

# setup
if UsbCameraProviderHardware.is_operable():
    camera_provider = UsbCameraProviderHardware()
else:
    camera_provider = UsbCameraProviderSimulation()
    camera_provider.add_camera(camera_provider.create_calibrated('test_cam', width=800, height=600))
CameraServer(camera_provider)


async def refresh() -> None:
    for uid, camera in camera_provider.cameras.items():
        if uid not in feeds:
            feeds[uid] = ui.interactive_image('', cross=False)
        await feeds[uid].set_source(camera.latest_image_uri)


# ui
feeds = {}
ui.timer(0.3, refresh)

# start
ui.on_startup(rosys.startup)
ui.on_shutdown(rosys.shutdown)
ui.run(title='RoSys')
