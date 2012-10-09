import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string(" 2012, #sqrt{s} = 8 TeV, H #rightarrow #tau #tau, L = 5.0 fb^{-1}"),
    #dataset = cms.string(" 2011, #sqrt{s} = 7 TeV, H #rightarrow #tau #tau, L = 4.9 fb^{-1}"),
    dataset = cms.string(" Preliminary, #sqrt{s} = 7-8 TeV, H #rightarrow #tau #tau, L = 10 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("Best fit for #sigma/#sigma_{SM}"),
    ## is this mssm?
    mssm = cms.bool(False),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## min for plotting
    min = cms.double(-1.),
    ## max for plotting
    max = cms.double(8.), ##12
    ## min for plotting
    log = cms.int32(0),
    ## define verbosity level
    verbosity   = cms.uint32(2),
    ## Process of interest
    POI = cms.string("r_ggH"), #other options are r_qqH, r_bbH, CV, CF - just whatever you have produced
    ## define output label
    outputLabel = cms.string("sm"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(range(110, 146, 5))
)
