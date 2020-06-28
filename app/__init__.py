# Import flask and template operators
from flask import Flask, render_template


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object("config.DevelopmentConfig")


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

