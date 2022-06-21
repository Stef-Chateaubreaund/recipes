from flask_app import app
from flask import render_template, flash, redirect, request, session
from flask_app.models.recipe import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration", methods=["POST"])
def register():

    if User.reg_valid(request.form) == False:
        return redirect("/")
    else:    
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "confirm_pass": request.form["confirm_pass"],
            "password": pw_hash
        }
        
        User.save(data)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    data = {
        "password": request.form["password"],
        "email": request.form["email"]
    }
    
    user = User.get_one_by_email_obj(data)

    #if not user_in_db:
        #flash("invalid email or password")
        #return redirect("/")

    #if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):

#       # flash("invalid email or password")
#       # return redirect ("/")
    
    #session["user_id"] = user_in_db.id 
    #session["email"] = user_in_db.email
    session["email"] = request.form["email"]
    return redirect("/dashboard")
