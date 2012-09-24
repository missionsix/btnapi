"""
JSON-RPC interface to the BTNAPI

Author:  missionsix <btn-api@missionsix.net>
Date:  Sept 2012
"""
import httplib
import json
import random
import string
import types
import urllib

from itertools import count

class BTNAPIException(Exception):
    def __init__(self, status, msg):
        super(BTNAPIException, self).__init__("%d: %s" %(status, msg))


IDCHARS = string.ascii_lowercase+string.digits
def random_id(length=8):
    return_id = ''
    for i in range(length):
        return_id += random.choice(IDCHARS)
    return return_id


def dumps(params=[], method=None, encoding='utf-8', rpcid=None, notify=None):
    s = {"jsonrpc": "2.0"}

    if not isinstance(method, str):
        raise ValueError('Method name must be a string')

    s['method'] = method
    if params:
        s['params'] = params

    if not notify:
        s['id'] = rpcid if rpcid else random_id()
            
    return json.dumps(s, encoding=encoding)


def loads(data):
    if not data:
        return None
    return json.loads(data)


class _Request:
    def __init__(self, call, name):
        self.__call = call
        self.__name = name

    def __call__(self, *args, **kwargs):
        if len(args) > 0:
            return self.__call(self.__name, args)
        else:
            return self.__call(self.__name, kwargs)


class BtnApi:

    __port = 80
    __conn = None
    __rpcid = 0

    def __init__(self, api_key, btn_uri, api_port=80):
        self.api_key = api_key
        self.__port = api_port
        
        schema, uri = urllib.splittype(btn_uri)
        if schema not in ('http', 'https'):
            raise IOError('Unsupported JSON-RPC protocol.')

        self.__host, self.__handler = urllib.splithost(uri)
        if not self.__handler:
            self.__handler = '/'

        self.__conn = httplib.HTTPConnection(self.__host, self.__port)
        

    def __request(self, method, req_params=None):
        params = [self.api_key]
        if req_params is not None:
            params.extend(req_params)

        self.__rpcid = random_id()
        request = dumps(params, method, rpcid=self.__rpcid)
        headers = {'Content-Type': 'application/json'}
        self.__conn.request('POST', self.__handler, body=request, headers=headers)

        resp = self.__conn.getresponse()

        if resp.status != 200:
            raise BTNAPIException(resp.status, resp.reason)

        result = loads(resp.read())
        return self.__result(result)


    def __result(self, response):
        if response['id'] != self.__rpcid:
            raise BTNAPIException(500, 'Invalid Response from server.')

        if 'error' in response:
            raise BTNAPIException(response['error']['code'],
                                  response['error']['message'])

        return response['result']


    def __getattr__(self, name):
        return _Request(self.__request, name)


    def __del__(self):
        if self.__conn:
            self.__conn.close()

    
