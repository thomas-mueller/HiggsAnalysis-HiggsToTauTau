
import ROOT

import math

class mssm_xsec_tools():

    def __init__(self, inputFileName):
        self.inputFileName_ = inputFileName
        self.inputFile_ = ROOT.TFile(self.inputFileName_)
        self.unit_pb = 1.
        self.unit_fb = self.unit_pb*1.e-3

    @staticmethod
    def _add_in_quadrature(*xs):
        return math.sqrt(sum(x*x for x in xs))

    def lookup_value(self, parameter1, tan_beta, histo):
        try:
            histo = self.inputFile_.Get(histo)
            bin = histo.FindBin(parameter1, tan_beta)
            return histo.GetBinContent(bin)
        except AttributeError:
            print "Failed to load histogram '%s' from file %s !!" % (histo, inputFileName_)

    @staticmethod
    def santander_matching(mass, xsec_4f, xsec_5f):
        t = ROOT.TMath.Log(mass/4.75) - 2.0
        return (1.0/(1.0 + t))*(xsec_4f + t*xsec_5f)

    @staticmethod
    def santander_error_matching(mass, x_4f, x_5f):
        t = ROOT.TMath.Log(mass/4.75) - 2.0
        return (1.0/(1.0 + t))*(x_4f + t*x_5f)

    def _add_br_htt(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR-tautau'] = self.lookup_value(parameter1, tan_beta, "h_brtautau_%s" % type)

    def _add_br_hmm(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for A/H/h->mumu"
        # Unpack
        type, type_info = input
        type_info['BR-mumu'] = self.lookup_value(parameter1, tan_beta, "h_brmumu_%s" % type)

    def _add_br_hbb(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for A/H/h->bb"
        # Unpack
        type, type_info = input
        type_info['BR-bb'] = self.lookup_value(parameter1, tan_beta, "h_brbb_%s" % type)

    def _add_br_Hhh(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for A/H/h->bb"
        # Unpack
        type, type_info = input
        type_info['BR-hh'] = self.lookup_value(parameter1, tan_beta, "h_brh0h0_%s" % type)

    def _add_br_AZh(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for A/H/h->bb"
        # Unpack
        type, type_info = input
        type_info['BR-Zh'] = self.lookup_value(parameter1, tan_beta, "h_brZh0_%s" % type)

    def _add_br_tHpb(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for t->Hp+b"
        # Unpack
        type, type_info = input
        type_info['BR-tHpb'] = self.lookup_value(parameter1, tan_beta, "h_brHpb_t")

    def _add_br_taunu(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for Hp->tau+nu"
        # Unpack
        type, type_info = input
        print parameter1, tan_beta, self.lookup_value(parameter1, tan_beta, "h_brtaunu_%s" % type)
        type_info['BR-taunu'] = self.lookup_value(parameter1, tan_beta, "h_brtaunu_%s" % type)

    def _add_mass(self, parameter1, tan_beta, input):
        " Lookup the mass for a given higgs type "
        type, type_info = input
        if type == 'A':
            if self.inputFileName_.find('lowmH')>-1 :
                type_info['mass'] = self.lookup_value(parameter1, tan_beta, "h_m%s" % type)
                return
            else :
                type_info['mass'] = parameter1
                return
        type_info['mass'] = self.lookup_value(parameter1, tan_beta, "h_m%s" % type)

    def _add_xsec(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('xsec', {})
        for prod_type, unit in [ ('ggF', self.unit_pb), ('bbH', self.unit_pb), ('bbH4f', self.unit_pb) ]:
            type_info['xsec'][prod_type] = unit*self.lookup_value(parameter1, tan_beta, "h_%s_xsec_%s" % (prod_type, type))

    def _add_santander(self, input):
        # Type gives Higgs type
        type, type_info = input
        mass_of_this_type = type_info['mass']
        xsec_4f = type_info['xsec']['bbH4f']
        xsec_5f = type_info['xsec']['bbH']
        type_info['xsec']['santander'] = mssm_xsec_tools.santander_matching(mass_of_this_type, xsec_4f, xsec_5f)

        # Add errors.
        mu_up_4f = type_info['mu']['bbH4f'][1]
        mu_up_5f = type_info['mu']['bbH'][1]
        pdf_up_5f = type_info['pdf']['bbH'][1]
        
        mu_down_4f = type_info['mu']['bbH4f'][-1]
        mu_down_5f = type_info['mu']['bbH'][-1]
        pdf_down_5f = type_info['pdf']['bbH'][-1]

        # Separate uncertainties
        type_info['mu']['santander'] = {
            0 : 0,
            1 : mssm_xsec_tools.santander_error_matching(
                mass_of_this_type, mu_up_4f, mu_up_5f),
            -1 : mssm_xsec_tools.santander_error_matching(
                mass_of_this_type, mu_down_4f, mu_down_5f),
        }

        # CV: Apply PDF uncertainty to 5 flavor calculation only
        #     as in C++ version https://twiki.cern.ch/twiki/pub/LHCPhysics/MSSMNeutral/mssm_xs_tools.C
        #    (functions 'GiveXsec_UncDown_Santander_A', 'GiveXsec_UncDown_Santander_H', 'GiveXsec_UncDown_Santander_h')
        t = ROOT.TMath.Log(mass_of_this_type/4.75) - 2.0
        type_info['pdf']['santander'] = {
            0 : 0,
            1 : (1.0/(1.0 + t))*pdf_up_5f,
            -1 : (1.0/(1.0 + t))*pdf_down_5f
        }

    def _add_muHp(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('mu', {})
        type_info['mu']['HpHp'] = {
            -1 : float(0.21),
            +1 : float(0.21),
            0 : 0,
            }
        type_info['mu']['HpW'] = {
            -1 : float(0.21),
            +1 : float(0.21),
            0 : 0,
            }

    def _add_mu(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('mu', {})
        if(self.inputFileName_.find('7TeV')>-1 or self.inputFileName_.find('8TeV')>-1 ) :
            if(self.inputFileName_.find('mhmax-mu+200')>-1) : #for old mhmax scenario not produced with sushi
                type_info['mu']['bbH'] = {
                    -1 : self.lookup_value(parameter1, tan_beta, 'h_bbH_mudown_%s' % type)*self.unit_pb,
                    +1 : self.lookup_value(parameter1, tan_beta, 'h_bbH_muup_%s' % type)*self.unit_pb,
                    0 : 0,
                    }
            else :
                type_info['mu']['bbH'] = {
                    -1 : (self.lookup_value(parameter1, tan_beta, 'h_bbH_mudown_%s' % type) -
                          self.lookup_value(parameter1, tan_beta, 'h_bbH_xsec_%s' % type))*self.unit_pb,
                    +1 : (self.lookup_value(parameter1, tan_beta, 'h_bbH_muup_%s' % type) -
                          self.lookup_value(parameter1, tan_beta, 'h_bbH_xsec_%s' % type))*self.unit_pb,
                    0 : 0,
                    }
            type_info['mu']['ggF'] = {
                -1 : (self.lookup_value(parameter1, tan_beta, 'h_ggF_xsec20_%s' % type) -
                      self.lookup_value(parameter1, tan_beta, 'h_ggF_xsec_%s' % type))*self.unit_pb,
                +1 : (self.lookup_value(parameter1, tan_beta, 'h_ggF_xsec05_%s' % type) -
                      self.lookup_value(parameter1, tan_beta, 'h_ggF_xsec_%s' % type))*self.unit_pb,
                0 : 0,
                }
        else:
            type_info['mu']['bbH'] = {
                -1 : (self.lookup_value(parameter1, tan_beta, 'h_bbH_xsecDown_%s' % type) -
                      self.lookup_value(parameter1, tan_beta, 'h_bbH_xsec_%s' % type))*self.unit_pb,
                +1 : (self.lookup_value(parameter1, tan_beta, 'h_bbH_xsecUp_%s' % type) -
                      self.lookup_value(parameter1, tan_beta, 'h_bbH_xsec_%s' % type))*self.unit_pb,
                0 : 0,
                }
            type_info['mu']['ggF'] = {
                -1 : (self.lookup_value(parameter1, tan_beta, 'h_ggF_xsecDown_%s' % type) -
                      self.lookup_value(parameter1, tan_beta, 'h_ggF_xsec_%s' % type))*self.unit_pb,
                +1 : (self.lookup_value(parameter1, tan_beta, 'h_ggF_xsecUp_%s' % type) -
                      self.lookup_value(parameter1, tan_beta, 'h_ggF_xsec_%s' % type))*self.unit_pb,
                0 : 0,
                }

        type_info['mu']['bbH4f'] = {
            -1 : (self.lookup_value(parameter1, tan_beta, 'h_bbH4f_xsec_%s_low' % type) -
                  self.lookup_value(parameter1, tan_beta, 'h_bbH4f_xsec_%s' % type))*self.unit_pb,
            +1 : (self.lookup_value(parameter1, tan_beta, 'h_bbH4f_xsec_%s_high' % type) -
                  self.lookup_value(parameter1, tan_beta, 'h_bbH4f_xsec_%s' % type))*self.unit_pb,
            0 : 0,
            }
            
            


    def _add_pdf(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('pdf', {})
        if(self.inputFileName_.find('7TeV')>-1 or self.inputFileName_.find('8TeV')>-1 ) :
            if(self.inputFileName_.find('mhmax-mu+200')>-1) : #for old mhmax scenario not produced with sushi
                type_info['pdf']['bbH'] = {
                    -1 : self.lookup_value(parameter1, tan_beta, 'h_bbH_pdfalphas68down_%s' % type)*self.unit_pb,
                    +1 : self.lookup_value(parameter1, tan_beta, 'h_bbH_pdfalphas68up_%s'   % type)*self.unit_pb,
                    0 : 0,
                    }
            else :
                bbH_alphasdown = self.lookup_value(parameter1, tan_beta, 'h_bbH_pdfalphas68down_%s' % type)
                bbH_pdfdown = self.lookup_value(parameter1, tan_beta, 'h_bbH_pdf68down_%s' % type)
                
                bbH_alphasup = self.lookup_value(parameter1, tan_beta, 'h_bbH_pdfalphas68up_%s' % type)
                bbH_pdfup = self.lookup_value(parameter1, tan_beta, 'h_bbH_pdf68up_%s' % type)
                
                type_info['pdf']['bbH'] = {               
                    -1 : mssm_xsec_tools._add_in_quadrature(bbH_alphasdown, bbH_pdfdown)*self.unit_pb,
                    +1 : mssm_xsec_tools._add_in_quadrature(bbH_alphasup, bbH_pdfup)*self.unit_pb,
                    0 : 0,
                    }
            
            ggF_alphasdown = self.lookup_value(parameter1, tan_beta, 'h_ggF_alphasdown_%s' % type)
            ggF_pdfdown = self.lookup_value(parameter1, tan_beta, 'h_ggF_pdfdown_%s' % type)
            
            ggF_alphasup = self.lookup_value(parameter1, tan_beta, 'h_ggF_alphasup_%s' % type)
            ggF_pdfup = self.lookup_value(parameter1, tan_beta, 'h_ggF_pdfup_%s' % type)
            
            type_info['pdf']['ggF'] = {
                -1 : mssm_xsec_tools._add_in_quadrature(ggF_alphasdown, ggF_pdfdown)*self.unit_pb,
                +1 : mssm_xsec_tools._add_in_quadrature(ggF_alphasup, ggF_pdfup)*self.unit_pb,
                0 : 0,
                }
            
        else :
            type_info['pdf']['bbH'] = {               
                -1 : self.lookup_value(parameter1, tan_beta, 'h_bbH_pdfalphasDown_%s' % type),
                +1 : self.lookup_value(parameter1, tan_beta, 'h_bbH_pdfalphasUp_%s' % type),
                0 : 0,
                }
            type_info['pdf']['ggF'] = {
                -1 : self.lookup_value(parameter1, tan_beta, 'h_ggF_pdfalphasDown_%s' % type),
                +1 : self.lookup_value(parameter1, tan_beta, 'h_ggF_pdfalphasUp_%s' % type),
                0 : 0,
                }
        
        # Supposedly negligble compared to scale
        type_info['pdf']['bbH4f'] = {
               -1 : 0,
               +1 : 0,
               0 : 0,
               }


    def query(self, parameter1, tan_beta, ana_type): #parameter1 = mu in case of lowmH and mA in all other scenarios 
        
        output = {}
        
        if ana_type=='Htaunu' :
            higgs_types = [ 'Hp' ]
         
            # Build emtpy dictionaries for each Higgs type
            output = {
                'parameter1' : parameter1,
                'tan_beta' : tan_beta,
                'higgses' : {
                    'Hp' : {}
                    }
                }
         
            for higgs_type in higgs_types:
                self._add_mass(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_br_tHpb(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_br_taunu(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                #self._add_xsec(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_muHp(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                
        else :
            higgs_types = [ 'h', 'A', 'H' ]
            
            # Build emtpy dictionaries for each Higgs type
            output = {
                'parameter1' : parameter1,
                'tan_beta' : tan_beta,
                'higgses' : {
                    'h' : {},
                    'A' : {},
                    'H' : {}
                    }
                }
            for higgs_type in higgs_types:
                self._add_br_htt(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_br_hmm(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_br_hbb(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                if ana_type=='Hhh' or ana_type=='AZh' :
                    self._add_br_Hhh(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                    self._add_br_AZh(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_mass(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_xsec(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_mu(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_pdf(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_santander((higgs_type, output['higgses'][higgs_type]))
            

        print output
        return output
    
