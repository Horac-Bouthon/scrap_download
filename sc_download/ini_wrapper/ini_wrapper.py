import configparser
import os

import logging
import ini_wrapper


class IniWrapper:

    def __init__(self,
                 file_name
                 ):
        self.logger = logging.getLogger(ini_wrapper.LOGGER_NAME)
        self.data = dict()
        self.file_name = file_name
        if os.path.isfile(file_name):
            self.config = configparser.ConfigParser()
            self.config.read(self.file_name)
        else:
            self.config = None
        self.logger.info('Create: {}'.format(repr(self)))

    def read_data(self):
        """ Modify to load data for specific application """
        """ 
        if self.config and self.config['SECTION']['my_ini_var']:
            set_value = self.config['MAIN']['my_ini_var'].replace('"', '')
            self.data['my_ini_var'] = set_value
        else:
            self.data['my_ini_var'] = 'default value'
        """
        if self.config and \
                ('MAIN' in self.config) and \
                ('down_sites' in self.config['MAIN']):
            mez_value = self.config['MAIN']['down_sites'].replace('"', '')
            set_value = mez_value.strip("][").split(", ")
            self.data['down_sites'] = set_value
        else:
            self.data['down_sites'] = ['https://www.katalogodpadu.cz/ke-stazeni.php', ]

        if self.config and \
                ('MAIN' in self.config) and \
                ('work_file' in self.config['MAIN']):
            set_value = self.config['MAIN']['work_file'].replace('"', '')
            self.data['work_file'] = set_value
        else:
            self.data['work_file'] = './data/katalog.xlsx'

        if self.config and \
                ('MAIN' in self.config) and \
                ('extension_file' in self.config['MAIN']):
            set_value = self.config['MAIN']['extension_file'].replace('"', '')
            self.data['extension_file'] = set_value
        else:
            self.data['extension_file'] = './data/extension.xlsx'

        if self.config and \
                ('MAIN' in self.config) and \
                ('JsonMainKey' in self.config['MAIN']):
            set_value = self.config['MAIN']['JsonMainKey'].replace('"', '')
            self.data['JsonMainKey'] = set_value
        else:
            self.data['JsonMainKey'] = 'products'

        if self.config and \
                ('MAIN' in self.config) and \
                ('ApiUrl' in self.config['MAIN']):
            set_value = self.config['MAIN']['ApiUrl'].replace('"', '')
            self.data['ApiUrl'] = set_value
        else:
            self.data['ApiUrl'] = 'http://httpbin.org/post'

        if self.config and \
                ('MAIN' in self.config) and \
                ('CronCommand' in self.config['MAIN']):
            set_value = self.config['MAIN']['CronCommand'].replace('"', '')
            self.data['CronCommand'] = set_value
        else:
            self.data['CronCommand'] = 'python3 main.py'

        if self.config and \
                ('MAIN' in self.config) and \
                ('ApiType' in self.config['MAIN']):
            set_value = self.config['MAIN']['ApiType'].replace('"', '')
            self.data['ApiType'] = set_value
        else:
            self.data['ApiType'] = 'BATCH'

        self.logger.info('Set data: {}'.format(self.data))

    def __repr__(self):
        return "IniWrapper('{}')"\
            .format(self.file_name)

    def __str__(self):
        return self.file_name

