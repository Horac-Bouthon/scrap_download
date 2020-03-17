import requests
import sys
import json
from json_wrapper.json_wrapper import JsonWrapper

import logging
import api_wrapper


class ApiWrapper:

    def post_json(self, json_obj):
        try:
            r = requests.post(self.url, json=json_obj, headers={"Content-Type": "application/json"})
            self.logger.debug('Post (json) response: {}'.format(r))
            self.logger.debug('Post (json) response text: {}'.format(r.text))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.logger.error('Exception - post_json: {}'.format(exc_value))

    def __init__(self, url):
        self.logger = logging.getLogger(api_wrapper.LOGGER_NAME)
        self.url = url
        self.logger.debug('Create: {}'.format(repr(self)))

    def __repr__(self):
        return "ApiWrapper('{}')"\
            .format(self.url)

    def __str__(self):
        return self.url
