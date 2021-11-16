# Blog App Django Backend

An REST API built with Django, Django Rest Framework and python for the blog application.

Github link of Blog App React Frontend: https://github.com/chrisnumber49/React-Blog-App-Frontend

## Project Screen Shots
<img src="https://github.com/chrisnumber49/DjangoBlogAppBackend/blob/master/screen%20shot/demo1.PNG" width="600" > 
<img src="https://github.com/chrisnumber49/DjangoBlogAppBackend/blob/master/screen%20shot/demo2.PNG" width="600" > 
<img src="https://github.com/chrisnumber49/DjangoBlogAppBackend/blob/master/screen%20shot/demo3.PNG" width="600" > 

## Installation and Setup Instructions

Clone down this repository. You will need `Django` and `Django Rest Framework` installed globally on your machine.  

Installation: `pip install Django` and `pip install djangorestframework`

Creating new migrations: `python manage.py makemigrations`

Applying migrations: `python manage.py migrate`

To Start Server: `python manage.py runserver`  

To Visit App: `localhost:8000/`

## Reflection 

This is my first side project of integrating full stack development with React frontend and Django backend. In the Django backend I built a REST API for blog application, in the database we have 3 Models map to each single table: **Post**, **User** and **Comment**. In the **Post** Model, athor field has many to one relationship with **User** Model; Identically, **Comment** Model also has many to one relationship with **User** Model and **Post** Model in its author and post field, that means one single post will contain an author of the post and also might have few post comments inside. Trough the setting of serializers and url routers, we can send request to the specific url to implement the CRUD operation and serch any post with specific keyword from the frontedn interface.

I started this project by using the command `django-admin startproject` to create the boilerplate of project, then create new app with command `python manage.py startapp`, two dependencies were installed, `pillow` is for for saving and serving static files to the client, and `django-cors-headers` is to allow resources to be accessed on other domains.

In the backend REST API of this side project, I learned about...
