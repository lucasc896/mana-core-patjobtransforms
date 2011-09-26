###############################################################
#
# Skeleton top job options for DQHistogramMerge_trf
#
#==============================================================

#hack: we are forced to use athena (as a dummy) within the current PyJobTransformsCore
theApp.EvtMax=1

# merge and/or rename monitoring histogram file
# file with list of ROOT files to merge
mergeListFile=open('hist_merge_list.txt','w')
inFiles=runArgs.inputFile
for f in inFiles:
    mergeListFile.write( str(f) + '\n' )    
mergeListFile.close()

# call DQHistogramMerge
cmd = 'DQHistogramMerge.py hist_merge_list.txt %s False' % (runArgs.outputHISTFile)
import commands
(status, output) = commands.getstatusoutput(cmd)
print "---------------------------------------------------------------------------------------"
print '## Output of \'' + cmd + '\':'
print output
print '## DQHistogramMerge.py finished with retcode = %s' % (status)
print "---------------------------------------------------------------------------------------"

if not status==0:
    raise RuntimeError("DQ HiST merging did NOT work. Stopping!")
