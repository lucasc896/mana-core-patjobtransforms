#!/usr/bin/env python

__doc__ ="""Any reconstruction step: RAW->RAW (run HLT) and/or RAW->ESD and/or ESD->AOD and/or ESD->DPD and/or AOD->DPD and/or ESD->TAG.
The job is self-configuring from the input file name and from its input arguments in general.
It requires a dictionary in its constructor and needs to be executed with exeArgDict().
Once the configuration is decided, the whole job stops if any intermediate job fails."""

from PyJobTransformsCore.trf import Author,JobReport
from RecJobTransforms.RAWtoESD_trf import RAWtoESDJobTransform
from RecJobTransforms.RDOtoBS_trf import RDOtoBSJobTransform
#from RecJobTransforms.ESDtoESD_trf import ESDtoESDJobTransform
from PATJobTransforms.MergePool_trf import MergePoolJobTransform
from RecJobTransforms.ESDtoAOD_trf import ESDtoAODJobTransform
from PATJobTransforms.ESDtoDPD_trf import ESDtoDPDJobTransform
from PATJobTransforms.AODtoDPD_trf import AODtoDPDJobTransform
from PATJobTransforms.AODtoTAG_trf import AODtoTAGJobTransform
from PATJobTransforms.DQHistogramMerge_trf import DQHistogramMergeJobTransform
from PATJobTransforms.RAWtoRAWHLT_trf import RAWtoRAWHLTJobTransform
from PATJobTransforms.ArgDicTools import DefaultConfigFromSysArgv
from PATJobTransforms.BaseOfCompositeTrf import BaseOfCompositeTrf


#Note ListOfDefaultPositionalKeys needs to be maintained by hand, to support 'grep' from ProdSys
ListOfDefaultPositionalKeys=['inputBSFile','inputRDOFile','inputEVNTFile','inputESDFile','inputAODFile','maxEvents','skipEvents','RunNumber','autoConfiguration','preInclude','postInclude','preExec','postExec','topOptions','DBRelease','conditionsTag','geometryVersion','beamType','AMITag','outputBSFile','outputESDFile','outputCBNTFile','outputNTUP_TRKVALIDFile','outputNTUP_MUONCALIBFile','outputTAG_COMMFile','outputTAGFile','outputAODFile','triggerConfig','outputHISTFile','outputNTUP_MUFASTFile','outputNTUP_TRIGFile','outputHIST_TRIGEXPERTFile','outputDESDM_EGAMMAFile','outputDESD_PHOJETFile','outputDESD_SGLELFile','outputDESDM_MUONFile','outputDESD_SGLMUFile','outputDESDM_CALJETFile','outputDESD_CALJETFile','outputDESDM_TRACKFile','outputDESD_METFile','outputDESDM_METFile','outputDESD_MBIASFile','outputDESD_PIXELCOMMFile','outputDESD_IDCOMMFile','outputDESD_CALOCOMMFile','outputDESD_TILECOMMFile','outputDESD_MUONCOMMFile','outputDESD_HIRAREFile','outputDESDM_HIRAREFile','outputDESDM_RPVLLFile','outputDESDM_RPVLLCCFile','outputD2ESD_JPSIUPSMMFile','outputD2ESD_ZMMFile','outputD2ESD_WENUFile','outputD2ESD_WMUNUFile','outputDAODM_SGLEMFile','outputDAODM_SGLMUFile','outputDAODM_SGLPHFile','outputDAODM_SGLTAUFile','outputDAOD_2EMFile','outputDAOD_2PHFile','outputDAOD_2MUFile','outputDAOD_EMMUFile','outputDAOD_EMTAUFile','outputDAOD_MUTAUFile','outputDAOD_EMMETFile','outputDAOD_MUMETFile','outputDAOD_JETMETFile','outputDAOD_EMJETFile','outputDAOD_MUJETFile','outputDAOD_TAUJETFile','outputD2AODM_TOPELFile','outputD2AODM_TOPMUFile','outputD2AODM_TOPQCDELFile','outputD2AODM_TOPQCDMUFile','outputDAOD_ONIAMUMUFile','outputD2AODM_TOPQCDJ1File','outputD2AODM_TOPQCDJ2File','outputDESD_COLLCANDFile','outputDAOD_EGLOOSEFile','outputDAOD_PHLOOSEFile','outputD2ESD_DIPHOFile','outputDESDM_DIPHOFile','outputD2AOD_DIPHOFile','outputDAOD_ELLOOSE18File','outputD2AOD_ELLOOSE18File','outputDAOD_MUFile','outputDRAW_ZEEFile','outputDRAW_WENUFile','outputDRAW_ZMUMUFile','outputDRAW_WMUNUFile','outputNTUP_BTAGFile','outputNTUP_EGAMMAFile','outputNTUP_MINBIASFile','outputNTUP_PROMPTPHOTFile','outputNTUP_JETMETFile','outputDESDM_BEAMSPOTFile','outputNTUP_WZFile','outputNTUP_TRTFile','outputNTUP_HECNOISEFile','outputNTUP_SUSYFile','outputNTUP_SMEWFile','outputDAOD_SUSYJETSFile','outputDAOD_SUSYMUONSFile','outputDAOD_SUSYEGAMMAFile','outputNTUP_TOPFile','outputNTUP_HIFile','outputD2ESDM_TRKJETFile','--ignoreerrors','--athenaopts','--omitvalidation','tmpESD','tmpAOD','extraParameter','outputDAOD_RNDMFile','outputNTUP_TOPVALFile','outputD2AODM_TOPJETFile','outputNTUP_SGTOPFile','outputNTUP_MCPFile','outputDAOD_2LHSG2File','outputNTUP_SCTFile','outputNTUP_HIGHMULTFile','outputNTUP_1LHSG2File','outputNTUP_ENHBIASFile','outputNTUP_L1CALOFile','outputNTUP_L1CALOPROBFile','outputNTUP_FASTMONFile','outputNTUP_PHOTONFile']

#Default values of input/output types, for standard tests now set in PATJobTransforms/python/DefaultInputs.py
#The transform class itself
class FlexibleRecoTransform( BaseOfCompositeTrf ):
    def __init__(self, inDic):
        BaseOfCompositeTrf.__init__(self,inputDic=inDic,ProdSysKeys=ListOfDefaultPositionalKeys,
                                    name="Reco_trf",                                    
                                    authors = [ Author('David Cote et al.','david.cote@cern.ch') ] ,
                                    help = __doc__ )

        #Construct dictionaries
        self.dicRAWToRAWHLT=self.AddNewSubStep("r2r",self.runRAWtoRAW)
        self.dicRAWToESD=self.AddNewSubStep("r2e",self.runRAWtoESD)
        self.dicRDOToBS=self.AddNewSubStep("r2b",self.runRDOtoBS)
        self.dicESDToESD=self.AddNewSubStep("e2e",self.runESDtoESD)
        self.dicESDToAOD=self.AddNewSubStep("e2a",self.runESDtoAOD)
        self.dicESDToDPD=self.AddNewSubStep("e2d",self.runESDtoDPD)
        self.dicAODToDPD=self.AddNewSubStep("a2d",self.runAODtoDPD)
        self.dicAODToTAG=self.AddNewSubStep("a2t",self.runAODtoTAG)

        #Internal sub-step configuration (i.e. fill dictionaries)
        self.ConfigureInternalSubSteps()
        self.ConfigureInputOutputs()
        self.CommonSpecialFinalConfig()
        return

    def runJob(self):
        #initialization...
        allOK=True
        esdOK=False
        aodOK=False
        dpdEsdOK=False
        dpdAodOK=False
        report=JobReport()
        report.setProducer('RecoTrf')

        #First setup DBRelease if requested (do not propagate this arg to sub-transforms)
        if self.inDic.has_key('DBRelease'):
            self.getArgument('DBRelease').install()



        ########################
        # RDO->BS
        if (allOK and self.SubStepIsExecuted('r2b')):
            dic=self.dicRDOToBS.copy()
            print "RDOtoBS dic:",dic
            BS = RDOtoBSJobTransform(dic)
            BS._lastInChain=False
            BS.setParent(self)
            BS.setJobReportOptions('Summary')
            reportBS = BS.exeArgDict( dic )
            report.addReport( reportBS )
            bsOK = ( reportBS.exitCode() == 0 )
            print "bsOK is ",bsOK
            allOK = (allOK and bsOK)
        else:
            print "Skipping RDO->BS step..."



        ########################
        # RAW->RAW, run HLT
        if (allOK and self.SubStepIsExecuted('r2r')):
            print ">>> Raw to raw transform, re-running HLT"
            print self.dicRAWToRAWHLT
            dic=self.dicRAWToRAWHLT.copy()
            print "RAWToRAWHLT dic:",dic
            RAW = RAWtoRAWHLTJobTransform(dic)
            RAW._lastInChain=False
            RAW.setParent(self)
            RAW.setJobReportOptions('Summary')
            reportRAW = RAW.exeArgDict( dic )
            report.addReport( reportRAW )
            rawOK = ( reportRAW.exitCode() == 0 )
            print "rawOK is ",rawOK
            allOK = (allOK and rawOK)
        else:
            print "Skipping RAW->RAW runHLT step..."


        ########################
        # RAW->ESD
        if (allOK and self.SubStepIsExecuted('r2e')):
            dic=self.dicRAWToESD.copy()
            print "RAWtoESD dic:",dic
            ESD = RAWtoESDJobTransform(dic)
            ESD._lastInChain=False
            ESD.setParent(self)
            ESD.setJobReportOptions('Summary')
            reportESD = ESD.exeArgDict( dic )
            report.addReport( reportESD )
            esdOK = ( reportESD.exitCode() == 0 )
            print "esdOK is ",esdOK
            allOK = (allOK and esdOK)
        else:
            print "Skipping RAW->ESD step..."

        ########################
        # ESD->ESD, moved to ESD->MergedESD
        if(allOK and self.SubStepIsExecuted('e2e')):
            dic=self.dicESDToESD.copy()
            print "ESDtoESD dic:",dic
            #ESD = ESDtoESDJobTransform(dic)
            ESD = MergePoolJobTransform(dic)
            ESD._lastInChain=False
            ESD.setParent(self)
            ESD.setJobReportOptions('Summary')
            reportESD = ESD.exeArgDict( dic )
            report.addReport( reportESD )
            esdOK = ( reportESD.exitCode() == 0 )
            print "esdOK is ",esdOK
            allOK = (allOK and esdOK)
        else:
            print "Skipping ESD->ESD step..."

        ########################
        # ESD->AOD
        if(allOK and self.SubStepIsExecuted('e2a')):
            dic=self.dicESDToAOD.copy()
            print "ESDtoAOD dic:",dic
            AOD = ESDtoAODJobTransform(dic)
            AOD._lastInChain=False
            AOD.setParent(self)
            AOD.setJobReportOptions('Summary')
            reportAOD = AOD.exeArgDict( dic )
            report.addReport( reportAOD )
            aodOK = ( reportAOD.exitCode() == 0 )
            print "aodOK is ",aodOK
            allOK = (allOK and aodOK)
        else:
            print "Skipping ESD->AOD step..."

        ######################
        # ESD->DPD
        if(allOK and self.SubStepIsExecuted('e2d')):
            dic=self.dicESDToDPD.copy()            
            print "ESDtoDPD dic:",dic
            dpdESD = ESDtoDPDJobTransform(dic)        
            dpdESD._lastInChain=False
            dpdESD.setParent(self)
            dpdESD.setJobReportOptions('Summary')            
            reportDpdEsd = dpdESD.exeArgDict( dic )
            report.addReport( reportDpdEsd )
            dpdEsdOK = ( reportDpdEsd.exitCode() == 0 )
            print "dpdEsdOK is ",dpdEsdOK
            allOK = (allOK and dpdEsdOK)
        else:
            print "Skipping ESD->DPD step..."
            
        ######################
        # AOD->DPD
        if(allOK and self.SubStepIsExecuted('a2d')):
            dic=self.dicAODToDPD.copy()
            print "AODtoDPD dic:",dic            
            dpdAOD = AODtoDPDJobTransform(dic)
            dpdAOD._lastInChain=False
            dpdAOD.setParent(self)
            dpdAOD.setJobReportOptions('Summary')
            reportDpdAod = dpdAOD.exeArgDict( dic )
            report.addReport( reportDpdAod )
            dpdAodOK = ( reportDpdAod.exitCode() == 0 )
            print "dpdAodOK is ",dpdAodOK
            allOK = (allOK and dpdAodOK)
        else:
            print "Skipping AOD->DPD step..."

        ######################
        # AOD->TAG
        if(allOK and self.SubStepIsExecuted('a2t')):
            dic=self.dicAODToTAG.copy()            
            print "AODtoTAG dic:",dic
            tagAOD = AODtoTAGJobTransform(dic)
            tagAOD._lastInChain=False
            tagAOD.setParent(self)
            tagAOD.setJobReportOptions('Summary')
            reportTagAod = tagAOD.exeArgDict( dic )
            report.addReport( reportTagAod )
            tagAodOK = ( reportTagAod.exitCode() == 0 )
            print "tagAodOK is ",tagAodOK
            allOK = (allOK and tagAodOK)
        else:
            print "Skipping AOD->TAG step..."

        ##########################
        # Monitoring file merging
        if(allOK and self.inDic.has_key('outputHISTFile')):
            dic={}
            dic['inputFile']=[]
            if self.runRAWtoESD() and self.dicRAWToESD.has_key('outputDQMonitorFile'): dic['inputFile'].append(self.dicRAWToESD['outputDQMonitorFile'])
            if self.runESDtoAOD() and self.dicESDToAOD.has_key('outputDQMonitorFile'): dic['inputFile'].append(self.dicESDToAOD['outputDQMonitorFile'])
            dic['outputHISTFile']=self.inDic['outputHISTFile']
            print "DQHistogramMerg dic:",dic
            DQMerge = DQHistogramMergeJobTransform(dic)
            DQMerge._lastInChain=False
            DQMerge.setParent(self)
            DQMerge.setJobReportOptions('Summary')
            reportDQMerge = DQMerge.exeArgDict( dic )
            report.addReport( reportDQMerge )
            DQMergeOK = ( reportDQMerge.exitCode() == 0 )
            print "DQMergeOK is ",DQMergeOK
            allOK = (allOK and DQMergeOK)
        else:
            print "Skipping monitoring file merging step..."

        return report


    def ConfigureInternalSubSteps(self):
        self.ConfigureCommonInternalSubSteps()

        #Final hack to separate RDO->BS->ESD and RDO->ESD
        if self.runRDOtoBS() and self.dicRAWToESD.has_key('inputRDOFile'):
            self.dicRAWToESD.pop('inputRDOFile')

        #Final hack for Monitoring
        if self.inDic.has_key("outputHISTFile"):
            self.dicRAWToESD['outputDQMonitorFile']="Monitor.root"
            self.dicESDToAOD['outputDQMonitorFile']="MonitorESD.root"
        return

    def ConfigureInputOutputs(self):
        #Check for potential misconfigurations...        
        if self.inDic.has_key('inputAODFile') and self.inDic.has_key('outputAODFile'):
            raise RuntimeError("input AND output AOD is not supported.")
        if self.inDic.has_key("outputHISTFile") and self.inDic.has_key("outputDQMonitorFile"):
            raise RuntimeError("outputHISTFile *and* outputDQMonitorFile is not supported. Please use one or the other.")

        #--------------------------
        # Daisy-chaining input->output

        #RAW->RAW->ESD
        if self.runRAWtoRAW() and self.dicRAWToRAWHLT.has_key('outputBSFile') and self.hasOutput(self.dicRAWToESD):
            if not self.hasInput(self.dicRAWToESD):
                self.dicRAWToESD['inputBSFile']=self.dicRAWToRAWHLT['outputBSFile']
            else:
                msg="""Illegal configuration. Confusion about RAW->ESD input.
                To run RAW->RAW->ESD, please use inputBSFile_r2r='%s'""",self.dicRAWToRAWHLT['outputBSFile']
                raise RuntimeError(msg)

        #RDO->BS->ESD
        if self.runRDOtoBS() and self.hasOutput(self.dicRAWToESD):
            if not self.hasInput(self.dicRAWToESD):
                self.dicRAWToESD['inputBSFile']=self.dicRDOToBS['outputBSFile']
            else:
                msg="""Illegal configuration. Confusion about RAW->ESD input.
                To run RDO->BS->ESD, please use inputRDOFile outputBSFile outputESDFile"""
                raise RuntimeError(msg)

        #RAW->ESD->AOD+DPD
        outESD=None
        if self.dicRAWToESD.has_key('outputESDFile'): outESD=self.dicRAWToESD['outputESDFile']
        elif self.dicRAWToESD.has_key('tmpESD'): outESD=self.dicRAWToESD['tmpESD']
        if self.runRAWtoESD() and outESD!=None:
            if self.hasOutput(self.dicESDToAOD):
                if not self.hasInput(self.dicESDToAOD):
                    self.dicESDToAOD['inputESDFile']=outESD
                else:
                    raise RuntimeError("Illegal configuration. Confusion about ESD->AOD input.")
            if self.hasOutput(self.dicESDToDPD):
                if not self.hasInput(self.dicESDToDPD):
                    self.dicESDToDPD['inputESDFile']=outESD
                else:
                    raise RuntimeError("Illegal configuration. Confusion about ESD->DPD input.")
                    
        #ESD->ESD->AOD/DPD
        outESD=None
        if self.dicESDToESD.has_key('outputESDFile'): outESD=self.dicESDToESD['outputESDFile']
        elif self.dicESDToESD.has_key('tmpESD'): outESD=self.dicESDToESD['tmpESD']
        if self.runESDtoESD() and outESD!=None:        
            if self.hasOutput(self.dicESDToAOD):
                if self.hasInput(self.dicESDToAOD):
                    print "WARNING oldESD->newESD configuration: newESD will be used as input for ESD->AOD"
                self.dicESDToAOD['inputESDFile']=outESD

            if self.hasOutput(self.dicESDToDPD):
                if self.hasInput(self.dicESDToDPD):
                    print "WARNING oldESD->newESD configuration: newESD will be used as input for ESD->DPD"
                self.dicESDToDPD['inputESDFile']=outESD
                    
        #ESD->AOD->DPD/TAG
        outAOD=None
        if self.dicESDToAOD.has_key('outputAODFile'): outAOD=self.dicESDToAOD['outputAODFile']
        elif self.dicESDToAOD.has_key('tmpAOD'): outAOD=self.dicESDToAOD['tmpAOD']
        if self.runESDtoAOD() and outAOD!=None:
            if self.hasOutput(self.dicAODToDPD):
                if not self.hasInput(self.dicAODToDPD):
                    self.dicAODToDPD['inputAODFile']=outAOD
                else:
                    raise RuntimeError("Illegal configuration. Confusion about AOD->DPD input.")

            if self.hasOutput(self.dicAODToTAG):
                if not self.hasInput(self.dicAODToTAG):
                    self.dicAODToTAG['inputAODFile']=outAOD
                else:
                    raise RuntimeError("Illegal configuration. Confusion about AOD->TAG input.")

        return

    def GetFirstSubStep(self):
        if self.runRAWtoRAW():
            return ["r2r"] #["dicRAWToRAWHLT"]
        elif self.runRAWtoESD():
            return ["r2e"] #["dicRAWToESD"]
        elif self.runRDOtoBS():
            return ["r2b"] #["dicRDOToBS"]          
        elif self.runESDtoESD():
            return ["e2e"] #["dicESDToESD"]                                       
        elif self.runESDtoAOD() or self.runESDtoDPD():
            return ["e2a","e2d"] #["dicESDToAOD","dicESDToDPD"]
        elif self.runAODtoDPD() or self.runAODtoTAG():
            return ["a2d","a2t"] #["dicAODToDPD","dicAODToTAG"]
        return None

    def runRAWtoRAW(self):
        return (self.hasInput(self.dicRAWToRAWHLT) and self.dicRAWToRAWHLT.has_key('outputBSFile'))

    def runRAWtoESD(self):
        return (self.hasInput(self.dicRAWToESD) and self.hasOutput(self.dicRAWToESD))

    def runRDOtoBS(self):
        return (self.dicRDOToBS.has_key('inputRDOFile') and self.dicRDOToBS.has_key('outputBSFile'))
    
    def runESDtoESD(self):
        return (self.hasInput(self.dicESDToESD) and self.dicESDToESD.has_key('outputESDFile'))

    def runESDtoAOD(self):
        return (self.hasInput(self.dicESDToAOD) and self.hasOutput(self.dicESDToAOD))

    def runESDtoDPD(self):
        return (self.hasInput(self.dicESDToDPD) and self.hasOutput(self.dicESDToDPD))

    def runAODtoDPD(self):
        return (self.hasInput(self.dicAODToDPD) and self.hasOutput(self.dicAODToDPD))

    def runAODtoTAG(self):
        return (self.hasInput(self.dicAODToTAG) and self.dicAODToTAG.has_key('outputTAGFile'))


    
###############
if __name__ == '__main__':
    #Special preparation for command-line
    import sys
    from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
    inDic=BuildDicFromCommandLine(sys.argv)
    #Construct and execute the transform
    trf = FlexibleRecoTransform(inDic)
    trf._lastInChain=True
    #trf.Print()
    sys.exit(trf.exeArgDict(inDic).exitCode())

