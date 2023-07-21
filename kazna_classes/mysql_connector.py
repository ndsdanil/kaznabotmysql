import mysql.connector

#class created to implement the all necessary interactions between app's and mysql's containers
class Mysql_connector:

    #method to incert in mysql db information about new income or expense you need to set type parametr as 'Income' or 'Expense'. New value in the chosen column will be counted approprietly. 
    def insert_sql_query(type:str, source:str, column:str, value:str):
        cnx = mysql.connector.connect(
            host='mysql',  # assuming the MySQL container is running on the separate docker container with mysql image
            port='3306',  # the port defined in the docker-compose.yaml file
            user='root',  # default username for the MySQL container
            password='12345',  # the password defined in the docker-compose.yaml file
            database='kazna_bot_mysql'  # the database name defined in the docker-compose.yaml file
        )

        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()
        # Get values from the last inserted row to be able to count the new columns values based on new incertion. If there is no previous row, colums will get the 0 values
        cursor.execute('SELECT cash_euro_with_me, cash_euro_not_with_me, cash_$_with_me, cash_$_not_with_me, card_euro, card_$, cash_RUB_not_with_me, card_RUB, bitcoin, shares_RUB from kazna_mysql_table ORDER BY id DESC LIMIT 1;')
        results = cursor.fetchall()
        if results:
            results = results[0]
        else:
            results = '(0,0,0,0,0,0,0,0,0,0)'
        #insert values from the previous row into the new row, get id of this new row
        cursor.execute('INSERT INTO kazna_mysql_table (cash_euro_with_me, cash_euro_not_with_me, cash_$_with_me, cash_$_not_with_me, card_euro, card_$, cash_RUB_not_with_me, card_RUB, bitcoin, shares_RUB) VALUES ' + str(results) + ';')
        cursor.execute('SELECT LAST_INSERT_ID();')
        id = cursor.fetchall()[0][0]

        #get value of the last insertion for the targeted column. Add(or subtract) the new value to the last one depends on chosen type ('Income' or 'Expense')
        cursor.execute('(SELECT '+ str(column) + ' FROM kazna_mysql_table WHERE id ='+ str(id) + ');')
        if type == 'Income':
            target_column_value = str(cursor.fetchall()[0][0] + float(value))  
            query_update = 'UPDATE kazna_mysql_table SET Income = '+ str(value) +', Source = \'' + str(source) + '\', ' + str(column) + '=' + target_column_value + ' WHERE id ='+ str(id) +';'
            cursor.execute(query_update)
        elif type == 'Expense':
            target_column_value = str(cursor.fetchall()[0][0] - float(value))
            query_update = 'UPDATE kazna_mysql_table SET Expense = '+ str(value) +', Source = \'' + str(source) + '\', ' + str(column) + '=' + target_column_value + ' WHERE id ='+ str(id) +';'
            cursor.execute(query_update)
        else:
            print('Function has wrong type parametr')
        
        #Without commit our transations will be rollbacked from the database
        query_commit = 'COMMIT;'
        cursor.execute(query_commit)
        print('last query value update passed')
        
        # Close the cursor and the connection
        cursor.close()
        cnx.close()
        
    def get_debt_loan_info_from_db(debt_or_loan_type:str):
        cnx = mysql.connector.connect(
            host='mysql',  # assuming the MySQL container is running on the separate docker container with mysql image
            port='3306',  # the port defined in the docker-compose.yaml file
            user='root',  # default username for the MySQL container
            password='12345',  # the password defined in the docker-compose.yaml file
            database='kazna_bot_mysql'  # the database name defined in the docker-compose.yaml file
        )

        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()
        # Get values from the last inserted row to be able to count the new columns values based on new incertion. If there is no previous row, colums will get the 0 values
        cursor.execute('SELECT id, Debt_or_Loan_type, Person, Debt_Loan_sum, Details FROM debts_loans_table WHERE Debt_or_Loan_type = \'' + str(debt_or_loan_type) + '\';')
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        return results
    
    def insert_debt_loan_to_db(debt_or_loan_type:str, type:str, person:str, details_or_sum:str):
        details_or_sum_column = ''
        if type== 'Money':
            details_or_sum_column = 'Debt_Loan_sum'
        elif type== 'Other':
            details_or_sum_column = 'Details'
            details_or_sum = '\''+ str(details_or_sum)+ '\''

        for i in range(10):
            print(details_or_sum_column)
            print(type)

        cnx = mysql.connector.connect(
            host='mysql',  # assuming the MySQL container is running on the separate docker container with mysql image
            port='3306',  # the port defined in the docker-compose.yaml file
            user='root',  # default username for the MySQL container
            password='12345',  # the password defined in the docker-compose.yaml file
            database='kazna_bot_mysql'  # the database name defined in the docker-compose.yaml file
        )

        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()
        # Get values from the last inserted row to be able to count the new columns values based on new incertion. If there is no previous row, colums will get the 0 values
        cursor.execute('INSERT INTO debts_loans_table (Debt_or_Loan_type, Type, Person , ' + str(details_or_sum_column) + ') VALUES (\'' + debt_or_loan_type +'\', \'' + str(type) + '\', \'' + str(person) + '\', ' + str(details_or_sum) +');')
        cursor.execute('COMMIT;')
        cursor.close()
        cnx.close()
        

        
