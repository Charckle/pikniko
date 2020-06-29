# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import BooleanField, IntegerField, StringField, TextAreaField, PasswordField, HiddenField, SubmitField, validators # BooleanField

# Import Form validators
from wtforms.validators import Email, EqualTo, ValidationError


#email verification
import re
import os.path


# Define the login form (WTForms)

class EditEntryForm(FlaskForm):
    id = HiddenField('id', [validators.InputRequired(message='Dont fiddle around with the code!')])
    
    title = StringField('Title of new note', [validators.InputRequired(message='You need to specify a title'),
                                             validators.Length(max=128)])    

    note_text = TextAreaField('Entry Text', [validators.InputRequired(message='You need to fill something.')])
    
    submit = SubmitField('Submit changes')
    
class EntryForm(FlaskForm):
    title = StringField('Title of new note', [validators.InputRequired(message='You need to specify a title'),
                                             validators.Length(max=128)])
    entry_text = TextAreaField('Entry Text', [validators.InputRequired(message='You need to fill something.')])
    
    submit = SubmitField('Add Entry')
          

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', [validators.InputRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [validators.InputRequired(message='Must provide a password.')])
    remember = BooleanField()
    
    submit = SubmitField('Login')

class EditUserForm(FlaskForm):

    id = HiddenField('id', [validators.InputRequired(message='Dont fiddle around with the code!')])
    name   = StringField('Name', [validators.InputRequired(message='We need a name for the user.')])
    email    = StringField('Email', [validators.InputRequired(message='We need an email for your account.')])
    password  = PasswordField('Password')    
    password_2 = PasswordField('Repeat password', [EqualTo('password', message='Passwords must match')])
      
    submit = SubmitField('Submit changes')
    

class RegisterForm(FlaskForm):
    username   = StringField('Username', [validators.InputRequired(message='We need a username for your account.')])
    email    = StringField('Email', [validators.InputRequired(message='We need an email for your account.')])
    password  = PasswordField('Password')    
    password_2 = PasswordField('Repeat password', [validators.InputRequired(), EqualTo('password', message='Passwords must match')])
    
    submit = SubmitField('Register')
    
    #When you add any methods that match the pattern validate_<field_name>, WTForms takes those as custom validators and invokes them in addition to the stock validators
    def validate_username(self, username):
            if user_sql_check_username(username.data) is not False:
                raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        
        #check if it is a real email
        if(re.search(regex,email.data)):  
            #if it is, check if there is another user with the same email
        
            if user_sql_check_username(email.data) is not False:
                raise ValidationError('Please use a different email address.')     
        
        else:  
            raise ValidationError('Please use a valid email address.')          
        
        
class CalculateStuffForm(FlaskForm):
    
    peoplenum = IntegerField('peoplenum', [validators.InputRequired(message='Vnesi stevilo ljudi, ki bo sodelovalo.')])
    vegiSlider = IntegerField('vegiSlider', [validators.InputRequired(message='Vnesi stevilo vegetarjancev, ki bo sodelovalo.')])
    childnum = IntegerField('childnum', [validators.InputRequired(message='Vnesi stevilo otrok, ki bo sodelovalo.')])
    vegiChild = IntegerField('vegiChild', [validators.InputRequired(message='Vnesi stevilo otrok vegetarjancev, ki bo sodelovalo.')])
    
    cevap = IntegerField('cevap', [validators.InputRequired(message='Vnesi razmerje cevapcicev.')])
    plesk = IntegerField('plesk', [validators.InputRequired(message='Vnesi razmerje pleskavic.')])
    vratovina = IntegerField('vratovina', [validators.InputRequired(message='Vnesi razmerje vratovine.')])
    perutinicke = IntegerField('perutinicke', [validators.InputRequired(message='Vnesi razmerje perutnick.')])
    
    bucke = IntegerField('bucke', [validators.InputRequired(message='Vnesi razmerje buck.')])
    gobce = IntegerField('gobce', [validators.InputRequired(message='Vnesi razmerje gobic.')])
    paprikas = IntegerField('paprikas', [validators.InputRequired(message='Vnesi razmerje paprik.')])
    melancanno = IntegerField('melancanno', [validators.InputRequired(message='Vnesi razmerje melancan.')])
    
    pivicko = IntegerField('pivicko', [validators.InputRequired(message='Vnesi razmerje piva.')])
    colica = IntegerField('colica', [validators.InputRequired(message='Vnesi razmerje colica.')])    
    sokec = IntegerField('sokec', [validators.InputRequired(message='Vnesi razmerje soka.')])
    ledek = IntegerField('ledek', [validators.InputRequired(message='Vnesi razmerje ledu.')])
      
    submit = SubmitField('Izračunaj')