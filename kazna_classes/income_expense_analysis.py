
import requests
from bs4 import BeautifulSoup
from mysql_connector import Mysql_connector
from telebot import types

class Income_expense_analysis:
    def __init__(self, bot):
        self.bot = bot 

    def get_overall_account_sum(self, message):
        #count sum in rub, eur, $, show grafics for income expense, show info ang grafics about debt
        cur = message.text
        print('Cur is '+ cur)
        options = ['cash_euro_with_me(1), cash_euro_not_with_me(2), cash_$_with_me(3), cash_$_not_with_me(4), card_euro(5), card_$(6), cash_RUB_not_with_me(7), card_RUB(8), bitcoin(9), shares_RUB(10)']
        income_expense_info_list = list()

        link_euro_dollar = 'https://www.google.com/finance/quote/EUR-USD?sa=X&ved=2ahUKEwi2t4iW3cL9AhVUgv0HHQ7cD7oQmY0JegQIBhAd'
        link_euro_bitc = 'https://www.google.com/finance/quote/EUR-BTC?sa=X&ved=2ahUKEwic0PLF5ML9AhUegP0HHQCBC9MQ-fUHegQIHRAf'
        link_euro_rub = 'https://www.google.com/finance/quote/EUR-RUB?sa=X&ved=2ahUKEwjU_vzp5ML9AhUD_7sIHfyVBBAQmY0JegQIExAd'

        eurocard_coef = 0.02
        euro_dollar_value = 0
        euro_bitc_value = 0
        euro_rub_value = 0
        link_list = (link_euro_dollar, link_euro_bitc, link_euro_rub )

        data_dict = {
            link_euro_dollar :euro_dollar_value,
            link_euro_bitc:euro_bitc_value,
            link_euro_rub:euro_rub_value,}
        coeff_dict = {'euro_dollar':0, 'euro_bitc':0, 'euro_rub':0}

        for key, val in data_dict.items():
            response = requests.get(key)
            soup = BeautifulSoup(response.text, 'html.parser') 
            exchange_value = soup.find('div', attrs = {'class':'YMlKec fxKbKc'}).text
            print(str(exchange_value))
            #Update coeficients
            data_dict[key] = exchange_value 

        print(str(data_dict))
            
        income_expense_info_list  = Mysql_connector.get_income_expense_info_query()


        #cash_euro_with_me(0)(H), cash_euro_not_with_me(1)(I), cash_$_with_me(2)(J), cash_$_not_with_me(3)(K), card_euro(4)(L), card_$(5)(M), cash_RUB_not_with_me(6)(N), card_RUB(7)(O), bitcoin(8)(P), shares_RUB(9)(Q)
        # 'euro_dollar':AA3, 'euro_bitc':AA2, 'euro_rub':AA5}

        #H2+I2+(J2/AA$3)+(K2/AA$3)+(L2-(L2*AA$4))+(M2/AA$3-((M2/AA$3)*AA$4))+(N2/AA$5)+(O2/AA$5)+(P2/AA$2)+(Q2/AA$5)

        result_eur = income_expense_info_list[0][0][0] + income_expense_info_list[0][0][1] + (float(income_expense_info_list[0][0][2])/float(data_dict[link_euro_dollar])) + (float(income_expense_info_list[0][0][3])/float(data_dict[link_euro_dollar])) + (income_expense_info_list[0][0][4] - (income_expense_info_list[0][0][4]* eurocard_coef)) + (float(income_expense_info_list[0][0][5])/float(data_dict[link_euro_dollar]) - ((float(income_expense_info_list[0][0][5])/float(data_dict[link_euro_dollar]))*eurocard_coef)) + (float(income_expense_info_list[0][0][6])/float(data_dict[link_euro_rub])) + (float(income_expense_info_list[0][0][7])/float(data_dict[link_euro_rub])) + (float(income_expense_info_list[0][0][8])/float(data_dict[link_euro_bitc])) + (float(income_expense_info_list[0][0][9])/float(data_dict[link_euro_rub]))
        print('result = ' + str(result_eur))
        if cur == 'eur':
            self.bot.send_message(message.chat.id, result_eur)
        elif cur == 'rub':
            result_rub = result_eur * float(data_dict[link_euro_rub])
            self.bot.send_message(message.chat.id, result_rub)
        elif cur == '$':
            result_doll = result_eur * float(data_dict[link_euro_dollar])
            self.bot.send_message(message.chat.id, result_doll )