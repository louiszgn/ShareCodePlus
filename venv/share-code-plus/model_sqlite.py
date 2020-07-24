#!/usr/bin/env python3

from string import ascii_letters, digits
from itertools import chain
from random import choice
from sqlite3 import *
import os


create_table_codes = "CREATE TABLE IF NOT EXISTS codes (uid TEXT, code TEXT, language TEXT)"
create_table_users = "CREATE TABLE IF NOT EXISTS users (ip TEXT, nav TEXT, date DATETIME)"
connect(create_table_codes)
connect(create_table_users)

def connectdb(var, command=None, uid=None, code=None, lang=None):
    """ Gère la connexion à la bdd """
    conn = connect("data.txt")
    cur = conn.cursor()
    r = []
    if lang:
        cur.execute(var, (uid, code, lang))
    elif code:
        cur.execute(var, (uid, code))
    elif uid:
        cur.execute(var, (uid,))
    else:
        cur.execute(var)
    
    if command is "insert":
        conn.commit()
    if command is "select":
        r = cur.fetchall()

    cur.close()
    conn.close()
    return r


def create_uid(n=9):
    '''Génère une chaîne de caractères alétoires de longueur n
    en évitant 0, O, I, l pour être sympa.'''
    chrs = [ c for c in chain(ascii_letters,digits)
                        if c not in '0OIl'  ]
    return ''.join( ( choice(chrs) for i in range(n) ) ) 

def save_code(uid=None,code=None,lang=None):
    '''Crée/Enregistre le document sous la forme d'un fichier
    data/uid. Return the file name.
    '''
    if uid is None:
        uid = create_uid()
        code = '# Write your code here...'
        lang = "Python"
        insert = "INSERT INTO codes(uid, code, language) VALUES(?, ?, ?)"
        connectdb(insert, "insert", uid, code, lang)
    else:
        update = "UPDATE codes SET code = ?, language = ? WHERE uid = ?"
        connectdb(update, "insert", code, lang, uid)

    return uid

def read_code(uid):
    '''Lit le document data/uid'''
    select = "SELECT code,language FROM codes WHERE uid = ?"
    r = connectdb(select, "select", uid)
    return r

def get_last_entries_from_db(n=10,nlines=10):
    select = "SELECT uid,code FROM codes"
    r = connectdb(select, "select")
    # r = r.sort(key=lambda t: t[0])

    d = []
    for i in range(len(r)):
        if i >= n:
            break
        d.append({ 'uid':r[i][0], 'code':r[i][1] })
    return d


# cur.close()
# conn.close()

# cur.execute("INSERT INTO codes(uid, code, language) VALUES(uid, code, lang)")

# x = 'Patrick'
# cur.execute("SELECT code,language FROM codes WHERE uid = ?",(uid,))