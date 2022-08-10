# Home Appliance Services Backend

<!-- ABOUT THE PROJECT -->
I built the app to manage home appliance services and troubleshoot the problem. It keeps symptoms, problems, and solutions that later(future projects) can be used to predict the behavior of a given home appliance. 

I built the backend using containerized(Docker) Django and Django Rest Framework divided into 3 modules(appliances, profiles, and services) using test-driven development with more than 230 tests and deployed on Heroku.

#### Live links

Yseful links to try, it may take some time to first load.

* [Frontend app - try the project with a sample account](https://www.djangoproject.com/)
* [Live backend API url](https://www.django-rest-framework.org/)

#### Frontend github page

* [Frontend github page](https://www.djangoproject.com/)
  
## API EndPoints
You can find auth endpoints em [dj-auth-rest endpoints](https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html), the basics are:

### Auth

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

### Profiles

### Appliances

### Services

## Built With

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
