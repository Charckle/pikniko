# Import flask and template operators
from flask import Flask, render_template, redirect, url_for
import time
from os import environ 

# Define the WSGI application object
app = Flask(__name__)



@app.route('/robots.txt')
def static_file():
    return app.send_static_file("robots.txt")

# Import a module / component using its blueprint handler variable (mod_auth)
from app.main_page_module.controllers import main_page_module as main_module

# Register blueprint(s)
app.register_blueprint(main_module)
# app.register_blueprint(xyz_module)
# ..
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("main_page_module.index"))

