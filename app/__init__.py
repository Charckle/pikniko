# Import flask and template operators
from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

# Import SQLite3
import MySQLdb

from flaskext.markdown import Markdown


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object("config.DevelopmentConfig")

Markdown(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
#connection = sqlite3.connect("sqlite:///razor_notes.sqlite3")
connection = MySQLdb.connect (host = "localhost",
                              user = "root",
                              passwd = "",
                              db = "razor_notes")
cursor = connection.cursor()

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.main_page_module.controllers import main_page_module as main_module

# Register blueprint(s)
app.register_blueprint(main_module)
# app.register_blueprint(xyz_module)
# ..

