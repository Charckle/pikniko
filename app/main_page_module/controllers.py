# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, send_file


# Import module forms
from app.main_page_module.forms import CalculateStuffForm
from app.main_page_module.calculations import calclulate_food, add_stats, json_read


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
@main_page_module.route('/', methods=['GET'])
#@login_required
def index():
    add_stats("landing")

    form = CalculateStuffForm(request.form)
    
    #return render_template("main_page_module/index_2.html", form = form)
    return render_template("main_page_module/index_2.html", form = form)


@main_page_module.route('/kontakt/', methods=['GET'])
#@login_required
def kontakt():
    add_stats("kontakt")

    
    #return render_template("main_page_module/index_2.html", form = form)
    return render_template("main_page_module/kontakt.html")


# Set the route and accepted methods
@main_page_module.route('/pivo/', methods=['GET'])
#@login_required
def pivo():
    add_stats("pivo")

    return redirect('https://bevog.si/', code=302)


# Set the route and accepted methods
@main_page_module.route('/statistika/', methods=['GET'])
#@login_required
def statistika():
    #if check_login(): return redirect(url_for("main_page_module.login"))
    data = {"landing": [0,0,0,0,0,0,0,0,0,0,0,0],
            "plan": [0,0,0,3,0,0,0,0,0,0,0,0],
            "kontakt": [0,0,0,0,0,0,0,0,2,0,0,0],
            "pivo": [0,0,0,0,0,0,0,0,0,0,0,0]
            }
    
    data = json_read(".", "data.json")

    statistika =[sum([i for i in data["landing"]]), 
                 sum([i for i in data["plan"]]), 
                 sum([i for i in data["kontakt"]]), 
                 sum([i for i in data["pivo"]])]
    
    meseci = [0,0,0,0,0,0,0,0,0,0,0,0]
    
    for key, value in data.items():
        for index, i in enumerate(value):
            meseci[index] += i
            

    #return render_template("main_page_module/index_2.html", form = form)
    return render_template("main_page_module/statistika.html", statistika=statistika, meseci=meseci)


@main_page_module.route('/plan/', methods=['GET'])
#@login_required
def plan_create():
    try:
        peoplenum = int(request.args.get("peoplenum"))
        vegiSlider = int(request.args.get("vegiSlider"))
        childnum = int(request.args.get("childnum"))
        vegiChild = int(request.args.get("vegiChild"))
        cevap = int(request.args.get("cevap"))
        plesk = int(request.args.get("plesk"))
        vratovina = int(request.args.get("vratovina"))
        perutinicke = int(request.args.get("perutinicke"))
        bucke = int(request.args.get("bucke"))
        gobce = int(request.args.get("gobce"))
        paprikas = int(request.args.get("paprikas"))
        melancanno = int(request.args.get("melancanno"))
        pivicko = int(request.args.get("pivicko"))
        colica = int(request.args.get("colica"))
        sokec = int(request.args.get("sokec"))
        ledek = int(request.args.get("ledek"))  
        
        
        
        osnovni_p, meso, meso_sum, vegi, zelenjava, zelenjava_sum, pivo, sokovi, ostalo, price_sum = calclulate_food(peoplenum, vegiSlider, childnum, vegiChild, cevap, plesk, 
                                                                                                                     vratovina, perutinicke, bucke, gobce, paprikas,
                                                                                                                     melancanno, pivicko, colica, sokec, ledek)
        add_stats("plan")
        
        return render_template("main_page_module/plan_4.html", osnovni_p=osnovni_p, meso=meso, meso_sum=meso_sum, vegi=vegi, zelenjava=zelenjava, zelenjava_sum=zelenjava_sum,
                               pivo=pivo, sokovi=sokovi, ostalo=ostalo, price_sum=price_sum)
    except:
        redirect(url_for("main_page_module.index"))  


@main_page_module.route('/plan2/', methods=['POST'])
#@login_required
def plan_create2():

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
    
        osnovni_p, meso, meso_sum, vegi, zelenjava, zelenjava_sum, pivo, sokovi, ostalo, price_sum = calclulate_food(peoplenum, vegiSlider, childnum, vegiChild, cevap, plesk, 
                                                                                                                     vratovina, perutinicke, bucke, gobce, paprikas,
                                                                                                                     melancanno, pivicko, colica, sokec, ledek)
        
        return render_template("main_page_module/plan_4.html", osnovni_p=osnovni_p, meso=meso, meso_sum=meso_sum, vegi=vegi, zelenjava=zelenjava, zelenjava_sum=zelenjava_sum,
                               pivo=pivo, sokovi=sokovi, ostalo=ostalo, price_sum=price_sum)
        #return jsonify(results)
   
    
    flash('Som Tin Wong!', 'error')
    
    return render_template("main_page_module/index.html")


