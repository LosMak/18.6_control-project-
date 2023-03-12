import requests
import json
from config import keys


class ConvertException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def currency_convert(origin_cur=str, target_cur=str, amount=int):
        if origin_cur == target_cur:
            raise ConvertException(f'Конвертация {origin_cur} в {target_cur} невозможна.')
        try:
            origin_cur == keys[origin_cur]
        except KeyError:
            raise ConvertException('Эту валюту мы пока не можем конвертировать, но мы над этим работаем!')
        try:
            target_cur == keys[target_cur]
        except KeyError:
            raise ConvertException('Эту валюту мы пока не можем конвертировать, но мы над этим работаем!')
        try:
            amount == int(amount)
        except ValueError:
            raise ConvertException('Сумму необходимо ввести цифрами, вводите целое число!')

        r = requests.get(
                    f'https://min-api.cryptocompare.com/data/price?fsym={keys[origin_cur]}&tsyms={keys[target_cur]}')
        currency_rate = json.loads(r.content)[keys[target_cur]]

        return currency_rate
