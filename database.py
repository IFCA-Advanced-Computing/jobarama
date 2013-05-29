#-------------------------------------------------------------------------------
import sqlite3
import bcrypt
import os
import shutil

#-------------------------------------------------------------------------------
database = 'database.db'

#-------------------------------------------------------------------------------
def init():
    if not os.path.isfile( database ):
        shutil.copy( 'template.db', database )

#-------------------------------------------------------------------------------
def checkUser( name, passwd ):
    conn = sqlite3.connect('template.db')
    c = conn.cursor()
    t = (name,)
    c.execute( 'SELECT passwd FROM user WHERE name=?', (name,) )
    val = c.fetchone()
    if val is not None:
        return bcrypt.hashpw( passwd, val[0] ) == val[0]

    return False

#-------------------------------------------------------------------------------
