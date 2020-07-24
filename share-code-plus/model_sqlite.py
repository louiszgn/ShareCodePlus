#!/usr/bin/env python3

from string import ascii_letters, digits
from itertools import chain
from random import choice
from sqlite3 import *
from flask import request
import datetime
import socket
import os

def connectdb(var, command=None, var1=None, var2=None, var3=None, var4=None):
    """ Gère la connexion à la bdd """
    conn = connect("data.txt")
    cur = conn.cursor()
    r = []
    if var4:
        cur.execute(var, (var1, var2, var3, var4))
    elif var3:
        cur.execute(var, (var1, var2, var3))
    elif var2:
        cur.execute(var, (var1, var2))
    elif var1:
        cur.execute(var, (var1,))
    else:
        cur.execute(var)
    
    if command is "insert":
        conn.commit()
    if command is "select":
        r = cur.fetchall()

    cur.close()
    conn.close()
    return r

create_table_codes = "CREATE TABLE IF NOT EXISTS codes (uid TEXT, code TEXT, language TEXT)"
create_table_users = "CREATE TABLE IF NOT EXISTS users (uid TEXT, ip TEXT, nav TEXT, date DATETIME)"
connectdb(create_table_codes)
connectdb(create_table_users)

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
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    ua = request.user_agent.browser
    dt = datetime.datetime.now()

    if uid is None:
        uid = create_uid()
        code = '# Write your code here...'
        lang = "Python"
        insert_code = "INSERT INTO codes(uid, code, language) VALUES(?, ?, ?)"
        connectdb(insert_code, "insert", uid, code, lang)

        insert_user = "INSERT INTO users(uid, ip, nav, date) VALUES(?, ?, ?, ?)"
        connectdb(insert_user, "insert", uid, IPAddr, ua, dt)
    else:
        update_code = "UPDATE codes SET code = ?, language = ? WHERE uid = ?"
        connectdb(update_code, "insert", code, lang, uid)

        update_user = "UPDATE users SET ip = ?, nav = ?, date = ? WHERE uid = ?"
        connectdb(update_user, "insert", IPAddr, ua, dt, uid)

    return uid

def read_code(uid):
    '''Lit le document data/uid'''
    select = "SELECT code,language FROM codes WHERE uid = ?"
    r = connectdb(select, "select", uid)
    return r

def get_last_entries_from_db(n=10):
    select = "SELECT uid,code FROM codes"
    r = connectdb(select, "select")
    d = []

    for i in range(len(r)):
        if i >= n:
            break
        d.append({ 'uid':r[i][0], 'code':r[i][1] })
    return d

def get_users_from_db(n=10):
    select = "SELECT uid,ip,nav,date FROM users"
    r = connectdb(select, "select")
    d = []
    
    for i in range(len(r)):
        if i >= n:
            break
        d.append({ 'uid':r[i][0], 'ip':r[i][1], 'nav':r[i][2], 'date':r[i][3] })
    return d