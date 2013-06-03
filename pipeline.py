#-------------------------------------------------------------------------------
import multiprocessing
import os
from os import path
import subprocess
import re
import time
import config
import database

#-------------------------------------------------------------------------------
remotehost = config.REMOTEHOST
remotehome = config.REMOTEHOME

reJOBID = re.compile(r"Submitted batch job (?P<slurmid>\d+)")

#-------------------------------------------------------------------------------
def startJob( user, var1, fileid ):
    jobid = database.createJob( user )

    p = multiprocessing.Process( target=runjob, args=(user, jobid, var1, fileid ) )
    p.start()

#-------------------------------------------------------------------------------
def runjob( user, jobid, var1, fileid ):
    print "RUNNING JOB " + str(jobid)

    # stagein
    localfile = database.getFileFullName( fileid )
    (localdir, localbase) = os.path.split( localfile )
    remotedir = os.path.join( remotehome, localdir )
    remotefile = os.path.join( remotehome, localfile )
    os.system('ssh "%s" "mkdir -p %s"' % (remotehost, remotedir) )
    os.system('scp "%s" "%s:%s"' % (localfile, remotehost, remotefile) )
    database.addJobFile( jobid, fileid, database.FILEIN )

    # submit
    command = ["ssh", remotehost, "./launch_pipeline.sh", user, var1, remotefile ]
    proc = subprocess.Popen( command, stdout=subprocess.PIPE )
    output = proc.communicate()[0]
    mm = reJOBID.search( output )
    if mm:
        slurmid = int(mm.group('slurmid'))
        print "Slurm ID", str(slurmid)
        database.setJobSubmitted( jobid, slurmid )
    else:
        raise (-1)

#-------------------------------------------------------------------------------
def run():
    p = multiprocessing.Process( target=pipelineLoop )
    p.start()
    return p

#-------------------------------------------------------------------------------
def pipelineLoop():
    try:
        while (1 == 1):
            time.sleep( 100 )
            print "checking jobs"
    except KeyboardInterrupt:
        print "ending pipeline loop"

#-------------------------------------------------------------------------------
