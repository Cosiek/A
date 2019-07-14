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
