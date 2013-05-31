#-------------------------------------------------------------------------------
import random
import database

#-------------------------------------------------------------------------------
def startJob( user, var1, fileid ):
    jobid = database.createJob( user )

    print "RUNNING JOB " + str(jobid)
    print "  var1 = " + var1
    print "  fileid = " + str(fileid)

#-------------------------------------------------------------------------------
