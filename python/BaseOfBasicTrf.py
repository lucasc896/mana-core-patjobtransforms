#!/usr/bin/env python

from PyJobTransformsCore.trf import JobTransform

class BaseOfBasicTrf( JobTransform ):
    def __init__(self,inDic,authors,skeleton,help,name="default"):
        JobTransform.__init__(self, name=name, authors=authors, skeleton=skeleton, help=help)

        if not isinstance(inDic,dict):
            raise TypeError("inDic has type '%s' but should be a dictionary." %type(inDic))

        from PATJobTransforms.ConfigDicUtils import AutoConfigureFromDic
        self.inDic=inDic
        AutoConfigureFromDic(self,inDic)

    def matchEventsExpectEqual(self,inputFileArgName,outputFileArgName):
        #Note: _namedArgs has lower case keys 
        inputFileArgName=inputFileArgName.lower()
        outputFileArgName=outputFileArgName.lower()
        
        if self._namedArgs.has_key("inputfile"):
            inFile=self.getArgument("inputfile")
        elif self._namedArgs.has_key(inputFileArgName):
            inFile=self.getArgument(inputFileArgName)
        else:
            self.logger().warning("No input file matching '%s'. MatchEvents not executed."%inputFileArgName)
            return

        if self._namedArgs.has_key(outputFileArgName):
            outFile=self.getArgument(outputFileArgName)
        else:
            self.logger().warning("No output file matching '%s'. MatchEvents not executed."%outputFileArgName)
            return

        maxEvents=-1
        if self._namedArgs.has_key("maxevents"):
            maxEvents=self.getArgument("maxevents").value()

        inEvents=inFile.eventCount()
        if (maxEvents > 0) and (maxEvents < inEvents):
            self.logger().info("MaxEvents < input_Events. MatchEvents not executed.")
            return

        outEvents=outFile.eventCount()
        diff=inEvents-outEvents
        if diff==0:
            self.logger().info("Input and output files have the same number of events. That's good!")
        else:
            from PyJobTransformsCore import AtlasErrorCodes
            self.logger().warning("Input (%i events) and output (%i events) files have different number of events. That's unexpected."%(inEvents,outEvents))
            self.addError( acronym = 'TRF_OUTFILE_TOOFEW', severity = AtlasErrorCodes.FATAL )

        return


