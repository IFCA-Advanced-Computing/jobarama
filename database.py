#-------------------------------------------------------------------------------
import sqlite3
import bcrypt
import os
import shutil
import data

#-------------------------------------------------------------------------------
BCRYPT_ROUNDS = 5
template = 'ddbb/template.db'
database = 'ddbb/database.db'

# JOB STATE
JOB_CREATED = 0   # Just Created
JOB_SUBMITTED = 1 # Submitted
JOB_RUNNING = 2   # Running
JOB_COMPLETED = 3 # Completed

# JOB FILE TYPE
FILEIN = 0
FILEOUT = 1

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

    c.execute( "CREATE TABLE job (jid INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, state INTEGER, slurmid INTEGER)" )
    conn.commit()

    c.execute( "CREATE TABLE jobfile (jid INTEGER, fid INTEGER, jobfiletype INTEGER, PRIMARY KEY(jid, fid) )" )
    conn.commit()

    conn.close()

#-------------------------------------------------------------------------------
def clearDB():
    mkEmptyDatabase( template )
    if os.path.isfile( database ):
        os.remove( database )

#-------------------------------------------------------------------------------
def init():
    if not os.path.isfile( template ):
        clearDB()

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
def createFile( userid, filename ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'INSERT INTO file VALUES (null,?,?,?)', (userid,0,filename) )
    c.execute( 'SELECT last_insert_rowid() FROM file' )
    fileid = c.fetchone()[0]
    conn.commit()
    conn.close()
    return fileid

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
def getFileFullName( fid ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'SELECT uid,filename FROM file WHERE fid=?', (fid,) )
    fdata = c.fetchone()
    if fdata is None:
        conn.close()
        raise DataBaseError

    c.execute('SELECT name FROM user WHERE uid=?', (fdata[0],) )
    udata = c.fetchone()
    if udata is None:
        conn.close()
        raise DataBaseError

    conn.close()

    return data.getUserFilename( udata[0], fdata[1] )

#-------------------------------------------------------------------------------
def createJob( user ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'SELECT uid FROM user WHERE name=?', (user,) )
    uid = c.fetchone()
    if uid is not None:
        c.execute( 'INSERT INTO job VALUES (null,?,0,-1)', (uid[0],) )
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
def addJobFile( jobid, fileid, jftype ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'INSERT INTO jobfile VALUES (?,?,?)', (jobid,fileid,jftype) )
    conn.commit()
    conn.close()

#-------------------------------------------------------------------------------
def setJobSubmitted( jobid, slurmid ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'UPDATE job SET slurmid=?, state=1 WHERE jid=?', (slurmid,jobid) )
    conn.commit()
    conn.close()

#-------------------------------------------------------------------------------
def setJobRunning( jobid ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'UPDATE job SET state=2 WHERE jid=?', (jobid,) )
    conn.commit()
    conn.close()

#-------------------------------------------------------------------------------
def setJobCompleted( jobid ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'UPDATE job SET state=3 WHERE jid=?', (jobid,) )
    conn.commit()
    conn.close()

#-------------------------------------------------------------------------------
def getJobInfo( jobid ):
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute('SELECT state,slurmid FROM job WHERE jid=?', (jobid,) )
    jdata = c.fetchone()
    if jdata is None:
        conn.close()
        raise DataBaseError

    c.execute('SELECT fid,jobfiletype FROM jobfile WHERE jid=?', (jobid,) )
    jfiles = c.fetchall()

    files = []
    for jf in jfiles:
        c.execute('SELECT filename FROM file WHERE fid=?', (jf[0],) )
        fdata = c.fetchone()
        if fdata is None:
            conn.close()
            raise DataBaseError

        files.append( {'fid': jf[0], 'name': fdata[0], 'type': jf[1] } )

    conn.close()

    return { 'jobid': jobid, 'state': jdata[0], 'slurmid': jdata[1], 'files': files }

#-------------------------------------------------------------------------------
def getActiveJobs():
    conn = sqlite3.connect( database )
    c = conn.cursor()
    c.execute( 'SELECT jid,uid,state,slurmid FROM job WHERE state=1 OR state=2' )
    jdata = c.fetchall()
    jobs = []
    for j in jdata:
        jobs.append( {'jid':j[0],'uid':j[1],'state':j[2],'slurmid':j[3]} )

    return jobs

#-------------------------------------------------------------------------------
