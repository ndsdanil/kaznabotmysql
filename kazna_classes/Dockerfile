# Use an appropriate base image for your Python application
FROM python:3.11

# Set the working directory inside the container
WORKDIR /kazna_mysql/kazna_classes/

# Copy the Python files into the container
COPY Expense_class.py ./
COPY Income_class.py ./  
COPY kaznabot_main.py ./
COPY mysql_connector.py ./
COPY .env ./

# Install any necessary dependencies (if required)

RUN apt-get update
RUN apt-get install python3
RUN pip install certifi        
RUN pip install idna
RUN pip install mysql-connector-python
RUN pip install packaging
RUN pip install protobuf
RUN pip install pyTelegramBotAPI   
RUN pip install python-decouple
RUN pip install requests
RUN pip install telebot
RUN pip install urllib3
RUN pip install websocket-client
RUN pip install charset-normalizer 
RUN pip install setuptools 
RUN rm /etc/mysql/my.cnf
RUN touch /etc/mysql/my.cnf
RUN echo -e '# The MariaDB configuration file\n#\n# The MariaDB/MySQL tools read configuration files in the following order:\n# 0. "/etc/mysql/my.cnf" symlinks to this file, reason why all the rest is read.\n# 1. "/etc/mysql/mariadb.cnf" (this file) to set global defaults,\n# 2. "/etc/mysql/conf.d/*.cnf" to set global options.\n# 3. "/etc/mysql/mariadb.conf.d/*.cnf" to set MariaDB-only options.\n# 4. "~/.my.cnf" to set user-specific options.\n#\n# If the same option is defined multiple times, the last one will apply. \n# \n# One can use all long options that the program supports. \n# Run program with --help to get a list of available options and with \n# --print-defaults to see which it would actually understand and use. \n#\n# If you are new to MariaDB, check out https://mariadb.com/kb/en/basic-mariadb-articles/ \n# \n# This group is read both by the client and the server \n# use it for options that affect everything \n# \n[client-server] \n# Port or socket location where to connect \nport = 3306 \nsocket = /run/mysqld/mysqld.sock \n#bind-address        = 127.0.0.1 \n# Import all .cnf files from configuration directory \n!includedir /etc/mysql/conf.d/ \n!includedir /etc/mysql/mariadb.conf.d/' > /etc/mysql/my.cnf

