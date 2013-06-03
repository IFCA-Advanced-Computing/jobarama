#-------------------------------------------------------------------------------
import multiprocessing
import os
from os import path
import config
import database

#-------------------------------------------------------------------------------
remotehost = config.REMOTEHOST
remotehome = config.REMOTEHOME

#-------------------------------------------------------------------------------
def startJob( user, var1, fileid ):
    jobid = database.createJob( user )

    p = multiprocessing.Process( target=runjob, args=(jobid, var1, fileid ) )
    p.start()

#-------------------------------------------------------------------------------
def runjob( jobid, var1, fileid ):
    print "RUNNING JOB " + str(jobid)
    print "  var1 = " + var1
    print "  fileid = " + str(fileid)

    # stagein
    localfile = database.getFileFullName( fileid )
    (localdir, localbase) = os.path.split( localfile )
    remotedir = os.path.join( remotehome, localdir )
    remotefile = os.path.join( remotehome, localfile )
    os.system('ssh "%s" "mkdir -p %s"' % (remotehost, remotedir) )
    os.system('scp "%s" "%s:%s"' % (localfile, remotehost, remotefile) )
    database.addJobFile( jobid, fileid, database.FILEIN )

#-------------------------------------------------------------------------------

    # submit

