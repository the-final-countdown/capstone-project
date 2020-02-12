# CSC289 Capstone Project

An application that allows users to view their stock portfolios

## Development Setup

### Local Development

1. Clone the repository

        > git clone https://github.com/the-final-countdown/capstone-project

2. Change working directory
    
        > cd capstone-project

3. Create or update your development branch
    
    Create a new branch:
    
        (master)> git checkout -b <your branch name\>
    
    Update your existing branch:
    
        (master)> git checkout <your branch name\>
        (dev-branch)> git merge master
    
4. Install dependencies
        
        (dev-branch)> pip install .
    
    OR
        
        run pip3 install pipenv -> pipenv install -> pipenv shell (This will create a virtual environment 
        using pipenv and will install the required packages based on the pipfile)

5. Create the databse by starting the app *(for Windows. For Mac and Linux, use **export** instead of **set**)*:

        (dev-branch)> set FLASK_ENV=development
        (dev-branch)> flask run

6. Ctrl-C out of the application so we can populate the database with users
    
    1. Create a free account on https://mockaroo.com/
    
    2. Within Mockaroo, setup an API endpoint at */users.json* that serves the data we need.
    Duplicate or import the data from here--https://mockaroo.com/71771080. The format is consistent with the form data
    we'll be getting so we can use the same function to insert the users into the database as we do to register users)
    
    3. Back in your *capstone-project* directory, create a **.env** file and add the line below (if you don't have it
    yet, *pip install python-dotenv* so this will work)
        
        > API_KEY_MOCKAROO=*<your Mockaroo api key\>*

    4. Navigate back to the command line and type the command below (This may take 30 seconds or so while
    it makes a request to your newly created endpoint).

            flask populate-db

7. Start the app again with

        flask run

8. Navigate to your application at http://127.0.0.1:5000/

### Deploying to Heroku

1. Create a Heroku account

2. On the dashboard, click **New** > **Create new app**

3. Choose a name for the app

4. On the **Deploy** tab, find **Deployment method** and choose **GitHub**

5. Select **the-final-countdown** repository

6. Search for **capstone-project** and then click **Connect**

7. On the **Resources** tab, search and install **Heroku Postgres**

8. Choose your branch and use one of the deployment methods to build your app

9. After your app finishes building, populate the database
    
    1. On the **Settings** tab, add your *API_KEY_MOCKAROO* to the **Config Vars**
    
    2. On the **Deploy** tab, navigate to **More** > **Run Console** and type
    
            flask populate-db
            
10. Open your Heroku app and click the admin tab to view your newly added users

## Endpoints

### / (Homepage)

**GET** - *While a user is logged in, displays a summary of their portfolios. From a dropdown,
the user can also select individual portfolios to view individual stock performance within
that portfolio.*

*If a user is not logged in, TBD*

### /register

**GET** - *Display a registration form*

**POST** - *Send registration form data to application*

### /login

**GET** - *Display a login form*

**POST** - *Send login form data to application*

### /admin

**GET** - *View all user portfolios*
