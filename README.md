![Screenshot](https://github.com/HumdahQamar/The_Vetted/blob/master/the_vetted/roster/static/roster/rostrr_index_large.png)

# Rostrr app for The Vetted
An application for effective team management across multiple companies.

## Getting Started

### Prerequisites
All required libraries are listed under ```requirements.txt```

### Installation
It is a good idea to install all project dependencies in a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/).

Install all relevant libraries and dependencies by executing the following command in the project root directory:
```shell
pip install -r requirements.txt
```

## Starting the server
Run the following command from ```The_Vetted/the_vetted``` directory to run the server on your local machine
```shell
python manage.py runserver
```
The default port for the application is ```8000```

To create a super user, run
```shell
python manage.py cratesuperuser
```

In order to access the admin site, navigate to ```localhost:8000/admin```

## Running the tests
To run the automated testing suite for this application, run
```shell
python manage.py test roster
```

## Built with
* [Django](https://docs.djangoproject.com/en/2.1/)
* HTML5, Bootstrap, CSS

## Author
[Humdah Qamar](https://github.com/HumdahQamar)