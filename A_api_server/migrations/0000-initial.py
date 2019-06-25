#!/usr/bin/env python
# encoding: utf-8

from db import engine, metadata
from migrator import BaseMigration
from models import Device


class Migration(BaseMigration):
    rollback_on_error = False

    def run(self):
        metadata.create_all(engine, tables=[Device.__table__,])
