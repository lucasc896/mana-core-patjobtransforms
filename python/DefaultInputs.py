#!/usr/bin/env python

# Creation: John Chapman (Cambridge), September 2010
# Usage:
#   -specify default inputs for transforms

#Default values of input/output types, for standard tests
DefaultInputs={
    'inputBSFile' : '/afs/cern.ch/atlas/offline/test/data10_7TeV.00162882.physics_Egamma.merge.RAW._lb0201.10evts._0001.data',
    'inputRDOFile': '/afs/cern.ch/atlas/offline/ReleaseData/v3/testfile/valid1.005200.T1_McAtNlo_Jimmy.digit.RDO.e322_s488_d151_tid039414_RDO.039414._00001_extract_10evt.pool.root',
    'inputESDFile': '/afs/cern.ch/atlas/offline/test/data10_7TeV.00162882.physics_Egamma.merge.ESD._lb201.10evts.pool.root', 
    'inputAODFile': '/afs/cern.ch/atlas/offline/test/data10_7TeV.00162882.physics_Egamma.merge.AOD._lb201.10evts.pool.root', 
    'cosmicsBS'   : '/afs/cern.ch/atlas/offline/test/data09_cos.00135664.physics_IDCosmic.daq.RAW._lb0000._SFO-2._0001_10evts.data',
    
    'inputEvgenFile': '/afs/cern.ch/atlas/offline/ProdData/15.6.11.3/mu_E50_eta0-25-7000.evgen.pool.root',
    'inputHitsFile' : 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.105200.T1_McAtNlo_Jimmy.simul.HITS.e564_s851_tid149330_00/HITS.149330._000232.pool.root.1',
    'NDMinbiasHitsFile': 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.105001.pythia_minbias.merge.HITS.e479_s851_s860_tid149154_00/HITS.149154._000075.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.105001.pythia_minbias.merge.HITS.e479_s851_s860_tid149154_00/HITS.149154._000079.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.105001.pythia_minbias.merge.HITS.e479_s851_s860_tid149154_00/HITS.149154._000104.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.105001.pythia_minbias.merge.HITS.e479_s851_s860_tid149154_00/HITS.149154._000106.pool.root.1',
    #'SDMinbiasHitsFile': '/afs/cern.ch/atlas/offline/ProdData/15.6.11.3/mu_E50_eta0-25-7000_ATLAS-GEO-11-00-00.hits.pool.root',
    #'DDMinbiasHitsFile': '/afs/cern.ch/atlas/offline/ProdData/15.6.11.3/mu_E50_eta0-25-7000_ATLAS-GEO-11-00-00.hits.pool.root',
    'cavernHitsFile': 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.005008.CavernInput.simul.HITS.e4_e563_s854_tid149152_00/HITS.149152._000028.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.005008.CavernInput.simul.HITS.e4_e563_s854_tid149152_00/HITS.149152._000080.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.005008.CavernInput.simul.HITS.e4_e563_s854_tid149152_00/HITS.149152._000368.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.005008.CavernInput.simul.HITS.e4_e563_s854_tid149152_00/HITS.149152._000372.pool.root.1',
    'beamHaloHitsFile': 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.108852.BeamHaloInputs.simul.HITS.e4_e567_s852_tid149394_00/HITS.149394._000094.pool.root.1',
    'beamGasHitsFile': 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc09/mc09_14TeV.108863.Hijing_beamgas.simul.HITS.e4_s853_tid149149_00/HITS.149149._000009.pool.root.1'
    }



