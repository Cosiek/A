#!/usr/bin/env python
# encoding: utf-8

import json

from db import Session

from calendar_ import *
from enums import TransportModeEnum
from infrastructure import Station, Platform, Section, OrganizerStation
from organization import (Organizer, Carrier, Driver, VehicleType, Vehicle,
                          DriverEmployment, OrganizerCarrier)
from schedule import *


def populate_infrastructure(session, fixture):
    for model in [Station, Platform, Section, OrganizerStation]:
        for object_data in fixture.get(model.__tablename__, []):
            session.add(model(**object_data))


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
    populate_organization(session, fixture)
    populate_infrastructure(session, fixture)
    session.commit()
