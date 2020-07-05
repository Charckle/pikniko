# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, send_file

#from app import connection, cursor
# Import module forms
from app.main_page_module.forms import LoginForm, RegisterForm, EntryForm, EditEntryForm, EditUserForm, CalculateStuffForm


#import os
import re
import os
import zipfile
import io
import pathlib
from functools import wraps
import datetime



# Define the blueprint: 'auth', set its url prefix: app.url/auth
main_page_module = Blueprint('main_page_module', __name__, url_prefix='/')

#login decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        
        else:
            flash("Please login to access the site.", "error")
            
            return redirect(url_for("main_page_module.login"))
    
    return wrapper


#login check
def check_login():
    if "user_id" not in session:
        return True
    
# Set the route and accepted methods
@main_page_module.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    #if check_login(): return redirect(url_for("main_page_module.login"))  

    form = CalculateStuffForm(request.form)
    
    return render_template("main_page_module/index.html", form = form)

@main_page_module.route('/plan/', methods=['POST'])
#@login_required
def plan_create():
    #ljudje
    '''
    peoplenum = request.form["peoplenum"]
    vegiSlider = request.form["vegiSlider"]
    childnum = request.form["childnum"]
    vegiChild = request.form["vegiChild"]
    
    #meso
    cevap = request.form["cevap"]
    plesk = request.form["plesk"]
    vratovina = request.form["vratovina"]
    perutinicke = request.form["perutinicke"]
    
    #zelenjava
    bucke = request.form["bucke"]
    gobce = request.form["gobce"]
    paprikas = request.form["paprikas"]
    melancanno = request.form["melancanno"]
    
    #pijaca
    pivicko = request.form["pivicko"]
    sokec = request.form["sokec"]
    ledek = request.form["ledek"]
    '''
    
    form = CalculateStuffForm(request.form)
    
    # Verify the sign in form
    if form.validate_on_submit():
        peoplenum = form.peoplenum.data
        vegiSlider = form.vegiSlider.data
        childnum = form.childnum.data
        vegiChild = form.vegiChild.data
        #izracun ljudi in otrok mesojedcev
        mesojedci = peoplenum - vegiSlider
        otroci_mesa = childnum - vegiChild  
        #skupno vsi ljudje
        skupno_ljudje = peoplenum + childnum
        
        #meso
        cevap = form.cevap.data
        plesk = form.plesk.data
        vratovina = form.vratovina.data
        perutinicke = form.perutinicke.data
        #
        skupna_mozna_kolicina_mesa = cevap + plesk + vratovina + perutinicke
        #        
        cevap_proc = cevap * 1 / skupna_mozna_kolicina_mesa
        plesk_proc = plesk * 1 / skupna_mozna_kolicina_mesa
        vratovina_proc = vratovina * 1 / skupna_mozna_kolicina_mesa
        perutinicke_proc = perutinicke * 1 / skupna_mozna_kolicina_mesa   
        
        #zelenjava
        bucke = form.bucke.data
        gobce = form.gobce.data
        paprikas = form.paprikas.data
        melancanno = form.melancanno.data
        #
        skupna_mozna_kolicina_zelenjave = bucke + gobce + paprikas + melancanno
        #           
        bucke_proc = bucke * 1 / skupna_mozna_kolicina_zelenjave
        gobce_proc = gobce * 1 / skupna_mozna_kolicina_zelenjave
        paprikas_proc = paprikas * 1 / skupna_mozna_kolicina_zelenjave
        melancanno_proc = melancanno * 1 / skupna_mozna_kolicina_zelenjave
        
        #pijaca
        pivicko = form.pivicko.data        
        colica = form.sokec.data
        sokec = form.sokec.data
        skupna_mozna_kolicina_brezalko = colica + sokec
        colica_proc = colica / skupna_mozna_kolicina_brezalko
        sokec_proc = sokec / skupna_mozna_kolicina_brezalko
        #
        ledek = form.ledek.data
        #
        ledek_proc = ledek * 1 / 50
        
        #
        
        meso_odrasli_g = 200
        meso_otroci_g = 100
        
        vegi_odrasli_g = 200
        vegi_otroci_g = 100
        
        zelenjava_odrasli_g = 200
        zelenjava_otroci_g = 100
        
        perutnicke_razmerje = 1.6
        
        kruh_odrasli_g = 100
        kruh_otroci_g = 50
        
        cebula_odrasli_g = 25
        cebula_otroci_g = 15
        
        pivo_ml = 1500
        cola_odrasli_ml = 1200
        cola_otroci_ml = 700
        sok_odrasli_ml = 1200
        sok_otroci_ml = 700
        led_odrasli_g = 150
        
        #teza na kos
        kruh_g = 50
            
        
        #results
        
        #meso
        skupno_cevap = int(((mesojedci * meso_odrasli_g) + (otroci_mesa * meso_otroci_g)) * cevap_proc)
        skupno_plesk = int(((mesojedci * meso_odrasli_g) + (otroci_mesa * meso_otroci_g)) * plesk_proc)
        skupno_vratovina = int(((mesojedci * meso_odrasli_g) + (otroci_mesa * meso_otroci_g)) * vratovina_proc)
        skupno_perutinicke = int(((mesojedci * meso_odrasli_g) + (otroci_mesa * meso_otroci_g)) * perutnicke_razmerje * perutinicke_proc)

        skupna_meso = skupno_cevap + skupno_plesk + skupno_vratovina + skupno_perutinicke
        
        #vegi
        skupno_vegi = ((vegiSlider * meso_odrasli_g) + (vegiChild * meso_otroci_g))
        #zelenjava
        skupno_bucke = int(((peoplenum * zelenjava_odrasli_g) + (childnum * zelenjava_otroci_g)) * bucke_proc)
        skupno_gobce = int(((peoplenum * zelenjava_odrasli_g) + (childnum * zelenjava_otroci_g)) * gobce_proc)
        skupno_paprikas = int(((peoplenum * zelenjava_odrasli_g) + (childnum * zelenjava_otroci_g)) * paprikas_proc)
        skupno_melancanno = int(((peoplenum * zelenjava_odrasli_g) + (childnum * zelenjava_otroci_g)) * melancanno_proc)
        #pivo
        skupno_pivo = peoplenum * pivo_ml
        skupno_pivo_veliko = int(skupno_pivo / 500) + (skupno_pivo % 500 > 0)
        skupno_pivo_malo = int(skupno_pivo / 330) + (skupno_pivo % 330 > 0)
        #brezalko
        skupno_cola = ((peoplenum * cola_odrasli_ml) + (childnum * cola_otroci_ml)) * colica_proc
        skupno_cola_literpol = int(skupno_cola / 1500) + (skupno_cola % 1500 > 0)        
        skupno_sok = ((peoplenum * sok_odrasli_ml) + (childnum * sok_otroci_ml)) * sokec_proc
        skupno_sok_liter = int(skupno_sok / 1000) + (skupno_sok % 1000 > 0)
        #led
        skupno_led_g = skupno_ljudje * led_odrasli_g * ledek_proc
        #ostalo
        skupno_cebula_g = (peoplenum * cebula_odrasli_g) + (childnum * cebula_otroci_g)
        skupno_kruh_g = (peoplenum * kruh_odrasli_g) + (childnum * kruh_otroci_g)
        skupno_kruh_kos = int(skupno_kruh_g / kruh_g) + (skupno_kruh_g % kruh_g > 0)    
        skupno_oglje = skupna_meso + skupno_vegi
        
        osnovni_p = {"odrasli_m": ["Število odraslih - Meso", mesojedci],
         "odrasli_v": ["Število odraslih - Vegi", vegiSlider],
         "otroci_m": ["Število otrok - Meso", otroci_mesa],
         "otroci_v": ["Število otrok - Vegi", vegiChild]
         }
        
        meso = {"cevap": ["Čevapčiči", skupno_cevap],
         "plesk": ["Pleskavice", skupno_plesk],
         "vrat": ["Vratovina", skupno_vratovina],
         "perut": ["Perutničke", skupno_perutinicke]
         }
        
        vegi = {
         "vegi": ["Vegi odrasli", skupno_vegi]
         }
        
        zelenjava = {"bucke": ["Bučke", skupno_bucke],
         "gobe": ["Gobice", skupno_gobce],
         "pap": ["Paprika", skupno_paprikas],
         "melan": ["Melancani", skupno_melancanno]
         }
        
        pivo = {"skup_pivo": ["Skupno Pivo ml", skupno_pivo],
         "veliko_pivo": ["Velikega", skupno_pivo_veliko],
         "malo_pivo": ["Ali majhnega", skupno_pivo_malo]
         }
        
        sokovi = {"skup_cola": ["Skupno Cola ml", skupno_cola],
         "cola_literpol": ["Cola 1,5l", skupno_cola_literpol],
         "skup_sok": ["Skupno Sok", skupno_sok],
         "sok_liter": ["Sokl 1l", skupno_sok_liter]
         }
        
        ostalo = {"led_g": ["Gramov Ledu", skupno_led_g],
         "gram_veb": ["Gramov čebule", skupno_cebula_g],
         "gram_kruh": ["Gramov kruha", skupno_kruh_g],
         "kos_kruh": ["Kosov kruha", skupno_kruh_kos],
         "skupno_oglje": ["Gramov oglja", skupno_oglje]
        }
        
        return render_template("main_page_module/plan.html", osnovni_p=osnovni_p, meso=meso, vegi=vegi, zelenjava=zelenjava, pivo=pivo, sokovi=sokovi, ostalo=ostalo)
        #return jsonify(results)
   
    
    flash('Som Tin Wong!', 'error')
    
    return render_template("main_page_module/index.html")
    #results = {r[0]: [r[1], r[2]] for r in res if (int(r[0]) in user_notes)}
    
    #return jsonify(results)

@main_page_module.route('/search/', methods=['GET'])
@login_required
def search():
    #if check_login(): return redirect(url_for("main_page_module.login"))  

    return render_template("main_page_module/search.html")

@main_page_module.route('/search/', methods=['POST'])
@login_required
def search_results():
    key = request.form["key"]

    banana = WSearch()
    if key == "":
        asterix = ""
    else:
        asterix = "*"
    res = banana.index_search(key + asterix)
    
    #get IDs of the notes the user can access
    user_notes = note_sql_get_all_active_of_user(session['user_id'])
    results = {r[0]: [r[1], r[2]] for r in res if (int(r[0]) in user_notes)}
    
    return jsonify(results)

@main_page_module.route('/delete/', methods=['POST'])
@login_required
def delete_entry():
    note_id = request.form["id"]
    note = note_sql_get_one(note_id)
    
    if note is None:
        flash('No entries with this ID found to delete.', 'error')
        
        return redirect(url_for("main_page_module.all_entry"))  
    
    note_sql_delete_one(note_id)     
    
    flash(f'Note {note[1]} successfully deleted.', 'success')  
    
    return redirect(url_for("main_page_module.index"))   
    
@main_page_module.route('/trash_note/', methods=['POST'])
@login_required
def trash_entry():
    note_id = request.form["id"]
    note = note_sql_get_one(note_id)
    
    if note is None:
        flash('No notes with this ID found to trash.', 'error')
        
        return redirect(url_for("main_page_module.all_entry"))  
    
    if note[6] != session['user_id']:
        flash('You do not have the permission to trash this note', 'error')
        
        return redirect(url_for("main_page_module.all_entry")) 
    
    note_sql_trash_one(note_id)     
    
    flash(f'Note -{note[1]}- successfully trashed.', 'success')  
    
    return redirect(url_for("main_page_module.all_entry"))  


@main_page_module.route('/all_entry_trashed/')
@login_required
def all_entry_trashed():
    notes = note_sql_get_all_trashed(session['user_id'])
   
    return render_template("main_page_module/all_entry_trashed.html", notes=notes)


@main_page_module.route('/new_entry', methods=['GET', 'POST'])
@login_required
def new_entry():
    # If sign in form is submitted
    form = EntryForm(request.form)
    
    # Verify the sign in form
    if form.validate_on_submit():
        note_title = str(form.title.data).strip()
        
        try:
            note_sql_create(note_title, form.entry_text.data, session['user_id'])
            note_id = cursor.lastrowid
            
            note_user_table_sql_create(note_id, session['user_id'], True)
        except:
            connection.rollback()        
        
        #create argus index
        notes = note_sql_get_all_active()
        new_index = WSearch()
        new_index.index_create(notes)
        
        flash('Entry successfully created!', 'success')
        flash('Argus index successfully updated', 'success')
        
        return redirect(f"view_entry/{note_id}")
        #return redirect(url_for("main_page_module.view_entry"), entry_name=new_filename)

    return render_template("main_page_module/new_entry.html", form=form)

@main_page_module.route('/all_entry/')
@login_required
def all_entry():
    notes = note_sql_get_all_active()
   
    return render_template("main_page_module/all_entry.html", notes=notes)

@main_page_module.route('/view_entry/<note_id>', methods=['GET', 'POST'])
@login_required
def view_entry(note_id):
    note = note_sql_get_one(note_id)
    
    if note is None:
        flash('No entrie found', 'error')
        
        return redirect(url_for("main_page_module.index"))

    title = note[1]
    text = note[2]

    return render_template("main_page_module/view_entry.html", entry_name=title, entry_text=text, note_id=note_id)

@main_page_module.route('/edit_entry/<note_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(note_id):
    note = note_sql_get_one(note_id)
    
    if note is None:
        flash('No entrie found', 'error')
        
        return redirect(url_for("main_page_module.all_entry"))
    
    form = EditEntryForm()
    form.process(id = note[0],
                 title = note[1],
                 note_text = note[2])    
    
    return render_template("main_page_module/edit_entry.html", note=note, form=form)

@main_page_module.route('/change_entry/', methods=['POST'])
@login_required
def change_entry():
    form = EditEntryForm(request.form)
    note_id = form.id.data
    
    if form.validate_on_submit():
        note = note_sql_get_one(note_id)
        
        if note is  None:
            flash('No entrie found', 'error')
            
            return redirect(url_for("main_page_module.all_entry"))  
        
        note_sql_update_one(note_id, form.title.data, form.note_text.data, session['user_id'] )
        
        #create argus index
        notes = note_sql_get_all_active()
        new_index = WSearch()
        new_index.index_create(notes)
        
        flash('Entry successfully Eddited!', 'success')
        flash('Argus index successfully updated', 'success')
        
        return redirect(url_for("main_page_module.view_entry", note_id=form.id.data))
    
    flash('Invalid Data', 'error')
    
    return redirect(url_for("main_page_module.all_entry"))      
        
    
@main_page_module.route('/get_zipped_entries/')
@login_required
def get_zipped_entries():
    now = datetime.datetime.now()
    
    base_path = pathlib.Path('app//main_page_module//data//')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            print
            z.write(f_name, os.path.basename(f_name))
    data.seek(0)
    
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename=f'all_entries_{now.strftime("%Y-%m-%d_%H-%M")}.zip',
        cache_timeout=0
    )


@main_page_module.route('/admin/all_users/')
@login_required
def all_users():
    users = user_sql_get_all()
   
    return render_template("main_page_module/admin/all_users.html", users=users)


@main_page_module.route('/admin/view_user/<user_id>')
@login_required
def view_user(user_id):
    user = user_sql_get_one(user_id)
   
    if not user:
        flash('User does not exist.', 'error')
        
        return redirect(url_for("main_page_module.all_users"))     
    
    form = EditUserForm()
    form.process(id = user[0],
                 name = user[1],
                 email = user[3])
    
   
    return render_template("main_page_module/admin/view_user.html", form=form, user=user)

@main_page_module.route('/admin/modify_user/', methods=['POST'])
@login_required
def modify_user():
    form = EditUserForm(request.form)
    
    if form.validate_on_submit():
        user = user_sql_get_one(form.id.data)
        
        if not user:
            flash('User does not exist.', 'error')
        
            return redirect(url_for("main_page_module.all_users")) 
        
        user_sql_update_one(form.id.data, form.name.data, form.email.data, form.password.data)

        
        flash('User successfully Eddited!', 'success')
        
        return redirect(url_for("main_page_module.view_user", user_id=form.id.data, form=form))
    
    flash('Invalid data.', 'error')

    return redirect(url_for("main_page_module.all_users"))     
    

@main_page_module.route('/admin/delete/', methods=['POST'])
@login_required
def delete_user():
    user = user_sql_get_one(request.form["id"])
       
    if not user:
        flash('User does not exist.', 'error')
        
        return redirect(url_for("main_page_module.all_users")) 
    
    else:
        user_sql_delete_one(user[0])
        
        flash(f'User {user[1]} - {user[2]} successfully deleted.', 'success')
        
        return redirect(url_for("main_page_module.all_users")) 
    

# Set the route and accepted methods
@main_page_module.route('/login/', methods=['GET', 'POST'])
def login():

    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        user_id = user_sql_login_check(form.username_or_email.data, form.password.data)

        if user_id is not False:
            session['user_id'] = user_id[0]
            
            #set permanent login, if selected
            if form.remember.data == True:
                session.permanent = True

            flash('Welcome %s' % user_id[1], 'success')
            
            return redirect(url_for('main_page_module.index'))

        flash('Wrong email or password', 'error')
    
    try:
        if(session['user_id']):
            return redirect(url_for("main_page_module.index"))
    
    except:
        return render_template("main_page_module/auth/login.html", form=form)

@main_page_module.route('/logout/')
@login_required
def logout():
    session.pop("user_id", None)
    session.permanent = False
    
    flash('You have been logged out. Have a nice day!', 'success')

    return redirect(url_for("main_page_module.login"))

# Set the route and accepted methods
@main_page_module.route('/register/', methods=['GET', 'POST'])
def register():
    #insert check, if the user is already logged in
    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user_sql_create(form.username.data, form.email.data, form.password.data)
        
        flash('Congratulations, you are now a registered user!', 'success')
        
        return redirect(url_for('main_page_module.login'))
    return render_template('main_page_module/auth/register.html', title='Register', form=form)
