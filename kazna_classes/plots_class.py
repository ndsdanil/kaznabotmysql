from db_connector import db_connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from decimal import Decimal
from datetime import datetime




class Plots:
    def __init__(self, bot):
        self.bot = bot

    def set_euro_value_for_expense(self, df):
        # Custom JSON decoder to handle Decimal objects
        def decimal_decoder(obj):
            if isinstance(obj, str):
                try:
                    return Decimal(obj)
                except ValueError:
                    pass
            return obj
        try:
            with open('exchange_rates.json', 'r') as file:
                exchange_rates = json.load(file, object_hook=decimal_decoder)
        except FileNotFoundError:
            print("Exchange rates file not found.")
        dol_list = ['cash_$_with_me', 'cash_$_not_with_me', 'card_$']
        rub_list = ['cash_RUB_not_with_me', 'card_RUB', 'shares_RUB']
        btc_list = ['bitcoin']
        eth_list = ['ethir']

        if df['Income_Expense_Column'] in dol_list:
            return df['Expense'] / float(exchange_rates['euro_dollar'])
        if df['Income_Expense_Column'] in rub_list:
            return df['Expense'] / float(exchange_rates['euro_rub'])
        if df['Income_Expense_Column'] in btc_list:
            return df['Expense'] / float(exchange_rates['euro_bitc'])
        if df['Income_Expense_Column'] in eth_list:
            return df['Expense'] / float(exchange_rates['euro_ethir'])
        else:
            return df['Expense']

    def make_plots(self, MY_USER_ID):
        df = db_connector.get_five_months_dataframe_query()
        df.set_index('date', inplace=True, drop=False)
        one_month_before = str(df.index.max() - pd.Timedelta(days=30))
        df_month = df[df.index > one_month_before ]
        df_month['Expense'] = df_month['Expense'].fillna(0)

        #Create line plot of the overall assets sum in euro for month
        plt.figure(figsize = (15, 5))
        plt.title('Overall assets sum in euro (5 months)')
        sns.lineplot(data = df['overall_eur'], label ='overall sum in eur')
        plt.xlabel('date')
        plt.grid()
        plt.savefig('overall_assets_sum_three_months.png')

        #Create line plot of the overall assets sum in euro for month
        plt.figure(figsize = (15, 5))
        plt.title('Overall assets sum in euro (month)')
        sns.lineplot(data = df_month['overall_eur'], label ='overall sum in eur')
        plt.xlabel('date')
        plt.grid()
        plt.savefig('overall_assets_sum_month.png')
        df_month["eq_expense"] = df_month.apply(self.set_euro_value_for_expense, axis = 1)

        # Create barplot for every month of expenses
        df['date'] = pd.to_datetime(df['date'])
        df["eq_expense"] = df.apply(self.set_euro_value_for_expense, axis = 1)
        df['month'] = df['date'].dt.to_period('M')  # Create a new column for month
        df = df[~df['Source'].str.contains('Transfer|transfer', case=False)]
        grouped = df.groupby(['month', 'Source'])['eq_expense'].sum().unstack(fill_value=0)
        grouped.plot(kind='bar', grid = True, stacked=True, figsize=(30, 18))
        plt.xlabel('Month')
        plt.ylabel('Total Expense')
        plt.title('Total Expense by Month and Source')
        plt.legend(title='Source', bbox_to_anchor = (1.05,1), loc='upper left')
        plt.savefig('expenses_barplot_month.png')

        # Create the list of expenses for the current month
        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        # Filter the DataFrame for rows where the 'date' column corresponds to the current month
        month_expense_list = df[(df['date'].dt.month == current_month) & (df['date'].dt.year == current_year)]
        month_expense_list = month_expense_list[~month_expense_list['Source'].str.contains('Transfer|transfer', case=False)]
        month_expense_list = month_expense_list[['Source','eq_expense']].groupby(['Source']).sum()
        month_expense_list = month_expense_list.sort_values(by='eq_expense', ascending=False)



        #Send charts in telegram
        self.bot.send_photo(MY_USER_ID , photo=open('overall_assets_sum_three_months.png', 'rb'))
        self.bot.send_photo(MY_USER_ID , photo=open('overall_assets_sum_month.png', 'rb'))
        self.bot.send_photo(MY_USER_ID , photo=open('expenses_barplot_month.png', 'rb'))
        self.bot.send_message(MY_USER_ID , str(month_expense_list))