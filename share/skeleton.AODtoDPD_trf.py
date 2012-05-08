###############################################################
#
# Skeleton top job options for AOD->DPD 
# Put here outputs that require rec.doAOD=False
#
#==============================================================

#Common job options disable most RecExCommon by default. Re-enable below on demand.
include("PATJobTransforms/CommonSkeletonJobOptions.py")
rec.doAOD=False

from AthenaCommon.Logging import logging
recoLog = logging.getLogger('aod_to_dpd')
recoLog.info( '****************** STARTING AOD->DPD MAKING *****************' )


## Automatically turn ON/OFF and set output file name of each possible DPD
listOfFlags=[]
try:
    from PrimaryDPDMaker.PrimaryDPDFlags import primDPD
    listOfFlags.append(primDPD)
except ImportError:
    print "WARNING PrimaryDPDFlags not available. Only OK if you're using job transforms without the AtlasAnalysis project."
try:
    from D2PDMaker.D2PDFlags import D2PDFlags
    listOfFlags.append(D2PDFlags)
except ImportError:
    print "WARNING D2PDFlags not available. Requires D2PDMaker-00-00-50 in AtlasAnalysis."
try:
    from TopPhysD2PDMaker.TopPhysD2PDFlags import topPhysDPD
    listOfFlags.append(topPhysDPD)
except ImportError:
    print "WARNING TopPhysD2PDFlags not available. Only OK if you're using job transforms without the AtlasAnalysis project."
try:
    from D3PDMakerConfig.D3PDProdFlags import prodFlags
    listOfFlags.append( prodFlags )
except ImportError:
    print "WARNING D3PDProdFlags not available. Only OK if you're using job transforms without the AtlasAnalysis project."

from PATJobTransforms.DPDUtils import SetupOutputDPDs
rec.DPDMakerScripts.append(SetupOutputDPDs(runArgs,listOfFlags))


from PATJobTransforms.OutputsMgr import outputsMgr,magicKey
for key in dir(runArgs):
    if key.startswith(magicKey):
        outputsMgr.addOutput(key,getattr(runArgs,key))

## Input
if hasattr(runArgs,"inputFile"): athenaCommonFlags.FilesInput.set_Value_and_Lock( runArgs.inputFile )
if hasattr(runArgs,"inputEVNTFile"): athenaCommonFlags.FilesInput.set_Value_and_Lock( runArgs.inputEVNTFile )
if hasattr(runArgs,"inputAODFile"):
    globalflags.InputFormat.set_Value_and_Lock('pool')
    rec.readAOD.set_Value_and_Lock( True )
    rec.readRDO.set_Value_and_Lock( False )
    athenaCommonFlags.PoolAODInput.set_Value_and_Lock( runArgs.inputAODFile )
if hasattr(runArgs,"inputTAGFile"):
    #for TAG->AOD->skimmedAOD
    rec.readTAG.set_Value_and_Lock( True )
    rec.readAOD.set_Value_and_Lock( True )
    rec.doAOD.set_Value_and_Lock( False )
    rec.TAGFromRDO.set_Value_and_Lock( False )
    athenaCommonFlags.FilesInput.set_Value_and_Lock( runArgs.inputTAGFile )

## Outputs
if hasattr(runArgs,"outputAODFile"):
    #for TAG->AOD->skimmedAOD
    rec.doWriteAOD.set_Value_and_Lock( True )
    athenaCommonFlags.PoolAODOutput.set_Value_and_Lock( runArgs.outputAODFile )

if hasattr(runArgs,"outputNTUP_BTAGFile"):
    from BTagging.BTaggingFlags import BTaggingFlags
    BTaggingFlags.doJetTagNtuple = True
    BTaggingFlags.JetTagNtupleName = runArgs.outputNTUP_BTAGFile

if hasattr(runArgs,"outputNTUP_PROMPTPHOTFile"):
    from PhotonAnalysisUtils.PhotonAnalysisUtilsFlags import PAUflags
    PAUflags.FileName = runArgs.outputNTUP_PROMPTPHOTFile
    #little hack while autoConfiguration=everything is still not the default...
    if hasattr(runArgs,"inputAODFile") and not hasattr(runArgs,"inputFile"):
        athenaCommonFlags.FilesInput.set_Value_and_Lock( runArgs.inputAODFile )

if hasattr(runArgs,"outputNTUP_SMEWFile"):
    from WWAnalyze.WWD3PDFlags import WWD3PDFlags
    WWD3PDFlags.OutputFilename = runArgs.outputNTUP_SMEWFile
    #little hack while autoConfiguration=everything is still not the default...
    if hasattr(runArgs,"inputAODFile") and not hasattr(runArgs,"inputFile"):
        athenaCommonFlags.FilesInput.set_Value_and_Lock( runArgs.inputAODFile )

if hasattr(runArgs,"outputNTUP_TRUTHFile"):
    from TruthD3PDMaker.TruthD3PDMakerFlags import TruthD3PDFlags
    TruthD3PDFlags.TruthD3PDOutputFileName = runArgs.outputNTUP_TRUTHFile
    include("TruthD3PDMaker/TruthD3PDfromEVGEN_preInclude.py")

# If we have TOP NTUPs switch on V0Finder
if len([ f for f in dir(runArgs) if f.find('NTUP_TOP') > -1 ]) > 0:
    InDetFlags.doV0Finder.set_Value_and_Lock(True)


if hasattr(runArgs,"outputDAOD_2LHSG2File"):
    #FIXME: input/outputs should configured via job properties instead of directly using the runArgs object
    from HSG2DPDUtils import HSG2DPDFlags
if hasattr(runArgs,"outputDAOD_HSG2File"):
    #FIXME: input/outputs should configured via job properties instead of directly using the runArgs object
    from HSG2DPDUtils import HSG2DPDFlags


if hasattr(runArgs,"outputNTUP_1LHSG2File"):
    #FIXME: input/outputs should configured via job properties instead of directly using the runArgs object
    from HSG2DPDUtils import HSG2DPDFlags
if hasattr(runArgs,"outputNTUP_2LHSG2File"):
    #FIXME: input/outputs should configured via job properties instead of directly using the runArgs object
    from HSG2DPDUtils import HSG2DPDFlags
if hasattr(runArgs,"outputNTUP_HSG2File"):
    #FIXME: input/outputs should configured via job properties instead of directly using the runArgs object
    from HSG2DPDUtils import HSG2DPDFlags


 
if hasattr(runArgs,"outputNTUP_SCTFile"):
    from TrackD3PDMaker.TrackD3PDMakerSCTFlags import TrackD3PDSCTFlags
    TrackD3PDSCTFlags.outputFile = runArgs.outputNTUP_SCTFile
    if hasattr(runArgs,"inputESDFile") and not hasattr(runArgs,"inputFile"):
        athenaCommonFlags.FilesInput.set_Value_and_Lock( runArgs.inputESDFile )


if hasattr(runArgs,"outputNTUP_FASTMONFile"):
    rec.doFastPhysMonitoring.set_Value_and_Lock(True)
    rec.RootFastPhysMonOutput.set_Value_and_Lock(runArgs.outputNTUP_FASTMONFile)
    


#Import D3PD flags before preExec, for convenience
from D3PDMakerConfig.D3PDProdFlags  import oldProdFlags
from D3PDMakerConfig.D3PDMakerFlags import D3PDMakerFlags
from SUSYD3PDMaker.SUSYD3PDFlags    import SUSYD3PDFlags

## Pre-exec
if hasattr(runArgs,"preExec"):
    recoLog.info("transform pre-exec")
    for cmd in runArgs.preExec:
        recoLog.info(cmd)
        exec(cmd)

## Pre-include
if hasattr(runArgs,"preInclude"): 
    for fragment in runArgs.preInclude:
        include(fragment)

#========================================================
# Central topOptions (this is one is a string not a list)
#========================================================
if hasattr(runArgs,"topOptions"): include(runArgs.topOptions)
else: include( "RecExCommon/RecExCommon_topOptions.py" )

## Make "old style" D3PDs.
for c in SetupOutputDPDs(runArgs, [oldProdFlags]): c()

## Offline prescales (has to be *after* the topOptions)
if hasattr(runArgs,"prescales"):
    recoLog.info( '**** DPD offline prescale arguments:' )
    from PrimaryDPDMaker.JobTransformConfiguration import ApplyPrescale
    for prescale in runArgs.prescales:
        recoLog.info( prescale )
        ApplyPrescale(prescale)

## Post-include
if hasattr(runArgs,"postInclude"): 
    for fragment in runArgs.postInclude:
        include(fragment)

## Post-exec
if hasattr(runArgs,"postExec"):
    recoLog.info("transform post-exec")
    for cmd in runArgs.postExec:
        recoLog.info(cmd)
        exec(cmd)

