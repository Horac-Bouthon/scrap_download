import os
import sys
import logging
import cron2_wrapper
from crontab import CronTab


def touch(file_name):
    ret_val = False
    if os.path.exists(file_name):
        os.utime(file_name, None)
    else:
        open(file_name, 'a').close()
        ret_val = True
    return ret_val


def append_to_file(file_name, add_str):
    with open(file_name, 'a') as f:
        f.write(add_str + '\n')
    return

class Cron2Wrapper:

    def __init__(self,
                 cron_text='0/1 * * ? *',
                 action=None,
                 coment='',
                 ):
        self.logger = logging.getLogger(cron2_wrapper.LOGGER_NAME)
        self.cron_text = cron_text
        self.action = action
        self.coment = coment
        self.ct = CronTab(user=cron2_wrapper.CRON_USER)
        if hasattr(cron2_wrapper, 'CRON_FILE'):
            if touch(cron2_wrapper.CRON_FILE):
                try:
                    append_to_file(cron2_wrapper.CRON_FILE, cron2_wrapper.CRON_STRING)
                except:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.logger.error("Can't write into cron file {}".format(cron2_wrapper.CRON_FILE))

            self.ct.read(cron2_wrapper.CRON_FILE)
        self.logger.debug('Create: {}'.format(repr(self)))

    def save_oper(self):
        try:
            if hasattr(cron2_wrapper, 'CRON_FILE'):
                if len(self.ct.crons) < 1:
                    if os.path.exists(cron2_wrapper.CRON_FILE):
                        os.remove(cron2_wrapper.CRON_FILE)
                        self.logger.debug('File {} is removed.'.format(cron2_wrapper.CRON_FILE))
                else:
                    self.ct.write(cron2_wrapper.CRON_FILE)
            else:
                # write default
                self.ct.write()
        except:
            self.logger.error("Can't write into cron file {}".format(cron2_wrapper.CRON_FILE))
        return

    def create_command(self):
        """ Modify to set cron command """
        set_command = ""
        set_command += 'cd {}'.format(sys.path[0])
        set_command += ' && '
        set_command += '{}'.format(os.path.join(sys.path[0], self.action))
        return set_command

    def install(self):
        job = self.ct.new(
            command=self.create_command(),
            comment=self.coment,
        )
        job.setall(self.cron_text)
        self.save_oper()
        return

    @property
    def crontab_list(self):
        self.logger.debug('start crontab_list')
        ret_val = list()
        for job in self.ct:
            ret_val.append(str(job))
        self.logger.debug('crontab_list done')
        return ret_val

    def uninstall_cron(self, CronId):
        if CronId and CronId != '':
            # do something
            job = self.ct.find_comment(CronId)
            if job:
                self.ct.remove(job)
                self.save_oper()
        else:
            self.logger.error('You must set non empty CronId.')
        return

    def __repr__(self):
        return "CronWrapper('{}', '{}', '{}')"\
            .format(self.cron_text, self.action, self.coment)

    def __str__(self):
        return "{} | {} | {}".format(self.cron_text, self.action, self.coment)
