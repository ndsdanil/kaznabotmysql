-- This file is used by docker-compose.yaml as DB setting file to setup MYSQL database when the docker container with MYSQL database is launching.
CREATE DATABASE IF NOT EXISTS kazna_bot_mysql;
USE kazna_bot_mysql;
CREATE TABLE kazna_mysql_table(id int AUTO_INCREMENT PRIMARY KEY,date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,Income FLOAT(10, 2),Expense FLOAT(10, 2),Source VARCHAR(30),cash_euro_with_me FLOAT(10, 2), cash_euro_not_with_me FLOAT(10, 2), cash_$_with_me FLOAT(10, 2),cash_$_not_with_me FLOAT(10, 2),card_euro FLOAT(10, 2),card_$ FLOAT(10, 2),cash_RUB_not_with_me FLOAT(10, 2),card_RUB FLOAT(10, 2),bitcoin FLOAT(10,7),shares_RUB FLOAT(10, 2));
