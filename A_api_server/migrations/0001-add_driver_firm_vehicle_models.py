#!/usr/bin/env python
# encoding: utf-8

from db import engine, metadata
from migrator import BaseMigration
from models import Driver, Firm, Vehicle


class Migration(BaseMigration):
    rollback_on_error = False
    depends_on = ['0000-initial.py']

    def run(self):
        metadata.create_all(engine, tables=[Driver.__table__, Firm.__table__,
                                            Vehicle.__table__])
