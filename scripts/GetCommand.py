#!/usr/bin/env python
import sys
from PATJobTransforms.ArgDicTools import BuildDicFromCommandLine
from RecExConfig.RecoFunctions import OverlapLists

#characters that are problematic for the unix shell
badCharList=[' ','*',';','(',')','{','}','[',']',';']

def HandleDBRelease(DBRel):
    print "***Note: using DBRelease is not mandatory for tests on afs and copies large files on your run directory, you might consider NOT using it."
    if DBRel.count('.')>2:
        DBRel2 = DBRel[0]+DBRel[1]+DBRel[2]+DBRel[3]+DBRel[4]
        print "WARNING original DB version: %s is not available on afs! Version %s is available."%(DBRel,DBRel2)
        DBRel = DBRel2
    print '   If you still want to use it, you can modify your command to use:   DBRelease=/afs/cern.ch/atlas/www/GROUPS/DATABASE/pacman4/DBRelease/DBRelease-'+DBRel+'.tar.gz\n'



def GetKeysAndValues(outDic):
    print "\n"
    keyAndValue=''
    for key in outDic.keys():
        tmp=key
        value=str(outDic[key])
        if value!='':
            if OverlapLists(value,badCharList):
                cFirst=value[0]
                cLast=value[len(value)-1]
                if (cFirst=="'" and cLast=="'") or (cFirst=='"' and cLast=='"'):
                    pass
                else:
                    zeChar="'"
                    if value.rfind("'")>0:
                        zeChar='"'
                        if value.rfind('"')>0:
                            print "WARNING cannot properly handle value:",value
                            zeChar=''
                    
                oldValue=value
                value=zeChar+value+zeChar
                if value!=oldValue: print "INFO: %s=%s has been updated to %s=%s"%(key,oldValue,key,value)
                pass
            tmp+=('='+value)
        tmp+=' '
        keyAndValue+=tmp
    return keyAndValue


def GetCommand(sysArgv):
    cmdList=BuildDicFromCommandLine(sysArgv,returnList=True)
    if cmdList==[]:
        print "\nGetCommand finds nothing, probably because you didn't specify an AMI tag."
        print "Please use syntax:  GetCommand.py AMI=<tag>"
        return

    i=1
    for cmd in cmdList:
        trf=cmd['info']['amiTransform']
        if trf=='Reco_trf' or trf=='/afs/cern.ch/atlas/project/tzero/prod1/projects/data08_cos/trfs/Recon.v5.py, based on Reco_trf.py':
            trf='Reco_trf.py'

        if trf=='csc_digi_trf.py':
            trf='Digi_trf.py'

        if trf=='csc_atlasG4_trf.py':
            trf='AtlasG4_trf.py'

        outDic=cmd['outDic']
        keysAndValues=GetKeysAndValues(outDic)
        print "\n\n###################################################################"
        print "This is command #%i:\n"%i
        print trf,keysAndValues
        print "\n"
        if outDic.has_key('DBRelease'): HandleDBRelease(outDic['DBRelease'])            
        i+=1
        

    print "***Note: input and output file names are just suggestions, you're expected to change them as you need.***\n"

if __name__ == '__main__':
    GetCommand(sys.argv)

        
