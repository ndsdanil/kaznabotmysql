import requests
import decimal
from decouple import config

def get_crypto_rate(amount_in_euros=1):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "eur"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        exchange_rate = data["bitcoin"]["eur"]
        price_in_euros = round(decimal.Decimal(amount_in_euros) / decimal.Decimal(exchange_rate), 7)
        return price_in_euros
    else:
        print(f"Error: {response.status_code}")
        return None

    #use exchangerate-api https://v6.exchangerate-api.com/v6/YOURAPINUMBER/latest/USD
def get_cur_exchange():
    EXRATE_API = str(config("EXRATE_API"))
    url = "https://v6.exchangerate-api.com/v6/" + EXRATE_API + "/EUR"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json().get("conversion_rates")
        eur_usd = data.get("USD")
        eur_rub = data.get("RUB")
        return eur_usd, eur_rub
    else:
        print(f"Error: {response.status_code}")
        return None
    
def get_exchange_rates():
    exchange_values_list = list()
    eur_bitcoin = get_crypto_rate(amount_in_euros=1)
    eur_usd, eur_rub = get_cur_exchange()
    exchange_values_list.append(eur_bitcoin)
    exchange_values_list.append(eur_usd)
    exchange_values_list.append(eur_rub)
    return exchange_values_list

#list = get_exchange_rates()
#print(list[1])
#print(list[0])
#print(list[2])

