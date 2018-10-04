# Fast-Food-Fast

[![Build Status](https://travis-ci.org/ongebo/fast-food-fast.svg?branch=ft-register-user-160882822)](https://travis-ci.org/ongebo/fast-food-fast)
[![Coverage Status](https://coveralls.io/repos/github/ongebo/fast-food-fast/badge.svg?branch=api-with-db)](https://coveralls.io/github/ongebo/fast-food-fast?branch=api-with-db)

Order Fast-Food Online, Have it Delivered Fast

## Overview
Fast-Food-Fast is a web app used by a restaurant for food delivery. It is a bootcamp code challenge for Andela Uganda fellowship cycle 12. With the app, a customer need not go to a restaurant to have fast-food, it can be delivered at his/her doorstep.

A demo of the app's interface can be found on github pages at:
https://ongebo.github.io/fast-food-fast/UI/
### Features
The app offers different features for normal users and administrators.

With the app normal users can:
* create an account and log in
* place an order for food
* see a history of ordered food

Admins are able to:
* add, edit, or delete fast-food items
* see a list of fast-food items
* see a list of food orders
* accept or decline food orders
* mark food orders as completed
### API Description
The backend of Fast-Food-Fast is powered by a RESTful API implemented in Flask, a python web microframework. Version 1 of the API is hosted on Heroku and the home page can be accessed at: https://gbo-fff-with-db.herokuapp.com. The functionality of the API with corresponding endpoints is described below:

Endpoint                           | Function
-----------------------------------|------------------------------------------------
POST /api/v1/auth/signup           | Registers a user to the database
POST /api/v1/auth/login            | Logs in a registered user
POST /api/v1/users/orders          | Creates a new user order for food
GET /api/v1/users/orders           | Fetches the order history of a user
GET /api/v1/orders/                | Gets all orders in the database (only for admins)
GET /api/v1/orders/\<orderID\>     | Gets a specific order by ID (only for admins)
PUT /api/v1/orders/\<orderID\>     | Updates the status of a specified user (only for admins)
GET /api/v1/menu                   | Retrieves the food items available on the menu
POST /api/v1/menu                  | Adds a new food item to the menu (only for admins)

When using the API, an example order is represented in JSON as:
```javascript
{
    "items": [
        {"item": "hamburger", "quantity": 2, "cost": 12000},
        {"item": "pizza", "quantity": 1, "cost": 20000}
    ],
    "status": "pending",
    "total-cost": 22000,
    "order-id": 23
}
```
Points to note:
* "items" is compulsory and its value must be a list of individual items
* When posting an order, "status", "total-cost", and "order-id" are optional, they are automatically assigned by the API
* Version 1 of the RESTful API uses data structures to store orders, so the orders don't persist among multiple runs of the application

## Installation Instructions
To run the application, follow these steps:
* Install python 3 and Postman on your local machine
* Clone this repository and checkout to the api-with-db branch
* Navigate to the repository root (fast-food-fast) and create a virtual environment
```
$ cd fast-food-fast
$ python3 -m venv venv
```
* Activate the virtual environment and install dependencies in requirements.txt
```
$ . venv/bin/activate
$ pip install -r requirements.txt
```
* Run the run.py script
```
$ python3 run.py
```
* Test the API endpoints using Postman

## Source Tree
The root directory contains the files run.py, requirements.txt, Procfile, and README.md for the following purposes:

File                | Purpose
--------------------|--------------------------------------------------------
run.py              | Runs the application with the command _python run.py_
requirements.txt    | Defines the python dependencies for the application
Procfile            | Enables deployment of the application to Heroku
README.md           | Provides information about the project

The tests directory contains code for testing the application scripts in fastfoodfast. The tests can be run using pytest, a python testing framework.

The application's code lives in fastfoodfast:
* fastfoodfast/fastfoodfast.py defines flask route functions mapped to request URLs
* fastfoodfast/models.py contains Python classes which are responsible for managing the data for the application
* fastfoodfast/__init__.py marks the fastfoodfast directory as a Python package

## Contributors
* Isaac Ongebo - *isaacongebo@gmail.com*

## Credits
* Testing Python Applications with Pytest - https://semaphoreci.com/community/tutorials/testing-python-applications-with-pytest
* What is CRUD - https://www.codecademy.com/articles/what-is-crud
