import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("#scale[1.5]{CMS}   h,H,A#rightarrow#tau#tau                     19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)"),
    #dataset = cms.string("#scale[1.5]{CMS} (unpublished)  h,H,A#rightarrow#tau#tau, 19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)"),
    #dataset = cms.string("#scale[1.5]{CMS}   h,H,A#rightarrow#tau#tau                                         + 18.3 fb^{-1} (7 TeV)"),
    ## x-axis title
    xaxis = cms.string("m_{A} [GeV]"),
    ## y-axis title
    yaxis = cms.string("#bf{tan#beta}"),
    ## theory label 
    theory = cms.string("MSSM low-tan#beta-high scenario"),
    ## min for plotting
    min = cms.double(0.5),
    ## max for plotting
    max = cms.double(9.5),
    ## min for plotting
    log = cms.int32(0),
    ## print to png
    png = cms.bool(True),
    ## print to pdf
    pdf = cms.bool(True),
    ## print to txt
    txt = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## define verbosity level
    verbosity = cms.uint32(3),
    ## define output label
    outputLabel = cms.string("HypoTest") ,
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
   150.
   ,160.
   ,170.
   ,180.
   ,190.
   ,200.
   ,210.
   ,220.
   ,230.
   ,240.
   ,250.
   ,275.
   ,300.
   ,325.
   ,350.
   ,375.
   ,400.
   ,425.
   ,450.
   ,475.
   ,500
     ),
    ## is this mssm?
    mssm = cms.bool(True),
    ## is this MSSMvsSM?
    MSSMvsSM = cms.bool(True),
    ## plot black and white friendly?
    BlackWhite = cms.bool(False),
    ## print the 2-sigma band
    outerband = cms.bool(True),
    ## plot expected only
    expectedOnly = cms.bool(False),
    ## plot transparent?
    transparent = cms.bool(True),
    ## print constraints from mH=125GeV
    higgs125 = cms.bool(True),
    ## add arXiv-1211-6956 (ATLAS) to plot
    arXiv_1211_6956 = cms.bool(False),
    ## add arXiv-1204-2760 (ATLAS) to plot
    arXiv_1204_2760 = cms.bool(False),
    ## add arXiv-1302-2892
    arXiv_1302_2892 = cms.bool(False),
    ## add arXiv-1205-5736
    arXiv_1205_5736 = cms.bool(False),
    ## add HIG-12-052
    HIG_12_052 = cms.bool(False),
)
