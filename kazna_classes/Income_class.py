from mysql_connector import Mysql_connector
from telebot import types
from income_expense_analysis import Income_expense_analysis

#This class represents Income scenario, all these methods - the steps to get the Income information inserted in the telegram bot and set it into mysql database.
class Income:
    
    def __init__(self, bot):
        self.bot = bot 

    def info_message_income(self, message):
        self.bot.send_message(message.chat.id, "You chose Income, please, incert the number of Income")
        self.bot.register_next_step_handler(message, self.set_income)
    
    def set_income(self, message):
        self.user_income_number = message.text
        self.bot.send_message(message.chat.id, "You inserted your income, now please insert the source of Income: ")  
        self.bot.register_next_step_handler(message, self.set_income_source)   
    
    def set_income_source(self, message):
        self.user_income_source = message.text
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['cash_euro_with_me', 'cash_euro_not_with_me', 'cash_$_with_me', 'cash_$_not_with_me', 'card_euro', 'card_$', 'cash_RUB_not_with_me', 'card_RUB', 'bitcoin', 'shares_RUB']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "You set the income source, please set the income column", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.set_income_column)
    
    def set_income_column(self, message):
        self.user_income_column = message.text
        Mysql_connector.insert_sql_query('Income', self.user_income_source, self.user_income_column, self.user_income_number)
        Income_expense_analysis.get_overall_account_sum()
        self.bot.send_message(message.chat.id, "You inserted income entry succesfully ")   
        
        





