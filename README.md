# django-heroku-docker-boilerplate

<!-- ABOUT THE PROJECT -->
Easily deploy django apps on heroku or run locally with docker-compose up.


<!-- GETTING STARTED -->
## Getting Started locally

```sh
  git clone https://github.com/laercioigorps/django-heroku-docker-boilerplate.git
  cd django-heroku-docker-boilerplate
  docker-compose up

  ```

## setUp on heroku
  Sign up for Heroku account (if you don’t already have one), and then install the Heroku CLI.

```sh
    heroku create
  ```
  you will receive the app name, and we will refer it as your_app_name.
  
  Add the SECRET_KEY environment variable:
  ```sh
    heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a your_app_name
  ```
  >Change SOME_SECRET_VALUE to a randomly generated string that's at least 50 characters, and replace your_app_name.

Add your URL to allowed hosts in settings.py:
>ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your_app_name.herokuapp.com']

Commit your changes:
```sh
    git add .
    git commit -m "updated allowed_hosts"
  ```
  
Set Postgres:
```sh
    heroku addons:create heroku-postgresql:hobby-dev -a your_app_name
  ```
Set the Stack of your app to container:
```sh
    heroku stack:set container -a your_app_name
  ```
  
  Install the heroku-manifest plugin from the beta CLI channel:
  ```sh
    heroku update beta
    heroku plugins:install @heroku-cli/plugin-manifest
  ```
  
  Then, add the Heroku remote:
  ```sh
    heroku git:remote -a your_app_name
  ```
  
  Push the code up to Heroku to build the image and run the container:
  ```sh
    git push heroku HEAD:master
  ```
  
  Make migrations:
  ```sh
    heroku run python manage.py makemigrations -a your_app_name
  
    heroku run python manage.py migrate -a your_app_name
  ```
  
  You should be able to view the app at https://your_app_name.herokuapp.com. It should return a 404.
