import xlrd
import logging
import xlsx_wrapper


class XlsxWrapper:

    def __init__(self,
                 file_name,
                 ):
        self.logger = logging.getLogger(xlsx_wrapper.LOGGER_NAME)
        self.file_name = file_name
        self.data = list()
        self.nrows = 0
        self.ncols = 0
        self.logger.info('Create: {}'.format(repr(self)))

    def read_file(self, start=0):
        self.logger.debug('Read file: {}'.format(self.file_name))
        workbook = xlrd.open_workbook(self.file_name)
        worksheet = workbook.sheet_by_index(0)
        self.data.clear()
        for row_index in range(start, worksheet.nrows):
            add = list()
            for coll_index in range(0, worksheet.ncols):
                if worksheet.cell(row_index, coll_index).ctype != 0:
                    add_val = worksheet.cell(row_index, coll_index).value
                else:
                    add_val = None
                add.append(add_val)
            self.data.append(add)
        self.nrows = worksheet.nrows
        self.ncols = worksheet.ncols
        self.logger.info('Read ...done')
        self.log_data()

    def log_data(self):
        self.logger.info('xlsx wrapper - data dump')
        for line in self.data:
            self.logger.info('data line: {}'.format(line))
        self.logger.info('xlsx wrapper - data dump - done')

    def __repr__(self):
        return "XlsxWrapper('{}')".format(self.file_name)

    def __str__(self):
        return 'xlsx workbook: {}'.format(self.file_name)
