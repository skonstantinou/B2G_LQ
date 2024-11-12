#condor: python runPlotter.py +r pset_SkimAnalysis_categories.py +c True
#local:  python runPlotter.py +r pset_SkimAnalysis_categories.py

from setup.pyPlotter import *
import copy
from tools.xsecDictionaries import TLTL, TLQ5L, Q5LQ5L, TLL, TLVL, Q5LVL, VLL
pset = pset()

# ---------------------------------------------------------------------------------
#   General settings
# ---------------------------------------------------------------------------------

years=["2018"]
analysisName = 'categories'

for year in years:
    analysisName = analysisName + '_' + year

pset.analysis=analysisName
pset.useMT = False
pset.canvas.style = 'Analysis'
pset.canvas.showUncertainty = True
pset.canvas.ratioYLow = 0.0
pset.canvas.ratioYHigh = 2.0
pset.saveHisto = True

pset.canvas.label=analysisName

# [1] Adding aliases
import tools.aliases
pset.aliases += tools.aliases.aliases

# [2] Update global selections (1L)
#pset.globalSelection='PassLumiJsonFilter>0&&(LightLepton_N)==1'
pset.globalSelection='TrigAccept>0 && Event_IsTight>0 && PassMETFilters>0 && PassLumiJsonFilter>0 && LightLepton_N>0'

# [3] Additional aliases
pset.aliases.append( ('ZPt','vecPt(LightLepton_Pt,LightLepton_Eta,LightLepton_Phi,2)') )
pset.aliases.append( ('AllLeptMass','invMass(LightLepton_Pt,LightLepton_Eta,LightLepton_Phi)') )
pset.aliases.append(('AllLepton_N','LightLepton_N + Tau_N'))
pset.aliases.append(('Custom_ST_AltRange','Custom_ST'))
pset.aliases.append(('AllJet_Pt_Duplicate','AllJet_Pt'))
pset.aliases.append(('AltHT','sum(AllJet_Pt)'))
pset.aliases.append( ('nOnZ', 'int nOnZ = 0; for (size_t i=0; i<Event_BestMOSSF.size(); i++) {int isOnZ =int(abs(Event_BestMOSSF.at(i)-91.)<=15.); nOnZ += isOnZ; } return nOnZ;'))
#pset.aliases.append(('OSSF_N', 'size(Event_BestMOSSF)'))
pset.aliases.append(('OSSF_N', 'Event_LightLeptonOSSFN[0]'))
pset.aliases.append(('IsOSSF', 'Event_LightLeptonChargeSum==0 && Event_LightLeptonOSSFN[0]==1'))
pset.aliases.append(('IsOSDF', 'Event_LightLeptonChargeSum==0 && Event_LightLeptonOSSFN[0]==0'))
pset.aliases.append(('IsSS',   'Event_LightLeptonChargeSum!=0'))
pset.force.mcOnly.aliases.append(('PassLumiJsonFilter', '1.0'))


pset.aliases.append(('Category', 'eventCategories(LooseTopFatJet_N, LooseWFatJet_N, LightLepton_N, IsOSSF, IsOSDF, IsSS)'))
pset.aliases.append(('CategoryLepInc', 'eventCategoriesLepInc(LooseTopFatJet_N, LooseWFatJet_N)'))
pset.aliases.append(('CategoryEXO21002', 'eventCategoriesEXO21002(LightLepton_N, Tau_N)'))

pset.aliases.append(('PassTopSelections',  'LooseTopFatJet_N > 0'))
pset.aliases.append(('Pass0TSelections',   'LooseTopFatJet_N==0 && CustomJet_N>1 && CustomBJet_N>0'))
#pset.aliases.append(('Pass0T0WSelections', 'LooseTopFatJet_N==0 && LooseWFatJet_N==0 && CustomJet_N>1 && CustomBJet_N>0 && Event_BestMOSSF[0]>MZhigh__'))
pset.aliases.append(('PassSelections', 'PassTopSelections || Pass0TSelections'))

pset.variables=[
    ('LightLepton_N','No. of light leptons',6,-0.5,5.5),
    ('IsOSSF', 'IsOSSF', 2, -0.5, 1.5),
    ('IsOSDF', 'IsOSDF', 2, -0.5, 1.5),
    ('IsSS', 'IsSS', 2, -0.5, 1.5),
    ('nOnZ','nOnZ',4,-0.5,3.5),
    ('OSSF_N','OSSF_N',4,-0.5,3.5),
    ('Tau_N','No. of taus (hadronic)',6,-0.5,5.5),
    ('AllLepton_N','No. of light leptons plus taus (hadronic)',11,-0.5,10.5),
    ('CustomJet_N','No. of jets',21,-0.5,20.5),
    ('CustomBJet_N','No. of b jets',11,-0.5,10.5),
    ('Custom_ST','S_{T}',30,0,3000),
    ('Custom_ST_AltRange','S_{T}',10,0,2000),
    ('Event_BestMOSSF[0]','Best M_{OSSF}',50, 0, 1000),
    ('Category', 'Category', 26,-0.5,25.5),
    ('CategoryLepInc', 'Lepton-Inclusive Category', 8,-0.5,7.5),
    ('CategoryEXO21002', 'EXO-21-002 Category', 9,-0.5,8.5),
    ('LooseTopFatJet_N', 'LooseTopFatJet_N', 5,-0.5,4.5),
    ('LooseWFatJet_N', 'LooseWFatJet_N', 5,-0.5,4.5),
    ('CustomMET','E_{T}^{miss}',50,0,1000),
    ('LT','L_{T}',20,0,2000),
    ('Custom_HT','H_{T}',20,0,2000),

]

cate = {
    "1" : "2T, 1L",
    "2" : "2T, 2LOSSF",
    "3" : "2T, 2LOSDF",
    "4" : "1T1W, 1L",
    "5" : "1T1W, 2LOSSF",
    "6" : "1T1W, 2LOSDF",
    "7" : "2W, 1L",
    "8" : "2W, 2LOSSF",
    "9" : "2W, 2LOSDF",
    "10" : "1T0W, 1L",
    "11" : "1T0W, 2LOSSF",
    "12" : "1T0W, 2LOSDF",
    "13" : "1T0W, 2LSS",
    "14" : "1T0W, 3L",
    "15" : "0T1W, 1L",
    "16" : "0T1W, 2LOSSF",
    "17" : "0T1W, 2LOSDF",
    "18" : "0T1W, 2LSS",
    "19" : "0T1W, 3L",
    "20" : "0T0W, 1L",
    "21" : "0T0W, 2LOSSF",
    "22" : "0T0W, 2LOSDF",
    "23" : "0T0W, 2LSS",
    "24" : "0T0W, 3L",
    "25" : "0T0W, 4L",
    "26" : "ELSE",
}

cateLepInc = {
    "1" : "2T",
    "2" : "1T1W",
    "3" : "2W",
    "4" : "1T0W",
    "5" : "0T1W",
    "6" : "0T0W",
    "7" : "ELSE",
}

cateEXO21002 = {
    "1" : "4L",
    "2" : "3L1T",
    "3" : "3L",
    "4" : "2L2T",
    "5" : "2L1T",
    "6" : "1L3T",
    "7" : "1L2T",
    "8" : "ELSE",
}

pset.localSelections = [
    ('1','All'),
    #('LooseTopFatJet_N==2 && %s' % local1, '2T'),
    #('LooseTopFatJet_N==1 && LooseWFatJet_N==1 && %s' % local1, '1T1W'),
    #('LooseTopFatJet_N==1 && LooseWFatJet_N==0 && %s' % local1, '1T0W'),
    #('LooseTopFatJet_N==0 && LooseWFatJet_N==1 && %s' % local1, '0T1W'),
    #('LooseTopFatJet_N==0 && LooseWFatJet_N==2 && %s' % local1, '0T2W'),
    #('LooseTopFatJet_N==0 && LooseWFatJet_N==0 && %s' % local1, '0T0W'),
    ##('LooseTopFatJet_N==2', 'fast test'),
]

#pset.localSelections.append(("LightLepton_N>1", "N_LL>1"))
#pset.localSelections.append(("LightLepton_N>1 && nOnZ==0", "N_LL>1; nOnZ=0"))
#pset.localSelections.append(("LightLepton_N>1 && nOnZ==0 && CustomJet_N>1", "N_LL>1; nOnZ=0; N_CJ>1"))
#pset.localSelections.append(("LightLepton_N>1 && nOnZ==0 && CustomJet_N>1 && CustomBJet_N>0", "N_LL>1; nOnZ=0; N_CJ>1; N_CBJ>0"))
#pset.localSelections.append(("LightLepton_N>1 && nOnZ==0 && CustomJet_N>1 && CustomBJet_N>0 && ST>1000", "N_LL>1; nOnZ=0; N_CJ>1; N_CBJ>0; ST>1000"))

#for i in range(1,26):
#    pset.localSelections.append( ("nOnZ==0 && Event_BestMOSSF[0]>MZhigh__ && PassSelections && Category==%s" % i, cate["%s" % i]) )

#for i in range(1,8): # lepton-inclusive categories
#    pset.localSelections.append( ("CategoryLepInc==%s" % i, cateLepInc["%s" % i]) )
#    pset.localSelections.append( ("CategoryLepInc==%s && nOnZ==0" % i, cateLepInc["%s" % i] + "; nOnZ==0" ) )
#    pset.localSelections.append( ("CategoryLepInc==%s && nOnZ==0 && ST > 1000" % i, cateLepInc["%s" % i] + "; nOnZ==0; ST>1000" ) )
#    if i==3 or i==5 or i==6 or i==7: #Lep Inc Categories where N_Top == 0
#        pset.localSelections.append( ("CategoryLepInc==%s && nOnZ==0 && ST > 1000 && CustomJet_N>1 && CustomBJet_N>0" % i, cateLepInc["%s" % i] + "; nOnZ==0; ST>1000; Nj>1; Nb>0" ) )
#    if i==6: #Lep Inc Category with 0 boosted jets of any type (0T0W)
#        for j in range(1,9):
#            pset.localSelections.append( ("CategoryEXO21002==%s" % j, "0T0W; EXO-21-002 Sel. " + cateEXO21002["%s" % j]) )

#pset.localSelections.append( ("LightLepton_N==3 && CustomBJet_N > 0 && OSSF_N == 1 && Event_BestMOSSF[0] > 91", "3L, 1B")) # EXO-21-002 3L1B Advanced Bin 87

pset.localSelections.append( ("nOnZ==0 && (OSSF_N == 0 || Event_BestMOSSF[0]>MZhigh__) && PassSelections", "all categories"))
pset.localSelections.append( ("nOnZ==0 && (OSSF_N == 0 || Event_BestMOSSF[0]>MZhigh__) && PassSelections && Custom_ST > 500", "all categories (ST > 500 GeV)"))
pset.localSelections.append( ("nOnZ==0 && (OSSF_N == 0 || Event_BestMOSSF[0]>MZhigh__) && PassSelections && Custom_ST > 1000", "all categories (ST > 1000 GeV)"))


### SCHEME B FINAL STATES WITH CROSS SECTIONS ###
dsetNames = {
    "M1Y0pt01TLTL" :  "top tau top tau",
    "M1Y0pt01TLQ5L" : "top tau b nu",
}

#1L signals
inputsSignal18_1L = [
(dsetNames["M1Y0pt01TLTL"],TLTL["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/1L_Skim_medium_2018/Snapshot_LQ_TLTL_M1000_Y0pt01_0_0.root",1.00, 0.,"1","skimTree"),
(dsetNames["M1Y0pt01TLQ5L"],TLQ5L["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/1L_Skim_medium_2018/Snapshot_LQ_TLQ5L_M1000_Y0pt01_0_1.root",1.00, 0.,"1","skimTree"),
]


#2L signals
inputsSignal18_2LOS = [
(dsetNames["M1Y0pt01TLTL"],TLTL["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/2LOS_Skim_medium_2018/Snapshot_LQ_TLTL_M1000_Y0pt01_0_0.root",1.00, 0.,"1","skimTree"),
(dsetNames["M1Y0pt01TLQ5L"],TLQ5L["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/2LOS_Skim_medium_2018/Snapshot_LQ_TLQ5L_M1000_Y0pt01_0_1.root",1.00, 0.,"1","skimTree"),
]

inputsSignal18_2LSS = [
(dsetNames["M1Y0pt01TLTL"],TLTL["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/2LSS_Skim_medium_2018/Snapshot_LQ_TLTL_M1000_Y0pt01_0_0.root",1.00, 0.,"1","skimTree"),
(dsetNames["M1Y0pt01TLQ5L"],TLQ5L["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/2LSS_Skim_medium_2018/Snapshot_LQ_TLQ5L_M1000_Y0pt01_0_1.root",1.00, 0.,"1","skimTree"),
]


#3L signals
inputsSignal18_3L = [
(dsetNames["M1Y0pt01TLTL"],TLTL["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/3L_Skim_medium_2018/Snapshot_LQ_TLTL_M1000_Y0pt01_0_0.root",1.00, 0.,"1","skimTree"),
(dsetNames["M1Y0pt01TLQ5L"],TLQ5L["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/3L_Skim_medium_2018/Snapshot_LQ_TLQ5L_M1000_Y0pt01_0_1.root",1.00, 0.,"1","skimTree"),
]


#4L signals
inputsSignal18_4L = [
(dsetNames["M1Y0pt01TLTL"],TLTL["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/4L_Skim_medium_2018/Snapshot_LQ_TLTL_M1000_Y0pt01_0_0.root",1.00, 0.,"1","skimTree"),
(dsetNames["M1Y0pt01TLQ5L"],TLQ5L["Mass-"+"1"+"_Yukawa-"+"0.01"],"/cms/multilepton-3/pjm275/LQ_Skims/4L_Skim_medium_2018/Snapshot_LQ_TLQ5L_M1000_Y0pt01_0_1.root",1.00, 0.,"1","skimTree"), #No 4L events in this sample
]


#Get input lists
pset.inputs.file.list+=inputsSignal18_4L
pset.inputs.file.list+=inputsSignal18_3L
pset.inputs.file.list+=inputsSignal18_2LOS
pset.inputs.file.list+=inputsSignal18_2LSS
pset.inputs.file.list+=inputsSignal18_1L

import inputs.list_MC_1L_Skim_medium_2018_tagLQv0 as MC1L
import inputs.list_MC_2LOS_Skim_medium_2018_tagLQv0 as MC2LOS
import inputs.list_MC_2LSS_Skim_medium_2018_tagLQv0 as MC2LSS
import inputs.list_MC_3L_Skim_medium_2018_tagLQv0 as MC3L
import inputs.list_MC_4L_Skim_medium_2018_tagLQv0 as MC4L

pset.inputs.file.list+=MC1L.inputs
pset.inputs.file.list+=MC2LOS.inputs
pset.inputs.file.list+=MC2LSS.inputs
pset.inputs.file.list+=MC3L.inputs
pset.inputs.file.list+=MC4L.inputs

# ---------------------------------------------------------------------------------
#   Input & bundle settings
# ---------------------------------------------------------------------------------
#import inputs.list_MC_1L_Skim_medium_2018_tagLQv0 as MC [soti|fixme]: do we have the bkg?
#pset.inputs.file.list=MC.inputs

#pset.bundles.stack = ["DY", "ST", "TTPOW", "TTW", "TTZ", "W", "WW", "WZ", "ZZ"]
pset.bundles.stack = ["DY", "ST", "TT", "TTW", "TTZ", "WW", "WZ", "ZZ"]
#pset.bundles.stack = [ "TTW", "TTZ", "WZ", "WW", "ZZ"]
#pset.bundles.stack = [ "DY", "TTW", "TTZ", "WW", "WZ", "ZZ"]
pset.bundles.overlay = [dsetNames["M1Y0pt01TLTL"], dsetNames["M1Y0pt01TLQ5L"]]
pset.bundles.legend = {dsetNames["M1Y0pt01TLTL"]:1, dsetNames["M1Y0pt01TLQ5L"]:2, 'DY':634, 'ST':625, 'TT':793, 'TTW':831, 'TTZ':870, 'W':920, 'WW':611, 'WZ':801, 'ZZ':901}
# [5] ???
pset.bundles.isData = []
pset.bundles.sort = True

# [6] Adding MC Weights
pset.bundles.mcOnly.weights=[ 
    'XSecNormWeight'
    ,'LeptonPOGSFWeight'
    ,'TrigSFWeight'
    ,'LeptonCustomSFWeight'
    ,'PileupWeight'
    #,'L1PreWt_Nom'
]

pset.bundles.weights=[ 
]
