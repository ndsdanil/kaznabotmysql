from google_sheet_connector import google_sheet_connector
from datetime import datetime
from telebot import types

class Expense:
    def __init__(self, bot):
        self.bot = bot
        self.expense_list=[]

    def info_message_expense(self, message):
        self.bot.send_message(message.chat.id, "You chose Expense, please, incert the number of Expense")
        self.bot.register_next_step_handler(message, self.set_expense)
    
    def set_expense(self, message):
        self.user_expense_number = message.text
        current_date = str(datetime.now())
        self.expense_list.append(current_date)
        self.expense_list.append("Expense")
        self.expense_list.append(self.user_expense_number)
        self.bot.reply_to(message, "You inserted your expense, now please insert the source of Expense: ")   
        self.bot.register_next_step_handler(message, self.set_expense_source)
    
    def set_expense_source(self, message):

        self.user_expense_source = message.text
        self.expense_list.append(self.user_expense_source)
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['cash euro with me', 'cash euro not with me', 'cash $ with me', 'cash $ not with me', 'card euro', 'card $', 'cash (RUB) not with me', 'card (RUB)', 'bitcoin', 'shares(RUB)']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "You set the expense source, please set the expense column", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.set_expense_column)

    def set_expense_column(self, message):
        self.user_expense_column = message.text
        self.expense_list.append( self.user_expense_column)
        self.bot.send_message(message.chat.id, "You inserted expense entry succesfully ")
        google_sheet_connector.set_values_in_sheet(google_sheet_connector, self.expense_list)
        self.expense_list.clear()
    
