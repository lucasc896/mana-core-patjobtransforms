#!/usr/bin/env python
__doc__ =""" Generate Validation D3PDs """

import os
import subprocess

from PATJobTransforms.BaseOfBasicTrf import BaseOfBasicTrf
from PyJobTransformsCore.trf import Author

ListOfDefaultPositionalKeys=['maxEvents','inputFile','preInclude','postInclude','preExec','postExec','--ignoreerros']

#List of root files created by the transform (for merging)
rootfiles= [ 'PhysVal_InDetPerf.root', 'PhysVal_BackTracking.root', 'PhysVal_MissingET.root', 'PhysVal_Jets.root', 'PhysVal_Tau.root', 'PhysVal_Electrons.root','PhysVal_MUONSPLACEHOLDER.root','PhysVal_Btag.root', 'PhysVal_SUSY.root', 'PhysVal_MonTop.root', 'PhysVal_Zee.root', 'PhysVal_Exotics.root', 'PhysVal_HSG6.root'] 

class ValidationD3PDJobTransform( BaseOfBasicTrf ):
    def __init__(self,inDic):
        BaseOfBasicTrf.__init__(self,inDic,
                              authors = [ Author('Steven Beale','Steven.Beale@cern.ch') ],
                              skeleton='PATJobTransforms/skeleton.ValidateD3PD_trf.py' ,
                              help = __doc__ )
        #add the postRunAction associated with the transform.
        self._addPostRunAction(self)

    def postRunAction(self):
        inlist = [ ]
        for file in rootfiles:
            if os.path.exists(file):
                inlist.append(file)
  
        print "Merging root files: %s" % inlist 
      
        cmd = ['hadd' , 'PhysVal.root']
        cmd.extend(inlist)
        proc = subprocess.Popen(args = cmd,bufsize = 1, shell = False,stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
        while proc.poll() is None:
            line = proc.stdout.readline()
            if line:
                print line

        rc=proc.returncode

        if not rc==0:
            raise RuntimeError("hadd returned with value {0:d} instead of 0. Stopping!".format(rc))

        print "Merging finished"


if __name__ == '__main__':
    #Special preparation for command-line
    import sys
    from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
    inDic=BuildDicFromCommandLine(sys.argv)
    #Construct and execute the transform
    trf = ValidationD3PDJobTransform(inDic)
    sys.exit(trf.exeArgDict(inDic).exitCode())
