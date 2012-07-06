###############################################################
#
# Skeleton top job options for MergeNTUP_trf
#
#==============================================================

import subprocess
from PATJobTransforms.Configuration import ConfigDic
from PyJobTransformsCore.trferr import TransformArgumentError

theApp.EvtMax = 0

inFileArgs=0
outFileArgs=0
inKey=None
outKey=None

for key in ConfigDic.iterkeys():
    if key.startswith('outputNTUP') and key.endswith('File') and hasattr(runArgs,key):
        outFileArgs+=1
        outKey=key
        outFile=getattr(runArgs,key)
        print "Using argument ", key, " = ",outFile
    if key.startswith('inputNTUP') and key.endswith('File') and  hasattr(runArgs,key):
        inFileArgs+=1
        inKey=key
        inFile=getattr(runArgs,key)
        print "Using argument ", key, " = ",inFile

if outFileArgs!=1:
    raise TransformArgumentError(message='Wrong number of outputNTUPXXXFile arguments: {0:d} instead of 1. Stopping!'.format(outFileArgs))

if inFileArgs!=1:
    raise TransformArgumentError(message='Wrong number of inputNTUPXXXFile arguments: {0:d} instead of 1. Stopping!'.format(inFileArgs))

if inKey.lstrip('input') != outKey.lstrip('output'):
    raise TransformArgumentError(message='Using different input and output types: {0:s} and {0:s}. Stopping!'.format(inKey, outKey ))

# If we have the mergeChunks parameter, then we will use rhadd instead of hadd (due to memory leaks)
# Parallel merge can be considerably faster
if hasattr(runArgs,'mergeChunks'):
    cmd=['rhadd.py', '-n', str(getattr(runArgs,'mergeChunks'))]
    if hasattr(runArgs,'mergeParallel'):
        cmd.extend(['-p', str(getattr(runArgs, 'mergeParallel'))])
else:
    cmd=['hadd']

cmd.append(outFile)
cmd.extend(inFile)

print 'Will merge using: %s' % cmd
proc=subprocess.Popen( args=cmd, bufsize = 1, shell = False,stdout = subprocess.PIPE, stderr = subprocess.STDOUT )

while proc.poll() is None:
    line = proc.stdout.readline()
    if line:
        print line.rstrip()

rc=proc.returncode

if not rc==0:
    raise RuntimeError("hadd returned with value {0:d} instead of 0. Stopping!".format(rc))

print "Merging finished"                    
