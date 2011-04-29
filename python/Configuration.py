#!/usr/bin/env python

# Creation: David Cote (DESY), September 2008
# Usage:
#   -define the list of allowed input arguments 
#   -define the configuration functions to be executed by each input argument
#   -associate allowed input and config functions in ConfigDic

from PyJobTransformsCore.full_trfarg import *

#Note, each function in ConfigDic must accept arguments (transform_to_configure, input_dictionary)
#Hint: avoid giving default values to transform arguments
ConfigDic={}

#Use this function to add new keys in ConfigDic
def AddToConfigDic(key,val):
    if ConfigDic.has_key(key):
        raise RuntimeError("Key '%s' already defined in ConfigDic and cannot be overwritten."%key)
    if hasattr(val,"subSteps"):
        if not isinstance(getattr(val,"subSteps"),list):
            raise RuntimeError("subSteps must be a list.")
    else:
        val.subSteps=['any']
    ConfigDic[key]=val
    return

def DoNothing(trf,inDic):
    return

#Core transform options
AddToConfigDic('--uploadtoami',DoNothing)
AddToConfigDic('--usesqlite',DoNothing)
AddToConfigDic('--useathenaapp',DoNothing)
AddToConfigDic('--mcinput',DoNothing)
AddToConfigDic('--omitvalidation',DoNothing)
AddToConfigDic('--test',DoNothing)
AddToConfigDic('-t',DoNothing)
AddToConfigDic('--ccommand',DoNothing)
AddToConfigDic('-c',DoNothing)
AddToConfigDic('--leakcheckexecute',DoNothing)
AddToConfigDic('--rss',DoNothing)
AddToConfigDic('--vmem',DoNothing)
AddToConfigDic('--extrametadatadict',DoNothing)
AddToConfigDic('--extraignorefilters',DoNothing)
AddToConfigDic('--usenewmeta',DoNothing)
AddToConfigDic('--ignoreerrors',DoNothing)
AddToConfigDic('--ignoreunknown',DoNothing)
AddToConfigDic('--ignoreall',DoNothing)
AddToConfigDic('--athenaopts',DoNothing)
AddToConfigDic('--help',DoNothing)
AddToConfigDic('-h',DoNothing)
AddToConfigDic('dummy',DoNothing)


#############
# Automatically add all official primary DPD to ConfigDic
#
# AddDPDFunctionMaker is technically refered to as a "closure" in the standard python documentation.
# It's just a function that builds and returns another function, in this case: AddDPDXXX(trf,inDic)
def AddDPDFunctionMaker(dpdName, fileArg, **kw):
    if type(dpdName)!=str:
        raise RuntimeError("AddDPDFunctionMaker only accepts string input!")
    
    def AddDPDXXX(trf,inDic):
        trf.add( fileArg(name=dpdName, **kw) )
        return
    return AddDPDXXX

def AddDPDs (dpdNames, subSteps):
    for dpdName in dpdNames:        
        fileArg=OutputDPDFileArg #default value is pool dpd, bs and ntup handled below
        kw = {}
        extension='pool'
        if type(dpdName) != type(''):
            if hasattr (dpdName, 'TreeNames'):
                kw['tree_names'] = dpdName.TreeNames
                extension='root'
                fileArg=NtupleFileArg
                pass
            dpdName = dpdName.StreamName
            pass
        dName='output'+(dpdName.lstrip("Stream"))+'File'
        if dpdName.startswith('StreamDRAW') :
            extension='bs'
            fileArg=OutputSkimmedBSFileArg
            pass
        function=AddDPDFunctionMaker(dName, fileArg, **kw)
        function.isOutput=extension
        function.subSteps=subSteps
        AddToConfigDic(dName,function)
        pass
    return

def AddUserDPD(dpdName,subSteps):
    fileArg=OutputDPDFileArg #default value is pool dpd, bs and ntup handled below
    kw = {}
    extension='pool'
    if hasattr (dpdName, 'TreeNames'):
        kw['tree_names'] = dpdName.TreeNames
        extension='root'
        fileArg=NtupleFileArg
        dName=dpdName.trfKeyName
        function=AddDPDFunctionMaker(dName, fileArg, **kw)
        function.isOutput=extension
        function.subSteps=subSteps
        AddToConfigDic(dName,function)
        pass
    return

# Add a try: except: protection to be usable without AtlasAnalysis project
try:
    from PrimaryDPDMaker.PrimaryDPDFlags import listRAWtoDPD,listESDtoDPD,listAODtoDPD
    AddDPDs (listRAWtoDPD, ['r2e'] )
    AddDPDs (listESDtoDPD, ['e2d'] )
    AddDPDs (listAODtoDPD, ['a2d'] )
except ImportError:
    print "WARNING PrimaryDPDFlags not available. Only OK if you're using job transforms without the AtlasAnalysis project."

#Add Top D2AODMs
try:
    from TopPhysD2PDMaker.TopPhysD2PDFlags import TopPhysAllDAODs
    AddDPDs (TopPhysAllDAODs, ['a2d'])
except ImportError:
    print "WARNING TopPhysD2PDFlags not available. Only OK if you're using job transforms without the AtlasAnalysis project."

# Add D3PD
try:
    from D3PDMakerConfig.D3PDProdFlags import listAllKnownD3PD
    AddDPDs (listAllKnownD3PD, ['a2d','e2d'] )
except ImportError:
    print "WARNING D3PDProdFlags not available. Only OK if you're using job transforms without the AtlasAnalysis project."



######################
# Optional config args
def AddRunNumber(trf,inDic):
    trf.add( SkipEventsArg(name='RunNumber') )
    return
AddToConfigDic('RunNumber',AddRunNumber)

def AddSkipEvents(trf,inDic):
    trf.add( SkipEventsArg() )
    return
AddSkipEvents.subSteps=['first']
AddToConfigDic('skipEvents',AddSkipEvents)

def AddMaxEvents(trf,inDic):
    trf.add( MaxEventsArg() )
    return
AddToConfigDic('maxEvents',AddMaxEvents)

def AddDBRelease(trf,inDic):
    trf.add( DBReleaseArg() )
    return
AddDBRelease.subSteps=['none']
AddToConfigDic('DBRelease',AddDBRelease)

def AddSQLite(trf,inDic):
    trf.add( SQLiteSupport() )
    return
AddToConfigDic('useSQLite',AddSQLite)


## New optional config
def AddBeamType(trf,inDic):
    trf.add( BasicStringArg(name='beamType') )
    return
AddToConfigDic('beamType',AddBeamType)

def AddAMITag(trf,inDic):
    trf.add( BasicStringArg(name='AMITag') )
    return
AddToConfigDic('AMITag',AddAMITag)

def AddProjectName(trf,inDic):
    trf.add( BasicStringArg(name='projectName') )
    return
AddToConfigDic('projectName',AddProjectName)

def AddTrigStream(trf,inDic):
    trf.add( BasicStringArg(name='trigStream') )
    return
AddToConfigDic('trigStream',AddTrigStream)

def AddOutputTypes(trf,inDic):
    trf.add( BasicStringArg(name='outputTypes') )
    return
AddToConfigDic('outputTypes',AddOutputTypes)

def AddPreInclude(trf,inDic):
    trf.add( ListOfStringsArg(name='preInclude') )
    return
AddToConfigDic('preInclude',AddPreInclude)

def AddPostInclude(trf,inDic):
    trf.add( ListOfStringsArg(name='postInclude') )
    return
AddToConfigDic('postInclude',AddPostInclude)

def AddPreExec(trf,inDic):
    trf.add( BasicExec(name='preExec') )
    return
AddToConfigDic('preExec',AddPreExec)

def AddPostExec(trf,inDic):
    trf.add( BasicExec(name='postExec') )
    return
AddToConfigDic('postExec',AddPostExec)

def AddUserExec(trf,inDic):
    trf.add( BasicExec(name='userExec') )
    return
AddToConfigDic('userExec',AddUserExec)

def AddTopOptions(trf,inDic):
    trf.add( BasicStringArg(name='topOptions') )
    return
AddToConfigDic('topOptions',AddTopOptions)

def AddOfflinePrescales(trf,inDic):
    trf.add( ListOfStringsArg(name='prescales') )
    return
AddOfflinePrescales.subSteps=['e2d','a2d']
AddToConfigDic('prescales',AddOfflinePrescales)

def AddAutoConfiguration(trf,inDic):
    trf.add( ListOfStringsArg(name='autoConfiguration') )
    return
AddToConfigDic('autoConfiguration',AddAutoConfiguration)

def AddTriggerConfig(trf,inDic):
    trf.add( BasicStringArg(name='triggerConfig') )
    return
AddToConfigDic('triggerConfig',AddTriggerConfig)

def AddGeometryVersion(trf,inDic):
    trf.add( GeometryVersionArg() )
    return
AddToConfigDic('geometryVersion',AddGeometryVersion)

def AddConditionsTag(trf,inDic):
    trf.add( ConditionsTagArg() )
    return
AddToConfigDic('conditionsTag',AddConditionsTag)

#######################
# Mandatory input files
def AddInputFile(trf,inDic):    
    trf.add( ListOfStringsArg(name='inputFile') )
    return
AddInputFile.isInput=True
AddToConfigDic('inputFile',AddInputFile)

def AddInputTAGFile(trf,inDic):    
    trf.add( ListOfStringsArg(name='inputTAGFile') )
    return
AddInputTAGFile.subSteps=['e2d','a2d']
AddInputTAGFile.isInput=True
AddToConfigDic('inputTAGFile',AddInputTAGFile)

def AddInputEvgenFile(trf,inDic):    
    trf.add( InputEvgenFileArg() )
    return
AddInputEvgenFile.subSteps=['e2h']
AddInputEvgenFile.isInput=True
AddToConfigDic('inputEvgenFile',AddInputEvgenFile)

def AddInputHITSFile(trf,inDic):    
    trf.add( InputHitsFileArg() )
    return
AddInputHITSFile.subSteps=['h2r','mergeHITS']
AddInputHITSFile.isInput=True
AddToConfigDic('inputHitsFile',AddInputHITSFile)

def AddInputBSFile(trf,inDic):    
    trf.add( InputBSFileArg() )
    return
AddInputBSFile.subSteps=['r2r','r2e']
AddInputBSFile.isInput=True
AddToConfigDic('inputBSFile',AddInputBSFile)

def AddInputRDOFile(trf,inDic):    
    trf.add( InputRDOFileArg() )
    return
AddInputRDOFile.subSteps=['r2e','r2b']
AddInputRDOFile.isInput=True
AddToConfigDic('inputRDOFile',AddInputRDOFile)

def AddInputEVNTFile(trf,inDic):    
    trf.add( InputRDOFileArg(name='inputEVNTFile') )
    return
AddInputEVNTFile.subSteps=['r2e']
AddInputEVNTFile.isInput=True
AddToConfigDic('inputEVNTFile',AddInputEVNTFile)

def AddInputESDFile(trf,inDic):    
    trf.add( InputESDFileArg() )
    return
AddInputESDFile.subSteps=['e2a','e2d','e2e','merge']
AddInputESDFile.isInput=True
AddToConfigDic('inputESDFile',AddInputESDFile)

def AddInputAODFile(trf,inDic):    
    trf.add( InputAODFileArg() )
    return
AddInputAODFile.subSteps=['a2d','a2t','merge']
AddInputAODFile.isInput=True
AddToConfigDic('inputAODFile',AddInputAODFile)

class LogsFile( FileType ):
    defaultContents = 'logs'
    defaultType = 'tgz'
    def __init__(self,contents=defaultContents,type=defaultType):
        FileType.__init__(self,type,contents)

    def getGUID(self,filename):
        print "Checking!! LogsFile.getGUID"
        if TRF_SETTING[ 'testrun' ]:
            return None
##         guid = getCachedFileInfo( filename, 'file_guid' )
##         if guid is not None:
##             return guid
        cmd = 'uuidgen'
        status,guid = commands.getstatusoutput(cmd)
        if status != 0: 
            return None
        print "GUID retrieval: %s (%s) generated with %s" % ( guid, filename, cmd )
        return guid
 

class InputLogsFileArg(InputDataFileArg):
    """Input file - log tarballs """
    def __init__(self,help='default',name='default'):
        InputDataFileArg.__init__(self,help,LogsFile(),name)
         
    def MoveLogs(self):
        vals = self.value()
        for val in vals:
            if not fileutil.exists(val):
                found = fileutil.exists_suffix_number(val + '.')
                if not found:
                    code = AtlasErrorCodes.getCode('TRF_INFILE_NOTFOUND')
                    raise InputFileError( val, 'not found. Argument %s' % (self.name()), code )
                if found != val:
                    self.logger().warning('replacing %s with %s' % (val,found) )
                    vals[vals.index(val)] = found
                    val = found
            newval=val+".merged"
            os.system('mv -f %s %s' % (val,newval))

    def postRunAction(self):
        if not self: return
        #InputDataFileArg.postRunAction(self)
        self.MoveLogs()


    def isFullArgument(self):
        return True

def AddInputLogsFile(trf,inDic):    
    trf.add( InputLogsFileArg() )
    return
AddInputLogsFile.subSteps=['mergeHITS']
AddInputLogsFile.isInput=True
AddToConfigDic('inputLogsFile',AddInputLogsFile)

########################
## Optional output files
def AddOutputEvgenFile(trf,inDic):
    trf.add( OutputEvgenFileArg() )
    return
AddOutputEvgenFile.subSteps=['e2h']
AddOutputEvgenFile.isOutput='pool'
AddToConfigDic('outputEvgenFile',AddOutputEvgenFile)

def AddOutputHITFile(trf,inDic):
    trf.add( OutputHitsFileArg() )
    return
AddOutputHITFile.subSteps=['e2h','mergeHITS']
AddOutputHITFile.isOutput='pool'
AddToConfigDic('outputHitsFile',AddOutputHITFile)

def AddOutputRDOFile(trf,inDic):
    trf.add( OutputRDOFileArg() )
    return
AddOutputRDOFile.subSteps=['h2r']
AddOutputRDOFile.isOutput='pool'
AddToConfigDic('outputRDOFile',AddOutputRDOFile)

def AddOutputBSFile(trf,inDic):
    trf.add( OutputBSFileArg() )
    return
AddOutputBSFile.subSteps=['r2r','r2b']
AddOutputBSFile.isOutput='bs'
AddToConfigDic('outputBSFile',AddOutputBSFile)

def AddOutputESDFile(trf,inDic):
    trf.add( OutputESDFileArg() )
    return
AddOutputESDFile.subSteps=['r2e','e2e','merge']
AddOutputESDFile.isOutput='pool'
AddToConfigDic('outputESDFile',AddOutputESDFile)

def AddOutputAODFile(trf,inDic):
    trf.add( OutputAODFileArg() )
    return
AddOutputAODFile.subSteps=['e2a','merge']
AddOutputAODFile.isOutput='pool'
AddToConfigDic('outputAODFile',AddOutputAODFile)

def AddTmpESDFile(trf,inDic):
    trf.add( OutputESDFileArg(name='tmpESD',temporary=True) )
    return
AddTmpESDFile.subSteps=['r2e','e2e']
AddTmpESDFile.isOutput='pool'
AddToConfigDic('tmpESD',AddTmpESDFile)

def AddTmpAODFile(trf,inDic):
    trf.add( OutputAODFileArg(name='tmpAOD',temporary=True) )
    return
AddTmpAODFile.subSteps=['e2a']
AddTmpAODFile.isOutput='pool'
AddToConfigDic('tmpAOD',AddTmpAODFile)

def AddOutputDQMonitorFile(trf,inDic):
    trf.add( MonitorHistArg(name='outputDQMonitorFile',temporary=True) )
    return
AddOutputDQMonitorFile.subSteps=['none']
AddOutputDQMonitorFile.isOutput='root'
AddToConfigDic('outputDQMonitorFile',AddOutputDQMonitorFile)

def AddHIST(trf,inDic):
    trf.add( MonitorHistArg(name='outputHISTFile') )
    return
AddHIST.subSteps=['none']
AddHIST.isOutput='root'
AddToConfigDic('outputHISTFile',AddHIST)

def AddOutputHIST_PHYSVALMONFile(trf,inDic):
    trf.add( NtupleFileArg(name='outputHIST_PHYSVALMONFile') )
    return
AddOutputHIST_PHYSVALMONFile.subSteps=['e2a']
AddOutputHIST_PHYSVALMONFile.isOutput='root'
AddToConfigDic('outputHIST_PHYSVALMONFile',AddOutputHIST_PHYSVALMONFile)

#cmora added for ESDtoNT transform
def AddOutputNTUP_TRIG(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_TRIGFile',tree_names=["Tau/TrigTau","MinBias/TrigMinBias","Muon/TrigMuon","EGamma/EventInfo","Menu/TrigMenu"]) )
    return
AddOutputNTUP_TRIG.subSteps=['e2a']
AddOutputNTUP_TRIG.isOutput='root'
AddToConfigDic('outputNTUP_TRIGFile',AddOutputNTUP_TRIG)
        

def AddCBNT(trf,inDic):
    trf.add( NtupleFileArg(name='outputCBNTFile') )
    return
AddCBNT.subSteps=['r2e']
AddCBNT.isOutput='root'
AddToConfigDic('outputCBNTFile',AddCBNT)

def AddOutputNTUP_MUFASTFile(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_MUFASTFile') )
    return
AddOutputNTUP_MUFASTFile.subSteps=['r2r']
AddOutputNTUP_MUFASTFile.isOutput='root'
AddToConfigDic('outputNTUP_MUFASTFile',AddOutputNTUP_MUFASTFile)

def AddOutputHIST_TRIGEXPERTFile(trf,inDic):
    trf.add( NtupleFileArg(name='outputHIST_TRIGEXPERTFile') )
    return
AddOutputHIST_TRIGEXPERTFile.subSteps=['r2r']
AddOutputHIST_TRIGEXPERTFile.isOutput='root'
AddToConfigDic('outputHIST_TRIGEXPERTFile',AddOutputHIST_TRIGEXPERTFile)

def AddNTUP_BTAG(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_BTAGFile',tree_names="vtuple") )
    return
AddNTUP_BTAG.subSteps=['e2a','a2d']
AddNTUP_BTAG.isOutput='root'
AddToConfigDic('outputNTUP_BTAGFile',AddNTUP_BTAG)

def AddNTUP_SMEW(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_SMEWFile',tree_names="wwd3pd") )
    return
AddNTUP_SMEW.subSteps=['a2d']
AddNTUP_SMEW.isOutput='root'
AddToConfigDic('outputNTUP_SMEWFile',AddNTUP_SMEW)

def AddNTUP_1LHSG2(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_1LHSG2File',tree_names="physics") )
    return
AddNTUP_1LHSG2.subSteps=['a2d']
AddNTUP_1LHSG2.isOutput='root'
AddToConfigDic('outputNTUP_1LHSG2File',AddNTUP_1LHSG2)

def AddNTUP_2LHSG2(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_2LHSG2File',tree_names="physics") )
    return
AddNTUP_2LHSG2.subSteps=['a2d']
AddNTUP_2LHSG2.isOutput='root'
AddToConfigDic('outputNTUP_2LHSG2File',AddNTUP_2LHSG2)

def AddNTUP_HSG2(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_HSG2File',tree_names="physics") )
    return
AddNTUP_HSG2.subSteps=['a2d']
AddNTUP_HSG2.isOutput='root'
AddToConfigDic('outputNTUP_HSG2File',AddNTUP_HSG2)

def AddNTUP_WZ(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_WZFile',tree_names="physics") )
    return
AddNTUP_WZ.subSteps=['e2d']
AddNTUP_WZ.isOutput='root'
AddToConfigDic('outputNTUP_WZFile',AddNTUP_WZ)

def AddNTUP_TRT(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_TRTFile',tree_names="MyCollectionTree") )
    return
AddNTUP_TRT.subSteps=['e2d']
AddNTUP_TRT.isOutput='root'
AddToConfigDic('outputNTUP_TRTFile',AddNTUP_TRT)

def AddNTUP_PROMPTPHOT(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_PROMPTPHOTFile',tree_names=["PAUReco","HggUserData"]) )
    return
AddNTUP_PROMPTPHOT.subSteps=['e2d','a2d']
AddNTUP_PROMPTPHOT.isOutput='root'
AddToConfigDic('outputNTUP_PROMPTPHOTFile',AddNTUP_PROMPTPHOT)

def AddNTUP_MINBIAS(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_MINBIASFile',tree_names="MinBiasTree") )
    return
AddNTUP_MINBIAS.subSteps=['e2a']
AddNTUP_MINBIAS.isOutput='root'
AddToConfigDic('outputNTUP_MINBIASFile',AddNTUP_MINBIAS)

def AddNTUP_TRKVALID(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_TRKVALIDFile',tree_names="Validation/EventToTrackLink") )
    return
AddNTUP_TRKVALID.subSteps=['r2e']
AddNTUP_TRKVALID.isOutput='root'
AddToConfigDic('outputNTUP_TRKVALIDFile',AddNTUP_TRKVALID)

def AddNTUP_MUONCALIB(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_MUONCALIBFile',tree_names="PatternNtupleMaker/Segments") )
    return
AddNTUP_MUONCALIB.subSteps=['r2e','e2e']
AddNTUP_MUONCALIB.isOutput='root'
AddToConfigDic('outputNTUP_MUONCALIBFile',AddNTUP_MUONCALIB)

def AddNTUP_MCP(trf,inDic):
    trf.add( NtupleFileArg(name="outputNTUP_MCPFile",tree_names="CollectionTree") )
    return
AddNTUP_MCP.subSteps=['e2d']
AddNTUP_MCP.isOutput='root'
AddToConfigDic('outputNTUP_MCPFile', AddNTUP_MCP)

def AddNTUP_HECNOISE(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_HECNOISEFile',tree_names="HECNoise") )
    return
AddNTUP_HECNOISE.subSteps=['e2d']
AddNTUP_HECNOISE.isOutput='root'
AddToConfigDic('outputNTUP_HECNOISEFile',AddNTUP_HECNOISE)

def AddOutputNTUP_SCTFile(trf,inDic):
    trf.add( NtupleFileArg( name='outputNTUP_SCTFile',tree_names="InDetTrackTree" ) )
    return
AddOutputNTUP_SCTFile.subSteps=['r2e','e2d','a2d']
AddOutputNTUP_SCTFile.isOutput='root'
AddToConfigDic('outputNTUP_SCTFile',AddOutputNTUP_SCTFile)

def AddNTUP_ENHBIAS(trf,inDic):
    trf.add( NtupleFileArg(name='outputNTUP_ENHBIASFile',tree_names="vertices") )
    return
AddNTUP_ENHBIAS.subSteps=['e2a','e2d']
AddNTUP_ENHBIAS.isOutput='root'
AddToConfigDic('outputNTUP_ENHBIASFile',AddNTUP_ENHBIAS)

def AddNTUP_HIGHMULT(trf, inDic):
    trf.add( NtupleFileArg(name='outputNTUP_HIGHMULTFile', tree_names="MinBiasTree") )
    return
AddNTUP_HIGHMULT.subSteps=['e2a']
AddNTUP_HIGHMULT.isOutput='root'
AddToConfigDic('outputNTUP_HIGHMULTFile', AddNTUP_HIGHMULT)

def AddOutputTAGFile(trf,inDic):
    trf.add( OutputTAGFileArg() )
    return
AddOutputTAGFile.subSteps=['e2a','a2t']
AddOutputTAGFile.isOutput='root'
AddToConfigDic('outputTAGFile',AddOutputTAGFile)

def AddTAGComm(trf,inDic):
    trf.add( OutputTAGFileArg(name='outputTAG_COMMFile') )
    return
AddTAGComm.subSteps=['r2e']
AddTAGComm.isOutput='root'
AddToConfigDic('outputTAG_COMMFile',AddTAGComm)

def AddDESDM_BEAMSPOTFile(trf,inDic):
    trf.add( OutputDPDFileArg(name='outputDESDM_BEAMSPOTFile') )
    return
AddDESDM_BEAMSPOTFile.subSteps=['e2a']
AddDESDM_BEAMSPOTFile.isOutput='pool'
AddToConfigDic('outputDESDM_BEAMSPOTFile',AddDESDM_BEAMSPOTFile)

def AddDAOD_2LHSG2File(trf,inDic):
    trf.add( OutputDPDFileArg(name='outputDAOD_2LHSG2File') )
    return
AddDAOD_2LHSG2File.subSteps=['a2d','e2d']
AddDAOD_2LHSG2File.isOutput='pool'
AddToConfigDic('outputDAOD_2LHSG2File',AddDAOD_2LHSG2File)

def AddDAOD_HSG2File(trf,inDic):
    trf.add( OutputDPDFileArg(name='outputDAOD_HSG2File') )
    return
AddDAOD_HSG2File.subSteps=['a2d','e2d']
AddDAOD_HSG2File.isOutput='pool'
AddToConfigDic('outputDAOD_HSG2File',AddDAOD_HSG2File)


#Dummy outputs for ESD/AOD synonyms. Special case: do not copy this example! 
def AddOutputDESD_ZEEFile(trf,inDic):
    trf.add( OutputESDFileArg( name='outputDESD_ZEEFile' ) )
    return
AddOutputDESD_ZEEFile.subSteps=['none']
AddOutputDESD_ZEEFile.isOutput='pool'
AddToConfigDic('outputDESD_ZEEFile',AddOutputDESD_ZEEFile)

def AddOutputDAOD_ZEEFile(trf,inDic):
    trf.add( OutputESDFileArg( name='outputDAOD_ZEEFile' ) )
    return
AddOutputDAOD_ZEEFile.subSteps=['none']
AddOutputDAOD_ZEEFile.isOutput='pool'
AddToConfigDic('outputDAOD_ZEEFile',AddOutputDAOD_ZEEFile)

def AddOutputDESD_ZMUMUFile(trf,inDic):
    trf.add( OutputESDFileArg( name='outputDESD_ZMUMUFile' ) )
    return
AddOutputDESD_ZMUMUFile.subSteps=['none']
AddOutputDESD_ZMUMUFile.isOutput='pool'
AddToConfigDic('outputDESD_ZMUMUFile',AddOutputDESD_ZMUMUFile)

def AddOutputDAOD_ZMUMUFile(trf,inDic):
    trf.add( OutputESDFileArg( name='outputDAOD_ZMUMUFile' ) )
    return
AddOutputDAOD_ZMUMUFile.subSteps=['none']
AddOutputDAOD_ZMUMUFile.isOutput='pool'
AddToConfigDic('outputDAOD_ZMUMUFile',AddOutputDAOD_ZMUMUFile)

def AddOutputDESD_WENUFile(trf,inDic):
    trf.add( OutputESDFileArg( name='outputDESD_WENUFile' ) )
    return
AddOutputDESD_WENUFile.subSteps=['none']
AddOutputDESD_WENUFile.isOutput='pool'
AddToConfigDic('outputDESD_WENUFile',AddOutputDESD_WENUFile)

def AddOutputDAOD_WENUFile(trf,inDic):
    trf.add( OutputESDFileArg( name='outputDAOD_WENUFile' ) )
    return
AddOutputDAOD_WENUFile.subSteps=['none']
AddOutputDAOD_WENUFile.isOutput='pool'
AddToConfigDic('outputDAOD_WENUFile',AddOutputDAOD_WENUFile)

def AddOutputDESD_WMUNUFile(trf,inDic):
    trf.add( OutputESDFileArg( name='outputDESD_WMUNUFile' ) )
    return
AddOutputDESD_WMUNUFile.subSteps=['none']
AddOutputDESD_WMUNUFile.isOutput='pool'
AddToConfigDic('outputDESD_WMUNUFile',AddOutputDESD_WMUNUFile)

def AddOutputDAOD_WMUNUFile(trf,inDic):
    trf.add( OutputESDFileArg( name='outputDAOD_WMUNUFile' ) )
    return
AddOutputDAOD_WMUNUFile.subSteps=['none']
AddOutputDAOD_WMUNUFile.isOutput='pool'
AddToConfigDic('outputDAOD_WMUNUFile',AddOutputDAOD_WMUNUFile)


def AddOutputNTUP_FASTMONFile(trf,inDic):
    #trf.add(MonitorHistArg(name='outputNTUP_FASTMONFile') )
    trf.add(NtupleFileArg(name='outputNTUP_FASTMONFile', tree_names="") )
    return
AddOutputNTUP_FASTMONFile.subSteps=['a2d','e2a']
AddOutputNTUP_FASTMONFile.isOutput='root'
AddToConfigDic('outputNTUP_FASTMONFile',AddOutputNTUP_FASTMONFile)


## def Add(trf,inDic):
##     return
## AddToConfigDic('',)


