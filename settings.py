# -*- coding: utf-8 -*-
"""Settings for bot."""
import logging
import datetime


log_file = '../Wikireality-VoteCounter-data/log.log'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)-15s %(message)s',
                    handlers=[logging.FileHandler(log_file),
                              logging.StreamHandler()])

api_uc_limit = 50

output_file = '../Wikireality-VoteCounter-data/output.txt'

start_date = datetime.datetime(2018, 7, 12)
end_date = datetime.datetime(2018, 10, 12)
