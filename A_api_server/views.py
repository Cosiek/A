#!/usr/bin/env python
# encoding: utf-8

import json

from aiohttp import web

from db import Session
from models import Driver
from validation import validate


# Device registration -----------------

async def device_register(request):
    """
    Validates if signature key passed to device registration form
    is valid. This view doesn't write anything.
    """
    ses = Session()
    is_valid, response_kwargs, _, _ = await validate(request, ses)
    ses.close()
    return web.Response(**response_kwargs)


# Driver login ------------------------

async def drivers(request):
    """
    Returns a list of drivers associated with devices firm and some data
    needed for driver login.
    """
    session = Session()
    # validate request
    is_valid, response_kwargs, device, params = await validate(request, session)
    if not is_valid:
        session.close()
        return web.Response(**response_kwargs)
    # get list of drivers working for devices firm
    drivers = session.query(Driver)\
            .filter_by(firm_id=device.firm_id, is_active=True)
    # serialize data
    d = {
        "last": None,  # TODO: pass
        "list": [],
        "passwordRequired": True,  # TODO: keep password required for now
    }
    for driver in drivers:
        d["list"].append(driver.to_dict())
    # prepare data package
    response_kwargs['text'] = json.dumps(d)
    # TODO update device timestamp
    session.close()
    return web.Response(**response_kwargs)


async def driver_login(request):
    """
    Returns with Ok (200) status if login was successful
    """
    # validate request
    session = Session()
    # validate request
    required = ['login', 'password']
    is_valid, response_kwargs, device, params = await validate(request, session,
                                                               required)
    if not is_valid:
        session.close()
        return web.Response(**response_kwargs)
    # search db against given params
    driver = session.query(Driver).filter_by(firm_id=device.firm_id,
                                             is_active=True,
                                             name=params['login'],
                                             password=params['password'])\
                                  .first()
    if driver is None:
        response_kwargs['status'] = 401
        response_kwargs['text'] = "Błędny login lub hasło."
        return web.Response(**response_kwargs)
    # TODO: update device timestamp and driver
    # write event
    session.close()
    # respond
    return web.Response(**response_kwargs)
