#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings


engine = create_engine(settings.DATABASE['db_url'])

Base = declarative_base()

metadata = Base.metadata

Session = sessionmaker(bind=engine)


def db_session(f):
    async def wrapper(request):
        session = Session()
        try:
            request['db_session'] = session
            resp = await f(request)
            return resp
        except:
            session.rollback()
            raise
        finally:
            session.close()
    return wrapper
