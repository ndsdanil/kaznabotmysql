import mysql.connector
class Mysql_connector:

    #insert income, insert expense (both have a lot sourses), insert debts, loans.
    def insert_sql_query(type:str, source:str, column:str, value:str):
        cnx = mysql.connector.connect(
            host='mysql',  # assuming the MySQL container is running on the same machine
            port='3306',  # the port defined in the docker-compose.yaml file
            user='root',  # default username for the MySQL container
            password='12345',  # the password defined in the docker-compose.yaml file
            database='kazna_bot_mysql'  # the database name defined in the docker-compose.yaml file
        )

        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()
        # Execute the SQL query with the provided values
        query_get_prev_values = 'SELECT cash_euro_with_me, cash_euro_not_with_me, cash_$_with_me, cash_$_not_with_me, card_euro, card_$, cash_RUB_not_with_me, card_RUB, bitcoin, shares_RUB from kazna_mysql_table ORDER BY id DESC LIMIT 1;'
        cursor.execute(query_get_prev_values)
        results = cursor.fetchall()

        print('first query get value passed ' +  str(results))
        
        if results:
            results = results[0]
        else:
            results = '(0,0,0,0,0,0,0,0,0,0)'

        query_set_new_value = 'INSERT INTO kazna_mysql_table (cash_euro_with_me, cash_euro_not_with_me, cash_$_with_me, cash_$_not_with_me, card_euro, card_$, cash_RUB_not_with_me, card_RUB, bitcoin, shares_RUB) VALUES ' + str(results) + ';'
        cursor.execute(query_set_new_value)
        print('second query INSERT new value passed')


        query_check_id ='SELECT LAST_INSERT_ID();'
        cursor.execute(query_check_id)
        id = cursor.fetchall()[0][0]
        print('third query get id passed '+ str(id))

        
        cursor.execute('(SELECT '+ str(column) + ' FROM kazna_mysql_table WHERE id ='+ str(id) + ');')
        if type == 'Income':
            target_column_value = str(cursor.fetchall()[0][0] + float(value))  
            print('target culumn value ' + target_column_value )
            print('Source = ' + source+' . Column = ' + column)
            query_update = 'UPDATE kazna_mysql_table SET Income = '+ str(value) +', Source = \'' + str(source) + '\', ' + str(column) + '=' + target_column_value + ' WHERE id ='+ str(id) +';'
            cursor.execute(query_update)
        elif type == 'Expense':
            target_column_value = str(cursor.fetchall()[0][0] - float(value))  
            print('target culumn value ' + target_column_value )
            query_update = 'UPDATE kazna_mysql_table SET Expense = '+ str(value) +', Source = \'' + str(source) + '\', ' + str(column) + '=' + target_column_value + ' WHERE id ='+ str(id) +';'
            cursor.execute(query_update)
        else:
            print('Function has wrong type parametr')

        query_get_prev_values2 = 'SELECT * FROM kazna_mysql_table;'
        cursor.execute(query_get_prev_values2)
        results2 = cursor.fetchall()
        print('Lets recheck the final result'+ str(results2 ))
        
        query_commit = 'COMMIT;'
        cursor.execute(query_commit)
        print('last query value update passed')
        
        # Close the cursor and the connection
        cursor.close()
        cnx.close()
        

       

        
        

        
