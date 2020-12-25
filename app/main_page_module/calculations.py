import math
import re
import json
from unidecode import unidecode
import datetime

def add_stats(page):
    mesec = get_date()
    data = json_read(".", "data.json")
    data[page][mesec-1] += 1 

    json_write(".", "data.json", data)    

def get_date():
    dt = datetime.datetime.now()

    return dt.month

#sanitize the code for saving to a file on the OS
def get_valid_filename(s):

    """
    Stolen from Django, me thinks?
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """

    s = unidecode(str(s).strip().replace(' ', '_'))

    return re.sub(r'(?u)[^-\w.]', '', s)

def json_write(location, filename, dictio, sanitation=True):
    
    location = location.strip()

    if sanitation == True:
        filename = get_valid_filename(filename)
    
    location_filename = location + "/" + filename

    with open(f'{location_filename}', 'w') as outfile:
        json.dump(dictio, outfile)

def json_read(location, filename):
    
    location_filename = location + "/" + filename

    with open(f'{location_filename}') as json_file:
        data = json.load(json_file)
        
        return data
    

def calclulate_food(peoplenum, vegiSlider, childnum, vegiChild, cevap, plesk, vratovina, perutinicke,
                    bucke, gobce, paprikas, melancanno, pivicko, colica, sokec, ledek):

    #izracun ljudi in otrok mesojedcev
    mesojedci = peoplenum - vegiSlider
    otroci_mesa = childnum - vegiChild  
    #skupno vsi ljudje
    skupno_ljudje = peoplenum + childnum
    
    #meso
    skupna_mozna_kolicina_mesa = cevap + plesk + vratovina + perutinicke
    #        
    cevap_proc = cevap * 1 / skupna_mozna_kolicina_mesa
    plesk_proc = plesk * 1 / skupna_mozna_kolicina_mesa
    vratovina_proc = vratovina * 1 / skupna_mozna_kolicina_mesa
    perutinicke_proc = perutinicke * 1 / skupna_mozna_kolicina_mesa   
    
    #zelenjava
    skupna_mozna_kolicina_zelenjave = bucke + gobce + paprikas + melancanno
    #           
    bucke_proc = bucke * 1 / skupna_mozna_kolicina_zelenjave
    gobce_proc = gobce * 1 / skupna_mozna_kolicina_zelenjave
    paprikas_proc = paprikas * 1 / skupna_mozna_kolicina_zelenjave
    melancanno_proc = melancanno * 1 / skupna_mozna_kolicina_zelenjave
    
    #pijaca
    skupna_mozna_kolicina_brezalko = colica + sokec
    colica_proc = colica / skupna_mozna_kolicina_brezalko
    sokec_proc = sokec / skupna_mozna_kolicina_brezalko
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
    
    kruh_odrasli_g = 150
    kruh_otroci_g = 50
    
    cebula_odrasli_g = 25
    cebula_otroci_g = 15
    
    pivo_ml = pivicko * 500
    cola_odrasli_ml = 1200
    cola_otroci_ml = 700
    sok_odrasli_ml = 780
    sok_otroci_ml = 455
    led_odrasli_g = 750
    
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
    
    namazi = math.ceil((skupno_ljudje / 8)) * 0.25
    
    osnovni_p = {"odrasli_m": ["Število odraslih - Meso", mesojedci],
     "odrasli_v": ["Število odraslih - Vegi", vegiSlider],
     "otroci_m": ["Število otrok - Meso", otroci_mesa],
     "otroci_v": ["Število otrok - Vegi", vegiChild]
     }
    
    meso = {"cevap": ["Čevapčiči", round(skupno_cevap * 0.001, 2), round(skupno_cevap * 0.001 * 12, 2)],
     "plesk": ["Pleskavice", round(skupno_plesk * 0.001, 2), round(skupno_plesk * 0.001 * 6.2, 2)],
     "vrat": ["Vratovina", round(skupno_vratovina * 0.001, 2), round(skupno_vratovina * 0.001 * 7, 2)],
     "perut": ["Perutničke", round(skupno_perutinicke * 0.001, 2), round(skupno_perutinicke * 0.001 * 5.5, 2)]
     }
    
    meso_sum = sum([ list[1] for index, list in meso.items()])
    meso_price = sum([ list[2] for index, list in meso.items()])
    
    vegi = {
     "vegi": ["Vegi odrasli", skupno_vegi]
     }
    
    bucke_vegi = bucke_proc * skupno_vegi
    gobe_vegi = gobce_proc * skupno_vegi
    pap_vegi = paprikas_proc * skupno_vegi
    melan_vegi = melancanno_proc * skupno_vegi
    
    zelenjava = {"bucke": ["Bučke", round((skupno_bucke + bucke_vegi) * 0.001, 2), round((skupno_bucke + bucke_vegi)  * 0.001 * 0.9, 2)],
     "gobe": ["Gobice", round((skupno_gobce + gobe_vegi) * 0.001, 2), round((skupno_gobce + gobe_vegi) * 0.001 * 5, 2)],
     "pap": ["Paprika", round((skupno_paprikas + pap_vegi) * 0.001, 2), round((skupno_paprikas + pap_vegi) * 0.001*3, 2)],
     "melan": ["Melancani", round((skupno_melancanno + melan_vegi) * 0.001, 2), round((skupno_melancanno + melan_vegi) * 0.001 * 3, 2)]
     }
    
    zelenjava_sum = sum([ list[1] for index, list in zelenjava.items()])
    zelenjava_price = sum([ list[2] for index, list in zelenjava.items()])
    
    pivo = {"skup_pivo": ["Skupno Pivo", round(skupno_pivo * 0.001, 2), round(skupno_pivo * 0.001 * 1, 2)],
     "veliko_pivo": ["Velikega", skupno_pivo_veliko, 0],
     "malo_pivo": ["Ali majhnega", skupno_pivo_malo, 0]
     }
    
    pivo_price = sum([ list[2] for index, list in pivo.items()])
    
    sokovi = {"skup_cola": ["Skupno Cola ", round(skupno_cola * 0.001, 2), round(skupno_cola * 0.001 * 1.1, 2)],
     "cola_literpol": ["Cola 1,5l", skupno_cola_literpol, 0],
     "skup_sok": ["Skupno Sok", round(skupno_sok * 0.001, 2), round(skupno_sok * 0.001 * 1.2, 2)],
     "sok_liter": ["Sokl 1l", skupno_sok_liter, 0]
     }
    
    sokovi_price = sum([ list[2] for index, list in sokovi.items()])
    
    ostalo = {"led_g": ["Gramov Ledu", round(skupno_led_g * 0.001, 2), round(skupno_led_g * 0.001 * 1.3, 2)],
     "gram_veb": ["Gramov čebule", round(skupno_cebula_g * 0.001, 2), round(skupno_cebula_g * 0.001 * 1, 2)],
     "gram_kruh": ["Gramov kruha", round(skupno_kruh_g * 0.001, 2), round(skupno_kruh_g * 0.001 * 1.4, 2)],
     "kos_kruh": ["Kosov kruha", skupno_kruh_kos, 0],
     "kajmak": ["Kajmak", namazi, namazi * 2 * 2.9],
     "ajvar": ["Ajvar", namazi, namazi * 2 * 1.7],
     "ketchup": ["Ketchup", namazi, namazi * 2 * 2.3],
     "majoneza": ["Majoneza", round(namazi /2, 2), round(namazi * 2 * 2.29, 2)],
     "pikantna": ["Robit Hot", 1, 3.4],
     "skupno_oglje": ["Oglje", round(skupno_oglje * 0.001, 2), round(skupno_oglje * 0.001 * 1.7, 2)],
     "olje": ["Olje", 1, 1.8],     
     "rola_papir": ["Rola papirja", 1, 0.9],
     "servjet": ["Servjeti", skupno_ljudje * 4, (skupno_ljudje * 4) * 0.075],
     "vrece_cmeti": ["Vreče za smeti", math.ceil(skupno_ljudje * 0.2), math.ceil(skupno_ljudje * 0.2) * 0.18],
     "kozarci": ["Kozarci", skupno_ljudje * 3, round((skupno_ljudje * 3) * 0.14)],
     "krozniki": ["Krožniki", skupno_ljudje * 2, round((skupno_ljudje * 2) * 0.14)]
    }
    
    ostalo_price = sum([ list[2] for index, list in ostalo.items()])
    
    price_sum = meso_price + zelenjava_price + pivo_price + sokovi_price + ostalo_price
    
    
    return osnovni_p, meso, meso_sum, vegi, zelenjava, zelenjava_sum, pivo, sokovi, ostalo, price_sum