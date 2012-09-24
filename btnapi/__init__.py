#/usr/bin/python
"""
pyBTN API library

A python python package used for utilizing the BTN API.

Author: missionsix <btn-api@missionsix.net>
Date: 2012
"""
import ConfigParser
import os
import sys

CONFIG_FILE = os.path.expanduser('~/.config/btn-api')

config = ConfigParser.SafeConfigParser()
if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)
else:
    config.add_section('config')
    config.set('config', 'api-key', "YOUR API KEY")
    config.set('config', 'api-host', "http://api.btnapps.net/")
    config.set('config', 'api-port', '80')
    with open(CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)

if not config.has_option('config', 'api-key'):
    raise ConfigParser.ParsingError("Invalid config file: %s"% CONFIG_FILE)

api_key = config.get('config', 'api-key')
api_host = config.get('config', 'api-host')
api_port = config.getint('config', 'api-port')

if api_key is None:
    raise ConfigParser.Error("Invalid API key in config file: %s" % CONFIG_FILE)

from btnapi import BtnApi
sys.modules[__name__] = BtnApi(api_key, api_host, api_port)
