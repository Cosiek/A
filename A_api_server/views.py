#!/usr/bin/env python
# encoding: utf-8

import json

from aiohttp import web

from db import db_session
from models import Driver
from validation import view_validation


# Device registration -----------------

@db_session
@view_validation()
async def device_register(request):
    """
    Validates if signature key passed to device registration form
    is valid. This view doesn't write anything.
    """
    return web.Response(**request['response_kwargs'])


# Driver login ------------------------

@db_session
@view_validation(update_t=False)
async def drivers(request):
    """
    Returns a list of drivers associated with devices firm and some data
    needed for driver login.
    """
    if not request['is_valid']:
        return web.Response(**request['response_kwargs'])
    # get list of drivers working for devices firm
    drivers_ = request['db_session'].query(Driver)\
        .filter_by(firm_id=request['device'].firm_id, is_active=True)
    # serialize data
    d = {
        "last": None,  # TODO: retrieve suggested driver instead of last one
        "list": [d.to_dict() for d in drivers_],
        "passwordRequired": True,  # TODO: keep password required for now
    }
    # prepare data package
    request['response_kwargs']['text'] = json.dumps(d)
    return web.Response(**request['response_kwargs'])


@db_session
@view_validation(required_params=['login', 'password'])
async def driver_login(request):
    """
    Returns with Ok (200) status if login was successful
    """
    response_kwargs, device = request['response_kwargs'], request['device']
    params = request['params']
    if not request['is_valid']:
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
    # update device driver
    device.driver_id = driver.id
    # TODO: write event
    # respond
    return web.Response(**response_kwargs)


@db_session
@view_validation()
async def driver_logout(request):
    """
    Returns with Ok (200) status if logout was successful
    """
    response_kwargs, device = request['response_kwargs'], request['device']
    if not request['is_valid']:
        return web.Response(**response_kwargs)
    # update device driver
    device.driver_id = None
    # TODO: write event
    # respond
    return web.Response(**response_kwargs)
