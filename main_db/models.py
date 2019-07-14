#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from db import Base
from enums import TransportModeEnum


class Organizer(Base):
    __tablename__ = 'organizers'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)


class Carrier(Base):
    __tablename__ = 'carriers'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=True)
    login = Column(String(64), unique=True, nullable=False)
    password = Column(String(16), nullable=False)


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)

    carrier_id = Column(Integer, ForeignKey('carriers.id'), nullable=True)
    name = Column(String(64), unique=False, nullable=True)

    production_year = Column(Integer, nullable=True)
    vin = Column(String(17), nullable=True)
    registration = Column(String(12), nullable=True)
    type_id = Column(Integer, ForeignKey('vehicle_types.id'), nullable=True)
    capacity = Column(Integer, nullable=True)


class VehicleType(Base):
    __table__ = 'vehicle_types'

    id = Column(Integer, primary_key=True)

    mode = Column(Enum(TransportModeEnum), nullable=False)
    brand = Column(String(32), unique=False, nullable=False)
    name = Column(String(64), unique=True, nullable=False)
