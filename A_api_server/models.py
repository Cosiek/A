#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from db import Base


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String(13), unique=True)
    key = Column(String(32))
    timestamp = Column(Integer)
    is_active = Column(Boolean, default=True, nullable=False)

    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    vehicle = relationship("Vehicle", uselist=False, back_populates="devices")

    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=True)
    driver = relationship("Driver", uselist=False, back_populates="device")

    firm_id = Column(Integer, ForeignKey('firms.id'))
    firm = relationship("Firm", back_populates="devices")


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    vin = Column(String(13), unique=True)
    name = Column(String(13))
    is_active = Column(Boolean, default=True, nullable=False)

    firm_id = Column(Integer, ForeignKey('firms.id'))
    firm = relationship("Firm", back_populates="vehicles")

    __table_args__ = (UniqueConstraint('firm_id', 'name',
                                       name='_firm_vehicle'),)


Vehicle.devices = relationship("Device", back_populates="vehicle")


class Firm(Base):
    __tablename__ = 'firms'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    is_active = Column(Boolean, default=True, nullable=False)


Firm.devices = relationship("Device", back_populates="firm")
Firm.drivers = relationship("Driver", back_populates="firm")
Firm.vehicles = relationship("Vehicle", back_populates="firm")


class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    password = Column(String(12))
    is_active = Column(Boolean, default=True, nullable=False)

    firm_id = Column(Integer, ForeignKey('firms.id'))
    firm = relationship("Firm", back_populates="drivers")

    device = relationship("Device", uselist=False, back_populates="driver")

    __table_args__ = (UniqueConstraint('firm_id', 'name', name='_firm_worker'),)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'firm_id': self.firm_id,
        }
