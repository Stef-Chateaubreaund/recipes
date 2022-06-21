from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
import re

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("recipes_schema").query_db(query,data)

    @staticmethod
    def reg_valid(user_data):
        is_valid = True
        query="SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL("recipes_schema").query_db(query,user_data)
        print(results)
        email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(results) >= 1:
            flash("email already exist")
            is_valid = False
        if User.get_by_email(user_data):
            flash("email is already registered add a new email ")
            is_valid = False
        if len(user_data["first_name"]) < 2:
            flash("please fill your fist name")
            is_valid = False
        if len(user_data["last_name"]) < 2:
            flash("please fill your last name")
            is_valid = False
        if len(user_data["password"]) < 8:
            flash("confirm your password")
            is_valid = False
        if not email_reg.match(user_data['email']):
            flash("wrong email or password")
            is_valid = False
        if user_data["confirm_pass"] != user_data["password"]:
            flash("the passwords does not match")
            is_valid = False

        return is_valid

    @classmethod
    def get_one_by_email_obj(cls, data):
        query = "SELECT * FROM users "
        query += "WHERE email = %(email)s ;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0]) #it will be uh.. result 0 is going to give you ah.. in the .. table that shows up.. which will only give you AHAHAH
#                 #one whole user... select the first table user.. wich is the only user.....
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        user_db = connectToMySQL("recipes_schema").query_db(query,data)
    
    @classmethod
    def get_user_recipes(cls,data):
        query="SELECT * FROM recipes JOIN recipes ON users.id = user_id WHERE users.id = %(user_id)s"
        all_user_recipes = connectToMySQL("recipes_schema").query_db(query,data)

        user_recipes = cls(all_user_recipes[0])
        
        for ur in all_user_recipes:
            recipe_data = {
                "id": ur["recipes.id"],
                "name": ur["name"],
                "description": ur["description"],
                "instructions": ur["instructions"],
                "under30": ur["under30"],
                "date_made": ur["date_made"],
                "created_at": ur["recipes.created_at"],
                "updated_at": ur["recipes.updated_at"],
                "user_id": ur["user_id"]
            }
            user_recipes.recipes.append(recipe.Recipe(recipe_data))

        return user_recipes

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL("recipes_schema").query_db(query,data)
        return cls(results[0])
