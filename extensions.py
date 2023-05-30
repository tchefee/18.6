import requests
import json


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            r = requests.get(f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={base}&tsyms={quote}')
            result = json.loads(r.content)[base][quote] * float(amount)
        except ValueError:
            raise APIException(f'Неверное количество {amount} {base}')

        return result