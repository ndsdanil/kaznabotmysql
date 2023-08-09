#import mysql.connector
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import pymysql

class db_connector:
    def __init__(self, bot):
        self.bot = bot 
    #method to incert in mysql db information about new income or expense you need to set type parametr as 'Income' or 'Expense'. New value in the chosen column will be counted approprietly. 
    def get_dataframe_query():
        con_string = 'mysql+pymysql://root:12345@mysql:3306/kazna_bot_mysql' #'mysql+pymysql://root:12345@127.0.0.1:3306/kazna_bot_mysql'
        engine = create_engine(con_string)

        query = 'SELECT date, Income, Expense, Source, cash_euro_with_me, cash_euro_not_with_me, cash_$_with_me, cash_$_not_with_me, card_euro, card_$, cash_RUB_not_with_me, card_RUB, bitcoin, shares_RUB, overall_eur, overall_rub, overall_dol FROM kazna_mysql_table;'
        df = pd.read_sql(query, engine)
        return df
    
    def get_expense_dataframe_query():
        con_string = 'mysql+pymysql://root:12345@mysql:3306/kazna_bot_mysql'
        engine = create_engine(con_string)

        query = 'SELECT date, Income, Expense, Source, cash_euro_with_me, cash_euro_not_with_me, cash_$_with_me, cash_$_not_with_me, card_euro, card_$, cash_RUB_not_with_me, card_RUB, bitcoin, shares_RUB, overall_eur, overall_rub, overall_dol FROM kazna_mysql_table WHERE Expense != \'NULL\';'
        df = pd.read_sql(query, engine)
        return df