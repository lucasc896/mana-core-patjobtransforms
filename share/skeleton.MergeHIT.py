#import glob, os, re
import traceback

from AthenaCommon.Logging import logging
merHitLog = logging.getLogger('MergeHITS')

merHitLog.info( '****************** STARTING HIT MERGING *****************' )

from AthenaCommon.AlgSequence import AlgSequence
topSequence = AlgSequence()

#==============================================================
# Job definition parameters:
#==============================================================
from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
#Jobs should stop if an include fails.
if hasattr(runArgs,"IgnoreConfigError"):
    athenaCommonFlags.AllowIgnoreConfigError=runArgs.IgnoreConfigError 
else:
    athenaCommonFlags.AllowIgnoreConfigError=False

from AthenaCommon.AppMgr import theApp
EvtMax=-1
if hasattr(runArgs,"maxEvents"):
    EvtMax = runArgs.maxEvents
theApp.EvtMax = EvtMax

if not hasattr(runArgs,"geometryVersion"):
    raise RuntimeError("No geometryVersion provided.")
DetDescrVersion = runArgs.geometryVersion
from AthenaCommon.GlobalFlags import globalflags
globalflags.DetDescrVersion.set_Value_and_Lock( runArgs.geometryVersion )

#--------------------------------------------------------------
# Load POOL support
#--------------------------------------------------------------
from AthenaCommon.AppMgr import ServiceMgr
from AthenaPoolCnvSvc.AthenaPoolCnvSvcConf import AthenaPoolCnvSvc
ServiceMgr += AthenaPoolCnvSvc()

ServiceMgr.AthenaPoolCnvSvc.PoolAttributes = [ "DEFAULT_BUFFERSIZE = '2048'" ]

import AthenaPoolCnvSvc.ReadAthenaPool

from CLIDComps.CLIDCompsConf import ClassIDSvc
ServiceMgr += ClassIDSvc()
include( "PartPropSvc/PartPropSvc.py" )

# load all possible converters for EventCheck
GeoModelSvc = Service( "GeoModelSvc" )
GeoModelSvc.IgnoreTagDifference=True

# set up all detector description stuff 
include( "RecExCond/AllDet_detDescr.py" )

#==============================================================
# Job Configuration parameters:
#==============================================================
## Pre-exec
if hasattr(runArgs,"preExec"):
    merHitLog.info("transform pre-exec")
    for cmd in runArgs.preExec:
        merHitLog.info(cmd)
        exec(cmd)

## Pre-include
if hasattr(runArgs,"preInclude"): 
    for fragment in runArgs.preInclude:
        include(fragment)

#--------------------------------------------------------------
# Setup Input
#--------------------------------------------------------------
if not hasattr(runArgs,"inputHitsFile"):
    raise RuntimeError("No inputHitsFile provided.")
In = runArgs.inputHitsFile
EventSelector = ServiceMgr.EventSelector
EventSelector.InputCollections = In

# Check collection type
try:
  EventSelector.CollectionType = CollType
except:
  print "Reading from file"

SkipEvents=0
if hasattr(runArgs,"skipEvents"):
    SkipEvents = runArgs.skipEvents
ServiceMgr.EventSelector.SkipEvents = SkipEvents

#--------------------------------------------------------------
# Setup Output
#--------------------------------------------------------------
if not hasattr(runArgs,"outputHitsFile"):
    raise RuntimeError("No outputHitsFile provided.")
Out = runArgs.outputHitsFile 
from AthenaPoolCnvSvc.WriteAthenaPool import AthenaPoolOutputStream
try: 
  StreamHITS = AthenaPoolOutputStream( "StreamHITS", Out, True )
except:
  StreamHITS = AthenaPoolOutputStream( "StreamHITS", "DidNotSetOutputName.root", True )
StreamHITS.TakeItemsFromInput=TRUE;
StreamHITS.ForceRead=TRUE;  #force read of output data objs
# The next line is an example on how to exclude clid's if they are causing a  problem
#StreamHITS.ExcludeList = ['6421#*']

# Look for lists of filter algorithms
try:
  StreamHITS.AcceptAlgs = AcceptList
except:
  print "No accept algs indicated in AcceptList"
try:
  StreamHITS.RequireAlgs = RequireList
except:
  print "No accept algs indicated in RequireList"
try:
  StreamHITS.VetoAlgs = VetoList
except:
  print "No accept algs indicated in VetoList"

# Copy InFile MetaData using MetaDataTools
from AthenaServices.AthenaServicesConf import AthenaOutputStream
StreamHITS_FH = AthenaOutputStream( "StreamHITS_FH" )
StreamHITS_FH.ItemList += [ "IOVMetaDataContainer#*" ]

#from IOVDbMetaDataTools.IOVDbMetaDataToolsConf import IOVDbMetaDataTool
#ServiceMgr.MetaDataSvc.MetaDataTools += [ "IOVDbMetaDataTool" ] ## 'IOVDbMetaDataTool' already in list at this point

MessageSvc = ServiceMgr.MessageSvc
MessageSvc.OutputLevel = INFO

StreamHITS.ExtendProvenanceRecord = False

ServiceMgr.AthenaPoolCnvSvc.MaxFileSizes = [ "15000000000" ]

#--------------------------------------------------------------

## Post-include
if hasattr(runArgs,"postInclude"):
    for fragment in runArgs.postInclude:
        include(fragment)

## Post-exec
if hasattr(runArgs,"postExec"):
    digilog.info("transform post-exec")
    for cmd in runArgs.postExec:
        digilog.info(cmd)
        exec(cmd)
