# erp-bet flask 
flask metronic template for ERP-BET application

In this application template you will find all the usefull flask plugins already configured. check the requirements.txt for the details.
The project uses Metronic V7 HTML admin demo1 template. Metronic is based on Booostrap 4 and contains every thing you'll need to build your pages.Check the metronic page for front side documentations [https://keenthemes.com/metronic/](https://keenthemes.com/metronic/).

The project is build using flask blueprints. Two blueprints are implemented Base and Home. The file structure is as follow

```
└── erp-bet
    ├── app
    │   ├── __init__.py # main init file
    │   ├── base        # base blueprint folder
    │   ├── home        # home blueprint folder
    ├── config.py       # the app config file containing different configuration for development, production or debug mode 
    ├── .env            # all the app environement variable are set here
    ├── .gitignore
    ├── requirements.txt
    └── run.py         # the application entry point
```
The authentication is done using a rest API, the rest of the app uses Jinja templating and WTForm 

###### Base blueprint
The base blueprint contains authentication logic, the project models, different usefull tools and the project static files.
```
└── base
    ├── static             # all the app static files folder
    ├── template            # html files
    ├── __init__.py         # the blueprint initialisation
    ├── auth.py             # authentication classes using rest api
    ├── forms.py            # authentication forms and validation using WTForm
    ├── models.py           # all the project models
    ├── orm_tools.py        # database related tools
    ├── routes.py           # main application routes
    ├── tools.py            # different util functions and classes 
```

###### Home blueprint
The home blueprint contains the authenticated users main pages
```
└── home
    ├── template            # html files
    ├── __init__.py         # the blueprint initialisation
    ├── forms.py            # authentication forms and validation using WTForm
    ├── routes.py           # the home blueprint routes
```

# Requirement

Python 3.7, virtualenv, mysql