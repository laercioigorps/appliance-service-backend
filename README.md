# Django-Heroku-Docker-boilerplate

<!-- ABOUT THE PROJECT -->
Easily deploy django REST apps on heroku or run locally with docker-compose up.

* Free and rapidly Django REST APP deploy on Heroku
* User login and registration endpoints


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
  You will receive the app name, and we will refer it as your_app_name.
  
  Add the SECRET_KEY environment variable:
  ```sh
    heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a your_app_name
  ```
  >Change SOME_SECRET_VALUE to a randomly generated string that's at least 50 characters, and replace your_app_name.

Add your URL to ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS in settings.py:
>ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your_app_name.herokuapp.com']

>CSRF_TRUSTED_ORIGINS = ['https://your_app_name.herokuapp.com']

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
  
  You can also create a superuser:
  
   ```sh
    heroku run python manage.py createsuperuser -a your_app_name
  ```
  After creating superuser, you lan go to the https://your_app_name.herokuapp.com/admin and login to test.
  
## API EndPoints
You can find auth endpoints em [dj-auth-rest endpoints](https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html), the basics are:

#### Login
> /dj-rest-auth/login/ (POST)
>* username
>*  email
>*  password
>>Returns Token key


#### Registration
> /dj-rest-auth/registration/ (POST)
>* username
>*  email
>*  password1
>*  password2
>>Returns Token key


## Testing
You can test if your app is accepting requsts, we are using the command-line HTTP client [httpie](https://httpie.io/docs/cli/linux). To test if its working:

```sh
    hhttp --version
  ```


#### Registration request
```sh
    http POST https://your_app_name.herokuapp.com/dj-rest-auth/registration/ \
      username=testusername \
      email=test@email.com \
      password1=testpassword \
      password2=testpassword
  ```
  > Don't forget to replace your_app_name

  You will receive a key as a response if the registration is OK, for example:
  
    {"key": "59f98be42a25e0c7ded64aa0c53b9a0d150b5cda"}
    
    
#### Login request
```sh
    http POST https://your_app_name.herokuapp.com/dj-rest-auth/login/ \
      username=testusername \
      password=testpassword 
  ```
  > Don't forget to replace your_app_name

  You will receive a key as a response if the login is OK, for example:
  
    {"key": "59f98be42a25e0c7ded64aa0c53b9a0d150b5cda"}

  
### Built With

This section should list any major Tools/frameworks/libraries used.

* [Django](https://www.djangoproject.com/)
* [Django REST](https://www.django-rest-framework.org/)
* [dj_rest_auth](https://dj-rest-auth.readthedocs.io/en/latest/)
* [Postgres](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [whitenoise](http://whitenoise.evans.io/en/stable/)
* [gunicorn](https://gunicorn.org/)
* [Heroku](https://www.heroku.com/)

<p align="right">(<a href="#top">back to top</a>)</p>
