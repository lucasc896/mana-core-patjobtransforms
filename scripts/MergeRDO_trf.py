#!/usr/bin/env python

__doc__=""" Merging of RDO files """

from PATJobTransforms.BaseOfBasicTrf import BaseOfBasicTrf
from PyJobTransformsCore.trf import Author

class MergeRDOJobTransform( BaseOfBasicTrf ):
    def __init__(self,inDic):
        BaseOfBasicTrf.__init__(self,inDic,
                              authors = [ Author('Steven Beale','Steven.Beale@cern.ch'),
                                          Author('John Chapman', '@cern.ch') ] ,
                              skeleton='PATJobTransforms/skeleton.MergeRDO.py' ,
                              help = __doc__ )

# execute transform it if not imported
if __name__ == '__main__':
    #Special preparation for command-line
    import sys
    from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
    inDic=BuildDicFromCommandLine(sys.argv)
    #Construct and execute the transform
    trf = MergeRDOJobTransform(inDic)
    sys.exit(trf.exeArgDict(inDic).exitCode())
