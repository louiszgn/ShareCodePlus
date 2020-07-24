#!/usr/bin/env python3

from string import ascii_letters, digits
from itertools import chain
from random import choice
from sqlite3 import *
import os

conn = connect("data.txt")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS codes (uid TEXT, code TEXT, language TEXT)")


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
    curs = conn.cursor()
    curs.execute("INSERT INTO codes(uid, code, language) VALUES(uid, code, lang)")
    conn.commit()
    return uid

def read_code(uid):
    '''Lit le document data/uid'''
    try:
        curs = conn.cursor()
        curs.execute("SELECT code,lang FROM codes WHERE uid = ?",(uid,))
        r = curs.fetchone()
        return r
    except:
        return None

def get_last_entries_from_files(n=10,nlines=10):
    entries = os.scandir('data')
    d = []
    entries = sorted(list(entries),
                     key=(lambda e: e.stat().st_mtime),
                     reverse=True) 
    for i,e in enumerate(entries):
        if i >= n:
            break
        if e.name.startswith('.'):
            continue
        if e.name.endswith('.lang'):
            continue
        with open('data/{}'.format(e.name)) as fd:
            code = ''.join(( fd.readline() for i in range(nlines) ))
            if fd.readline():
                code += '\n...'
        d.append({ 'uid':e.name, 'code':code })
    return d

# cur.close()
# conn.close()

# cur.execute("INSERT INTO codes(uid, code, language) VALUES(uid, code, lang)")

# x = 'Patrick'
# cur.execute("SELECT code,lang FROM codes WHERE uid = ?",(uid,))