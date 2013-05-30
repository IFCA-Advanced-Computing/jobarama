#-------------------------------------------------------------------------------
import sqlite3
import bcrypt
import os
import shutil

#-------------------------------------------------------------------------------
BCRYPT_ROUNDS = 5
template = 'template.db'
database = 'database.db'

#-------------------------------------------------------------------------------
def mkEmptyDatabase( dbname ):
    if os.path.isfile( dbname ):
        os.remove( dbname )

    conn = sqlite3.connect( dbname )
    c = conn.cursor()
    c.execute( "CREATE TABLE user (uid INTEGER PRIMARY KEY AUTOINCREMENT, name text, passwd text)" )

    name = 'admin' # same name and passwd
    h = bcrypt.hashpw( name, bcrypt.gensalt(BCRYPT_ROUNDS) )
    c.execute( 'INSERT INTO user VALUES (null,?,?)', (name,h) )
    conn.commit()

    c.execute( "CREATE TABLE file (fid INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, global INTEGER, filename text)" )

    conn.commit()

    conn.close()

#-------------------------------------------------------------------------------
def init():
    if not os.path.isfile( database ):
        shutil.copy( template, database )

#-------------------------------------------------------------------------------
def insertUser( name, passwd ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    h = bcrypt.hashpw( name, bcrypt.gensalt(BCRYPT_ROUNDS) )
    c.execute( 'INSERT INTO user VALUES (?,?)', (name,h) )
    conn.commit()
    conn.close()

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
