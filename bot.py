# -*- coding: utf-8 -*-
"""MediaWiki bot for counting vote power from user contributions."""
import datetime
import logging
import requests

import botsettings
from exceptions import MediaWikiAPIError


logger = logging.getLogger('bot')


def get_user_contributions_count(user, start_date, end_date, namespace):
    """Run bot."""
    user_contributions_count = 0

    while True:
        params = {
            'action': 'query',
            'list': 'usercontribs',
            'uclimit': botsettings.api_uc_limit,
            'ucnamespace': namespace,
            'ucuser': user,
            'ucdir': 'newer',
            'ucstart': int(start_date.timestamp()),
            'ucend': int(end_date.timestamp()),
            'format': 'json',
        }
        r = requests.get('http://wikireality.ru/w/api.php', params=params)
        logging.debug('Sent GET request to {}'.format(r.url))
        if r.status_code != 200:
            raise MediaWikiAPIError()
        data = r.json()
        user_contributions_count += len(data['query']['usercontribs'])
        if 'query-continue' not in data:
            break
        start_date = datetime.datetime.strptime(
            data['query-continue']['usercontribs']['ucstart'],
            '%Y-%m-%dT%H:%M:%SZ')

    return user_contributions_count


def main():
    """Get contributions data for users and calculate vote power."""
    with open(botsettings.output_file, 'wt') as output_file:
        output_file.write('Start: {}\n'.format(botsettings.start_date))
        output_file.write('End:   {}\n'.format(botsettings.end_date))
        output_file.write('\n')
        for user in botsettings.target_users:
            logging.info('Processing user {}'.format(user))
            user_vote_power = 0.0
            user_data = dict()
            for namespace in botsettings.namespaces:
                user_contributions_count = get_user_contributions_count(
                    user, botsettings.start_date, botsettings.end_date,
                    namespace)
                user_data['N{}'.format(namespace)] = user_contributions_count
                user_vote_power += (user_contributions_count
                                    * botsettings.namespaces[namespace])
            user_data['VotePower'] = user_vote_power
            logger.info('User {}, data: {}'.format(user, user_data))
            output_file.write('User {}\n'.format(user))
            for key in user_data:
                output_file.write('{}: {}\n'.format(key, user_data[key]))
            output_file.write('\n')
    logger.info('Finished')


if __name__ == '__main__':
    main()
