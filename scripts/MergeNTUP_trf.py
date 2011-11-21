#!/usr/bin/env python

__doc__ = """Merge NTUP files."""

from PATJobTransforms.BaseOfBasicTrf import BaseOfBasicTrf
from PyJobTransformsCore.trf import Author

class MergeNTUPJobTransform( BaseOfBasicTrf ):
    def __init__(self,inDic):
        BaseOfBasicTrf.__init__(self,inDic,
                                authors = [ Author('Bjorn Sarrazin', 'Bjorn.Sarrazin@cern.ch')],
                                skeleton='PATJobTransforms/skeleton.MergeNTUP_trf.py',
                                help = __doc__ )

    def matchEvents(self):
        for key in self._namedArgs.iterkeys():
            if key.startswith('inputntup') and key.endswith('file'):
                inputFileArgName=key
            if key.startswith('outputntup') and key.endswith('file'):
                outputFileArgName=key

        inFile=self.getArgument(inputFileArgName)
        outFile=self.getArgument(outputFileArgName)

        in_tree_names=inFile._fileType.tree_names 
        out_tree_names=outFile._fileType.tree_names

        if not in_tree_names:
            self.logger().info("MatchEvents is not executed for MergeNTUP. No tree_name is given for input file.")
            return

        if not out_tree_names:
            self.logger().info("MatchEvents is not executed for MergeNTUP. No tree_name is given for output file.")
            return

        if in_tree_names!=out_tree_names:
            self.logger().info("MatchEvents is not executed for MergeNTUP. Different tree_name given for input and output file.")
            return
                
        self.matchEventsExpectEqual(inputFileArgName, outputFileArgName)
        
        return

#----------------------------------------------------------------------
if __name__ == '__main__':    
    #Special preparation for command-line
    import sys
    from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
    inDic=BuildDicFromCommandLine(sys.argv)
    #Construct and execute the transform
    trf = MergeNTUPJobTransform(inDic)          
    sys.exit(trf.exeArgDict(inDic).exitCode())

