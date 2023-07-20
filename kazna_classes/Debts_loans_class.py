import telebot
from mysql_connector import Mysql_connector
from telebot import types


#This class represents Debts, Loans scenario, all these methods - the steps to get the information about Loans, Debts inserted in the telegram bot and set/delete it into mysql database.
class Debts_loans:
    
    #Debt part
    def __init__(self, bot):
        self.bot = bot 

    def set_debt_type(self, message):
        self.bot.send_message(message.chat.id, "You chose to set a new Debt, please, choose the type of Debt (Money, Other)")
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['Money', 'Other']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.register_next_step_handler(message, self.set_person_debt)

    def set_person_debt(self, message):
        self.debt_type = message.text
        self.bot.send_message(message.chat.id, "You have chosen the type of Debt, now please enter name of the Person you owe")  
        if self.debt_type == 'Money':
            self.bot.register_next_step_handler(message, self.set_debt_sum)
        elif self.debt_type == 'Other':
            self.bot.register_next_step_handler(message, self.set_details_debt)  
        else:
            self.bot.send_message(message.chat.id,'Wrong debt type')

    def set_debt_sum(self, message):
        self.debt_person  = message.text
        self.bot.send_message(message.chat.id, "You inserted name of the Person you owe, now please insert the summ of debt")  
        self.bot.register_next_step_handler(message, self.set_debt_to_db)   
    
    def set_details_debt(self, message):
        self.debt_person = message.text
        self.bot.send_message(message.chat.id, "You inserted name of the Person you owe, now please insert the Details of your Debt")  
        self.bot.register_next_step_handler(message, self.set_debt_to_db)   

    def set_debt_to_db(self, message):
        self.debt_details_or_sum = message.text
        Mysql_connector.insert_debt_loan_to_db('Debt', self.debt_type, self.debt_person, self.debt_details_or_sum) 
        self.bot.send_message(message.chat.id, "You inserted Debt entry succesfully ") 
        


    #Loan part
    def set_loan_type(self, message):
        self.bot.send_message(message.chat.id, "You chose to set a new Loan, please, choose the type of Loan (Money, Other)")
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['Money', 'Other']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.register_next_step_handler(message, self.set_person_loan)

    def set_person_loan(self, message):
        self.loan_type = message.text
        self.bot.send_message(message.chat.id, "You have chosen the type of Loan, now please enter name of the Person which owe you")  
        if self.loan_type == 'Money':
            self.bot.register_next_step_handler(message, self.set_loan_sum)
        elif self.loan_type == 'Other':
            self.bot.register_next_step_handler(message, self.set_details_loan)  
        else:
            self.bot.send_message(message.chat.id,'Wrong loan type')

    def set_loan_sum(self, message):
        self.loan_person  = message.text
        self.bot.send_message(message.chat.id, "You inserted name of the Person which owe you, now please insert the summ of loan")  
        self.bot.register_next_step_handler(message, self.set_loan_to_db)   
    
    def set_details_loan(self, message):
        self.loan_person = message.text
        self.bot.send_message(message.chat.id, "You inserted name of the Person which owe you, now please insert the Details of your loan")  
        self.bot.register_next_step_handler(message, self.set_loan_to_db)   

    def set_loan_to_db(self, message):
        self.loan_details_or_sum = message.text
        Mysql_connector.insert_debt_loan_to_db('Loan', self.loan_type, self.loan_person, self.loan_details_or_sum) 
        self.bot.send_message(message.chat.id, "You inserted Loan entry succesfully ") 
        

    #get info about existing loan or Debt
    def get_loan_debt_info(self, message):
        self.debt_or_loan_type = message.text
        list_of_debts_or_loans = Mysql_connector.get_debt_loan_info_from_db( self.debt_or_loan_type)
        self.bot.send_message(message.chat.id, list_of_debts_or_loans)
        