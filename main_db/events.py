#!/usr/bin/env python
# encoding: utf-8

from geoalchemy2.types import Geography
from sqlalchemy import Column, Enum, ForeignKey, Integer, TIMESTAMP, JSON
from sqlalchemy.orm import relationship

from db import Base
from enums import EventType


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)

    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=True)
    vehicle = relationship('Vehicle', back_populates='devices')

    entries = relationship('Entry', back_populates='device')


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)

    device_id = Column(Integer, ForeignKey('devices.id'), nullable=True)
    device = relationship('Device', back_populates='entries')

    timestamp = Column(TIMESTAMP(True))
    location = Column(Geography(geometry_type='POINT'))
    event = Column(Enum(EventType))
    additional_data = Column(JSON(True))
