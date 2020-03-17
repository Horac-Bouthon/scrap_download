import logging
import crawl_obj

module_logger = logging.getLogger(crawl_obj.LOGGER_NAME)


class CrawlerObject:

    @classmethod
    def from_none(cls):
        return cls("", "", "")

    def __init__(self,
                 code,
                 description,
                 kind,
                 ):
        self.logger = logging.getLogger(crawl_obj.LOGGER_NAME)
        self.code = code
        self.description = description
        self.kind = kind
        self.logger.debug('Create: {}'.format(repr(self)))

    @staticmethod
    def headers_csv_dict():
        ret_val = list()
        ret_val.append('code')
        ret_val.append('description')
        ret_val.append('kind')
        module_logger.debug('Send headers list: {}'.format(ret_val))
        return ret_val

    def to_csv_dict(self):
        ret_val = list()
        ret_val.append(self.code)
        ret_val.append(self.description)
        ret_val.append(self.kind)
        self.logger.debug('Send csv values: {}'.format(ret_val))
        return ret_val

    def to_json_dict(self):
        ret_val = dict()
        ret_val['code'] = self.code
        ret_val['description'] = self.description
        ret_val['kind'] = self.kind
        self.logger.debug('Send json dictionary: {}'.format(ret_val))
        return ret_val

    def to_json_dict_one_by_one(self):
        ret_val = dict()
        ret_val['code'] = self.code
        ret_val['description'] = self.description
        ret_val['kind'] = self.kind
        self.logger.debug('Send json one by one dictionary: {}'.format(ret_val))
        return ret_val

    def __repr__(self):
        return "CrawlerObject('{}', '{}', '{}')"\
            .format(self.code, self.description, self.kind)

    def __str__(self):
        return "{} - {} - {}".format(self.code, self.description, self.kind)
