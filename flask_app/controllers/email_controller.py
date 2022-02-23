import bcrypt
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, session, redirect, request
from flask_app.models.user import User


@app.route("/")
def home():
    return render_template("index.html")




#################################################################### 
# register/ login
####################################################################

@app.route("/register", methods = ["POST"])
def login():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "pass_conf": request.form["pass_conf"]

    }
    if not User.is_valid(data):
        return redirect("/")
    # validating the information
    data["password"] = bcrypt.generate_password_hash(request.form['password'])

    # save new owner to database
    new_user_id = User.save(data)
    # enter owner id into session redirect to dashboard
    session["user_id"] = new_user_id

    return redirect("dashboard")


@app.route("/login", methods = ["POST"])
def login_reg():
    data = {
        "email": request.form["email"],
        "password": request.form["password"],


    }
    if not User.validate_login(data):
        return redirect("/")
    # 2 Query for user  info based on user
    user = User.get_by_email(data)
    session["user_id"] = user.id
    return redirect("dashboard")




@app.route("/dashboard")
def dash():
    data = {
        "user_id": session["user_id"] # coorolates with the get_owner_by id model

    }
    user = User.get_user_by_id(data)
    return render_template("login.html", user = user)

#### logout route#####
@app.route("/logout")
def logout_route():
    session.clear()
    return redirect("/")
