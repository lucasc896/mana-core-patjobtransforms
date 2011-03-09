#!/usr/bin/env python

# Creation: John Chapman (Cambridge), September 2010
# Usage:
#   -specify default inputs for transforms

#Default values of input/output types, for standard tests
DefaultInputs={
    'inputBSFile' : '/afs/cern.ch/atlas/offline/test/data10_7TeV.00162882.physics_Egamma.merge.RAW._lb0201.10evts._0001.data',
    'inputRDOFile': '/afs/cern.ch/atlas/offline/ReleaseData/v3/testfile/valid1.005200.T1_McAtNlo_Jimmy.digit.RDO.e322_s488_d151_tid039414_RDO.039414._00001_extract_10evt.pool.root',
    'inputESDFile': '/afs/cern.ch/atlas/offline/test/data10_7TeV.00162882.physics_Egamma.merge.ESD._lb201.10evts.rel16.pool.root', 
    'inputAODFile': '/afs/cern.ch/atlas/offline/test/data10_7TeV.00162882.physics_Egamma.merge.AOD._lb201.10evts.rel16.pool.root', 
    'cosmicsBS'   : '/afs/cern.ch/atlas/offline/test/data09_cos.00135664.physics_IDCosmic.daq.RAW._lb0000._SFO-2._0001_10evts.data',
    
    'inputEvgenFile': '/afs/cern.ch/atlas/offline/ProdData/15.6.11.3/mu_E50_eta0-25-7000.evgen.pool.root',
    'inputHitsFile' : 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.105200.T1_McAtNlo_Jimmy.simul.HITS.e598_s933_tid168076_00/HITS.168076._008421.pool.root.1',
    'NDMinbiasHitsFile': 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.105001.pythia_minbias.merge.HITS.e577_s932_s952_tid170554_00/HITS.170554._000034.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.105001.pythia_minbias.merge.HITS.e577_s932_s952_tid170554_00/HITS.170554._000043.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.105001.pythia_minbias.merge.HITS.e577_s932_s952_tid170554_00/HITS.170554._000060.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.105001.pythia_minbias.merge.HITS.e577_s932_s952_tid170554_00/HITS.170554._000082.pool.root.1',
    #'SDMinbiasHitsFile': '/afs/cern.ch/atlas/offline/ProdData/15.6.11.3/mu_E50_eta0-25-7000_ATLAS-GEO-11-00-00.hits.pool.root',
    #'DDMinbiasHitsFile': '/afs/cern.ch/atlas/offline/ProdData/15.6.11.3/mu_E50_eta0-25-7000_ATLAS-GEO-11-00-00.hits.pool.root',
    'cavernHitsFile': 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.005008.CavernInput.merge.HITS.e4_e607_s951_s952_tid170551_00/HITS.170551._000011.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.005008.CavernInput.merge.HITS.e4_e607_s951_s952_tid170551_00/HITS.170551._000111.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.005008.CavernInput.merge.HITS.e4_e607_s951_s952_tid170551_00/HITS.170551._000144.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.005008.CavernInput.merge.HITS.e4_e607_s951_s952_tid170551_00/HITS.170551._000150.pool.root.1,root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.005008.CavernInput.merge.HITS.e4_e607_s951_s952_tid170551_00/HITS.170551._000151.pool.root.1',
    'beamHaloHitsFile': 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.108852.BeamHaloInputs.merge.HITS.e4_e567_s949_s952_tid170552_00/HITS.170552._000001.pool.root.1',
    'beamGasHitsFile': 'root://castoratlas//castor/cern.ch/atlas/atlascerngroupdisk/proj-sit/digitization/RTT/mc10/mc10_7TeV.108863.Hijing_beamgas.merge.HITS.e4_s950_s952_tid170553_00/HITS.170552._000087.pool.root.1'
    }



