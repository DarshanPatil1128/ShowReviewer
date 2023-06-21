from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import show

import re

from flask import Flask, render_template, redirect, request, session, flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = connectToMySQL('shows').query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("shows").query_db(query,data)
        print(results)
        if results == ():
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("shows").query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def get_id(cls, user_id):

        data = {"id": user_id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("shows").query_db(query,data)
        return cls(result[0])



    @staticmethod
    def validate_create(user):
        is_valid = True
        if len(user['email']) < 6:
            flash("Email is too short")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is not in correct format!")
            is_valid = False 
        if len(user['first_name']) < 2:
            flash("First Name must be atleast 2 characters!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be atleast 2 characters!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password is too short")
            is_valid = False
        if user['password'] != user['password_conf']:
            flash("Passwords do not match")
            is_valid = False
        data = {
            "email": user['email']
        }
        user_in_db = User.get_by_email(data)
        if user_in_db:
            flash("Email already taken")
            is_valid = False
        #if email is in database
        return is_valid

    @staticmethod
    def validate_user(user):
        is_valid = True 
        if len(user['email']) < 1:
            flash("Cannot leave email field empty")
            is_valid = False
        if len(user['password']) < 1:
            flash("cannot leave password field empty")
            is_valid = False
        return is_valid 