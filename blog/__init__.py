from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
#Setup mysql connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/python_mysql'
#Setup secret key
app.config['SECRET_KEY']='djashfuisdhfuisdhf'
#Setup db use ORM models
db = SQLAlchemy(app)
#Setup encrypt and decrypt
bycrpt = Bcrypt(app)

#Setup Flask User login function
login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message_category = "info"


from blog import routes