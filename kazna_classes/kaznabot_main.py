import telebot
from telebot import types
from decouple import config
from Income_class import Income
from Expense_class import Expense

#Code bellow wil launch the telegram bot
BOT_TOKEN = config("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
# Define telegram user ID
MY_USER_ID = int(config("MY_USER_ID"))

#Income_class and Expense_class classes should get the bot object to run their separate scenarios (every class has its own set of steps, I moved these steps there to simplify logic of kaznabot_main.py)
income = Income(bot)
expense = Expense(bot)

# Define start menu options
option_income = types.KeyboardButton('Income')
option_expense = types.KeyboardButton('Expense')
options = [option_income, option_expense]

# Create start menu keyboard and add the list of options to it
start_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_menu.add(*options)

# Define a handler for the /start command that sends the start menu to the user
@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id == MY_USER_ID:
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['Income', 'Expense']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Welcome Danil! This bot will help you to leash your Income and Expenses. Please choose an option:", reply_markup=markup)
        bot.register_next_step_handler(message, setup_income_expense_options)

#Depends on selection in the step above, call the proper method with proper scenario
@bot.message_handler(commands=['Income', 'Expense'])
def setup_income_expense_options(message):
    user_data = message.text
    if user_data == 'Income':
        bot.register_next_step_handler(message,  income.info_message_income(message))    
    elif user_data == 'Expense':
        bot.register_next_step_handler(message,  expense.info_message_expense(message))
        
bot.infinity_polling()