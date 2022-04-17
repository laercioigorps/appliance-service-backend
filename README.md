# django-heroku-docker-boilerplate

Easily deploy django apps on heroku or run locally with docker-compose up.

Heroku setup:
  Sign up for Heroku account (if you don’t already have one), and then install the Heroku CLI.
 
 heroku create
 
 you will receive the app name.
 
 Add the SECRET_KEY environment variable:
  heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a your_app_name
  
  Change SOME_SECRET_VALUE to a randomly generated string that's at least 50 characters.
  
 Add your URL to allowed hosts in settings.py:
  ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your_app_name.herokuapp.com']
  
 Commit your change
  git add .
  git commit -m "updated allowed_hosts"
  
 Set Postgres
  heroku addons:create heroku-postgresql:hobby-dev -a your_app_name
  
 Set the Stack of your app to container:
  heroku stack:set container -a your_app_name
  
 Install the heroku-manifest plugin from the beta CLI channel:
  heroku update beta
  heroku plugins:install @heroku-cli/plugin-manifest
 
 Then, add the Heroku remote:
 heroku git:remote -a your_app_name
 
 Push the code up to Heroku to build the image and run the container:
  git push heroku master
  
 Make migrations:
  heroku run python manage.py makemigrations -a your_app_name
  
  heroku run python manage.py migrate -a your_app_name
