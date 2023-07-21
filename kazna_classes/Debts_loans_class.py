
from mysql_connector import Mysql_connector
from telebot import types


#This class represents Debts, Loans scenario, all these methods - the steps to get the information about Loans, Debts inserted in the telegram bot and set/delete it into mysql database.
class Debts_loans:
    
    #Debt part
    def __init__(self, bot):
        self.bot = bot 

    def set_debt_type(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['Money', 'Other']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "Please, choose the type of Debt (Money, Other)", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.money_or_other) 
    
    def money_or_other(self, message):
        self.money_other_type = message.text
        if self.money_other_type == 'Money':
            self.bot.register_next_step_handler(message, self.set_debt_sum(message))
        elif self.money_other_type == 'Other':
            self.bot.register_next_step_handler(message, self.set_details_debt(message))  
        else:
            self.bot.send_message(message.chat.id,'Wrong debt type')

    def set_debt_sum(self, message):
        self.money_or_other_type = message.text
        self.bot.send_message(message.chat.id, "Please insert the summ of debt")  
        self.bot.register_next_step_handler(message, self.set_person_debt)   
    
    def set_details_debt(self, message):
        self.money_or_other_type = message.text
        self.bot.send_message(message.chat.id, "Please insert the Details of your Debt")  
        self.bot.register_next_step_handler(message, self.set_person_debt)   

    def set_person_debt(self, message):
        self.debt_details_or_sum = message.text
        self.bot.send_message(message.chat.id, "Please enter name of the Person you owe")  
        self.bot.register_next_step_handler(message, self.set_debt_to_db) 

    def set_debt_to_db(self, message):
        self.debt_person = message.text
        Mysql_connector.insert_debt_loan_to_db('Debt', self.money_or_other_type, self.debt_person, self.debt_details_or_sum) 
        self.bot.send_message(message.chat.id, "You inserted Debt entry succesfully ") 
        self.bot.send_message(message.chat.id, '/start')
         


    #Loan part
    def set_loan_type(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        options = ['Money', 'Other']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "Please, choose the type of Loan (Money, Other)", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.money_or_other_loan)

    def money_or_other_loan(self, message):
        self.money_other_type = message.text
        if self.money_other_type == 'Money':
            self.bot.register_next_step_handler(message, self.set_loan_sum(message))
        elif self.money_other_type == 'Other':
            self.bot.register_next_step_handler(message, self.set_details_loan(message))  
        else:
            self.bot.send_message(message.chat.id,'Wrong loan type')

    def set_loan_sum(self, message):
        self.money_or_other_type_loan  = message.text
        self.bot.send_message(message.chat.id, "Please insert the summ of loan")  
        self.bot.register_next_step_handler(message, self.set_person_loan) 

    def set_details_loan(self, message):
        self.money_or_other_type_loan = message.text
        self.bot.send_message(message.chat.id, "Please insert the Details of loan")  
        self.bot.register_next_step_handler(message, self.set_person_loan)   

    def set_person_loan(self, message):
        self.loan_details_or_sum  = message.text
        self.bot.send_message(message.chat.id, "Please enter name of the Person which owe you")  
        self.bot.register_next_step_handler(message, self.set_loan_to_db) 


    def set_loan_to_db(self, message):
        self.loan_person= message.text
        self.bot.send_message(message.chat.id, "The loan is set" + str(self.loan_details_or_sum))
        Mysql_connector.insert_debt_loan_to_db('Loan', self.money_or_other_type_loan, self.loan_person, self.loan_details_or_sum) 
        self.bot.send_message(message.chat.id, "You inserted Loan entry succesfully ") 
        self.bot.send_message(message.chat.id, '/start')
         

    #get info about existing loan or Debt
    def get_loan_debt_info(self, message):
        self.debt_or_loan_type = message.text
        if self.debt_or_loan_type == 'Debt info':
            self.info_type = 'Debt'
        elif self.debt_or_loan_type == 'Loan info':
            self.info_type = 'Loan'
        else:
            self.bot.send_message(message.chat.id, 'Wrong info type')
        list_of_debts_or_loans = Mysql_connector.get_debt_loan_info_from_db(self.info_type)
        self.bot.send_message(message.chat.id, str(list_of_debts_or_loans)) 
        self.bot.send_message(message.chat.id, '/start')
        