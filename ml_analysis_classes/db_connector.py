import mysql.connector

class db_connector:
    def __init__(self, bot):
        self.bot = bot 
    #method to incert in mysql db information about new income or expense you need to set type parametr as 'Income' or 'Expense'. New value in the chosen column will be counted approprietly. 
    def insert_sql_query(type:str, source:str, column:str, value:str):

        results = []
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
        for i, data in enumerate(cursor):
            results.append(data)
        #results = cursor.fetchall()
       
        
        # Close the cursor and the connection
        cursor.close()
        cnx.close()