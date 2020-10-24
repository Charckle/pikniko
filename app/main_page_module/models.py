from datetime import datetime

from app import db

# Import password / encryption helper tools
#from werkzeug import check_password_hash, generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

 
def icon_create(name, link):
   
    sql_command = f"""INSERT INTO icons (name, link)
                  VALUES (%s, %s);"""
    
    cursor = db.query(sql_command, (name, link))
    db.conn.commit()
    
    icon_id = cursor.lastrowid
    
    return icon_id


def icon_change(icon_id, name, link):
    sql_command = f"""UPDATE icons SET name = %s, link = %s
     WHERE id = %s;"""
    
    cursor = db.query(sql_command, (name, link, icon_id))
    db.conn.commit()
    

def icon_get_one(icon_id):
    sql_command = f"SELECT * FROM icons WHERE id = %s;"
    
    cursor = db.query(sql_command, (icon_id,))
    result = cursor.fetchone()
    
    return result

        
def icon_get_all():
    sql_command = f"SELECT * FROM icons ORDER BY name ASC;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchall()
    
    return result


def mtag_create(name, myth_id):
    
    try:
        sql_command = f"""INSERT INTO mtags (name)
                      VALUES (%s);"""
        
        cursor = db.query(sql_command, (name,))
        mtag_id = cursor.lastrowid
        
        #add tag to location
        sql_command = f"""INSERT INTO myth_mtag (id_mtag, id_myth)
                      VALUES (%s, %s);"""
        
        cursor = db.query(sql_command, (id_mtag, id_myth))
        
        db.conn.commit()
        
    except:
        db.conn.rollback()


def mtag_add(myth_id, mtag_id):
   
    sql_command = f"""INSERT INTO myth_mtag (id_mtag, id_myth)
                  VALUES (%s, %s);"""
    
    cursor = db.query(sql_command, (myth_id, mtag_id))
    db.conn.commit()
    

def myth_mtag_get_one(myth_mtag_id):
    sql_command = f"SELECT * FROM myth_mtag WHERE id = %s;"
    
    cursor = db.query(sql_command, (myth_mtag_id,))
    result = cursor.fetchone()
    
    return result

def myth_mtag_get_one_by(myth_id, mtag_id):
    sql_command = f"SELECT * FROM myth_mtag WHERE id_myth = %s AND id_mtag = %s ;"
    
    cursor = db.query(sql_command, (myth_id, mtag_id))
    result = cursor.fetchone()
    
    return result

def mtag_get_one(mtag_id):
    sql_command = f"SELECT * FROM mtags WHERE id = %s;"
    
    cursor = db.query(sql_command, (mtag_id,))
    result = cursor.fetchone()
    
    return result


def myth_mtag_remove(myth_mtag_id, id_mtag):
   
    sql_command = f"DELETE FROM myth_mtag WHERE id = %s ;"
    cursor = db.query(sql_command, (myth_mtag_id,))
    db.conn.commit()
    
    try:
        #delete the tag connection
        sql_command = f"DELETE FROM myth_mtag WHERE id = %s;"
    
        cursor = db.query(sql_command, (myth_mtag_id,))
        db.conn.commit()
    
        #check if the tag is connected to anything anymore
        sql_command = f"SELECT * FROM myth_mtag WHERE id_mtag = %s;"
    
        cursor = db.query(sql_command, (id_mtag,))
        results = cursor.fetchall()
    
        #if not, delete it
        if (len(results) is 0):
            sql_command = f"DELETE FROM mtags WHERE id = %s;"
    
            cursor = db.query(sql_command, (id_mtag,))
            db.conn.commit()
    except:
        db.conn.rollback()   
        
def mtag_get_all():
    sql_command = f"SELECT * FROM mtags;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchall()
    
    return result


def mtag_get_numbers():
    sql_command = f"SELECT COUNT(*) FROM mtags;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchone()
    
    return result


def mtag_get_all_of_myth(myth_id):
    sql_command = f"SELECT * FROM myth_mtag LEFT JOIN mtags ON myth_mtag.id_mtag = mtags.id WHERE myth_mtag.id_myth = %s;"
    
    cursor = db.query(sql_command, (myth_id,))
    result = cursor.fetchall()
    
    return result


def myth_create(name, desc_s, desc_l, coord, info):
   
    sql_command = f"""INSERT INTO myths (name, desc_s, desc_l, coord, info)
                  VALUES (%s, %s, %s, %s, %s);"""
    
    cursor = db.query(sql_command, (name, desc_s, desc_l, coord, info))
    db.conn.commit()
    
    myth_id = cursor.lastrowid
    
    return myth_id

def myth_get_one(myth_id):
    sql_command = f"SELECT * FROM myths WHERE id = %s;"
    
    cursor = db.query(sql_command, (myth_id,))
    result = cursor.fetchone()
    
    return result


def myth_get_all():
    sql_command = f"SELECT id, name, LEFT(desc_s , 100) FROM myths ;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchall()
    
    return result


def myth_get_numbers():
    sql_command = f"SELECT COUNT(*) FROM myths;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchone()
    
    return result


def myth_get_all_with_mtag(mtag_id):
    sql_command = f"SELECT myths.id, myths.name, myths.desc_s FROM myth_mtag LEFT JOIN myths ON myth_mtag.id_myth = myths.id WHERE myth_mtag.id_mtag = %s;"
    
    cursor = db.query(sql_command, (mtag_id,))
    result = cursor.fetchall()
    
    return result

def myth_get_all_with_mtag_for_argus(mtag_id):
    sql_command = f"SELECT myths.id FROM myth_mtag LEFT JOIN myths ON myth_mtag.id_myth = myths.id WHERE myth_mtag.id_mtag = %s;"
    
    cursor = db.query(sql_command, (mtag_id,))
    result = cursor.fetchall()
    
    return result


def myth_change(myth_id, name, desc_s, desc_l, coord, info):
    sql_command = f"""UPDATE myths SET name = %s, desc_s = %s, desc_l = %s, coord = %s, info = %s
     WHERE id = %s;"""
    
    cursor = db.query(sql_command, (name, desc_s, desc_l, coord, info, myth_id))
    db.conn.commit()


def myth_delete_one(myth_id):
    sql_command = f"DELETE FROM myths WHERE id = %s;"
    
    cursor = db.query(sql_command, (myth_id,))
    db.conn.commit()
    
    
def loc_tag_remove(loc_tag_id, id_tag):
   
    sql_command = f"DELETE FROM loc_tag WHERE id = %s ;"
    cursor = db.query(sql_command, (loc_tag_id,))
    db.conn.commit()
    
    try:
        #delete the tag connection
        sql_command = f"DELETE FROM loc_tag WHERE id = %s;"
    
        cursor = db.query(sql_command, (loc_tag_id,))
        db.conn.commit()
    
        #check if the tag is connected to anything anymore
        sql_command = f"SELECT * FROM loc_tag WHERE id_tag = %s;"
    
        cursor = db.query(sql_command, (id_tag,))
        results = cursor.fetchall()
    
        #if not, delete it
        if (len(results) is 0):
            sql_command = f"DELETE FROM tags WHERE id = %s;"
    
            cursor = db.query(sql_command, (id_tag,))
            db.conn.commit()
    except:
        db.conn.rollback()    
    

def tag_create(name, location_id):
    
    try:
        sql_command = f"""INSERT INTO tags (name)
                      VALUES (%s);"""
        
        cursor = db.query(sql_command, (name,))
        tag_id = cursor.lastrowid
        
        #add tag to location
        sql_command = f"""INSERT INTO loc_tag (id_tag, id_loc)
                      VALUES (%s, %s);"""
        
        cursor = db.query(sql_command, (tag_id, location_id))
        
        db.conn.commit()
        
    except:
        db.conn.rollback()


def tag_add(location_id, tag_id):
   
    sql_command = f"""INSERT INTO loc_tag (id_loc, id_tag)
                  VALUES (%s, %s);"""
    
    cursor = db.query(sql_command, (location_id, tag_id))
    db.conn.commit()
    
    
def loc_tag_get_one(loc_tag_id):
    sql_command = f"SELECT * FROM loc_tag WHERE id = %s;"
    
    cursor = db.query(sql_command, (loc_tag_id,))
    result = cursor.fetchone()
    
    return result


def loc_tag_get_one_by(location_id, tag_id):
    sql_command = f"SELECT * FROM loc_tag WHERE id_loc = %s AND id_tag = %s ;"
    
    cursor = db.query(sql_command, (location_id, tag_id))
    result = cursor.fetchone()
    
    return result


def tag_get_one(tag_id):
    sql_command = f"SELECT * FROM tags WHERE id = %s;"
    
    cursor = db.query(sql_command, (tag_id,))
    result = cursor.fetchone()
    
    return result


def tag_get_all():
    sql_command = f"SELECT * FROM tags;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchall()
    
    return result


def tag_get_numbers():
    sql_command = f"SELECT COUNT(*) FROM tags;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchone()
    
    return result


def tag_get_all_of_location(location_id):
    sql_command = f"SELECT * FROM loc_tag LEFT JOIN tags ON loc_tag.id_tag = tags.id WHERE loc_tag.id_loc = %s;"
    
    cursor = db.query(sql_command, (location_id,))
    result = cursor.fetchall()
    
    return result
    
    
def tag_change(tag_id, name):
    sql_command = f"""UPDATE tags SET name = %s
     WHERE id = %s;"""
    
    cursor = db.query(sql_command, (name, tag_id))
    db.conn.commit()
    

def img_create(name, link, location_id):
   
    sql_command = f"""INSERT INTO imgs (name, link, id_location)
                  VALUES (%s, %s, %s);"""
        
    cursor = db.query(sql_command, (name, link, location_id))
    db.conn.commit()
    
    img_id = cursor.lastrowid
    
    return img_id
    
    
def img_get_one(img_id):
    sql_command = f"SELECT * FROM imgs WHERE id = %s;"
    cursor = db.query(sql_command, (img_id,))
    result = cursor.fetchone()
    
    #print(result)
    
    return result    

def img_get_all_of_location(location_id):
    sql_command = f"SELECT * FROM imgs WHERE id_location = %s;"
    
    cursor = db.query(sql_command, (location_id,))
    result = cursor.fetchall()
    
    return result


def img_remove(img_id):
    sql_command = f"DELETE FROM imgs WHERE id = %s ;"
    cursor = db.query(sql_command, (img_id,))
    db.conn.commit()


def parking_create(name, cost, coord, location_id):
   
    sql_command = f"""INSERT INTO parkings (name, cost, coord, id_location)
                  VALUES (%s, %s, %s, %s);"""
        
    cursor = db.query(sql_command, (name, cost, coord, location_id))
    db.conn.commit()


def parking_get_one(parking_id):
    sql_command = f"SELECT * FROM parkings WHERE id = %s;"
    cursor = db.query(sql_command, (parking_id,))
    result = cursor.fetchone()
    
    return result

def parking_get_all_of_location(location_id):
    sql_command = f"SELECT * FROM parkings WHERE id_location = %s;"
    
    cursor = db.query(sql_command, (location_id,))
    result = cursor.fetchall()
    
    return result

    
def parking_change(parking_id, cost, coord):
    sql_command = f"""UPDATE parkings SET name = %s, cost = %s, coord = %s
     WHERE id = %s;"""
    
    cursor = db.query(sql_command, (name, cost, coord, parking_id))
    db.conn.commit()


def parking_remove(parking_id):
   
    sql_command = f"DELETE FROM parkings WHERE id = %s ;"
    cursor = db.query(sql_command, (parking_id,))
    db.conn.commit()
 
    
def icon_create(name, link):
   
    sql_command = f"""INSERT INTO icons (name, link)
                  VALUES (%s, %s);"""
       
    cursor = db.query(sql_command, (name, link))
    db.conn.commit()
    
    icon_id = cursor.lastrowid
    
    return icon_id


def location_create(name, desc_s, desc_l, rating, tts, coord, mtld, contact, timetable, fee, child, season, icon):
   
    sql_command = f"""INSERT INTO locations (name, desc_s, desc_l, rating, tts, coord, mtld, contact, timetable, fee, child, season, icon)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
       
    cursor = db.query(sql_command, (name, desc_s, desc_l, rating, tts, coord, mtld, contact, timetable, fee, child, season, icon))
    db.conn.commit()
    
    location_id = cursor.lastrowid
    
    return location_id


def location_get_all():
    sql_command = f"SELECT locations.id, locations.name, LEFT(locations.desc_s , 100), icons.link, locations.coord, imgs.link FROM locations LEFT JOIN icons ON icons.id = locations.icon LEFT JOIN imgs ON imgs.id_location = locations.id GROUP BY locations.id;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchall()
    
    #print(result)
    
    
    return result


def location_get_all_where(command):
    sql_command = f"""SELECT locations.id, locations.name, LEFT(locations.desc_s , 100), icons.link, locations.coord, imgs.link FROM locations LEFT JOIN loc_tag ON loc_tag.id_loc = locations.id
    LEFT JOIN icons ON icons.id = locations.icon LEFT JOIN imgs ON imgs.id_location = locations.id WHERE locations.id > 0 %s GROUP BY locations.id ;"""
    
    cursor = db.query(sql_command, (command,))
    result = cursor.fetchall()       
    
    return result


def location_get_all_where_rating(rating):
    sql_command = f"SELECT id FROM locations WHERE rating = %s;"
    
    cursor = db.query(sql_command, (rating,))
    result = cursor.fetchall()       
    
    return result


def location_get_all_argus():
    sql_command = f"SELECT id, name, desc_l FROM locations ;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchall()
    
    return result

def myths_get_all_argus():
    sql_command = f"SELECT id, name, desc_l FROM myths ;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchall()
    
    return result


def location_get_all_with_ids(ids):
    ids = ','.join([str(i) for i in ids]) 
    sql_command = f"SELECT locations.id, locations.name, LEFT(locations.desc_s , 100), icons.link, locations.coord, imgs.link FROM locations LEFT JOIN icons ON icons.id = locations.icon LEFT JOIN imgs ON imgs.id_location = locations.id WHERE locations.id IN (%s) GROUP BY locations.id;"
    
    cursor = db.query(sql_command, (ids,))
    result = cursor.fetchall()
    
    return result

def location_get_all_with_tag(tag_id):
    sql_command = f"SELECT locations.id, locations.name, locations.desc_s, icons.link FROM loc_tag LEFT JOIN locations ON loc_tag.id_loc = locations.id LEFT JOIN icons ON icons.id = locations.icon WHERE loc_tag.id_tag = %s;"
    
    cursor = db.query(sql_command, (tag_id,))
    result = cursor.fetchall()
    
    return result

def location_get_all_id_with_tag(tag_id):
    sql_command = f"SELECT locations.id FROM loc_tag LEFT JOIN locations ON loc_tag.id_loc = locations.id LEFT JOIN icons ON icons.id = locations.icon WHERE loc_tag.id_tag = %s;"
    
    cursor = db.query(sql_command, (tag_id,))
    result = cursor.fetchall()
    
    return result

def location_get_all_with_tag_for_argus(tag_id):
    sql_command = f"SELECT locations.id FROM loc_tag LEFT JOIN locations ON loc_tag.id_loc = locations.id WHERE loc_tag.id_tag = %s;"
    
    cursor = db.query(sql_command, (tag_id,))
    result = cursor.fetchall()
    
    return result


def location_get_one(location_id):
    sql_command = f"SELECT * FROM locations LEFT JOIN icons ON icons.id = locations.icon WHERE locations.id = %s;"
    
    cursor = db.query(sql_command, (location_id,))
    result = cursor.fetchone()
    
    return result

def location_get_icon_link(location_id):
    sql_command = f"SELECT icons.link FROM locations LEFT JOIN icons ON icons.id = locations.icon WHERE locations.id = %s ;"
    
    cursor = db.query(sql_command, (location_id,))
    result = cursor.fetchone()
    
    return result


def location_get_numbers():
    sql_command = f"SELECT COUNT(*) FROM locations;"
    
    cursor = db.query(sql_command, ())
    result = cursor.fetchone()
    
    return result

    
def location_change(location_id, name, desc_s, desc_l, rating, tts, coord, mtld, contact, timetable, fee, child, season, icon):
    sql_command = f"""UPDATE locations SET name = %s, desc_s = %s, desc_l = %s, rating = %s, tts = %s, coord = %s, 
     mtld = %s, contact = %s, timetable = %s, fee = %s, child = %s, season = %s, icon = %s 
     WHERE id = %s;"""
      
    cursor = db.query(sql_command, (name, desc_s, desc_l, rating, tts, coord, mtld, contact, timetable, fee, child, season, icon, location_id))
    db.conn.commit()


def location_delete_one(location_id):
    try:
        sql_command = f"DELETE FROM imgs WHERE id_location = %s;"
        
        cursor = db.query(sql_command, (location_id,))
        
        
        sql_command = f"DELETE FROM locations WHERE id = %s;"
        
        cursor = db.query(sql_command, (location_id,))
        
        
        db.conn.commit()
        
    except:
        db.conn.rollback()       
    
    
def user_sql_create(username, email, password):
    password_hash = generate_password_hash(password)
    
    sql_command = f"""INSERT INTO users (name, username, email, password, status)
        VALUES (%s, %s, %s, %s, True);"""

    cursor = db.query(sql_command, (username, username, email, password_hash))
    db.conn.commit()    


def user_sql_check_username(username):
    
    sql_command = f"SELECT id, username, password FROM users WHERE (%s = username);"
    
    cursor = db.query(sql_command, (username,))
    results = cursor.fetchone()
    
    #is a user is found, returns its ID
    if results is not None:
        return results
    
    return False

def user_get_id_from_username(username):
    
    sql_command = f"SELECT id FROM users WHERE (%s = username);"
    
    cursor = db.query(sql_command, (username,))
    results = cursor.fetchone()
    
    return results

def user_sql_check_email(email):
    
    sql_command = f"SELECT id, email, password FROM users WHERE (%s = email);"
    
    cursor = db.query(sql_command, (email,))
    results = cursor.fetchone()
    
    #is a user is found, returns its ID
    if results is not None:
        return results
    
    return False

def user_sql_login_check(username_or_email, password):
    
    sql_command = f"SELECT id, username, email, password FROM users WHERE (%s = username) OR (%s = email);"
    
    cursor = db.query(sql_command, (username_or_email, username_or_email))
    results = cursor.fetchone()
    
    #is a user is found, returns its ID
    if results is not None:
        if check_password_hash(results[3], password):
            
            return results
    
    return False


def user_sql_get_all():
    sql_command = f"SELECT id, name, username FROM users;"
    
    cursor = db.query(sql_command, ())
    results = cursor.fetchall()
    
    return results


def user_sql_get_one(user_id):
    sql_command = f"SELECT * FROM users WHERE id = %s;"
    
    cursor = db.query(sql_command, (user_id,))
    result = cursor.fetchone()
    
    return result


def user_sql_delete_one(user_id):
    sql_command = f"DELETE FROM users WHERE id = %s;"
    
    cursor = db.query(sql_command, (user_id,))
    db.conn.commit()
    
    
def user_sql_update_one(user_id, name, email, password):
    password_for_sql = ""
    if password != "":
        password_hash = generate_password_hash(password)
        password_for_sql = f", password = '{password_hash}'"
  
    sql_command = f"UPDATE users SET name = %s, email = %s%s WHERE id = %s"
    
    cursor = db.query(sql_command, (name, email, password_for_sql, user_id))
    db.conn.commit()
