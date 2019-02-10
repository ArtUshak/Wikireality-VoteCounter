# Wikireality-VoteCounter

Script for getting MediaWiki user edit count for namespaces and calculating vote power (according to [Wikireality rules](http://wikireality.ru/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C:%D0%9A#4.4._.D0.92.D0.B5.D1.81_.D0.B3.D0.BE.D0.BB.D0.BE.D1.81.D0.B0)).

## Usage

```sh
votecounter.py run [OPTIONS] USER_LIST_FILE
```

Where `USER_LIST_FILE` is file with list of users (each user line contains user name).

### Options

`--namespacefile FILENAME` JSON file to read namespaces data from

`--start [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]` Start date for counting edits

`--end [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]` End date for counting edits

`--output-format [txt|mediawiki|json]` Output data format

`--help` Show help message and exit

### Example

```sh
pipenv run python votecounter.py run --start 2018-07-12 --end 2018-10-12 ../Wikireality-VoteCounter-data/voters.txt
```

#### User list file example (`../Wikireality-VoteCounter-data/voters.txt`)

```text
Arbnos
Arsenal
Cat1987
Dream
Fedya
MaxSvet
Nomerence
Ole Førsten
Petya
Serebr
Ssr
Амшель
Очередной Виталик
Рыцарь
Фред-Продавец звёзд
Яз
```

#### Namespaces file example (`namespaces.json`)

```json
{
    "edit_weights": {
        "0": 0.04,
        "1": 0.003,
        "4": 0.015,
        "5": 0.003,
        "6": 0.03,
        "7": 0.003,
        "8": 0.015,
        "9": 0.003,
        "10": 0.015,
        "11": 0.003,
        "14": 0.015,
        "15": 0.003
    },
    "page_weights": {
        "0": 0.6
    }
}
```

## Settings

Settings are stored in `settings.py` file.

*   `api_url` Wiki API URL
*   `api_uc_limit` API limit
*   `redirect_regex_text` Regular expression text for checking new page description for redirect creation.

## Notes

*   Redirects are not counted as new pages.

## Special thanks

*   [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) developers
*   [Wikireality](http://wikireality.ru) users, especially members of Dimetr's Telegram chat.
