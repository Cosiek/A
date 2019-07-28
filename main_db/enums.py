#!/usr/bin/env python
# encoding: utf-8

import enum


@enum.unique
class TransportModeEnum(enum.Enum):
    BUS = 1
    TROLLEY = 2
    TRAM = 3
    TRAIN = 4
    SUBWAY = 5
    FERRY = 6


@enum.unique
class EventType(enum.Enum):
    DEVICE_INSTALLATION = 1
    DEVICE_REGISTRATION = 2
    USER_LOGIN = 3
    USER_LOGOUT = 4
    TASK_CHOSEN = 5
    LOCATION_LOGGED = 6
