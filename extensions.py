import requests
import json
from config import API_KEY

keys = {'Евро':'EUR', 'Доллар':'USD', 'Рубль':'RUB'}
class APIException(Exception):
    pass

class CryptoCompareAPI:
    @staticmethod
    def get_price(base, quote, amount):
        url = f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}'
        response = requests.get(url, headers={'Authorization': f'Apikey {API_KEY}'})
        data = json.loads(response.content)
        if keys[quote] not in data:
            raise APIException(f'Ошибка при получении цены {quote} за {amount} {base}')
        return data[keys[quote]] * amount