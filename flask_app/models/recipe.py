from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
import re

class Recipe:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data ["name"]
        self.description = data["description"]
        self.instructions = data ["instructions"]
        self.under30 = data["under30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.date_made = data["date_made"]

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe["name"]) < 3:
            flash("recipe name has to be more than 3 characters long")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("description neeeds to contain at least 3 letters")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash("instructions neeeds to contain at least 3 letters")
            is_valid = False
        if len(recipe["date_made"]) < 1:
            flash("date needs to be entered")
            is_valid = False    
        if "under30" not in recipe:
            flash("please enter if recipe can be made under 30 minutes")
            is_valid = False

        return is_valid

    @classmethod
    def get_one_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes "
        query += "WHERE user_id = %(id)s ;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes_schema').query_db(query)
        # Create an empty list to append our instances of users
        recipes = []
        #THE LIST RIGHT HERE THE LIST!!!!!!!!!!
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
            #instances of user from every row of results
        return recipes

    @classmethod
    def save(cls,data):  # why keep showing up the mistake abt length???
        query="INSERT INTO recipes (name,description,instructions,date_made,under30,user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under30)s, %(user_id)s);"
        return connectToMySQL("recipes_schema").query_db(query,data)

    @classmethod
    def delete_recipe(cls,data):
        query="DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL('recipes_schema').query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM recipes WHERE id = %(id)s"
        recipe = connectToMySQL("recipes_schema").query_db(query,data)
        return cls(recipe[0])
    
    @classmethod
    def update(cls,data):
        query ="UPDATE recipes SET name = %(name)s, description=%(description)s, instructions=%(instructions)s, date_made =%(date_made)s, under30 = %(under30)s WHERE id = %(id)s;" 
        return connectToMySQL("recipes_schema").query_db(query,data)



        #not passing a password - not too many validations
        #not processing the data t give an user - paying attention on typos
        #not displaying a user from the correct table input - messing up the table 
        