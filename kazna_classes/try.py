
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from decimal import Decimal


def set_euro_value_for_expense(df):
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

    if df['Income_Expense_Column'] in ['cash_$_with_me', 'cash_$_not_with_me', 'card_$']:
         df['Expense'] = df['Expense'] / exchange_rates['euro_dollar']
    if df['Income_Expense_Column'] in ['cash_RUB_not_with_me', 'card_RUB', 'shares_RUB']:
         df['Expense'] = df['Expense'] / exchange_rates['euro_rub']
    if df['Income_Expense_Column'] in ['bitcoin']:
         df['Expense'] = df['Expense'] / exchange_rates['euro_bitc']
    return df