from db_connector import db_connector
import pandas as pd
import numpy as np
#import xgboost as xgb
#from sklearn.metrics import mean_squared_error
#from sklearn.model_selection import TimeSeriesSplit
from telebot import types
import matplotlib.pyplot as plt

class Prediction:
    def __init__(self, bot):
        self.bot = bot

    #Function to add lags
    def add_lag(self, df):
        mapping_data = df['overall_eur'].to_dict()
        df['lag1'] = (df.index - pd.Timedelta(days = 8)).map(mapping_data)
        return df
    
    #lets build new features
    def create_date_features(self, df):
        df = df.copy()
        df['dayofweek'] = df.index.dayofweek
        df['dayofyear'] = df.index.dayofyear
        df['dayofmonth'] = df.index.day
        df['quarter'] = df.index.quarter
        df['month'] = df.index.month
        df['weekofyear'] = df.index.isocalendar().week.astype(int)
        return df
    
    #Lets make a Time series prediction
    def make_week_prediction(self, MY_USER_ID):
        #Get data from the mysql db
        df = db_connector.get_dataframe_query()

        #Set date as index with date time type
        df.set_index('date', inplace=True, drop=False)
        df.index =pd.to_datetime(df.index)

        #Preparing data splits to cross validation
        dfsplit = TimeSeriesSplit(n_splits = 3, test_size = 7)
        df = df.sort_index()
        df = self.add_lag(df)

        #lets get test score for model
        preds = []
        scores = []
        for train_idx, val_idx in dfsplit.split(df):
            train = df.iloc[train_idx]
            test = df.iloc[val_idx]

            train = self.create_date_features(train)
            test = self.create_date_features(test)

            FEATURES = ['dayofweek', 'dayofyear', 'dayofmonth', 'quarter', 'month','weekofyear','lag1']
            TARGET = 'overall_eur'

            X_train = train[FEATURES]
            y_train = train[TARGET]

            X_test = test[FEATURES]
            y_test = test[TARGET]

            reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
                                n_estimators=1000,
                                early_stopping_rounds=50,
                                objective='reg:linear',
                                max_depth=3,
                                learning_rate=0.01)
            reg.fit(X_train, y_train,
                    eval_set=[(X_train, y_train), (X_test, y_test)],
                    verbose=False)

            y_pred = reg.predict(X_test)
            preds.append(y_pred)
            score = np.sqrt(mean_squared_error(y_test, y_pred))
            scores.append(score)

        # lets retrain model on the complete set of data
        df = self.create_date_features(df)

        FEATURES = ['dayofweek', 'dayofyear', 'dayofmonth', 'quarter', 'month','weekofyear','lag1']
        TARGET = 'overall_eur'

        X_all = df[FEATURES]
        y_all = df[TARGET]

        X_all = X_all.fillna(method='ffill')

        reg = xgb.XGBRegressor(base_score=0.5,
                            booster='gbtree',    
                            n_estimators=1000,
                            objective='reg:linear',
                            max_depth=3,
                            learning_rate=0.01)
        reg.fit(X_all, y_all,
                eval_set=[(X_all, y_all)],
                verbose=False)

        # Create future dataframe
        one_week_later = df.index.max() + pd.Timedelta(days=7)
        future = pd.date_range(str(df.index.max()),str(one_week_later), freq='1d')
        future_df = pd.DataFrame(index=future)
        future_df['isFuture'] = True
        df['isFuture'] = False
        df_and_future = pd.concat([df, future_df])
        df_and_future = self.create_date_features(df_and_future)
        df_and_future = self.add_lag(df_and_future)

        future_w_features = df_and_future.query('isFuture').copy()
        future_w_features['pred'] = reg.predict(future_w_features[FEATURES])

        future_w_features['pred'].plot(figsize=(10, 5),
                                    ms=1,
                                    lw=1,
                                    title='Overall assets sum prediction for the next week(eur)')

        #plt.show()
        plt.grid()
        plt.savefig('eur_overall_week_pred.png')
        self.bot.send_photo(MY_USER_ID , photo=open('eur_overall_week_pred.png', 'rb'))
        


