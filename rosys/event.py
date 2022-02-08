import asyncio
from asyncio.tasks import Task
import collections
import inspect
from aenum import Enum, auto
from typing import Awaitable, Callable, Union
import logging
import weakref

tasks: list[Task] = []
listeners = collections.defaultdict(set)
log = logging.getLogger('rosys.event')


class Id(Enum, init='value __doc__'):
    '''Event Identifier. Every event has its own set of parameters.'''

    def _generate_next_value_(name, start, count, last_values):
        '''uses enum name as value when calling auto()'''
        return name

    ROBOT_MOVED = auto(), 'triggered when a robot movement is detected'
    NEW_MACHINE_DATA = auto(), 'triggered in high frequency when machine data has been read'
    PAUSE_AUTOMATION = auto(), 'call this event to pause any running automation; provide a description of the cause as string parameter'
    AUTOMATION_PAUSED = auto(), 'triggered when the automation has been paused; provides a description of the cause as string parameter'
    NEW_NOTIFICATION = auto(), 'call this event to notify the user; provide the message as string parameter'
    NEW_CAMERA = auto(), 'called if new camera has been discoverd; provides camera as parameter'
    NEW_DETECTIONS = auto(), 'called after detection on an image is completed; provides image frame as parameter'


def register(event: Id, listener: Union[Callable, Awaitable]):
    if not callable(listener):
        raise Exception('non-callable listener')
    if listener.__name__ == '<lambda>':  # NOTE lambda functions must be stored without weakref because they will be collected otherwise
        ref = listener
    elif inspect.ismethod(listener):
        ref = weakref.WeakMethod(listener)
    else:
        ref = weakref.ref(listener)
    log.debug(f'registered {listener} to {event}')
    listeners[event].add(ref)


def unregister(event: Id, listener: Union[Callable, Awaitable]):
    marked = []
    for registered in listeners[event]:
        if hasattr(listener, '__name__') and listener.__name__ == '<lambda>' and listener == registered:
            marked.append(listener)
        if registered() == listener:
            marked.append(registered)
    [listeners[event].remove(m) for m in marked]
    log.debug(f'unregistered {listener} from {event}')


async def call(event: Id, *args):
    '''Fires event and waits async until all registered listeners are completed'''
    # if event != Id.NEW_MACHINE_DATA:
    #     log.info(f'calling {event=}')
    for listener in list(listeners.get(event, {})):
        try:
            if event != Id.NEW_MACHINE_DATA:
                log.debug(f'emitting {event} with {listener}')
            if hasattr(listener, '__name__') and listener.__name__ == '<lambda>':
                listener(*args)
                continue
            if listener() is None:
                listeners[event].remove(listener)
                log.debug(f'unregistered {listener} from {event}')
                continue
            if inspect.iscoroutinefunction(listener()):
                await listener()(*args)
            else:
                listener()(*args)
        except:
            log.exception(f'could not call {listener=} for {event=}')


def emit(event: Id, *args):
    '''Fires event without waiting for the result.'''
    assert asyncio.get_running_loop()

    # if event != Id.ROBOT_MOVED:
    #     log.info(f'emitting {event=}')
    loop = asyncio.get_event_loop()
    for listener in list(listeners.get(event, {})):
        if event != Id.ROBOT_MOVED:
            log.debug(f'emitting {event} with {listener}')
        try:
            if hasattr(listener, '__name__') and listener.__name__ == '<lambda>':
                listener(*args)
                continue
            if listener() is None:
                unregister(event, listener)
                continue
            if inspect.iscoroutinefunction(listener()):
                tasks.append(loop.create_task(listener()(*args), name=f'handle {event=}'))
            else:
                listener()(*args)
        except:
            log.exception(f'could not call {listener=} for {event=}')
