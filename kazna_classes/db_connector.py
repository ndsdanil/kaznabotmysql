#import mysql.connector
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
from datetime import date
from dateutil.relativedelta import relativedelta
from decouple import config

class db_connector:
    def __init__(self, bot):
        self.bot = bot 
    con_string = 'mysql+pymysql://root:'+str(config("DB_PASSWD")) +'@mysql:'+str(config("DB_PORT")) +'/kazna_bot_mysql' 
    #method to incert in mysql db information about new income or expense you need to set type parametr as 'Income' or 'Expense'. New value in the chosen column will be counted approprietly. 
    def get_dataframe_query():
        engine = create_engine(db_connector.con_string)

        query = 'SELECT date, Income, Expense, Source, cash_euro_with_me, cash_euro_not_with_me, cash_$_with_me, cash_$_not_with_me, card_euro, card_$, cash_RUB_not_with_me, card_RUB, bitcoin, ethir, shares_RUB, overall_eur, overall_rub, overall_dol FROM kazna_mysql_table;'
        df = pd.read_sql(query, engine)
        return df
    
    def get_five_months_dataframe_query():
        five_months = '\'' + str(date.today() - relativedelta(months =+5)) + '\''
        engine = create_engine(db_connector.con_string)

        query = 'SELECT date, Income, Expense, Income_Expense_Column, Source, overall_eur, overall_rub, overall_dol FROM kazna_mysql_table WHERE date >= ' + five_months + ';'
        df = pd.read_sql(query, engine)
        return df
    
    def get_expense_dataframe_query():
        engine = create_engine(db_connector.con_string)

        query = 'SELECT date, Income, Expense, Source, cash_euro_with_me, cash_euro_not_with_me, cash_$_with_me, cash_$_not_with_me, card_euro, card_$, cash_RUB_not_with_me, card_RUB, bitcoin, ethir, shares_RUB, overall_eur, overall_rub, overall_dol FROM kazna_mysql_table WHERE Expense != \'NULL\';'
        df = pd.read_sql(query, engine)
        return df
    
