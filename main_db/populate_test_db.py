#!/usr/bin/env python
# encoding: utf-8

import json

from db import Session

from calendar import *
from enums import TransportModeEnum
from infrastructure import Station, Platform, Section
from organization import (Organizer, Carrier, Driver, VehicleType, Vehicle,
                          DriverEmployment, OrganizerCarrier)
from schedule import *


def populate_infrastructure(session):
    data = {
        "Osiedle Górczewska": {
            "platforms": {
                "01": {
                    "previous": [("Coopera II", "01")]
                },
                "02": {
                    "previous": [("Bemowo Ratusz", "01")]
                },
                "03": {"previous": []},
            }
        },
        "Bemowo Ratusz": {
            "platforms": {
                "01": {
                    "previous": [("Osiedle Górczewska", "01")]
                },
                "02": {"previous": []},
            }
        },
        "Coopera II": {
            "platforms": {
                "01": {
                    "previous": [("Osiedle Górczewska", "03")]
                },
            }
        }}

    # add some stations
    for station_name in data.keys():
        data[station_name]['instance'] = Station(name=station_name)
        session.add(data[station_name]['instance'])
    session.commit()
    # add some platforms to those stations
    for station_name, station_data in data.items():
        station = data[station_name]['instance']
        for platform_name, platform_data in station_data["platforms"].items():
            instance = Platform(name=platform_name, station_id=station.id,
                                mode=TransportModeEnum.BUS)
            platform_data['instance'] = instance
            session.add(instance)
    session.commit()
    # and connect them with sections
    for station_name, station_data in data.items():
        for platform_name, platform_data in station_data["platforms"].items():
            end_platform = platform_data['instance']
            # get instance for "previous"
            for s_name, p_name in platform_data["previous"]:
                start_platform = data[s_name]["platforms"][p_name]["instance"]
                session.add(Section(mode=TransportModeEnum.BUS,
                                    start_platform_id=start_platform.id,
                                    end_platform_id=end_platform.id))
    session.commit()


def populate_organization(session, fixture):
    for model in [Organizer, Carrier, Driver, VehicleType, Vehicle,
                  DriverEmployment, OrganizerCarrier]:
        for object_data in fixture.get(model.__tablename__, []):
            session.add(model(**object_data))


if __name__ == "__main__":
    # read fixture
    with open('fixture.json', 'r') as f:
        fixture = json.loads(f.read())

    session = Session()
    #populate_infrastructure(session)
    populate_organization(session, fixture)
    session.commit()
