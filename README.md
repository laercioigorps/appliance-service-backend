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

#### List customers*
> /profiles/customers/?limit=16&offset=0 (GET)
>*  limit - set to choose the max number of customers
>*  offset - set to choose customers to ignore
>>Returns a list of customers

#### Customer detail*
> /profiles/customers/<customer_id> (GET)
>> Returns a a customer object

#### Customer addresses*
> /profiles/customers/<customer_id>/address/ (GET)
>> Returns all addresses from given customer

#### Customer address detail*
> /profiles/customers/<customer_id>/address/<address_id>/ (GET)
>> Returns address object

#### Customer history*
> /profiles/customers/<customer_id>/address/<address_id>/ (GET)
>> Returns a report with customers created by date: data, labels and total_count.

### Appliances

#### List Brands
> /services/brands/ (GET)

#### List Categories
> /services/brands/ (GET)

#### List Symptoms
> /services/brands/ (GET)

#### List Problems
> /services/brands/ (GET)

#### List Solutions
> /services/brands/ (GET)

#### List Historics*
> /services/historics/ (GET)
>> Lists all the historics the authenticated user has permission.

#### Historic detail*
> /services/historics/<historic_id> (GET)
>> Return the given historic if authenticated user has permission.

### Services

#### List oand create services*
> /services/?limit=16&offset=0 (GET)
>*  limit - set to choose the max number of customers
>*  offset - set to choose customers to ignore
>> Returns a list of customers

Create a service for the authenticated user organization
> /services/ (POST)
>>Returns a service object

#### service detail*
> /services/<service_id>/ (GET)
>> Returns a service object

#### service status report*
> /services/status/ (GET)
>> Returns a report with services status count.

#### list statuses*
> /services/status/ (GET)
>> return a list with all statuses.

#### services status report
> /services/services-by-status/<number_of_days>/ (GET)
>> return a report with current services statuses count in a giver date range in days.

#### services top customers service income
> /services/top-customers-income/<number_of_customers_to_get>/ (GET)
>> return a report with customers with more services income.


#### services top customers service count
> /services/op-customers-services/<number_of_customers_to_get>/ (GET)
>> return a report with customers with more services.


#### Create random sample data(will onlly be available locally for security reasons)
> /services/sample-create/ (POST)
>* customers - Number of customers to create
>* services - Number of services to create


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
