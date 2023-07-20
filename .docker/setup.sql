-- This file is used by docker-compose.yaml as DB setting file to setup MYSQL database when the docker container with MYSQL database is launching.
CREATE DATABASE IF NOT EXISTS kazna_bot_mysql;
USE kazna_bot_mysql;
CREATE TABLE kazna_mysql_table(id int AUTO_INCREMENT PRIMARY KEY,date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,Income FLOAT(10, 2),Expense FLOAT(10, 2),Source VARCHAR(30),cash_euro_with_me FLOAT(10, 2), cash_euro_not_with_me FLOAT(10, 2), cash_$_with_me FLOAT(10, 2),cash_$_not_with_me FLOAT(10, 2),card_euro FLOAT(10, 2),card_$ FLOAT(10, 2),cash_RUB_not_with_me FLOAT(10, 2),card_RUB FLOAT(10, 2),bitcoin FLOAT(10,7),shares_RUB FLOAT(10, 2));

-- Table for loans and debts
CREATE TABLE debts_loans_table(id int AUTO_INCREMENT PRIMARY KEY, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Debt_or_Loan_type VARCHAR(30), Type VARCHAR(30), Debt_Loan_sum FLOAT(10, 2), Person VARCHAR(30), Details VARCHAR(30), CHECK (Type == 'Money' OR Type == 'Other'));

--Table for accounting payable subscriptions
CREATE TABLE payable_subscriptions_table(id int AUTO_INCREMENT PRIMARY KEY, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Subscription_name VARCHAR(30), Price FLOAT(10, 2), Currency FLOAT(10, 2), Details VARCHAR(30), CHECK (Currency  == 'EUR' OR Currency  == 'RUB' OR Currency  == '$'));