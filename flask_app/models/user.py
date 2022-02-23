import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import app 
from flask_bcrypt import Bcrypt        
from flask import flash 
bcrypt = Bcrypt(app)


class User:
    def __init__(self,data):
        self.id = data["id"]
        
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        
        
        self.created_at = data["created_at"]
        self.updated_password = data["updated_at"]
    

    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL("email_db").query_db(query,data)
        return results
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL("email_db").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(user_id)s;"
        result = connectToMySQL("email_db").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    
    
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        user_in_db = User.get_by_email(data)
    # user is not registered in the db
        if not user_in_db:
            flash("Invalid Email/Password")
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password, data['password']): # needs to be elif
            # if we get False after checking the password
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid
    
    
    @staticmethod
    def is_valid(email):
        is_valid = True
        if len(email["first_name"]) < 3:
            flash("3 characters please")
            is_valid = False
        if len(email["last_name"]) < 3:
            flash("3 characters please")
            is_valid = False
        
        if not EMAIL_REGEX.match(email["email"]):
            flash("invalid email ")
            is_valid = False
        if User.get_by_email(email):
            flash("email in use")
            is_valid = False
        
        
        if len(email["password"]) < 5:
            flash("5 word please")
            is_valid = False
        if email["password"] != email["pass_conf"]:
            flash("need to match")
            is_valid = False
        
        return is_valid

        
    
        
        




# letters only, at least 2 characters and that it was submitted
# Last Name - letters only, at least 2 characters and that it was submitted
# Email - valid Email format, does not already exist in the database, and that it was submitted
# Password - at least 8 characters, and that it was submitted
# Password Confirmation - matches password


