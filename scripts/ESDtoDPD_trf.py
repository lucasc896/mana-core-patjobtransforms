#!/usr/bin/env python

__doc__ = """Make DPD from ESD."""

from PATJobTransforms.BaseOfBasicTrf import BaseOfBasicTrf
from PyJobTransformsCore.trf import Author

class ESDtoDPDJobTransform( BaseOfBasicTrf ):
    def __init__(self,inDic):
        BaseOfBasicTrf.__init__(self,inDic,
                                authors=[Author('David Cote','david.cote@cern.ch')],
                                skeleton='PATJobTransforms/skeleton.ESDtoDPD_trf.py' ,
                                help = __doc__ )

    def matchEvents(self):
        self.logger().info("MatchEvents is not executed for DPD outputs.")
        return


#----------------------------------------------------------------------
if __name__ == '__main__':
    #Special preparation for command-line
    import sys
    from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
    inDic=BuildDicFromCommandLine(sys.argv)
    #Construct and execute the transform
    trf = ESDtoDPDJobTransform(inDic)
    sys.exit(trf.exeArgDict(inDic).exitCode())
