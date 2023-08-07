from mysql_connector import Mysql_connector
from telebot import types
from income_expense_analysis import Income_expense_analysis

#This class represents Expense scenario, all these methods - the steps to get the Expense information inserted in the telegram bot and set it into mysql database.
class Expense:
    
    def __init__(self, bot):
        self.bot = bot

    def info_message_expense(self, message):
        self.bot.send_message(message.chat.id, "You chose Expense, please, incert the number of Expense")
        self.bot.register_next_step_handler(message, self.set_expense)
    
    def set_expense(self, message):
        self.user_expense_number = message.text 
        self.bot.reply_to(message, "You inserted your expense, now please insert the source of Expense: ")   
        self.bot.register_next_step_handler(message, self.set_expense_source)
    
    def set_expense_source(self, message):
        self.user_expense_source = message.text
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['cash_euro_with_me', 'cash_euro_not_with_me', 'cash_$_with_me', 'cash_$_not_with_me', 'card_euro', 'card_$', 'cash_(RUB)_not_with_me', 'card_(RUB)', 'bitcoin', 'shares(RUB)']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "You set the expense source, please set the expense column", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.set_expense_column)

    def set_expense_column(self, message):
        self.user_expense_column = message.text
        Mysql_connector.insert_sql_query('Expense', self.user_expense_source, self.user_expense_column, self.user_expense_number)
        Income_expense_analysis.get_overall_account_sum()
        self.bot.send_message(message.chat.id, "You inserted expense entry succesfully ")
        
