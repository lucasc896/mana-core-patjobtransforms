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
        print "Files to Merge: %s" %filelist

        #1st run mergePOOL.exe to get events.pool
        cmd = 'mergePOOL.exe -o events.pool.root '
        for file in filelist:
          cmd += '-i %s ' % file
        cmd += '-e MetaData -e MetaDataHdrDataHeaderForm -e MetaDataHdrDataHeader'

        p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE,close_fds=True)
        while p.poll() is None:
          line = p.stdout.readline()
          if line:
            print "mergePOOL.exe Report: %s" % line.strip()
        rc = p.returncode
        print "mergePOOL finished with code %s" % rc
        #2nd merge with metadata.pool to produce final output
        cmd = 'mergePOOL.exe -o events.pool.root -i %s ' % outputfile
        p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE,close_fds=True)
        while p.poll() is None:
          line = p.stdout.readline()
          if line:
            print "mergePOOL.exe Report: %s" % line.strip()
        rc = p.returncode
        print "mergePOOL finished with code %s" % rc
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
