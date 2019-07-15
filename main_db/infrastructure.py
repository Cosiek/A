#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from db import Base
from enums import TransportModeEnum


class Station(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=False)

    platforms = relationship("Platform", back_populates='station')


class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=True)
    mode = Column(Enum(TransportModeEnum), nullable=False)
    # location = Column()  # TODO

    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    station = relationship("Station", back_populates="platforms")

    outgoing = relationship("Section", back_populates="start_platform",
                            foreign_keys='Section.start_platform_id')
    incoming = relationship("Section", back_populates="end_platform",
                            foreign_keys='Section.end_platform_id')


class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=False, nullable=True)
    mode = Column(Enum(TransportModeEnum), nullable=False)

    start_platform_id = Column(Integer, ForeignKey('platforms.id'),
                               nullable=False)
    start_platform = relationship("Platform", back_populates="outgoing",
                                  foreign_keys=[start_platform_id])

    end_platform_id = Column(Integer, ForeignKey('platforms.id'),
                             nullable=False)
    end_platform = relationship("Platform", back_populates="incoming",
                                foreign_keys=[end_platform_id])
