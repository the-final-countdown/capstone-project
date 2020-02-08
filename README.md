# CSC289 Capstone Project

An application that allows customers to view their stock portfolios

## Development Setup

### Local Development

Clone the repository

    > git clone https://github.com/the-final-countdown/capstone-project

Change working directory

    > cd capstone-project
    
Merge/pull changes to your branch

    (master)> git checkout <your branch name>
    (dev-branch)> git 

Install dependencies

    > pip install .

Start app *(for Windows. For Mac and Linus, use **export** instead of **set**)*:

    > set FLASK_ENV=development
    > flask run

Application will be served on http://127.0.0.1:5000/

### Deploying to Heroku

Create a Heroku account if you don't already have one

On the dashboard, click **New** > **Create new app**

Choose a name for the app

Under the **Deploy** tab, find **Deployment method** and choose **GitHub**
*(you may have to login to Github first)*

Select **the-final-countdown** repository

Search for **capstone-project** and then click **Connect**

Choose your branch and deploy use one of the deployment methods.
**Note**: I believe there is a daily deploy limit so I recommend using the Manual deploy option




## Endpoints

### /

### /register

### /login

### /admin