#!/usr/bin/env python

__doc__ = """Merge NTUP files."""

from PATJobTransforms.BaseOfBasicTrf import BaseOfBasicTrf
from PyJobTransformsCore.trf import Author

ListOfDefaultPositionalKeys=['--ignoreerrors', '--omitvalidation', 'outputNTUP_SMDYMUMUFile', 'outputNTUP_HSG5WHFile', 'outputNTUP_HSG5ZHLLFile', 'inputNTUP_TAUSMALLFile', 'inputNTUP_SMDYEEFile', 'outputNTUP_SMWZSOFTFile', 'outputNTUP_TOPEJETFile', 'inputNTUP_SMWMUNUFile', 'outputNTUP_TRIGMUFile', 'inputNTUP_SMWENUFile', 'outputNTUP_MUFASTFile', 'inputNTUP_PROMPTPHOTFile', 'outputNTUP_SMWENUFile', 'inputNTUP_HIFile', 'outputNTUP_TRIGBJETFile', 'outputNTUP_SUSYSKIMFile', 'outputNTUP_TOPMUFile', 'inputNTUP_MCPFile', 'outputNTUP_PHOTONFile', 'inputNTUP_SMWENUJJFile', 'inputNTUP_HSG5GAMZFile', 'outputNTUP_TOPELFile', 'outputNTUP_SMWMUNUFile', 'inputNTUP_TOPVALFile', 'inputNTUP_SMBKGEFile', 'inputNTUP_L1CALOFile', 'outputNTUP_TOPFile', 'outputNTUP_SUSYLLPFile', 'outputNTUP_TAUSMALLFile', 'outputNTUP_BTAGD3PDFile', 'outputNTUP_TAUMEDIUMFile', 'outputNTUP_SUSYFile', 'outputNTUP_TRTFile', 'outputNTUP_L1TGCFile', 'inputNTUP_TRIGBJETFile', 'inputNTUP_TOPMUFile', 'inputNTUP_SMZEEFile', 'inputNTUP_TRIGFile', 'outputNTUP_HECNOISEFile', 'outputNTUP_MINBIASFile', 'outputNTUP_SMTRILEPFile', 'outputNTUP_BKGDFile', 'outputNTUP_JETMETFile', 'inputNTUP_TAUMEDIUMFile', 'outputNTUP_JETMETFULLFile', 'inputNTUP_BKGDFile', 'inputNTUP_JETMETWZFile', 'inputNTUP_TRKVALIDFile', 'outputNTUP_SMWMUNUJJFile', 'outputNTUP_SMZEEFile', 'outputNTUP_L1CALOFile', 'outputNTUP_TOPJETFile', 'outputNTUP_MCPFile', 'outputNTUP_HSG5GAMZFile', 'inputNTUP_MINBIASFile', 'inputNTUP_HSG5ZHMETFile', 'outputNTUP_TRUTHFile', 'outputNTUP_SMDYEEFile', 'inputNTUP_BTAGD3PDFile', 'outputNTUP_TRIGFile', 'outputNTUP_SMWENUJJFile', 'inputNTUP_SMBKGMUFile', 'inputNTUP_SUSYFile', 'outputNTUP_TOPBOOSTFile', 'inputNTUP_SUSY01LEPFile', 'outputNTUP_PHYSICSFile', 'inputNTUP_PHOTONFile', 'inputNTUP_MUFASTFile', 'inputNTUP_HSG5ZHLLFile', 'inputNTUP_PHYSICSFile', 'inputNTUP_ENHBIASFile', 'inputNTUP_TOPBOOSTFile', 'outputNTUP_SUSY01LEPFile', 'outputNTUP_MUONCALIBFile', 'outputNTUP_MUONFile', 'inputNTUP_FASTMONFile', 'inputNTUP_SMWZFile', 'outputNTUP_WZFile', 'inputNTUP_HECNOISEFile', 'inputNTUP_L1TGCFile', 'outputNTUP_HSG5GAMHFile', 'outputNTUP_SMDILEPFile', 'inputNTUP_SMDYMUMUFile', 'inputNTUP_SCTFile', 'outputNTUP_LARNOISEFile', 'outputNTUP_JETMETWZFile', 'inputNTUP_EGAMMAFile', 'inputNTUP_SMEWFile', 'outputNTUP_FASTMONFile', 'inputNTUP_JETMETEMCLFile', 'outputNTUP_PROMPTPHOTFile', 'inputNTUP_SUSY23LEPFile', 'outputNTUP_L1CALOPROBFile', 'inputNTUP_LARNOISEFile', 'inputNTUP_SMDILEPFile', 'outputNTUP_SMQCDFile', 'inputNTUP_SMWZSOFTFile', 'outputNTUP_HIGHMULTFile', 'outputNTUP_HIFile', 'outputNTUP_EGAMMAFile', 'inputNTUP_TOPELFile', 'outputNTUP_HSG5ZBBFile', 'inputNTUP_BTAGFile', 'outputNTUP_HSG5ZHMETFile', 'outputNTUP_SUSY23LEPFile', 'inputNTUP_SMTRILEPFile', 'inputNTUP_TOPFile', 'inputNTUP_TOPJETFile', 'outputNTUP_SGTOPFile', 'inputNTUP_HSG5WHFile', 'outputNTUP_SMWZFile', 'inputNTUP_JETMETFULLFile', 'inputNTUP_HIGHMULTFile', 'outputNTUP_SMBKGMUFile', 'inputNTUP_JETMETFile', 'inputNTUP_MUONFile', 'outputNTUP_TRKVALIDFile', 'outputNTUP_HSG2File', 'inputNTUP_SMZMUMUFile', 'inputNTUP_SMQCDFile', 'outputNTUP_SCTFile', 'inputNTUP_HSG5ZBBFile', 'outputNTUP_SMZMUMUFile', 'outputNTUP_ENHBIASFile', 'inputNTUP_HSG2File', 'outputNTUP_SMBKGEFile', 'inputNTUP_HSG5GAMHFile', 'outputNTUP_BTAGFile', 'inputNTUP_TRIGMUFile', 'inputNTUP_SUSYLLPFile', 'inputNTUP_MUONCALIBFile', 'inputNTUP_TOPEJETFile', 'inputNTUP_WZFile', 'inputNTUP_SMWMUNUJJFile', 'outputNTUP_SMEWFile', 'inputNTUP_L1CALOPROBFile', 'outputNTUP_TOPVALFile', 'outputNTUP_JETMETEMCLFile', 'inputNTUP_SUSYSKIMFile', 'inputNTUP_TRUTHFile', 'inputNTUP_TRTFile', 'outputNTUP_SUSYBOOSTFile', 'inputNTUP_SUSYBOOSTFile', 'outputNTUP_SUSY34LEPFile', 'inputNTUP_SUSY34LEPFile', 'outputNTUP_ZPRIMEMMFile', 'inputNTUP_ZPRIMEMMFile', 'outputNTUP_SUSYLEPTAUFile', 'inputNTUP_SUSYLEPTAUFile', 'outputNTUP_SUSYTAGFile', 'inputNTUP_SUSYTAGFile', 'outputNTUP_SUSYRAZORFile', 'inputNTUP_SUSYRAZORFile', 'outputNTUP_SUSY23LEPFile', 'inputNTUP_SUSY23LEPFile']

class MergeNTUPJobTransform( BaseOfBasicTrf ):
    def __init__(self,inDic):
        BaseOfBasicTrf.__init__(self,inDic,
                                authors = [ Author('Bjorn Sarrazin', 'Bjorn.Sarrazin@cern.ch')],
                                skeleton='PATJobTransforms/skeleton.MergeNTUP_trf.py',
                                help = __doc__ )

    def matchEvents(self):
        for key in self._namedArgs.iterkeys():
            if key.startswith('inputntup') and key.endswith('file'):
                inputFileArgName=key
            if key.startswith('outputntup') and key.endswith('file'):
                outputFileArgName=key

        inFile=self.getArgument(inputFileArgName)
        outFile=self.getArgument(outputFileArgName)

        in_tree_names=inFile._fileType.tree_names 
        out_tree_names=outFile._fileType.tree_names

        if not in_tree_names:
            self.logger().info("MatchEvents is not executed for MergeNTUP. No tree_name is given for input file.")
            return

        if not out_tree_names:
            self.logger().info("MatchEvents is not executed for MergeNTUP. No tree_name is given for output file.")
            return

        if in_tree_names!=out_tree_names:
            self.logger().info("MatchEvents is not executed for MergeNTUP. Different tree_name given for input and output file.")
            return
                
        self.matchEventsExpectEqual(inputFileArgName, outputFileArgName)
        
        return

#----------------------------------------------------------------------
if __name__ == '__main__':    
    #Special preparation for command-line
    import sys
    from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
    inDic=BuildDicFromCommandLine(sys.argv)
    #Construct and execute the transform
    trf = MergeNTUPJobTransform(inDic)          
    sys.exit(trf.exeArgDict(inDic).exitCode())

