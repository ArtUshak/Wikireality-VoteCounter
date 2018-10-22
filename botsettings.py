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

target_users = [
    'Arbnos',
    'Arsenal',
    'Cat1987',
    'Dream',
    'Fedya',
    'MaxSvet',
    'Nomerence',
    'Ole_Førsten',
    'Petya',
    'Serebr',
    'Ssr',
    'Амшель',
    'Очередной_Виталик',
    'Рыцарь',
    'Фред-Продавец_звёзд',
    'Яз',
]
start_date = datetime.datetime(2018, 7, 12)
end_date = datetime.datetime(2018, 10, 12)

namespaces = {
    0: 0.04,
    1: 0.003,
    4: 0.015,
    5: 0.003,
    6: 0.03,
    7: 0.003,
    8: 0.015,
    9: 0.003,
    10: 0.015,
    11: 0.003,
    14: 0.015,
    15: 0.003,
}
