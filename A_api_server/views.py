#!/usr/bin/env python
# encoding: utf-8

import hashlib
import hmac
import json

from aiohttp import web


def get_signature(params, key):
    # prepare data
    data = params.copy()
    del data['signature']
    dt = ""
    # dict fails as it might alter keys ordering
    for k in sorted(data.keys()):
        dt += str(k) + str(data[k])
    print(dt)
    # calculate signature
    # TODO: use OpenSSL
    m = hmac.new(key.encode('utf-8'), dt.encode('utf-8'), hashlib.md5)
    x = m.hexdigest()
    print(x)
    return x


async def validate(request):
    try:
        params = json.loads(await request.text())
    except json.decoder.JSONDecodeError:
        # invalid data
        return False, {'text': "Bad Request", 'status': 400}, None

    device_id = params.get("id")
    device_signature = params.get("signature")

    if device_id is None or device_signature is None:
        return False, {'text': "Bad Request", 'status': 400}, None

    # get device data from db
    device = {"id": device_id, "key": "123"}  # mock - for now
    if device is None:
        return False, {'text': "Not Found", 'status': 404}, None
    # generate signature based on passed data
    local_key = device["key"]
    print(device_signature)
    local_signature = get_signature(params, local_key)

    # compare signatures
    if device_signature == local_signature:
        return True, {'text': "Ok", 'status': 200}, None
    else:
        return True, {'text': "Unauthorized", 'status': 401}, params


async def device_register(request):
    """
    Validates if signature key passed to device registration form
    is valid. This view doesn't write anything.
    """
    is_valid, response_kwargs, _ = await validate(request)
    return web.Response(**response_kwargs)
