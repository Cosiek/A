#!/usr/bin/env python
# encoding: utf-8

import json

from aiohttp import web

from db import db_session
from models import Driver
from validation import validate


# Device registration -----------------

@db_session
async def device_register(request):
    """
    Validates if signature key passed to device registration form
    is valid. This view doesn't write anything.
    """
    _, response_kwargs, _, _ = await validate(request, request['db_session'])
    return web.Response(**response_kwargs)


# Driver login ------------------------

@db_session
async def drivers(request):
    """
    Returns a list of drivers associated with devices firm and some data
    needed for driver login.
    """
    # validate request
    is_valid, response_kwargs, device, params = await validate(
        request, request['db_session'])
    if not is_valid:
        return web.Response(**response_kwargs)
    # get list of drivers working for devices firm
    drivers_ = request['db_session'].query(Driver)\
        .filter_by(firm_id=device.firm_id, is_active=True)
    # serialize data
    d = {
        "last": None,  # TODO: pass
        "list": [d.to_dict() for d in drivers_],
        "passwordRequired": True,  # TODO: keep password required for now
    }
    # prepare data package
    response_kwargs['text'] = json.dumps(d)
    # TODO update device timestamp
    return web.Response(**response_kwargs)


@db_session
async def driver_login(request):
    """
    Returns with Ok (200) status if login was successful
    """
    # validate request
    required = ['login', 'password']
    is_valid, response_kwargs, device, params = \
        await validate(request, request['db_session'], required)
    if not is_valid:
        return web.Response(**response_kwargs)
    # search db against given params
    driver = request['db_session'].query(Driver) \
        .filter_by(firm_id=device.firm_id, is_active=True, name=params['login'],
                   password=params['password']) \
        .first()
    if driver is None:
        response_kwargs['status'] = 401
        response_kwargs['text'] = "Błędny login lub hasło."
        return web.Response(**response_kwargs)
    # TODO: update device timestamp and driver
    # write event
    # respond
    return web.Response(**response_kwargs)
