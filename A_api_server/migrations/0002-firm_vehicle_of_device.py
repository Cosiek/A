#!/usr/bin/env python
# encoding: utf-8

from db import engine
from migrator import BaseMigration
from models import Device


class Migration(BaseMigration):
    rollback_on_error = False
    depends_on = ['0001-add_driver_firm_vehicle_models.py']

    def run(self):
        conn = engine.connect()
        sql = "ALTER TABLE {} ADD COLUMN " \
              "firm_id INTEGER REFERENCES firms(id)"\
            .format(Device.__tablename__)
        conn.execute(sql)
        sql = "ALTER TABLE {} ADD COLUMN " \
              "vehicle_id INTEGER REFERENCES vehicles(id)"\
            .format(Device.__tablename__)
        conn.execute(sql)
