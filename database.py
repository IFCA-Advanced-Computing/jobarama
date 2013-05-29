#-------------------------------------------------------------------------------
import sqlite3
import bcrypt
import os
import shutil

#-------------------------------------------------------------------------------
template = 'template.db'
database = 'database.db'

#-------------------------------------------------------------------------------
def init():
    if not os.path.isfile( database ):
        shutil.copy( template, database )

#-------------------------------------------------------------------------------
def checkUser( name, passwd ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'SELECT passwd FROM user WHERE name=?', (name,) )
    val = c.fetchone()
    conn.close()
    if val is not None:
        return bcrypt.hashpw( passwd, val[0] ) == val[0]

    return False

#-------------------------------------------------------------------------------
