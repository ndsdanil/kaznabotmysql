# kazna_bot_mysql

This project is created to help manage expenses and incomes. Often I don't have a proper feeling about where I spend money and for what. I don't have enough control.
This app was created to turn back this control. This app is capable to get and store income and outcome payment data. The app consists of two docker containers, one with MySQL database, the second with the main app's logic and telegram bot. Due to the telegram bot, I can add information to the database at any time.

To launch this app you need to pull this GitHub repository and add the .env file into the kazna-classes folder. .env file should have two variables BOT_TOKEN (token of your telegram bot) and MY_USER_ID (telegram id of your user) due to your user id other telegram users won't be able to use your bot.

From the project's folder insert commands in your Linux terminal:
docker-compose build
docker-compose up

Your app is ready. Type /start in your telegram bot.

Released features:
-ability to add Income and Expense
-ability to insert, show, delete the debts and loans.
-ability to get the overall summ in euro, rub, dollars based on the actual coeficients.  
-ability to add, show, delete payable subscriptions to not forget about it. 
-ability to get the analisys of income and expenses (via plots). 
-ability to get the prediction of income, expenses using Machine Learning time series.

Useful docker comands:
docker exec -it bc7401fcc871 mysql -u root -p  - enter in mysql database in docker:    
docker ps   - show docker containers
docker container ls - show containers
docker-compose up  
docker stop $(docker ps -aq)
docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker-compose build && docker-compose up   
docker system prune -a  -clear after docker
