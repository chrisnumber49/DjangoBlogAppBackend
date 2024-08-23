# Blog App Django Backend

A REST API built with Django, Django Rest Framework, and Python for the blog application.
 
Github link of Blog App React Frontend: https://github.com/chrisnumber49/React-Blog-App-Frontend

## Project Screen Shots
<img src="https://github.com/chrisnumber49/DjangoBlogAppBackend/blob/master/screen%20shot/demo1.PNG" width="700" > 
<img src="https://github.com/chrisnumber49/DjangoBlogAppBackend/blob/master/screen%20shot/demo2.PNG" width="700" > 
<img src="https://github.com/chrisnumber49/DjangoBlogAppBackend/blob/master/screen%20shot/demo3.PNG" width="700" > 

## Installation and Setup Instructions

Clone down this repository. You will need `Django` and `Django Rest Framework` installed globally on your machine.  

Installation: `pip install Django` and `pip install djangorestframework`

Creating new migrations: `python manage.py makemigrations`

Applying migrations: `python manage.py migrate`

To Start Server: `python manage.py runserver`  
 
To Visit App: `localhost:8000/`

## Reflection 

This is my first side project of integrating full stack development with React frontend and Django backend. In the Django backend, I built a REST API for blog application, in the database we have 3 Models mapped to each single table: **Post**, **User**, and **Comment**. In the **Post** Model, the author field has many to one relationship with **User** Model; Identically, **Comment** Model also has many to one relationship with **User** Model and **Post** Model in its author and post field, that means one single post will contain an author of the post and also might have few post comments inside. Through the setting of serializers and URL routers, we can send requests to the specific URL to implement the CRUD operation and search any post with a specific keyword from the frontend interface.

I started this project by using the command `django-admin startproject` to create the boilerplate of the project, then create a new app with the command `python manage.py startapp`, two dependencies were installed, `pillow` is for for saving and serving static files to the client, and `django-cors-headers` is to allow resources to be accessed on other domains.

In the backend REST API of this side project, I learned about the concept of various components that make up REST framework, and understood each wrapper that Django Rest Framework provides for Views including function-based API Views, class-based API Views, GenericAPIView, viewsets, GenericViewSet and ModelViewSet, and lastly knew the Authentication and Permissions to restrict who can access the data.
