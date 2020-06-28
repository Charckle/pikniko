# Import the database object (db) from the main application module
from app import db

from datetime import datetime

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

from app import connection, cursor



# Define a base model for other database tables to inherit
class Base(db.Model):

    #__abstract__  = True

    id = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

class SharedNotes(db.Model):
    
    #__abstract__  = True
    
    __tablename__ = 'sharedNotes'
    
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users_table.id'), primary_key=True)
    writeable = db.Column(db.Boolean)
    
    user_enabled = db.relationship("User", back_populates="notes")
    note = db.relationship("Note", back_populates="users")



# Define a User model
class User(db.Model):
    #__abstract__  = True
    __tablename__ = 'users_table'
    id = db.Column(db.Integer, primary_key=True)
    
    # User Name
    name    = db.Column(db.String(128),  nullable=False)
    
    # UserName
    username    = db.Column(db.String(128),  nullable=False,
                            unique=True)    

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                         unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    notes = db.relationship("SharedNotes", back_populates="user_enabled")
    
    # New instance instantiation procedure
    def __init__(self, username, email, password):

        self.name     = username
        self.username = username
        self.email    = email
        self.password = password
        self.role = 0
        self.status = 1

    def __repr__(self):
        return '<User %r>' % (self.name)
    
    def set_password(self, password):
            self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password) 

# Define a Note model
class Note(db.Model):
    #__abstract__  = True
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User Name
    title    = db.Column(db.String(128),  nullable=False,
                            unique=True)
    
    # note text
    note_text    = db.Column(db.Text())
    
    #users that can use it
    users = db.relationship("SharedNotes", back_populates="note")
    

    # New instance instantiation procedure
    def __init__(self, title, note_text):

        self.title     = title
        self.note_text = note_text

    def __repr__(self):
        return '<Note %r>' % (self.title)
    



'''
#table taht holds which users can modify the note
sharedNotes = db.Table("notes_access", 
                       db.Column('user_id', db.Integer, db.ForeignKey('users_table.id'), primary_key=True),
                       db.Column('note_id', db.Integer, db.ForeignKey('notes.id'), primary_key=True),
                       db.Column('edit', db.Boolean)
                       )
'''

def user_sql_create(username, email, password):
    password_hash = generate_password_hash(password)
    
    sql_command = f"""INSERT INTO users (name, username, email, password, status)
        VALUES ('{username}', '{username}', '{email}', '{password_hash}', True);"""

    cursor.execute(sql_command)
    connection.commit()    

def user_sql_check_username(username):
    
    sql_command = f"SELECT id, username, password FROM users WHERE ('{username}' = username);"
    
    cursor.execute(sql_command)
    results = cursor.fetchone()
    
    #is a user is found, returns its ID
    if results is not None:
        return results
    
    return False

def user_sql_check_email(email):
    
    sql_command = f"SELECT id, email, password FROM users WHERE ('{email}' = email);"
    
    cursor.execute(sql_command)
    results = cursor.fetchone()
    
    #is a user is found, returns its ID
    if results is not None:
        return results
    
    return False

def user_sql_login_check(username_or_email, password):
    
    sql_command = f"SELECT id, username, email, password FROM users WHERE ('{username_or_email}' = username) OR ('{username_or_email}' = email);"
    
    cursor.execute(sql_command)
    results = cursor.fetchone()
    
    #is a user is found, returns its ID
    if results is not None:
        if check_password_hash(results[3], password):
            
            return results
    
    return False

def user_sql_get_all():
    sql_command = f"SELECT id, name, username FROM users;"
    
    cursor.execute(sql_command)
    results = cursor.fetchall()
    
    return results


def user_sql_get_one(user_id):
    sql_command = f"SELECT * FROM users WHERE id = {user_id};"
    
    cursor.execute(sql_command)
    result = cursor.fetchone()
    
    return result

def user_sql_delete_one(user_id):
    sql_command = f"DELETE FROM users WHERE id = {user_id};"
    
    cursor.execute(sql_command)
    connection.commit()
    
def user_sql_update_one(user_id, name, email, password):
    password_for_sql = ""
    if password != "":
        password_hash = generate_password_hash(password)
        password_for_sql = f", password = '{password_hash}'"
  
    sql_command = f"UPDATE users SET name = '{name}', email = '{email}'{password_for_sql} WHERE id = {user_id}"
    
    cursor.execute(sql_command)
    connection.commit()

def note_sql_create(title, text, id):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    sql_command = f"""INSERT INTO notes (title, text, date_mod, user_last_mod, owner_id)
                  VALUES ('{title}', '{text}', '{timestamp}', '{id}', '{id}');"""
    
    cursor.execute(sql_command)
    connection.commit()

def note_user_table_sql_create(note_id, user_id, write_access):
    
    sql_command = f"""INSERT INTO note_access (note_id, user_id, write_access)
                  VALUES ('{note_id}', '{user_id}', '{write_access}');"""
    
    cursor.execute(sql_command)
    connection.commit()

def note_sql_get_one(note_id):
    sql_command = f"SELECT * FROM notes WHERE id = {note_id};"
    
    cursor.execute(sql_command)
    result = cursor.fetchone()
    
    return result

def note_sql_get_all_active():
    sql_command = f"SELECT * FROM notes WHERE active = True;"
    
    cursor.execute(sql_command)
    results = cursor.fetchall()
    
    return results

def note_sql_get_all_active_of_user(user_id):
    sql_command = f"SELECT notes.id FROM notes RIGHT JOIN note_access ON notes.id = note_access.note_id WHERE note_access.user_id = '{user_id}' ;"
    
    cursor.execute(sql_command)
    results = cursor.fetchall()
    single_list = [x[0] for x in results]
    
    return single_list

def note_sql_get_all_trashed(user_id):
    sql_command = f"SELECT * FROM notes WHERE active = False AND owner_id = '{user_id}';"
    
    cursor.execute(sql_command)
    results = cursor.fetchall()
    
    return results

def note_sql_delete_one(note_id):
    sql_command = f"DELETE FROM notes WHERE id = {note_id};"
    
    cursor.execute(sql_command)
    connection.commit()

def note_sql_trash_one(note_id):
    sql_command = f"UPDATE notes SET active = False WHERE id = '{note_id}';"
    
    cursor.execute(sql_command)
    connection.commit()


def note_sql_update_one(note_id, title, text, user_id):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    sql_command = f"UPDATE notes SET title = '{title}', text = '{text}', date_mod = '{timestamp}', user_last_mod = '{user_id}' WHERE id = '{note_id}';"
    
    cursor.execute(sql_command)
    connection.commit()

