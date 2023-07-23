# appropriate base image for Python application
FROM python:3.11

# Set the working directory inside the container
WORKDIR /kazna_mysql/kazna_classes/

# Copy the Python files into the container
COPY Expense_class.py ./
COPY Income_class.py ./
COPY Debts_loans_class.py ./  
COPY kaznabot_main.py ./
COPY mysql_connector.py ./
COPY income_expense_analysis.py ./
COPY Payable_subscriptions_class.py ./
COPY .env ./

# Install necessary dependencies
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
RUN pip install beautifulsoup4

