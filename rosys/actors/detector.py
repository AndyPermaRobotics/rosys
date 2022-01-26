import socketio
from .. import event, task_logger
from ..world import BoxDetection, Image, PointDetection
from .actor import Actor


class Detector(Actor):
    interval: float = 0

    def __init__(self):
        super().__init__()
        self.sio = socketio.AsyncClient()
        self.is_connected = None

        @self.sio.event
        def connect():
            self.is_connected = True
            assert self.sio.transport() == 'websocket'

        @self.sio.event
        def connect_error(data):
            self.is_connected = False

        @self.sio.event
        def disconnect():
            self.is_connected = False

    async def connect(self, reconnect_delay: float = 3):
        try:
            self.log.info('connecting to detector')
            await self.sio.connect('ws://localhost:8004', socketio_path='/ws/socket.io')
            self.log.info('connected successfully')
            self.is_connected = True
        except:
            self.log.exception('connection failed; trying again')
            self.is_connected = None
            await self.sleep(reconnect_delay)

    async def step(self):
        if self.is_connected is None:
            await self.connect()

        if self.world.upload_queue:
            task_logger.create_task(self.upload(self.world.upload_queue.pop(0)), name='upload_image')

        detecting_cameras = [c for c in self.world.cameras.values() if c.detect]
        if not detecting_cameras:
            await self.sleep(0.02)
            return

        for camera in detecting_cameras:
            image = camera.images[-1]
            await self.detect(image)

    async def detect(self, image: Image) -> Image:
        if not self.is_connected:
            return
        try:
            result = await self.sio.call('detect', {'image': image.data, 'mac': image.camera_id})
            box_detections = [BoxDetection.parse_obj(d) for d in result.get('box_detections', [])]
            point_detections = [PointDetection.parse_obj(d) for d in result.get('point_detections', [])]
            image.detections = box_detections + point_detections
        except:
            self.log.exception(f'could not detect {image}')
        else:
            event.emit(event.Id.NEW_DETECTIONS, image)
            return image

    async def upload(self, image: Image):
        try:
            await self.sio.emit('upload', {'image': image.data, 'mac': image.camera_id})
        except:
            self.log.exception(f'could not upload  {image}')

    def __str__(self) -> str:
        state = {
            None: 'starting',
            True: 'connected',
            False: 'reconnecting',
        }[self.is_connected]
        return f'{type(self).__name__} ({state})'
