import os
import docker
import telebot
from telebot import types
from decouple import config
from Income_class import Income
from Expense_class import Expense

"""
In this part we setup the environment for kazna_bot_mysql app. 
We launch the docker-compose.yml file to create and setup MYSQL database.
To setup mysql database docker-compose.yaml file wil use init.sql file 
"""

client = docker.from_env()
current_dir = os.path.dirname(os.path.abspath(__file__))
compose_file = os.path.join(current_dir, 'docker-compose.yml')

docker_compose = docker.types.services.parse_yaml(compose_file)
services = docker_compose.get('services', {})

for service_name, service_config in services.items():
    client.services.create(**service_config, name=service_name)


"""
Code bellow wil launch the telegram bot
"""

BOT_TOKEN = config("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
# Define your user ID
MY_USER_ID = int(config("MY_USER_ID"))

income = Income(bot)
expense = Expense(bot)
currency_options = ['Euro', 'Ruble', 'Bitcoin']

# Define your start menu options
option_income = types.KeyboardButton('Income')
option_expense = types.KeyboardButton('Expense')

# Add your start menu options to a list
options = [option_income, option_expense]

# Create your start menu keyboard and add the list of options to it
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

@bot.message_handler(commands=['Income', 'Expense'])
def setup_income_expense_options(message):
    user_data = message.text

    if user_data == 'Income':
        bot.register_next_step_handler(message,  income.info_message_income(message))    
    elif user_data == 'Expense':
        bot.register_next_step_handler(message,  expense.info_message_expense(message))
        
bot.infinity_polling()