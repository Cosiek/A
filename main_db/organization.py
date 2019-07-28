#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base
from enums import TransportModeEnum


class Organizer(Base):
    __tablename__ = 'organizers'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    carriers = relationship("Carrier", secondary='organizer_carrier',
                            back_populates="organizers")
    lines = relationship('Line', back_populates='organizer')
    stations = relationship("Station", secondary="organizer_stations",
                            back_populates="organizers")


class Carrier(Base):
    __tablename__ = 'carriers'

    # fields
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)

    # relationships
    organizers = relationship("Organizer", secondary='organizer_carrier',
                              back_populates="carriers")
    drivers = relationship("Driver", secondary='driver_employment',
                           back_populates="carriers")
    vehicles = relationship("Vehicle", back_populates="carrier")


class OrganizerCarrier(Base):
    __tablename__ = 'organizer_carrier'

    organizer_id = Column(Integer, ForeignKey('organizers.id'), primary_key=True)
    carrier_id = Column(Integer, ForeignKey('carriers.id'), primary_key=True)


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=True)
    login = Column(String(64), unique=True, nullable=False)
    password = Column(String(16), nullable=False)

    # relationships
    carriers = relationship("Carrier", secondary='driver_employment',
                            back_populates="drivers")


class DriverEmployment(Base):
    __tablename__ = 'driver_employment'

    driver_id = Column(Integer, ForeignKey('drivers.id'), primary_key=True)
    carrier_id = Column(Integer, ForeignKey('carriers.id'), primary_key=True)
    driver_number = Column(String(64))
    is_active = Column(Boolean, default=True, nullable=False)


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=True)

    carrier_id = Column(Integer, ForeignKey('carriers.id'), nullable=True)
    carrier = relationship("Carrier", back_populates="vehicles")

    production_year = Column(Integer, nullable=True)
    vin = Column(String(17), nullable=True)
    registration = Column(String(12), nullable=True)
    capacity = Column(Integer, nullable=True)
    vehicle_type_id = Column(Integer, ForeignKey('vehicle_types.id'),
                             nullable=True)
    vehicle_type = relationship("VehicleType", back_populates="vehicles")
    devices = relationship("Device", back_populates="vehicle")


class VehicleType(Base):
    __tablename__ = 'vehicle_types'

    id = Column(Integer, primary_key=True)

    mode = Column(Enum(TransportModeEnum), nullable=False)
    brand = Column(String(32), unique=False, nullable=False)
    name = Column(String(64), unique=True, nullable=False)

    vehicles = relationship("Vehicle", back_populates="vehicle_type")
