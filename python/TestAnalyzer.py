__author__ = 'sbrochet'

from Core.Analyzer import Analyzer
from Models.Candidates import Candidates

from ROOT.Math import LorentzVector

class TestAnalyzer(Analyzer):
    def __init__(self, **kwargs):
        Analyzer.__init__(self)

        self.z = self.produces(Candidates, 'z', 'z_candidate_')

        # Since Jets producer already registers this collection, 'jet' will be set as an alias of 'jets'
        self.uses('vertices', 'std::vector<reco::Vertex>', kwargs['vertex_collection'])
        self.uses('jets', 'std::vector<pat::Jet>', kwargs['jet_collection'])
        self.uses('muons', 'std::vector<pat::Muon>', kwargs['muon_collection'])
        self.uses('electrons', 'std::vector<pat::Electron>', kwargs['electron_collection'])
        self.uses('mets', 'std::vector<pat::MET>', kwargs['met_collection'])

    def beginJob(self):
        print("Begin job!")
        pass

    def analyze(self, event, products):
        print("Analyzing event!")

        print "The event contain:", len(event.vertices), 'vertices', len(event.jets), 'jets', len(event.muons), 'muons', len(event.electrons), 'electrons', len(event.mets), 'mets'
        if len(event.muons) >= 2:
            p4 = event.muons[0].p4() + event.muons[1].p4()
            products.z.p4.push_back(LorentzVector('ROOT::Math::PtEtaPhiE4D<float>')(p4.Pt(), p4.Eta(), p4.Phi(), p4.E()))

        # Access product produced by the Jets producer
        for z in products.z.p4:
            print "Z candidate mass:", z.M()
        print products.jets.pu_jet_id[0]

    def endJob(self):
        print("End job!")
