
import os
import sys
import logging
import cron_wrapper


def touch(file_name):
    if os.path.exists(file_name):
        os.utime(file_name, None)
    else:
        open(file_name, 'a').close()


class CronWrapper:

    def __init__(self,
                 cron_text='0/1 * * ? *',
                 action=None
                 ):
        self.logger = logging.getLogger(cron_wrapper.LOGGER_NAME)
        self.cron_text = cron_text
        self.action = action
        self.logger.info('Create: {}'.format(repr(self)))

    def crontab_get_string(self):
        """ Modify to set cron command """
        set_command = ""
        set_command += 'cd {}'.format(sys.path[0])
        set_command += ' && '
        set_command += os.path.join(sys.path[0], self.action)
        ret_val = '{} {} {} {}'.format(self.cron_text, cron_wrapper.CRON_USER, set_command,
                                       '# {}'.format("ID: troy-crawler"))
        return ret_val

    def install(self):
        self.logger.debug('start crontab_install')
        base_path = sys.path[0]
        file_name = cron_wrapper.CRONTAB_FILE
        crontab_path = os.path.join(base_path, file_name)
        touch(crontab_path)
        cron_string = cron_wrapper.CRON_STRING
        cron_string += self.crontab_get_string()
        with open(crontab_path, 'w') as f:
            f.write(cron_string + '\n')
        self.logger.debug('crontab_install done')

    @property
    def crontab_list(self):
        self.logger.debug('start crontab_list')
        ret_val = list()
        base_path = sys.path[0]
        file_name = cron_wrapper.CRONTAB_FILE
        crontab_path = os.path.join(base_path, file_name)
        touch(crontab_path)
        with open(crontab_path, 'r') as f:
            for line in f:
                ret_val.append(line)
        self.logger.debug('crontab_list done')
        return ret_val

    def uninstall_cron(self):
        self.logger.debug('start uninstall_cron')
        ret_val = list()
        base_path = sys.path[0]
        file_name = cron_wrapper.CRONTAB_FILE
        crontab_path = os.path.join(base_path, file_name)
        try:
            if os.path.exists(crontab_path):
                os.remove(crontab_path)
            self.logger.debug('File {} is removed.'.format(crontab_path))
        except:
            self.logger.error('Can not remove file: {}'.format(crontab_path))
        self.logger.debug('uninstall_cron done')
        return ret_val

    def __repr__(self):
        return "CronWrapper('{}', '{}')"\
            .format(self.cron_text, self.action)

    def __str__(self):
        return "{} {}".format(self.cron_text, self.action)
