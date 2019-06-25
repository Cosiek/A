#!/usr/bin/env python
# encoding: utf-8

import argparse
from uuid import uuid4

from db import Session
from models import Device


def add_new_device(count):
    session = Session()
    for i in range(count):
        # generate name
        name = str(uuid4())[:13]
        # check if name isn't used yet
        while session.query(Device).filter_by(name=name).first():
            name = str(uuid4())[:13]
        # generate key
        key = str(uuid4()).replace("-", "")
        # create devices
        session.add(Device(name=name, key=key, timestamp=0))
    session.commit()


if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=1,
                        help="How many devices should be created")
    args = parser.parse_args()

    add_new_device(args.count)
