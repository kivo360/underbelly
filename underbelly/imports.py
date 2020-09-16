import abc
import base64
import collections
import uuid
import copy
import functools
import inspect
import multiprocessing
import random
import threading
import time
import typing
from hashlib import md5
from typing import Optional, Union, OrderedDict, Iterator, Tuple, Callable

import numpy as np
import toolz
from loguru import logger
from toolz import curried
from toolz.curried import (
    filter, itemmap, iterate, keyfilter, keymap, map, merge, pipe, reduce
)
from pydantic import BaseModel as base_model, create_model
from auto_all import start_all, end_all

from toolz.functoolz import curry

abstractmethod = abc.abstractmethod

MPool = multiprocessing.Pool
Manager = multiprocessing.Manager
MQueue = multiprocessing.Queue
TLocal = threading.local
TLock = threading.Lock


class VerificationType(abc.ABCMeta):
    """ We use this to check if the proper variables are available after the init function """

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj._post_init_hooks()
        return obj


__all__ = [
    "random",
    "abc",
    'start_all',
    'OrderedDict',
    'end_all',
    'base_model',
    'copy',
    'merge',
    "typing",
    "time",
    'threading',
    'Iterator',
    'base64',
    "logger",
    'Union',
    'Callable',
    'toolz',
    'np',
    'md5',
    'functools',
    'MPool',
    'Manager',
    'MQueue',
    'curried',
    'TLocal',
    'TLock',
    'abstractmethod',
    'Optional',
    'uuid',
    'Tuple',
    'collections',
    'curry',
    'inspect',
    'VerificationType',
    'reduce',
    'pipe',
    'map',
    'filter',
    'itemmap',
    'iterate',
    'keyfilter',
    'keymap',
]
