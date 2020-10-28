# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, send_file


# Import module forms
from app.main_page_module.forms import CalculateStuffForm
from app.main_page_module.calculations import calclulate_food


#import os
import re
import os
import io
import pathlib
from functools import wraps
import datetime



# Define the blueprint: 'auth', set its url prefix: app.url/auth
main_page_module = Blueprint('main_page_module', __name__, url_prefix='/')


    
# Set the route and accepted methods
@main_page_module.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    #if check_login(): return redirect(url_for("main_page_module.login"))  

    form = CalculateStuffForm(request.form)
    
    #return render_template("main_page_module/index_2.html", form = form)
    return render_template("main_page_module/index_2.html", form = form)


@main_page_module.route('/plan/', methods=['POST'])
#@login_required
def plan_create():

    form = CalculateStuffForm(request.form)
    
    # Verify the sign in form
    if form.validate_on_submit():
        peoplenum = form.peoplenum.data
        vegiSlider = form.vegiSlider.data
        childnum = form.childnum.data
        vegiChild = form.vegiChild.data
        
        #meso
        cevap = form.cevap.data
        plesk = form.plesk.data
        vratovina = form.vratovina.data
        perutinicke = form.perutinicke.data
        
        #zelenjava
        bucke = form.bucke.data
        gobce = form.gobce.data
        paprikas = form.paprikas.data
        melancanno = form.melancanno.data
        
        #pijaca
        pivicko = form.pivicko.data        
        colica = form.sokec.data
        sokec = form.sokec.data
        ledek = form.ledek.data
    
        osnovni_p, meso, vegi, zelenjava, pivo, sokovi, ostalo = calclulate_food(peoplenum, vegiSlider, childnum, vegiChild, cevap, plesk, vratovina, perutinicke,
                                                                                 bucke, gobce, paprikas, melancanno, pivicko, colica, sokec, ledek)
        
        return render_template("main_page_module/plan_3.html", osnovni_p=osnovni_p, meso=meso, vegi=vegi, zelenjava=zelenjava, pivo=pivo, sokovi=sokovi, ostalo=ostalo)
        #return jsonify(results)
   
    
    flash('Som Tin Wong!', 'error')
    
    return render_template("main_page_module/index.html")

@main_page_module.route('/plan_optimal/<people>/<vegi>/<child>/<vegichild>/', methods=['GET','POST'])
#@login_required
def plan_create_ideal(people, vegi, child, vegichild):
    
    peoplenum = int(people)
    vegiSlider = int(vegi)
    childnum = int(child)
    vegiChild = int(vegichild)

    #meso
    cevap = 50
    plesk = 10
    vratovina = 20
    perutinicke = 20

    #zelenjava
    bucke = 50
    gobce = 9
    paprikas = 20
    melancanno = 0

    #pijaca
    pivicko = 3       
    colica = 40
    sokec = 40
    ledek = 9

    osnovni_p, meso, vegi, zelenjava, pivo, sokovi, ostalo = calclulate_food(peoplenum, vegiSlider, childnum, vegiChild, cevap, plesk, vratovina, perutinicke,
                                                                                 bucke, gobce, paprikas, melancanno, pivicko, colica, sokec, ledek)

    return render_template("main_page_module/plan_3.html", osnovni_p=osnovni_p, meso=meso, vegi=vegi, zelenjava=zelenjava, pivo=pivo, sokovi=sokovi, ostalo=ostalo)

