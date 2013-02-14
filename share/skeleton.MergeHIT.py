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
# Peek at input to configure DetFlags
#--------------------------------------------------------------
if not hasattr(runArgs,"inputHitsFile"):
    raise RuntimeError("No inputHitsFile provided.")

def hitColls2SimulatedDetectors(inputlist):
    """Build a dictionary from the list of containers in the metadata"""
    simulatedDetectors = []
    simulatedDictionary = {'PixelHits': 'pixel', 'SCT_Hits': 'SCT', 'TRTUncompressedHits': 'TRT',
                           'BCMHits': 'BCM', 'LucidSimHitsVector': 'Lucid', 'LArHitEMB': 'LAr',
                           'LArHitEMEC': 'LAr', 'LArHitFCAL': 'LAr', 'LArHitHEC': 'LAr',
                           'MBTSHits': 'Tile', 'TileHitVec': 'Tile', 'MDT_Hits': 'MDT',
                           'CSC_Hits': 'CSC', 'TGC_Hits': 'TGC', 'RPC_Hits': 'RPC',
                           'TruthEvent': 'Truth'} #'': 'ALFA', '': 'ZDC',
    for entry in inputlist:
        if entry[1] in simulatedDictionary.keys():
            if simulatedDictionary[entry[1]] not in simulatedDetectors:
                simulatedDetectors += [simulatedDictionary[entry[1]]]
    return simulatedDetectors

import PyUtils.AthFile as af
try:
    f = af.fopen(runArgs.inputHitsFile[0])
except AssertionError:
    merHitLog.error("Failed to open input file: %s", runArgs.inputHitsFile[0])
#check evt_type of input file
if 'evt_type' in f.infos.keys():
    import re
    if not re.match(str(f.infos['evt_type'][0]), 'IS_SIMULATION') :
        merHitLog.error('This input file has incorrect evt_type: %s',str(f.infos['evt_type']))
        merHitLog.info('Please make sure you have set input file metadata correctly.')
        merHitLog.info('Consider using the job transforms for earlier steps if you aren\'t already.')
        #then exit gracefully
        raise SystemExit("Input file evt_type is incorrect, please check your g4sim and evgen jobs.")
else :
    merHitLog.warning('Could not find \'evt_type\' key in athfile.infos. Unable to that check evt_type is correct.')
metadatadict = dict()
if 'metadata' in f.infos.keys():
    if '/Simulation/Parameters' in f.infos['metadata'].keys():
        metadatadict = f.infos['metadata']['/Simulation/Parameters']
        if isinstance(metadatadict, list):
            merHitLog.warning("%s inputfile: %s contained %s sets of Simulation Metadata. Using the final set in the list.",inputtype,inputfile,len(metadatadict))
            metadatadict=metadatadict[-1]
else:
    ##Patch for older hit files
    if 'SimulatedDetectors' not in metadatadict.keys():
        if 'eventdata_items' in f.infos.keys():
            metadatadict['SimulatedDetectors'] = hitColls2SimulatedDetectors(f.infos['eventdata_items'])
        else :
            metadatadict['SimulatedDetectors'] = ['pixel','SCT','TRT','BCM','Lucid','LAr','Tile','MDT','CSC','TGC','RPC','Truth']

if 'SimulatedDetectors' in metadatadict.keys():
    from AthenaCommon.DetFlags import DetFlags
    # by default everything is off
    DetFlags.all_setOff()
    merHitLog.debug("Switching on DetFlags for subdetectors which were simulated")
    for subdet in metadatadict['SimulatedDetectors']:
        cmd='DetFlags.%s_setOn()' % subdet
        merHitLog.debug(cmd)
        try:
            exec cmd
        except:
            merHitLog.warning('Failed to switch on subdetector %s',subdet)
    #hacks to reproduce the sub-set of DetFlags left on by RecExCond/AllDet_detDescr.py
    DetFlags.digitize.all_setOff()
    DetFlags.geometry.all_setOff()
    DetFlags.pileup.all_setOff()
    DetFlags.readRDOBS.all_setOff()
    DetFlags.readRIOBS.all_setOff()
    DetFlags.readRIOPool.all_setOff()
    DetFlags.simulate.all_setOff()
    DetFlags.simulateLVL1.all_setOff()
    DetFlags.writeBS.all_setOff()
    DetFlags.writeRDOPool.all_setOff()
    DetFlags.writeRIOPool.all_setOff()

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

# set up all detector description stuff + some voodoo
include( "RecExCond/AllDet_detDescr.py" )
from AthenaCommon.DetFlags import DetFlags
DetFlags.Print()

#--------------------------------------------------------------
# Setup Input
#--------------------------------------------------------------
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
    merHitLog.info("transform post-exec")
    for cmd in runArgs.postExec:
        merHitLog.info(cmd)
        exec(cmd)
