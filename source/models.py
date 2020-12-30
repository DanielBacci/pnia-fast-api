import ast
import re
from collections import namedtuple
from functools import lru_cache

import requests

PhoneBusinessModel = namedtuple(
    'PhoneBusinessModel',
    ['number', 'number_neat', 'type', 'reason']
)


class PrefixTrie:

    FILE_PATH = 'files/prefixes.txt'
    END = 'end'

    @lru_cache
    def build(self):
        trie = {}
        with open(self.FILE_PATH) as file:
            for numbers in file.readlines():
                current_trie = trie
                for number in numbers:
                    if number != '\n':
                        current_trie = current_trie.setdefault(number, {})
                current_trie[self.END] = self.END
        return trie

    def search_prefix(self, trie: dict, phone: str):
        current_trie = trie
        prefix = ''
        for number in phone:
            if current_trie.get(number):
                prefix = f'{prefix}{number}'
                current_trie = current_trie[number]
        if current_trie.get(self.END):
            return prefix

        return None


class PhoneBusiness:

    URL = 'https://challenge-business-sector-api.meza.talkdeskstg.com/sector/'

    def phones_from_body(self, body):
        phones = ast.literal_eval(body.decode())
        return phones

    def neat_number(self, number):
        number_neat = number
        if number[0] == '0' and number[1] == '0':
            number_neat = number[2:]
        number_neat = re.sub("[^0-9]", "", number_neat)
        return number_neat

    def _retrieve_business(self, number):
        try:
            response = requests.get(f'{self.URL}{number}', timeout=1)
            response.raise_for_status()
            return PhoneBusinessModel(
                number=number,
                number_neat=self.neat_number(number),
                type=response.json()['sector'],
                reason=''
            )
        except requests.exceptions.Timeout:
            return PhoneBusinessModel(
                number=number,
                number_neat=self.neat_number(number),
                type=None,
                reason='Timeout'
            )
        except requests.exceptions.HTTPError:
            return PhoneBusinessModel(
                number=number,
                number_neat=self.neat_number(number),
                type=None,
                reason='Invalid Number'
            )

    def retrieve_business(self, numbers):
        if not numbers:
            return []

        phones = []
        for number in numbers:
            phone = self._retrieve_business(number)
            if not phone.type:
                continue
            phones.append(phone)
        return phones

    def build(self, phones):
        business = self.retrieve_business(phones)

        prefix_trie = PrefixTrie()
        trie = prefix_trie.build()

        items = {}
        for phone in business:
            prefix = prefix_trie.search_prefix(trie, phone.number_neat)
            if not prefix:
                continue

            if not items.get(prefix):
                items[prefix] = {phone.type: 1}
            elif items.get(prefix).get(phone.type):
                items[prefix][phone.type] += 1
            else:
                items[prefix].update({phone.type: 1})

        return items
