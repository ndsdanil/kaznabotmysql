from mysql_connector import Mysql_connector
from telebot import types

#This class represents Debts, Loans scenario, all these methods - the steps to get the information about Loans, Debts inserted in the telegram bot and set/delete it into mysql database.
class Payable_subscriptions:
    
    #Payable subscription part
    def __init__(self, bot):
        self.bot = bot 
    #'Insert subscription', 'Show subscriptions', 'Delete subscription'

    def process_chosen_option(self, message):
        self.money_other_type = message.text
        if self.money_other_type == 'Insert subscription':
            self.bot.send_message(message.chat.id, "Please insert the name of subscription") 
            self.bot.register_next_step_handler(message, self.set_name_subscription)
        elif self.money_other_type == 'Show subscriptions':
            subscriptions = Mysql_connector.get_subscriptions()
            clean_subscriptions='id  Name  Sum  Cur \n'
            for i in range(0,len(subscriptions)):
                clean_subscriptions = clean_subscriptions + str(subscriptions[i][0:6]).replace('(','').replace(')','')+'\n'
            self.bot.send_message(message.chat.id, str(clean_subscriptions)) 
            self.bot.send_message(message.chat.id, "/start")  
        elif self.money_other_type == 'Delete subscription':
            self.bot.send_message(message.chat.id, "Please set the id of subscription you want to delete")  
            self.bot.register_next_step_handler(message, self.del_subscription) 
            

    def set_name_subscription(self, message):
        self.subscription_name= message.text
        self.bot.send_message(message.chat.id, "Please set the sum of subscription")  
        self.bot.register_next_step_handler(message, self.set_sum_subscription)
    
    def set_sum_subscription(self, message):
        self.subscription_sum= message.text
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        options = ['$', 'RUB', 'EUR']
        buttons = [types.KeyboardButton(option) for option in options]
        markup.add(*buttons)
        self.bot.send_message(message.chat.id, "Please set the currency of subscription", reply_markup=markup)  
        self.bot.register_next_step_handler(message, self.set_cur_subscription) 

    def set_cur_subscription(self, message):
        self.subscription_cur= message.text
        self.bot.send_message(message.chat.id, self.subscription_name+ ' '+ self.subscription_sum + ' ' + self.subscription_cur) 
        Mysql_connector.set_subscription(self.subscription_name, self.subscription_sum, self.subscription_cur)
        self.bot.send_message(message.chat.id, "Subscription entry is created") 
        self.bot.send_message(message.chat.id, "/start")  
    
    def del_subscription(self, message):
        self.id= message.text
        Mysql_connector.del_subscriptions(self.id)
        self.bot.send_message(message.chat.id, "Subscription was deleted") 
        self.bot.send_message(message.chat.id, "/start")   





    