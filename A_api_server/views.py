#!/usr/bin/env python
# encoding: utf-8

from aiohttp import web

from db import Session
from validation import validate


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
    drivers = session.query(Driver).filter_by(firm_id=device.firm_id)
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
