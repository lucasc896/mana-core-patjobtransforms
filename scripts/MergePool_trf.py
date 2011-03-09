#!/usr/bin/env python

__doc__ = """Merge several input pool files into a single output file."""

from PyJobTransformsCore.trf import *
from PyJobTransformsCore.full_trfarg import *
from PyJobTransformsCore.trfutil import *

class MergePoolJobTransform( JobTransform ):
    def __init__(self,inDic):
        JobTransform.__init__(self,
                              authors = [ Author('David Cote', 'david.cote@cern.ch') ] ,
                              skeleton='PATJobTransforms/skeleton.MergePool.py' ,
                              help = __doc__ )

        if not isinstance(inDic,dict):
            raise TypeError("inDic has %s but should be a dictionary." %type(inDic))

        from PATJobTransforms.ConfigDicUtils import AutoConfigureFromDic
        self.inDic=inDic
        AutoConfigureFromDic(self,inDic)

# Python executable
if __name__ == '__main__':
    #Special preparation for command-line
    import sys
    from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
    inDic=BuildDicFromCommandLine(sys.argv)
    #Construct and execute the transform
    trf = MergePoolJobTransform(inDic)          
    sys.exit(trf.exeArgDict(inDic).exitCode())
