###############################################################
#
# Skeleton top job options for D3PD validation
#
#==============================================================


# ==============================================================================
# Load your input file that you want to process
# ==============================================================================
from AthenaCommon.AthenaCommonFlags import jobproperties as jp
jp.AthenaCommonFlags.FilesInput.set_Value_and_Lock(runArgs.inputFile)

#Default 'do' list:
doPhysInDetPerf     = True #!!
doPhysBackTrack     = True
doPhysMet           = True  
doPhysJets          = False ## Tag update needed
doPhysTau           = True
doPhysElectrons     = False ## Not tagged
doPhysMuons         = False ## Need to be implemented 
doPhysBtag          = True
doPhysSUSY          = True
doPhysMonTop        = True
doZee               = False ## Tag update needed
doExotics           = True
doHSG6              = True

Routines = ['PhysInDetPerf','PhysBackTrack','PhysMet','PhysJets','PhysTau','PhysElectrons','PhysMuons','PhysBtag','PhysSUSY','PhysMonTop','Zee','Exotics','HSG6']

#Switch on/off various validation routines:
if hasattr(runArgs,"d3pdVal"):
  for val in Routines:
    dostr = val
    dontstr = 'no'+val
    if dostr in runArgs.d3pdVal:
      vars()['do'+dostr] = True
    if dontstr in runArgs.d3pdVal:
      vars()['do'+dostr] = False


# ==============================================================================
# Set the number of events that you want to process or skip
# ==============================================================================
jp.AthenaCommonFlags.EvtMax.set_Value_and_Lock(runArgs.maxEvents)

# ==============================================================================
# Configure RecExCommon (the mother of all job options in Athena) 
# and schedule your DPD making.
# Unfortunately, for now, you still have to turn OFF some things by hand
# ==============================================================================

from InDetRecExample.InDetKeys import InDetKeys
InDetKeys.UnslimmedTracks.set_Value_and_Lock('Tracks')
InDetKeys.UnslimmedTracksTruth.set_Value_and_Lock('TrackTruthCollection')

from RecExConfig.RecFlags import rec
rec.doHist.set_Value_and_Lock(True)
rec.doWriteTAG.set_Value_and_Lock(False)
rec.doWriteAOD.set_Value_and_Lock(False)
rec.doCBNT.set_Value_and_Lock(False)

# ----------------------------------------------------------------------------------------------------
# If you have your own DPD Maker scripts
# (for examples, see in svn: PhysicsAnalysis/D2PDMaker/share/D2PD_ExampleSimple*.py ),
# then just append your script (wherever it is) to this list:
#       rec.DPDMakerScripts.append("MyPackage/MyScript")
# An example scripts is appended below, so you can see how it works!
# ----------------------------------------------------------------------------------------------------


# Set up trigger for All tools
from TrigDecisionTool.TrigDecisionToolConf import Trig__TrigDecisionTool
tdt = Trig__TrigDecisionTool("TrigDecisionTool")
ToolSvc += tdt
    
from TriggerJobOpts.TriggerFlags import TriggerFlags
TriggerFlags.configurationSourceList = ['ds']

# set up trigger config service
from TriggerJobOpts.TriggerConfigGetter import TriggerConfigGetter
cfg =  TriggerConfigGetter("ReadPool")
    
# ----------------------------------------------------------------------------------------------------
## primary tracking jobOptions
### Removed General definitions and filter
# ----------------------------------------------------------------------------------------------------
if doPhysInDetPerf:
    from InDetRecExample.InDetJobProperties import InDetFlags
    InDetFlags.doStandardPlots.set_Value_and_Lock(True)
    rec.DPDMakerScripts.append("RunPhysVal/PhysValInDetPerf_jobOptions.py")

# ----------------------------------------------------------------------------------------------------
## secondary tracking jobOptions
# ----------------------------------------------------------------------------------------------------
if doPhysBackTrack:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValBackTrack_jobOptions.py")


# ----------------------------------------------------------------------------------------------------
## Tau jobOptions
# ----------------------------------------------------------------------------------------------------
if doPhysTau:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValTau_jobOptions.py")


# ----------------------------------------------------------------------------------------------------
## b-tagging jobOptions
# ----------------------------------------------------------------------------------------------------
if doPhysBtag:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValBtag_jobOptions.py")


# ----------------------------------------------------------------------------------------------------
## MET jobOptions (ESD)
# ----------------------------------------------------------------------------------------------------
if doPhysMet:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValMET_jobOptions.py")


# ----------------------------------------------------------------------------------------------------
## Jets jobOptions 
# ----------------------------------------------------------------------------------------------------
if doPhysJets:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValJets_jobOptions.py")


# ----------------------------------------------------------------------------------------------------
## electrons jobOptions
# ----------------------------------------------------------------------------------------------------
if doPhysElectrons:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValElectrons_jobOptions.py")


# ----------------------------------------------------------------------------------------------------
## muons jobOptions
# ----------------------------------------------------------------------------------------------------
if doPhysMuons:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValMuons_jobOptions.py")

# ----------------------------------------------------------------------------------------------------
## SUSY jobOptions
# ----------------------------------------------------------------------------------------------------
if doPhysSUSY:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValSUSY_jobOptions.py")

# ----------------------------------------------------------------------------------------------------
## PhysValMon + Top jobOptions
# ----------------------------------------------------------------------------------------------------
if doPhysMonTop:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValMonTop_jobOptions.py")

# ----------------------------------------------------------------------------------------------------
## Zee jobOptions
# ----------------------------------------------------------------------------------------------------
if doZee:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValZee_jobOptions.py")

# ----------------------------------------------------------------------------------------------------
## Exotics jobOptions
# ----------------------------------------------------------------------------------------------------
if doExotics:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValExotics_jobOptions.py")

# ----------------------------------------------------------------------------------------------------
## HSG6 jobOptions
# ----------------------------------------------------------------------------------------------------
if doHSG6:
    rec.DPDMakerScripts.append("RunPhysVal/PhysValHSG6_jobOptions.py")

    
# ==============================================================================
# Now, include the master top options from RecExCommon.
# This automatically ensures that your Athena job will be set up correctly,
# i.e., if RecExCommon doesn't work, the release is broken!
# ==============================================================================
include ("RecExCommon/RecExCommon_topOptions.py")


