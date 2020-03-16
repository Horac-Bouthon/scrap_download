import json

import logging
import json_wrapper


class JsonWrapper:

    @classmethod
    def from_none(cls):
        return cls("")

    def load_string(self):
        self.dict = json.loads(self.string)

    def get_json_str(self):
        mezo = json.dumps(self.dict, indent=2, ensure_ascii=False).encode('utf8')
        ret_val = mezo.decode()
        self.logger.debug('Generate json: {}'.format(ret_val))
        return ret_val

    def get_json_str(self):
        mezo = json.dumps(self.dict, indent=2, ensure_ascii=False).encode('utf8')
        ret_val = mezo.decode()
        self.logger.debug('Generate json str: {}'.format(ret_val))
        return ret_val

    def get_json(self):
        return self.dict

    def __init__(self, string):
        self.logger = logging.getLogger(json_wrapper.LOGGER_NAME)
        self.string = string
        self.header = dict()
        self.dict = dict()
        self.logger.info('Create: {}'.format(repr(self)))

    def __repr__(self):
        return "JsonWrapper('{}')"\
            .format(self.string)

    def __str__(self):
        return self.string
