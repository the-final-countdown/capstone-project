# CSC289 Capstone Project

An application that allows users to view their stock portfolios

## Development Setup

### Local Development

1. Clone the repository
    > \> git clone https://github.com/the-final-countdown/capstone-project

2. Change working directory
    > \> cd capstone-project

3. Setup your development branch
    > (master)> git checkout \<your branch name\>
    >
    > (dev-branch)> git pull master 

4. Install dependencies
    > (dev-branch)> pip install .

5. Start app *(for Windows. For Mac and Linus, use **export** instead of **set**)*:
    > (dev-branch)> set FLASK_ENV=development
    >
    > (dev-branch)> flask run

6. Navigate to http://127.0.0.1:5000/

### Deploying to Heroku

1. Create a Heroku account if you don't already have one

2. On the dashboard, click **New** > **Create new app**

3. Choose a name for the app

4. Under the **Deploy** tab, find **Deployment method** and choose **GitHub**

5. Select **the-final-countdown** repository

6. Search for **capstone-project** and then click **Connect**

7. Under the **Resources** tab, search and install **Heroku Postgres**

8. Choose your branch and use one of the deployment methods to build your app

## Endpoints

### / (Homepage)

**GET** - *While a user is logged in, displays a summary of their portfolios. From a dropdown,
the user can also select individual portfolios to view individual stock performance within
that portfolio.

If a user is not logged in, TBD

### /register

**GET** - *Display a registration form*

**POST** - *Send registration form data to application*

### /login

**GET** - *Display a login form*

**POST** - *Send login form data to application*

### /admin

**GET** - *View all user portfolios*