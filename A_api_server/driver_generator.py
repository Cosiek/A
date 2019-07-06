#!/usr/bin/env python
# encoding: utf-8

import argparse
import random
from uuid import uuid4

from db import Session
from models import Driver
from validation import obscure


def get_random_name():
    first_names = ["Cosiek", "Martyna", "Morela", "Irmina"]
    last_names = ["Maksym", "Majchrzak",]
    return random.choice(first_names) + " " + random.choice(last_names)


def add_new_driver(count, writeout=True):
    session = Session()
    data = []
    for i in range(count):
        # generate name
        name = get_random_name()
        # check if name isn't used yet
        while session.query(Driver).filter_by(name=name).first():
            name = get_random_name()
        # generate password
        password = str(uuid4())[:4].replace("-", "")
        # obscure password before passing to db
        obscured = obscure(password)
        # create devices
        session.add(Driver(name=name, password=obscured, firm_id=1))
        data.append((name, password, obscured))
    # write out passwords to a file
    if writeout:
        file_name = '/tmp/drivers.txt'
        with open(file_name, 'w') as f:
            f.write("\n".join((" ".join(e) for e in data)))

    session.commit()


if __name__ == "__main__":
    # TODO: combine generator scripts
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=1,
                        help="How many drivers should be created")
    parser.add_argument("-w", "--write", action="store_true",
                        help="Should generated data be written to a text file")
    args = parser.parse_args()

    add_new_driver(args.count, args.write)
