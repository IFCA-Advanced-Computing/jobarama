#-------------------------------------------------------------------------------
import sqlite3
import bcrypt
import os
import shutil

#-------------------------------------------------------------------------------
BCRYPT_ROUNDS = 5
template = 'ddbb/template.db'
database = 'ddbb/database.db'

# JOB STATE
#  0 = Just Created
#  1 = Submitted
#  2 = Running
#  3 = Completed

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

    c.execute( "CREATE TABLE job (jid INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, state INTEGER)" )
    conn.commit()

    conn.close()

#-------------------------------------------------------------------------------
def clearDB():
    mkEmptyDatabase( template )
    if os.path.isfile( database ):
        os.remove( database )

#-------------------------------------------------------------------------------
def init():
    if not os.path.isfile( database ):
        shutil.copy( template, database )

#-------------------------------------------------------------------------------
def insertUser( name, passwd ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    h = bcrypt.hashpw( passwd, bcrypt.gensalt(BCRYPT_ROUNDS) )
    c.execute( 'INSERT INTO user VALUES (null,?,?)', (name,h) )
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
def insertFile( user, filename ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'SELECT uid FROM user WHERE name=?', (user,) )
    uid = c.fetchone()
    if uid is not None:
        c.execute( 'SELECT fid FROM file WHERE uid=? AND filename=?', (uid[0],filename) )
        exists = c.fetchone()
        if exists is None:
            c.execute( 'INSERT INTO file VALUES (null,?,?,?)', (uid[0],0,filename) )
            conn.commit()
            conn.close()
    else:
        conn.close()
        raise DataBaseError

#-------------------------------------------------------------------------------
def getUserFiles( user ):
    files = []
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'SELECT uid FROM user WHERE name=?', (user,) )
    uid = c.fetchone()
    if uid is not None:
        c.execute( 'SELECT fid,filename FROM file WHERE uid=? OR global=1', (uid[0],) )
        dbfiles = c.fetchall()
        for f in dbfiles:
            files.append( {'id': f[0], 'file': f[1]} )

    conn.close()

    return files

#-------------------------------------------------------------------------------
def createJob( user ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'SELECT uid FROM user WHERE name=?', (user,) )
    uid = c.fetchone()
    if uid is not None:
        c.execute( 'INSERT INTO job VALUES (null,?,0)', (uid[0],) )
        c.execute( 'SELECT last_insert_rowid() FROM job' )
        jobid = c.fetchone()[0]
        conn.commit()
        conn.close()
        return jobid
    else:
        conn.close()
        raise DataBaseError

#-------------------------------------------------------------------------------
def getUserJobs( user ):
    jobs = []
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'SELECT uid FROM user WHERE name=?', (user,) )
    uid = c.fetchone()
    if uid is not None:
        c.execute( 'SELECT jid FROM job WHERE uid=?', (uid[0],) )
        dbjobs = c.fetchall()
        for j in dbjobs:
            jobs.append( {'id': j[0]} )

    conn.close()

    return jobs

#-------------------------------------------------------------------------------
