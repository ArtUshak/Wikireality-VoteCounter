# -*- coding: utf-8 -*-
"""MediaWiki bot for counting vote power from user contributions."""
import copy
import datetime
import json

import click
import requests

import settings
# from exceptions import MediaWikiAPIError


def get_user_contributions_count(user, start_date, end_date, namespace):
    """Run bot."""
    user_contributions_count = 0

    while True:
        params = {
            'action': 'query',
            'list': 'usercontribs',
            'uclimit': settings.api_uc_limit,
            'ucnamespace': namespace,
            'ucuser': user,
            'ucdir': 'newer',
            'format': 'json',
        }
        if start_date is not None:
            params['ucstart'] = int(start_date.timestamp())
        if end_date is not None:
            params['ucend'] = int(end_date.timestamp())
        r = requests.get('http://wikireality.ru/w/api.php', params=params)
        if r.status_code != 200:
            # raise MediaWikiAPIError()
            raise Exception()
        data = r.json()
        user_contributions_count += len(data['query']['usercontribs'])
        if 'query-continue' not in data:
            break
        start_date = datetime.datetime.strptime(
            data['query-continue']['usercontribs']['ucstart'],
            '%Y-%m-%dT%H:%M:%SZ')

    return user_contributions_count


def read_user_data(input_file):
    """Read user list from text file."""
    users = map(lambda s: s.strip().replace(' ', '_'), input_file.readlines())
    return list(users)


@click.group()
def cli():
    """Run command line."""
    pass


@click.command()
@click.argument('user_list_file', type=click.File('rt'))
@click.option('--namespacefile', default='namespaces.json',
              type=click.File('rt'),
              help='JSON file to read namespaces data from')
@click.option('--start',
              type=click.DateTime(),
              help='Start date for counting edits')
@click.option('--end',
              type=click.DateTime(),
              help='End date for counting edits')
@click.option('--output-format', default='mediawiki',
              type=click.Choice(['txt', 'mediawiki', 'json']),
              help='Output data format')
def run(user_list_file, namespacefile, start, end, output_format):
    """Get edit counts for users from input file, and calculate vote power."""
    users = read_user_data(user_list_file)

    namespaces_raw = json.load(namespacefile)
    if not isinstance(namespaces_raw, dict):
        raise ValueError()
    namespaces = dict(map(lambda key: (int(key), namespaces_raw[key]),
                          namespaces_raw))

    users_data = dict()
    for user in users:
        user_vote_power = 0.0
        user_data = dict()
        for namespace in namespaces:
            user_contributions_count = get_user_contributions_count(
                user, start, end,
                namespace)
            user_data[namespace] = user_contributions_count
            user_vote_power += (user_contributions_count
                                * namespaces[namespace])
        user_data['VotePower'] = user_vote_power
        users_data[user] = copy.copy(user_data)
    if format == 'txt':
        for user in users_data:
            click.echo('User {}\n'.format(user))
            for key in user_data:
                click.echo('{}: {}\n'.format(key, user_data[key]))
            click.echo('\n')
    elif output_format == 'json':
        print(json.dumps(users_data))
    elif output_format == 'mediawiki':
        click.echo('{| class="wikitable"')
        click.echo(' ! Участник')
        for namespace in namespaces:
            click.echo(' ! N{}'.format(namespace))
        click.echo(' ! Сила голоса (автоматическая)')
        click.echo(' ! Сила голоса (итоговая)')
        for user in users_data:
            click.echo(' |-')
            click.echo(' | {}'.format(user))
            for key in users_data[user]:
                click.echo(' | {}'.format(users_data[user][key]))
            click.echo(' | ?')
        click.echo(' |}')
    else:
        for user in users_data:
            click.echo('User {}'.format(user))
            for key in users_data[user]:
                click.echo('N{}: {}'.format(key, users_data[user][key]))
            click.echo('')


cli.add_command(run)


if __name__ == '__main__':
    """Run command line."""
    cli()
