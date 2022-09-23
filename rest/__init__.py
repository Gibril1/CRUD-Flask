from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Init app
app = Flask(__name__)

# Database config
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'models.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init ma
ma = Marshmallow(app)
# Init bcrypt
bcrypt = Bcrypt(app)
# Init db
db = SQLAlchemy(app)


from rest import routes