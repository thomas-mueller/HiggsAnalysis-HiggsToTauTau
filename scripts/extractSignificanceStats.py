#!/usr/bin/env python

import ROOT
from ROOT import *
import math
import os
import string
import numpy as n

ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]", description="This script extracts all the necessary information needed for the tanb-mA(mu) plot of the MSSMvsSM and for MSSMvsBG. For MSSMvsSM it also plots the toy distributions for the MSSM and the SM hypothesis as well as the observed value of the test statistic. \n")
##
## MAIN OPTIONS
##
agroup = OptionGroup(parser, "OPTIONS", "These are the possible options")
agroup.add_option("-v", "--verbosity", dest="verbosity", default=False, action="store_true",
                  help="Prints out information. [Default: False]")
agroup.add_option("--filename", dest="filename", default="", type="string",
                  help="Name of the file to be inspected. [Default: ""] ")
agroup.add_option("--MSSMvsBG", dest="MSSMvsBG", default=False, action="store_true",
                  help="Caculations for MSSMvsBG. Default is MSSMvsSM [Default: false")
parser.add_option_group(agroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
#if len(args) < 1 :
#    parser.print_usage()
#    exit(1)



if options.MSSMvsBG :
    
    gROOT.ProcessLine(
        "struct staff_t {\
        Float_t quantileExpected;\
        Float_t mh;\
        Double_t limit;\
        }" )

    tanb=options.filename.lstrip("point_").rstrip(".root")
    print tanb
    file = ROOT.TFile(options.filename, 'r')
    #file.ls()
    tree = file.Get("limit")
    staff = staff_t()
    tree.SetBranchAddress("quantileExpected",AddressOf(staff,"quantileExpected"));
    tree.SetBranchAddress("mh",AddressOf(staff,"mh"));
    tree.SetBranchAddress("limit",AddressOf(staff,"limit"));

    ###for mA-tanb plotting save everything in a root file
    f = ROOT.TFile("HypothesisTest_{TANB}.root".format(TANB=tanb), "recreate")
    t = ROOT.TTree("tree", "HypoTest")
    tanbeta    = n.zeros(1, dtype=float) 
    minus2sigma= n.zeros(1, dtype=float)
    minus1sigma= n.zeros(1, dtype=float)
    exp        = n.zeros(1, dtype=float)
    plus1sigma = n.zeros(1, dtype=float)
    plus2sigma = n.zeros(1, dtype=float)
    obs        = n.zeros(1, dtype=float)
    minus2sigma[0]=999
    minus1sigma[0]=999
    exp[0]=999
    plus1sigma[0]=999
    plus2sigma[0]=999
    obs[0]=999
    
    t.Branch('tanb',        tanbeta,     'tanb/D')
    t.Branch('minus2sigma', minus2sigma, 'minus2sigma/D')
    t.Branch('minus1sigma', minus1sigma, 'minus1sigma/D')
    t.Branch('expected',    exp,         'expected/D')
    t.Branch('plus1sigma',  plus1sigma,  'plus1sigma/D')
    t.Branch('plus2sigma',  plus2sigma,  'plus2sigma/D')
    t.Branch('observed',    obs,         'observed/D')
    
    for i in range(tree.GetEntries()) :
        tree.GetEntry(i);
        #print i, staff.limit, staff.limit/float(tanb), staff.quantileExpected
        if abs(staff.quantileExpected-0.025) < 0.01  :
            minus2sigma[0]=staff.limit/float(tanb)
        if abs(staff.quantileExpected-0.160) < 0.01  :
            minus1sigma[0]=staff.limit/float(tanb)
        if abs(staff.quantileExpected-0.500) < 0.01  :
            exp[0]=staff.limit/float(tanb)
        if abs(staff.quantileExpected-0.840) < 0.01  :
            plus1sigma[0]=staff.limit/float(tanb)
        if abs(staff.quantileExpected-0.975) < 0.01  :
            plus2sigma[0]=staff.limit/float(tanb)
        if abs(staff.quantileExpected+1.000) < 0.01  :
            obs[0]=staff.limit/float(tanb)           
    tanbeta[0]=float(tanb)
    print tanbeta[0], minus2sigma[0], minus1sigma[0], exp[0], plus1sigma[0], plus2sigma[0], obs[0]
    t.Fill()
    f.Write()
    f.Close()


else :

    gROOT.ProcessLine(
        "struct staff_t {\
        Float_t q;\
        Float_t mh;\
        Float_t weight;\
        Int_t type;\
        }" )

    tanb=options.filename.lstrip("qmu.FixedMu_").rstrip(".root")
    
    file = ROOT.TFile(options.filename, 'r')
    #file.ls()
    tree = file.Get("q")
    staff = staff_t()
    tree.SetBranchAddress("q",AddressOf(staff,"q"));
    tree.SetBranchAddress("mh",AddressOf(staff,"mh"));
    tree.SetBranchAddress("weight",AddressOf(staff,"weight"));
    tree.SetBranchAddress("type",AddressOf(staff,"type"));

    xlow=999.0
    xup=-999.0
    nbins=(tree.GetEntries()-1)*10
    for i in range(tree.GetEntries()) :
        tree.GetEntry(i);
        if xlow>staff.q :
            xlow = staff.q
        if xup<staff.q :
            xup = staff.q    

    hSM   = ROOT.TH1F("hSM  ;S = -2 #times ln(L_{1}/L_{2});Number of Toys","",nbins,xlow-xlow/100,xup+xup/100)
    hMSSM = ROOT.TH1F("hMSSM;S = -2 #times ln(L_{1}/L_{2});Number of Toys","",nbins,xlow-xlow/100,xup+xup/100)
    hObs  = ROOT.TH1F("hObserved"                                         ,"",nbins,xlow-xlow/100,xup+xup/100);

    if options.verbosity :
        print "Start to loop on tree in file", options.filename
       
    v_SM   = []
    v_MSSM = []
    v_Obs  = []

    for i in range(tree.GetEntries()) :
        tree.GetEntry(i);
        if i==0 :
            if options.verbosity :
                print "MASS in the TREE =", staff.mh, staff.type
        if staff.type<0 : #SM Hypothesis ist eigentlicht <0 ?
            hSM.Fill(staff.q)
            v_SM.append(staff.q)
        elif staff.type>0 : #MSSM Hypothesis ist eigentlic >0 ?
            hMSSM.Fill(staff.q)
            v_MSSM.append(staff.q)
        else :
            if options.verbosity :
                print "observed:", staff.q
            hObs.Fill(staff.q)
            v_Obs.append(staff.q)       
    if options.verbosity :
        print "Finished to loop, sorting vectors"   
    v_SM.sort()
    v_MSSM.sort()
    v_Obs.sort()
    ntoysSM=int(hSM.GetEntries());
    ntoysMSSM=int(hMSSM.GetEntries());

    ##we assume that MSSM is on the right and SM on the left of zero
    #if v_MSSM[0]<v_SM[ntoysSM-1] :
    #    print "Swapped distributions!!! The alternative model should stay on the negative side of the significance."
    #    print "Please edit the code and change the sign of q when filling histos and vectors in the loop on tree entries"
    #    exit(1)

    ### caculation of CLs with binned histo
    medianSM=v_SM[int(ntoysSM/2)]
    medianMSSM=v_MSSM[int(ntoysMSSM/2)]
    medianObs=v_Obs[int(hObs.GetEntries()/2)]
    if options.verbosity :
        print "Toys generated for SM/MSSM:", ntoysSM, ntoysMSSM
        print "Mean of SM/MSSM hypothesis:", hSM.GetMean(), hMSSM.GetMean()
        print "RMS of SM/MSSM hypothesis:", hSM.GetRMS(), hMSSM.GetRMS()
        print "Median of SM/MSSM hypotheses:", medianSM, medianMSSM
        print "Median of observed", medianObs #, v_Obs[0]

    integralSM=hSM.Integral()
    integralMSSM=hMSSM.Integral()

    plus_one_sigma_bin=0
    minus_one_sigma_bin=0
    plus_two_sigma_bin=0
    minus_two_sigma_bin=0
    help=0
    for i in xrange(1, nbins) :
        binVal = hSM.GetBinContent(i)
        help += binVal/integralSM
        if help > 0.975 and plus_two_sigma_bin == 0 :
            plus_two_sigma_bin=i
        if help > 0.84 and plus_one_sigma_bin == 0 :
            plus_one_sigma_bin=i
        if help > 0.16 and minus_one_sigma_bin == 0 :
            minus_one_sigma_bin=i
        if help > 0.025 and minus_two_sigma_bin == 0 :
            minus_two_sigma_bin=i
    if options.verbosity :
        print "bins of -2 -1 median +1 +2 for hSM", minus_two_sigma_bin, minus_one_sigma_bin, hSM.FindBin(medianSM), plus_one_sigma_bin, plus_two_sigma_bin

    tailSMminus2sigma  =hSM.Integral  (1,minus_two_sigma_bin)
    tailMSSMminus2sigma=hMSSM.Integral(1,minus_two_sigma_bin)
    
    tailSMminus1sigma  =hSM.Integral  (1,minus_one_sigma_bin)
    tailMSSMminus1sigma=hMSSM.Integral(1,minus_one_sigma_bin)

    tailSMexp          =hSM.Integral  (1,hSM.FindBin(medianSM))
    tailMSSMexp        =hMSSM.Integral(1,hMSSM.FindBin(medianSM))
    
    tailSMplus1sigma   =hSM.Integral  (1,plus_one_sigma_bin)
    tailMSSMplus1sigma =hMSSM.Integral(1,plus_one_sigma_bin)
    
    tailSMplus2sigma   =hSM.Integral  (1,plus_two_sigma_bin)
    tailMSSMplus2sigma =hMSSM.Integral(1,plus_two_sigma_bin)
    
    tailSMobs          =hSM.Integral  (1,hObs.FindBin(medianObs))
    tailMSSMobs        =hMSSM.Integral(1,hObs.FindBin(medianObs))

    if options.verbosity :
        print "RESULT WITH BINNED HISTO"
        print "tailSMexp", tailSMexp, "  tailMSSMexp", tailMSSMexp, "  tailSMobs", tailSMobs, "  tailMSSMobs", tailMSSMobs
        print "-2 sigma separation power", tailMSSMminus2sigma/tailSMminus2sigma
        print "-1 sigma separation power", tailMSSMminus1sigma/tailSMminus1sigma
        print "Expected separation power", tailMSSMexp/tailSMexp
        print "+1 sigma separation power", tailMSSMplus1sigma/tailSMplus1sigma
        print "+2 sigma separation power", tailMSSMplus2sigma/tailSMplus2sigma
        print "Observed separation power", tailMSSMobs/tailSMobs


    ### Rebinning needed for plotting and fitting
    hSM.Rebin(100)
    hMSSM.Rebin(100)

    ### caculation of CLs with gaus fit to binned histo
    ## hSM.Fit("gaus")
    ## fitSM = ROOT.TF1(hSM.GetFunction("gaus"))
    ## chi2SM = fitSM.GetChisquare()
    ## if options.verbosity :
    ##     print "chi2 of hSM", chi2SM, "mean of fitSM", fitSM.GetParameter(1), "sigma of fitSM", fitSM.GetParameter(2)

    #par= n.zeros(6, dtype=float)
    #g1    = ROOT.TF1("g1","gaus",(xlow-xlow/100)/100,(xup+xup/100)/100);
    #g2    = ROOT.TF1("g2","gaus",(xlow-xlow/100)/100,(xup+xup/100)/100);
    #total = ROOT.TF1("total","gaus(0)+gaus(3)",(xlow-xlow/100)/100,(xup+xup/100)/100);
    #total.SetLineColor(2);
    #hMSSM.Fit(g1,"R");
    #hMSSM.Fit(g2,"R+");
    #g1.GetParameters(par[0]);
    #g2.GetParameters(par[3]);
    #total.SetParameters(par);
    #hMSSM.Fit(total,"R+");

    #DoubleGauss = ROOT.TF1("DG","[0]*exp(-0.5*((x-[1])/[2])**2)+[3]*exp(-0.5*((x-[4])/[5])**2)",(xlow-xlow/100)/100,(xup+xup/100)/100)
    #DoubleGauss.SetLineColor(2)
    #hMSSM.Fit(DoubleGauss, "R")

    #hMSSM.Fit("gaus")
    #fitMSSM = ROOT.TF1(hMSSM.GetFunction("gaus"))
    ##fitMSSM = ROOT.TF1(hMSSM.GetFunction("[0]*exp(-0.5*((x-[1])/[2])**2)+[3]*exp(-0.5*((x-[4])/[5])**2)")) 
    #chi2MSSM = fitMSSM.GetChisquare()
    #if options.verbosity :
    #    print "chi2 of hMSSM", chi2MSSM, "mean of fitMSSM", fitMSSM.GetParameter(1), "sigma of fitMSSM", fitMSSM.GetParameter(2)

    ## tailSMminus2sigma  =fitSM.Integral  (xlow-xlow/100,fitSM.GetParameter(1)-2*fitSM.GetParameter(2))
    ## tailMSSMminus2sigma=fitMSSM.Integral(xlow-xlow/100,fitSM.GetParameter(1)-2*fitSM.GetParameter(2))

    ## tailSMminus1sigma  =fitSM.Integral  (xlow-xlow/100,fitSM.GetParameter(1)-1*fitSM.GetParameter(2))
    ## tailMSSMminus1sigma=fitMSSM.Integral(xlow-xlow/100,fitSM.GetParameter(1)-1*fitSM.GetParameter(2))

    ## tailSMexp          =fitSM.Integral  (xlow-xlow/100,fitSM.GetParameter(1))
    ## tailMSSMexp        =fitMSSM.Integral(xlow-xlow/100,fitSM.GetParameter(1))

    ## tailSMplus1sigma   =fitSM.Integral  (xlow-xlow/100,fitSM.GetParameter(1)+1*fitSM.GetParameter(2))
    ## tailMSSMplus1sigma =fitMSSM.Integral(xlow-xlow/100,fitSM.GetParameter(1)+1*fitSM.GetParameter(2))

    ## tailSMplus2sigma   =fitSM.Integral  (xlow-xlow/100,fitSM.GetParameter(1)+2*fitSM.GetParameter(2))
    ## tailMSSMplus2sigma =fitMSSM.Integral(xlow-xlow/100,fitSM.GetParameter(1)+2*fitSM.GetParameter(2))

    ## tailSMobs          =fitSM.Integral  (xlow-xlow/100,medianObs)
    ## tailMSSMobs        =fitMSSM.Integral(xlow-xlow/100,medianObs)

    ## if options.verbosity :
    ##     print "RESULT WITH GAUS FITTED TO BINNED HISTO"
    ##     print "tailSMexp", tailSMexp, "  tailMSSMexp", tailMSSMexp, "  tailSMobs", tailSMobs, "  tailMSSMobs", tailMSSMobs
    ##     print "-2 sigma separation power", tailMSSMminus2sigma/tailSMminus2sigma
    ##     print "-1 sigma separation power", tailMSSMminus1sigma/tailSMminus1sigma
    ##     print "Expected separation power", tailMSSMexp/tailSMexp
    ##     print "+1 sigma separation power", tailMSSMplus1sigma/tailSMplus1sigma
    ##     print "+2 sigma separation power", tailMSSMplus2sigma/tailSMplus2sigma
    ##     print "Observed separation power", tailMSSMobs/tailSMobs


    ###for mA-tanb plotting save everything in a root file
    f = ROOT.TFile("HypothesisTest_{TANB}.root".format(TANB=tanb), "recreate")
    t = ROOT.TTree("tree", "HypoTest")
    tanbeta    = n.zeros(1, dtype=float)
    minus2sigma= n.zeros(1, dtype=float)
    minus1sigma= n.zeros(1, dtype=float)
    exp        = n.zeros(1, dtype=float)
    plus1sigma = n.zeros(1, dtype=float)
    plus2sigma = n.zeros(1, dtype=float)
    obs        = n.zeros(1, dtype=float)
    t.Branch('tanb',        tanbeta,     'tanb/D')
    t.Branch('minus2sigma', minus2sigma, 'minus2sigma/D')
    t.Branch('minus1sigma', minus1sigma, 'minus1sigma/D')
    t.Branch('expected',    exp,         'expected/D')
    t.Branch('plus1sigma',  plus1sigma,  'plus1sigma/D')
    t.Branch('plus2sigma',  plus2sigma,  'plus2sigma/D')
    t.Branch('observed',    obs,         'observed/D')
    tanbeta[0]=float(tanb)
    minus2sigma[0]=float(tailMSSMminus2sigma/tailSMminus2sigma)
    minus1sigma[0]=float(tailMSSMminus1sigma/tailSMminus1sigma)
    exp[0]        =float(tailMSSMexp/tailSMexp)
    plus1sigma[0] =float(tailMSSMplus1sigma/tailSMplus1sigma)
    plus2sigma[0] =float(tailMSSMplus2sigma/tailSMplus2sigma)
    obs[0]        =float(tailMSSMobs/tailSMobs)
    t.Fill()
    f.Write()
    f.Close()


    ### Output file containing number of toys so one does not have to look up all the plots
    numberToys = open("numberToys_{MASS}_{TANB}.out".format(MASS=int(staff.mh), TANB=tanb), 'w')
    numberToys.write("{MASS} {TANB} {NTOYS}".format(MASS=int(staff.mh), TANB=tanb, NTOYS=ntoysMSSM))
    numberToys.close()
    

    ###Fancy plot
    gStyle.SetOptStat(0)
    c2 = ROOT.TCanvas("c2","c2",800,800)
    c2.cd()
    hSM.SetXTitle("S = -2 #times ln(L_{1}/L_{2})")
    hSM.SetYTitle("Generated experiments")
    hMSSM.SetXTitle("S = -2 #times ln(L_{1}/L_{2})")
    hMSSM.SetYTitle("Generated experiments")
    hSM.SetLineColor(kMagenta-3)
    hSM.SetFillColor(kMagenta-3)
    hSM.SetLineWidth(2)
    hSM.SetFillStyle(3605)
    hMSSM.SetLineColor(kBlue+1)
    hMSSM.SetFillColor(kBlue+1)
    hMSSM.SetLineWidth(2)
    hMSSM.SetFillStyle(3695)
    hObs.SetLineColor(kBlack)
    hObs.SetLineWidth(2)
    hSM.Draw()
    hMSSM.Draw("sames")
    hObs.Draw("sames")
    ##how to draw at the right position an arrow at the x-axis?
    ##TArrow ar5(0.4,0.25,0.95,0.25,0.15,"|>")
    ##ar5.SetAngle(60)
    ##ar5.SetLineWidth(4)
    ##ar5.SetLineColor(4)
    ##ar5.SetFillColor(2)
    ##ar5.Draw()

    leg = ROOT.TLegend(0.12,0.7,0.3,0.88)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.AddEntry(hSM,  "  SM","f")
    leg.AddEntry(hMSSM,"  MSSM","f")
    leg.Draw()


    pt = ROOT.TPaveText(0.16,0.95,0.45,0.99,"NDC")
    pt.SetFillColor(0)
    pt.AddText("CMS Private")
    pt.SetBorderSize(0)
    pt2 = ROOT.TPaveText(0.45,0.95,0.89,0.99,"NDC")
    pt2.SetFillColor(0)
    pt2.AddText(" #sqrt{s} = 7 TeV, L = 4.9 fb^{-1}; #sqrt{s} = 8 TeV, L = 19.7 fb^{-1}")
    pt2.SetBorderSize(0)
    pt3 = ROOT.TPaveText(0.45,0.90,0.90,0.94,"NDC")
    pt3.SetFillColor(0)
    pt3.AddText(" mA = {MASS} GeV,  tanb = {TANB},   ntoys = {NTOYS}".format(MASS=staff.mh, TANB=tanb, NTOYS=ntoysMSSM))
    pt3.SetBorderSize(0)
    pt.Draw()
    pt2.Draw()
    pt3.Draw()
    c2.SaveAs("sigsep_"+tanb+".png")
    c2.SaveAs("sigsep_"+tanb+".pdf")
    #c2.SaveAs("sigsep_"+tanb+".root")

    #fitSM.Delete()
    #fitMSSM.Delete()





