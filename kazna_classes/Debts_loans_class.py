
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
        self.bot.register_next_step_handler(message, self.set_currency_debt) 

    def set_currency_debt(self, message):
        self.debt_person= message.text
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        options = ['$', 'RUB', 'EUR']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "Please, choose the currency type of Debt", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.set_debt_to_db)

    def set_debt_to_db(self, message):
        self.debt_currency = message.text
        Mysql_connector.insert_debt_loan_to_db('Debt', self.money_or_other_type, self.debt_person, self.debt_details_or_sum, self.debt_currency ) 
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
        self.bot.register_next_step_handler(message, self.set_currency_loan) 

    def set_details_loan(self, message):
        self.money_or_other_type_loan = message.text
        self.bot.send_message(message.chat.id, "Please insert the Details of loan")  
        self.bot.register_next_step_handler(message, self.set_person_loan)   

    def set_currency_loan(self, message):
        self.loan_details_or_sum= message.text
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        options = ['$', 'RUB', 'EUR']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "Please, choose the currency type of Loan", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.set_person_loan)

    def set_person_loan(self, message):
        if self.money_other_type == 'Money':
            self.currency = message.text
        elif self.money_other_type == 'Other':
            self.loan_details_or_sum = message.text
            self.currency = 'None'

        self.bot.send_message(message.chat.id, "Please enter name of the Person which owe you")   
        self.bot.register_next_step_handler(message, self.set_loan_to_db)

    def set_loan_to_db(self, message):
        self.loan_person= message.text
        #self.currency = message.text
        self.bot.send_message(message.chat.id, "The loan is set" + str(self.loan_details_or_sum))
        Mysql_connector.insert_debt_loan_to_db('Loan', self.money_or_other_type_loan, self.loan_person, self.loan_details_or_sum, self.currency) 
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
        clean_get_list='id  Type  Name  Sum  Cur  Info \n'
        for i in range(0,len(list_of_debts_or_loans)):
            clean_get_list = clean_get_list + str(list_of_debts_or_loans[i][0:6]).replace('(','').replace(')','')+'\n'
        self.bot.send_message(message.chat.id, str(clean_get_list)) 

        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        options = ['Delete Debt/Loan', 'Back']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "If you want, you can delete something by id", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.delete_loan_or_debt)

    def delete_loan_or_debt(self,message):
        self.delete_or_no = message.text
        self.bot.send_message(message.chat.id, self.delete_or_no)       
        if self.delete_or_no == 'Delete Debt/Loan':
            self.bot.send_message(message.chat.id, "Please, insert the ID")
            self.bot.register_next_step_handler(message, self.delete_loan_or_debt_by_id)
        elif self.delete_or_no == 'Back':
            self.bot.send_message(message.chat.id, '/start')
        else:
            print('aaasd')

    def delete_loan_or_debt_by_id(self,message):
        self.delete_id = message.text
        Mysql_connector.delete_loan_debt_by_id(self.delete_id)
        self.bot.send_message(message.chat.id, "Row was deleted")
        self.bot.send_message(message.chat.id, "/start")
