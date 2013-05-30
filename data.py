#-------------------------------------------------------------------------------
import shutil
import os
import os.path

#-------------------------------------------------------------------------------
DATADIR = "data"

#-------------------------------------------------------------------------------
def saveFile( filename, filedata ):
    dir = os.path.dirname( filename )
    if not os.path.isdir( dir ):
        os.makedirs( dir )

    with open( filename, 'w' ) as f:
        shutil.copyfileobj( filedata, f )

#-------------------------------------------------------------------------------
