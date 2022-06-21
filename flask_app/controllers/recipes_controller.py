from flask_app import app
from flask import render_template, session, redirect, flash, request
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
#store the email in session when they log in ------
@app.route("/dashboard")
def dashboard():
    data = {
        "email" : session["email"] # because im not passing an user id, its a email
    }
    user_recipes = User.get_one_by_email_obj(data)
    recipes = Recipe.get_all_recipes()
    return render_template("first_page.html", user_recipes = user_recipes, recipes = recipes)
#-== step 2 == get one user by email.. and then.. yeah
#step3 shut up, using the user obj to grab the id and teh we set user_id to id or to user id i dont know


@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!")
    return render_template("index.html")

@app.route("/create")
def create():
    print(session["user_id"])
    return render_template("create.html")

@app.route("/create/recipe", methods=["POST"])
def save():

    #if "user_id" not in session:
        #flash("you must be logged in ")
       # return redirect("/")

    if Recipe.validate_recipe(request.form):
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_made": request.form["date_made"],
            "under30": request.form["under30"],
            "user_id": session["user_id"]
        }
        Recipe.save(data) 
        return redirect("/dashboard")
    else:
        return redirect("/create")

@app.route("/edit/<int:id>")
def edit(id):
    data = {
        "id": id
    }
    recipe = Recipe.get_by_id(data)
    return render_template("edit_recipe.html", recipe=recipe)


@app.route("/editrecipe/<int:id>", methods = ["POST"])
def edit_recipe(id):
#   if "user_id" not in session:
#   flash("you must be logged in")
    #return redirect("/")

    if Recipe.validate_recipe(request.form):
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_made": request.form["date_made"],
            "under30": request.form["under30"],
            "id":id
        }

        Recipe.update(data) 
        return redirect("/dashboard")
    else:
    
        return redirect("/editrecipe")


@app.route("/recipe/instructions/<int:id>")
def show(id):
    data = {
        "id": id
    }
    user_data = {
        "id":session['user_id']
    }
    recipe = Recipe.get_by_id(data)
    user = User.get_by_id(user_data)
    return render_template("instructions.html", recipe=recipe, user=user)

@app.route("/delete/<int:id>")
def delete_recipe(id):    
    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    flash("deleted recipe")
    return redirect("/dashboard")