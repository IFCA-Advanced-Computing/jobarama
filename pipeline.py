#-------------------------------------------------------------------------------
import random
import database
import multiprocessing

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

    # submit

#-------------------------------------------------------------------------------
