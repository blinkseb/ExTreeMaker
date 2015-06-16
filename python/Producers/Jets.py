__author__ = 'sbrochet'

import Models.Jets
from Producer import Producer

import Core.Configuration
from Core import Classes

from Helper import fill_candidate

class Jets(Producer):

    def __init__(self, name, prefix, jet_collection, btag_collections=[]):
        Producer.__init__(self, name)

        self.btag_collections = btag_collections
        self.uses(name, 'std::vector<pat::Jet>', jet_collection)
        self.produces(Models.Jets.Jets, name, prefix)

    def produce(self, event, products):
        jets = getattr(event, self._name)
        product = getattr(products, self._name)
        for jet in jets:
            fill_candidate(jet, product)

            product.jecFactor.push_back(jet.jecFactor(0))
            product.area.push_back(jet.jetArea())
            product.partonFlavor.push_back(jet.partonFlavour())
            product.hadronFlavor.push_back(jet.hadronFlavour())

            if jet.hasUserFloat('pileupJetId:fullDiscriminant'):
                product.pu_jet_id.push_back(jet.userFloat('pileupJetId:fullDiscriminant'))

            product.vtxMass.push_back(jet.userFloat('vtxMass'))

            btaggers = Classes.StringFloatMap()
            for btagger in self.btag_collections:
                btaggers[btagger] = jet.bDiscriminator(btagger)

            product.btag.push_back(btaggers)

default_configuration = Core.Configuration.Producer(name='jets', clazz=Jets, prefix='jet_',
        jet_collection='slimmedJets', btag_collections=['pfCombinedInclusiveSecondaryVertexV2BJetTags'])
