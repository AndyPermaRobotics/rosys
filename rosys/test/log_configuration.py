import functools
import logging
import logging.config
import os
import sys
from typing import Optional

import coloredlogs
import icecream

import rosys

ABS_SYS_PATHS = sorted((os.path.abspath(p) + os.sep for p in sys.path), key=len, reverse=True)


class PackagePathFilter(logging.Filter):

    # https://stackoverflow.com/a/52582536/3419103
    @functools.lru_cache(maxsize=100)
    def find_relative_path(self, pathname: str) -> Optional[str]:
        for path in ABS_SYS_PATHS:
            if pathname.startswith(path):
                return os.path.relpath(pathname, path)
        return None

    def filter(self, record: logging.LogRecord) -> bool:
        record.relative_path = self.find_relative_path(record.pathname)
        return True


class RosysFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        from rosys.test.helpers import odometer as odo  # pylint: disable=import-outside-toplevel
        if odo:
            record.rosys_time = rosys.time()
            record.robot_pose = f'{odo.prediction.x:.2f}, {odo.prediction.y:1.2f}, {odo.prediction.yaw_deg:1.2f}'
        else:
            record.rosys_time = 0
            record.robot_pose = 'no robot pose yet'
        return True


def setup() -> None:
    icecream.install()

    config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                '()': coloredlogs.ColoredFormatter,
                'format': r'%(rosys_time).2f [%(levelname)s] %(robot_pose)s %(relative_path)s:%(lineno)d: %(message)s',
                'datefmt': r'%Y-%m-%d %H:%M:%S',
            },
        },
        'filters': {
            'package_path_filter': {
                '()': PackagePathFilter,
            },
            'rosys_filter': {
                '()': RosysFilter,
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'filters': ['package_path_filter', 'rosys_filter'],
                'level': 'INFO',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'rosys': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'rosys.ota': {
                'handlers': ['console'],
                'level': 'WARN',
                'propagate': False,
            }
        },
    }

    logging.config.dictConfig(config)
