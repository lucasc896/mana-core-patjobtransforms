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
        # Look to see if we should use the fast hybrid POOL merger (default)
        if self.inDic.get('fastPoolMerge', 'true').lower() == 'true':
            print "Using hybrid merge - will skip all events with athena and merge later."
            # This needs to become a run option, so set it early
            self.inDic['skipEvents'] = 10000000
            # This must be really set to trigger the correct JO fragments for fast merge 
            self.inDic['fastPoolMerge'] = 'true'
        AutoConfigureFromDic(self,inDic)
                
        self._addPostRunAction(self, prepend=True)


    def postRunAction(self):
        # Run fast merge as a post run action to the main transform
        print "Executing postRunActions for MergePoolJobTransform"
        if self.inDic.get('fastPoolMerge', 'true').lower() == 'true':
            print "Now doing hybrid event merge"
            self.fastMerge()


    def fastMerge(self):
        filelist = []
        outputfile = self._outputFiles[0].value()
        for file in self._inputFiles:
            if file:
                value = file.value()
                if type(value).__name__ == 'list':
                    filelist += value
            else:
                filelist.append(value)
        print "Files to Merge: %s" % filelist

        # First run mergePOOL.exe to get events.pool
        cmd = ['mergePOOL.exe', '-o', 'events.pool.root']
        for file in filelist:
            cmd.extend(['-i', file])
        cmd.extend(['-e', 'MetaData', '-e', 'MetaDataHdrDataHeaderForm', '-e', 'MetaDataHdrDataHeader', '-e', 'MetaDataHdr'])
        
        print "Will execute hybrid merge step 1: %s" % cmd

        p = Popen(cmd, stdout=PIPE, stderr=STDOUT, close_fds=True)
        while p.poll() is None:
            line = p.stdout.readline()
            if line:
                print "mergePOOL.exe Report: %s" % line.strip()
        rc = p.returncode
        print "1st mergePOOL (event data) finished with code %s" % rc
        if rc == 1:
            print "mergePOOL.exe finished with unknown status"
        elif rc != 0:
            raise TransformError("mergePOOL.exe (event merge) encountered a problem",error='TRF_MERGEERR') 

        # Second merge with metadata.pool to produce final output
        cmd = ['mergePOOL.exe', '-o', 'events.pool.root', '-i', outputfile]
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT, close_fds=True)
        while p.poll() is None:
            line = p.stdout.readline()
            if line:
                print "mergePOOL.exe Report: %s" % line.strip()
        rc = p.returncode
        print "2nd mergePOOL (metadata) finished with code %s" % rc
        if rc == 1:
            print "mergePOOL.exe finished with unknown status"
        elif rc != 0:
            raise TransformError("mergePOOL.exe (final merge) encountered a problem",error='TRF_MERGEERR') 
        else:
            shutil.move('events.pool.root',outputfile)


# Python executable
if __name__ == '__main__':
    #Special preparation for command-line
    import sys
    from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
    inDic=BuildDicFromCommandLine(sys.argv)
    #Construct and execute the transform
    trf = MergePoolJobTransform(inDic)          
    sys.exit(trf.exeArgDict(inDic).exitCode())
