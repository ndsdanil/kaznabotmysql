from google_sheet_connector import google_sheet_connector
from datetime import datetime
from telebot import types
#import kaznabot_main
class Income:
    
    def __init__(self, bot):
        self.bot = bot
        self.income_list=[]

    def info_message_income(self, message):
        self.bot.send_message(message.chat.id, "You chose Income, please, incert the number of Income")
        self.bot.register_next_step_handler(message, self.set_income)
    
    def set_income(self, message):
        self.user_income_number = message.text
        current_date = str(datetime.now())
        self.income_list.append(current_date)
        self.income_list.append("Income")
        self.income_list.append(self.user_income_number)
        self.bot.send_message(message.chat.id, "You inserted your income, now please insert the source of Income: ")  
        self.bot.register_next_step_handler(message, self.set_income_source)
        
    
    def set_income_source(self, message):
        self.user_income_source = message.text
        self.income_list.append(self.user_income_source)
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['cash euro with me', 'cash euro not with me', 'cash $ with me', 'cash $ not with me', 'card euro', 'card $', 'cash (RUB) not with me', 'card (RUB)', 'bitcoin', 'shares(RUB)']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "You set the income source, please set the income column", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.set_income_column)
    
    def set_income_column(self, message):
        self.user_income_column = message.text
        self.income_list.append( self.user_income_column)
        self.bot.send_message(message.chat.id, "You inserted income entry succesfully ")
        google_sheet_connector.set_values_in_sheet(google_sheet_connector, self.income_list)    
        self.income_list.clear()





