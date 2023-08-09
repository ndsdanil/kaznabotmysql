from db_connector import db_connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Plots:
    def __init__(self, bot):
        self.bot = bot
    def make_plots(self, MY_USER_ID):
        df = db_connector.get_dataframe_query()
        df.set_index('date', inplace=True, drop=False)
        one_month_before = df.index.max() - pd.Timedelta(days=30)
        one_month_before = str(one_month_before)
        df_month = df[df.index > one_month_before ]
        df_month['Expense'] = df_month['Expense'].fillna(0)

        #Create line plot of the overall assets sum in euro for all time
        plt.figure(figsize = (15, 5))
        plt.title('Overall assets sum in euro (month)')
        sns.lineplot(data = df_month['overall_eur'], label ='overall sum in eur')
        plt.xlabel('date')
        plt.grid()
        plt.savefig('eur_overall_assets_sum_month.png')

        #create the bar plot of all expenses
        plt.figure(figsize = (15, 5))
        plt.title('All expenses (month)')
        sns.lineplot(data = df_month['Expense'])
        plt.xlabel('date')
        plt.grid()
        plt.savefig('all_expenses_month.png')

        #create the bar plot of all income 
        plt.figure(figsize = (15, 5))
        plt.title('All Income (month)')
        sns.lineplot(data = df_month['Income'])
        plt.xlabel('date')
        plt.grid()
        plt.savefig('all_incomess_month.png')
        #plt.show()

        #Create pie chart of type of expense
        plt.figure(figsize = (15,10))
        plt.title('Types of expense (month)')
        df_monthexppie = df_month[['Source','Expense']].groupby(['Source']).sum()
        print(df_monthexppie)
        total_size = sum(df_monthexppie['Expense'])
        percentages = [(size / total_size) * 100 for size in df_monthexppie['Expense']]

        plt.pie(df_monthexppie['Expense'], labels = df_monthexppie.index, textprops={'fontsize': 10}) 
        labels = ['%s, %1.1f %%' % (l, s) for l, s in zip(df_monthexppie.index, percentages )]
        plt.legend(df_monthexppie.index, bbox_to_anchor=(1,0), loc="lower right", 
                                bbox_transform=plt.gcf().transFigure, labels = labels)
        plt.savefig('expenses_types_month.png')

        #Create pie chart of type of income
        plt.figure(figsize = (15,10))
        plt.title('Types of income (month)')
        df_monthincpie = df_month[['Source','Income']].groupby(['Source']).sum()
        total_size = sum(df_monthincpie['Income'])
        percentages = [(size / total_size) * 100 for size in df_monthincpie['Income']]
        plt.pie(df_monthincpie['Income'], labels = df_monthincpie.index, textprops={'fontsize': 10}) 
        labels = ['%s, %1.1f %%' % (l, s) for l, s in zip(df_monthincpie.index, percentages )]
        plt.legend(df_monthincpie.index, bbox_to_anchor=(1,0), loc="lower right", 
                                bbox_transform=plt.gcf().transFigure, labels = labels)
        plt.savefig('income_types_month.png')

        #Send charts in telegram 
        self.bot.send_photo(MY_USER_ID , photo=open('eur_overall_assets_sum_month.png', 'rb'))
        self.bot.send_photo(MY_USER_ID , photo=open('all_expenses_month.png', 'rb'))
        self.bot.send_photo(MY_USER_ID , photo=open('all_incomess_month.png', 'rb'))
        self.bot.send_photo(MY_USER_ID , photo=open('expenses_types_month.png', 'rb'))
        self.bot.send_photo(MY_USER_ID , photo=open('income_types_month.png', 'rb'))
