import requests
import decimal
from decouple import config
class Get_exchange_rates:
    def get_crypto_rate(self, amount_in_euros=1):
        bitcoin_price = 0
        ethereum_price = 0
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "eur"
        }
        params_eth = {
            "ids": "ethereum",
            "vs_currencies": "eur"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            exchange_rate = data["bitcoin"]["eur"]
            price_in_euros = round(decimal.Decimal(amount_in_euros) / decimal.Decimal(exchange_rate), 7)
            bitcoin_price = price_in_euros
        else:
            print(f"Error: {response.status_code}")
        
        response_eth = requests.get(url, params=params_eth)
        if response_eth.status_code == 200:
            data = response_eth.json()
            eth_exchange_rate = data["ethereum"]["eur"]
            eth_price_in_euros = round(decimal.Decimal(amount_in_euros) / decimal.Decimal(eth_exchange_rate), 7)
            ethereum_price = eth_price_in_euros
        else:
            print(f"Error: {response_eth.status_code}")
        
        return bitcoin_price, ethereum_price

        #use exchangerate-api https://v6.exchangerate-api.com/v6/YOURAPINUMBER/latest/USD
    def get_cur_exchange(self):
        EXRATE_API = str(config("EXRATE_API"))
        url = "https://v6.exchangerate-api.com/v6/" + EXRATE_API + "/latest/EUR"
        print(url)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json().get("conversion_rates")
            eur_usd = data.get("USD")
            eur_rub = data.get("RUB")
            return eur_usd, eur_rub
        else:
            print(f"Error: {response.status_code}")
            return None
        
    def get_exchange_rates(self):
        exchange_values_list = list()
        eur_bitcoin, eur_eth = self.get_crypto_rate(amount_in_euros=1)
        eur_usd, eur_rub = self.get_cur_exchange()
        exchange_values_list.append(eur_bitcoin)
        exchange_values_list.append(eur_eth)
        exchange_values_list.append(eur_usd)
        exchange_values_list.append(eur_rub)
        return exchange_values_list

#classtest = Get_exchange_rates()
#list = classtest.get_exchange_rates()
#print(list[0])
#print(list[1])
#print(list[2])
#print(list[3])

