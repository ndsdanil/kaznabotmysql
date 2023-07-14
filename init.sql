-- This file is used by docker-compose.yaml as DB setting file to setup MYSQL database when the docker container with MYSQL database is launching.
USE kazna_bot_mysql;

CREATE TABLE kazna_bot_mysql (
    Date DATE,
    Expense DECIMAL(10, 2),
    Income DECIMAL(10, 2)
);