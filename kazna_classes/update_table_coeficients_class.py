from google_sheet_connector import google_sheet_connector
import requests
from bs4 import BeautifulSoup


link_euro_dollar = 'https://www.google.com/finance/quote/EUR-USD?sa=X&ved=2ahUKEwi2t4iW3cL9AhVUgv0HHQ7cD7oQmY0JegQIBhAd'
link_euro_bitc = 'https://www.google.com/finance/quote/EUR-BTC?sa=X&ved=2ahUKEwic0PLF5ML9AhUegP0HHQCBC9MQ-fUHegQIHRAf'
link_euro_rub = 'https://www.google.com/finance/quote/EUR-RUB?sa=X&ved=2ahUKEwjU_vzp5ML9AhUD_7sIHfyVBBAQmY0JegQIExAd'

euro_dollar_cell = 'R3'
euro_bitc_cell = 'R2'
euro_rub_cell = 'R5'

#Bellow we esteblish connection with the google sheet
sheet = google_sheet_connector.get_sheet_connector()

data_dict = {
    'euro_dollar':{'request':link_euro_dollar, 'cell':euro_dollar_cell},
    'euro_bitc':{'request':link_euro_bitc, 'cell':euro_bitc_cell},
    'euro_rub':{'request':link_euro_rub, 'cell':euro_rub_cell},}

for key, val in data_dict.items():
    response = requests.get(val['request'])
    soup = BeautifulSoup(response.text, 'html.parser')
    exchange_value = soup.find('div', attrs = {'class':'YMlKec fxKbKc'}).text
    #Update coeficients
    sheet.update_acell(val['cell'], exchange_value)
    

    