import logging
import logger_wrapper
import argparse
import os
import json

from convert_http.http_convert import HttpConverter
from crawl_obj.crawler_obj import CrawlerObject
from json_wrapper.json_wrapper import JsonWrapper
from api_wrapper.api_wrapper import ApiWrapper
from ini_wrapper.ini_wrapper import IniWrapper
from logger_wrapper.logger_wrapper import LoggerWrapper
from cron_wrapper.cron_wrapper import CronWrapper
from xlsx_wrapper.xlsx_wrapper import XlsxWrapper

in_args = argparse.ArgumentParser()
in_args.add_argument('-i', '--install', help='Install/update cron table')
in_args.add_argument('-u', '--uninstall', help='Delete cron table', action='store_true')
in_args.add_argument('-c', '--config', type=str,  help='Set alternative *ini file')
in_args.add_argument('-t', '--crontab', help='List configured cron table', action='store_true')
in_args.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
in_args.add_argument('-ll', '--log_level', help='Set log level for this run.',
                     choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
in_args.add_argument('-s', '--api_send', help='Type of API send: batch or one by one .',
                     choices=['BATCH', 'ONE_BY_ONE'])
akt_args = in_args.parse_args()

lw = LoggerWrapper()
logger_name = logger_wrapper.LOGGER_NAME
logger = logging.getLogger(logger_name)
if akt_args.log_level:
    logger = lw.set_logger(logger, akt_args.verbose, akt_args.log_level)
elif akt_args.verbose:
    logger = lw.set_logger(logger, akt_args.verbose)
else:
    logger = lw.set_logger(logger)


def py_touch(filename):
    dir_tc = os.path.dirname(os.path.abspath(filename))
    if not os.path.isdir(dir_tc):
        os.mkdir(dir_tc)
    return


def crawl():
    logger.info("--------- Start crawling ----------")

    if akt_args.config:
        str_config = akt_args.config
    else:
        str_config = 'main.ini'

    if not os.path.isfile(str_config):
        logger.error("Can't find config file {}".format(str_config))
        raise Exception("Can't find config file {}".format(str_config))

    ini_obj = IniWrapper(str_config)
    ini_obj.read_data()

    if akt_args.api_send:
        str_api = akt_args.api_send
    elif 'ApiType' in ini_obj.data:
        str_api = ini_obj.data['ApiType']
    else:
        str_api = 'BATCH'

    if 'down_sites' in ini_obj.data:
        # download - parse - send
        for site_url in ini_obj.data['down_sites']:
            print('site url = {}'.format(site_url))
            direct = HttpConverter()
            direct.work_file = ini_obj.data['work_file']
            direct.load_site(site_url)
            py_touch(direct.work_file)
            file_name = direct.st_download_file()
            # read xlsx
            xslx_obj = XlsxWrapper(file_name)
            xslx_obj.read_file(6)
            # save to objects
            katalog = list()
            for line in xslx_obj.data:
                co = CrawlerObject.from_none()
                co.code = line[1]
                co.description = line[2]
                if (line[3] is None) or (not line[3]):
                    co.kind = 'G'
                else:
                    co.kind = line[3]
                katalog.append(co.to_json_dict())

            # --------------- extension file
            ext_file = ini_obj.data['extension_file']
            py_touch(ext_file)
            if os.path.isfile(ext_file):
                xslx_ext = XlsxWrapper(ext_file)
                xslx_ext.read_file()
                for line in xslx_ext.data:
                    co = CrawlerObject.from_none()
                    co.code = line[1]
                    co.description = line[2]
                    if (line[3] is None) or (not line[3]):
                        co.kind = 'G'
                    else:
                        co.kind = line[3]
                    katalog.append(co.to_json_dict())

            json_obj = JsonWrapper.from_none()
            json_obj.dict[ini_obj.data['JsonMainKey']] = katalog
            a_w = ApiWrapper(ini_obj.data['ApiUrl'])
            a_w.post_json(json_obj.get_json())
            logger.info(json_obj.get_json_str())
            # print(json_obj.get_json_str())
            ###########################
    else:
        logger.error('Ini file {}: down_sites not defined !!!'.format(str_config))

    logger.info('--------- END ----------')
    return


def install():
    logger.info("--------- Install cron ----------")
    if akt_args.config:
        str_config = akt_args.config
    else:
        str_config = 'main.ini'
    if not os.path.isfile(str_config):
        logger.error("Can't find config file {}".format(str_config))
        raise Exception("Can't find config file {}".format(str_config))
    ini_obj = IniWrapper(str_config)
    ini_obj.read_data()

    cron = CronWrapper(akt_args.install, ini_obj.data['CronCommand'])
    cron.install()

    logger.info('--------- END ----------')
    return


def list_cron():
    logger.info("--------- List cron ----------")
    if akt_args.config:
        str_config = akt_args.config
    else:
        str_config = 'main.ini'
    if not os.path.isfile(str_config):
        logger.error("Can't find config file {}".format(str_config))
        raise Exception("Can't find config file {}".format(str_config))
    ini_obj = IniWrapper(str_config)
    ini_obj.read_data()

    cron = CronWrapper(None, ini_obj.data['CronCommand'])
    file_content = cron.crontab_list
    print("List of existing cron commands:")
    for line in file_content:
        if not line.startswith("#"):
            if not line.startswith("\n"):
                print(line)
    logger.info('--------- END ----------')
    return


def uninstall_cron():
    logger.info("--------- Uninstall cron ----------")
    if akt_args.config:
        str_config = akt_args.config
    else:
        str_config = 'main.ini'
    if not os.path.isfile(str_config):
        logger.error("Can't find config file {}".format(str_config))
        raise Exception("Can't find config file {}".format(str_config))
    ini_obj = IniWrapper(str_config)
    ini_obj.read_data()

    cron = CronWrapper(None, ini_obj.data['CronCommand'])
    cron.uninstall_cron()

    logger.info('--------- END ----------')
    return


def main():
    if akt_args.install:
        install()
    elif akt_args.crontab:
        list_cron()
    elif akt_args.uninstall:
        uninstall_cron()
    else:
        crawl()
    return


if __name__ == '__main__':
    main()
