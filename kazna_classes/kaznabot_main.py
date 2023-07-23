import telebot
from telebot import types
from decouple import config
from Income_class import Income
from Expense_class import Expense
from Debts_loans_class import Debts_loans
from income_expense_analysis import Income_expense_analysis

#Code bellow wil launch the telegram bot
BOT_TOKEN = config("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
# Define telegram user ID
MY_USER_ID = int(config("MY_USER_ID"))

#Income_class and Expense_class classes should get the bot object to run their separate scenarios (every class has its own set of steps, I moved these steps there to simplify logic of kaznabot_main.py)
income = Income(bot)
expense = Expense(bot)
debt_loan = Debts_loans(bot)
income_expense_analysis = Income_expense_analysis(bot)

# Define start menu options
option_income = types.KeyboardButton('Income')
option_expense = types.KeyboardButton('Expense')
option_debts_loans = types.KeyboardButton('Debts Loans')
options = [option_income, option_expense, option_debts_loans]

# Create start menu keyboard and add the list of options to it
start_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_menu.add(*options)

# Define a handler for the /start command that sends the start menu to the user
@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id == MY_USER_ID:
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['Income', 'Expense', 'Debts Loans', 'Overall assets value']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Welcome ! This bot will help you to leash your Income, Expenses, Debts and Loans. Please choose an option:", reply_markup=markup)
        bot.register_next_step_handler(message, setup_income_expense_options)

#Depends on selection in the step above, call the proper method with proper scenario
@bot.message_handler(commands=['Income', 'Expense', 'Debts Loans', 'Overall assets value'])
def setup_income_expense_options(message):
    user_data = message.text
    
    markup_debts_loans = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    options_debts_loans = ['Debt', 'Loan', 'Get Info']
    buttons_debts_loans = [types.KeyboardButton(option) for option in options_debts_loans]
    markup_debts_loans.add(*buttons_debts_loans)

    markup_income_expense_analysis = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    options_income_expense_analysis = ['eur', '$', 'rub']
    buttons_income_expense_analysis = [types.KeyboardButton(option) for option in options_income_expense_analysis]
    markup_income_expense_analysis.add(*buttons_income_expense_analysis )

    #bot.send_message(message.chat.id, "Welcome ! This bot will help you to leash your Income, Expenses, Debts and Loans. Please choose an option:", reply_markup=markup)
    if user_data == 'Income':
        bot.register_next_step_handler(message,  income.info_message_income(message))    
    elif user_data == 'Expense':
        bot.register_next_step_handler(message,  expense.info_message_expense(message))
    elif user_data == 'Debts Loans':
        bot.send_message(message.chat.id, "You chosen debts and Loans option", reply_markup=markup_debts_loans)
        bot.register_next_step_handler(message,  choose_debt_loan_options(message))
    elif user_data == 'Overall assets value':
        bot.send_message(message.chat.id, "Choose currency for overall assets value", reply_markup=markup_income_expense_analysis)
        bot.register_next_step_handler(message,  choose_income_expense_analysis_cur)
############
@bot.message_handler(commands=['eur', '$', 'rub'])
def choose_income_expense_analysis_cur(message):
    bot.register_next_step_handler(message, Income_expense_analysis.get_overall_account_sum(income_expense_analysis,message))    
  

@bot.message_handler(commands=['Debts loans'])
def choose_debt_loan_options(message):
    user_debt_loan_data = message.text

    markup_info_debts_loans = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    options_info_debts_loans = ['Debt', 'Loan', 'Get Info']
    buttons_info_debts_loans = [types.KeyboardButton(option) for option in options_info_debts_loans]
    markup_info_debts_loans.add(*buttons_info_debts_loans)
    bot.register_next_step_handler(message, choose_debt_loan_options1)

@bot.message_handler(commands=['Debt', 'Loan', 'Get Info'])
def choose_debt_loan_options1(message):
    user_debt_loan_data1 = message.text
    
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    options = ['Debt info', 'Loan info', 'Back']
    buttons = [types.KeyboardButton(option) for option in options]
    markup.add(*buttons)
    #bot.register_next_step_handler(message,  choose_info_debt_loan_options(message))

    if user_debt_loan_data1 == 'Debt':
        bot.register_next_step_handler(message, debt_loan.set_debt_type(message))    
    elif user_debt_loan_data1 == 'Loan':
        bot.register_next_step_handler(message, debt_loan.set_loan_type(message)) 
    elif user_debt_loan_data1 == 'Get Info':
        bot.send_message(message.chat.id, "You chosen get info option:", reply_markup=markup)
        bot.register_next_step_handler(message,  choose_info_debt_loan_options)     

@bot.message_handler(commands=['Debt info', 'Loan info', 'Back'])
def choose_info_debt_loan_options(message):
    user_info_debt_loan_data = message.text
    if user_info_debt_loan_data  == 'Debt info':
        bot.register_next_step_handler(message,  debt_loan.get_loan_debt_info(message))  
    elif user_info_debt_loan_data  == 'Loan info': 
        bot.register_next_step_handler(message,  debt_loan.get_loan_debt_info(message)) 
    elif user_info_debt_loan_data  == 'Back': 
        bot.send_message(message.chat.id, "/start")

bot.infinity_polling()