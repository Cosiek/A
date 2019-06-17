#!/usr/bin/env python
# encoding: utf-8

import json

from aiohttp import web


async def device_register(request):
    # validate request
    # TODO: move unpacking/validating params somhwere else
    params = json.loads(await request.text())
    print(params)
    device_id = params.get("id")
    device_signature = params.get("signature")

    print("↔", device_id, device_signature)
    if device_id is None or device_signature is None:
        return web.Response(text="Bad Request", status=400)
    # get device data from db
    # generate signature based on passed data
    local_signature = "123"
    print(device_signature, local_signature, device_signature == local_signature)
    # compare signatures
    if device_signature != local_signature:
        return web.Response(text="Unauthorized", status=401)
    return web.Response(text="Ok", status=200)
