# appropriate base image for Python application
FROM python:3.11

# Set the working directory inside the container
WORKDIR /kazna_mysql/ml_analysis_classes/

# Copy the Python files into the container
COPY db_connector.py ./

# Install necessary dependencies
RUN apt-get update
RUN apt-get install python3
RUN pip install mysql-connector-python
RUN pip install telebot