# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import BooleanField, IntegerField, StringField, TextAreaField, PasswordField, HiddenField, SubmitField, SelectField, validators # BooleanField

# Import Form validators
from wtforms.validators import Email, EqualTo, ValidationError


#email verification
import re
import os.path
    
class CalculateStuffForm(FlaskForm):
    class Meta:
        csrf = False    
    
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