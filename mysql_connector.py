import mysql.connector

# Establish a connection to the MySQL database
cnx = mysql.connector.connect(
    host='localhost',  # assuming the MySQL container is running on the same machine
    port='3306',  # the port defined in the docker-compose.yaml file
    user='root',  # default username for the MySQL container
    password='12345',  # the password defined in the docker-compose.yaml file
    database='kazna_bot_mysql'  # the database name defined in the docker-compose.yaml file
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

# Define the SQL query to insert a new value into a table
query = "INSERT INTO your_table_name (column1, column2) VALUES (%s, %s)"

# Define the values to be inserted
values = ('value1', 'value2')  # replace with your actual values

# Execute the SQL query with the provided values
cursor.execute(query, values)

# Commit the changes to the database
cnx.commit()

# Close the cursor and the connection
cursor.close()
cnx.close()