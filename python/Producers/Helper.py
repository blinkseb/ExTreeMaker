__author__ = 'sbrochet'

import math

from Core import Classes

def fill_candidate(candidate, product):
    """
    Fill values from candidate into the product
    :param candidate: a candidate
    :param Models.Candidates.Candidates product: the product to fill
    :return:
    """
    p4 = Classes.LorentzVector(candidate.pt(), candidate.eta(), candidate.phi(),
                                                         candidate.energy())
    product.p4.push_back(p4)
    product.y.push_back(candidate.rapidity())
    product.charge.push_back(candidate.charge())

    gen = candidate.genParticle()
    if gen:
        product.has_matched_gen_particle.push_back(True)
        p4 = Classes.LorentzVector(gen.pt(), gen.eta(), gen.phi(), gen.energy())
        product.gen_p4.push_back(p4)
        product.gen_y.push_back(gen.rapidity())
        product.gen_charge.push_back(gen.charge())
    else:
        product.has_matched_gen_particle.push_back(False)
        product.gen_p4.push_back(Classes.LorentzVector())
        product.gen_y.push_back(0)
        product.gen_charge.push_back(0)


def fill_isolations(candidate, cone_size, chargedHadronIso, neutralHadronIso, photonIso, puIso, rho, eta, EA, product):
    """

    :param candidate:
    :param cone_size: The cone size. Can be "R04" or "R03"
    :param chargedHadronIso:
    :param neutralHadronIso:
    :param photonIso:
    :param puIso:
    :param rho:
    :param eta:
    :param EA:
    :param product:
    :return:
    """

    def get_product(name):
        return getattr(product, "%s%s" % (name, cone_size)) if "%s" not in name else getattr(product, name % cone_size)

    get_product("chargedHadronIso").push_back(chargedHadronIso)
    get_product("neutralHadronIso").push_back(neutralHadronIso)
    get_product("photonIso").push_back(photonIso)

    get_product("relativeIso").push_back((chargedHadronIso + neutralHadronIso + photonIso) / candidate.pt())
    get_product("relativeIso%s_deltaBeta").push_back(
        (chargedHadronIso + max((neutralHadronIso + photonIso) - 0.5 * puIso, 0.0)) / candidate.pt())

    if EA is not None:
        eta = math.fabs(eta)
        ea_value = EA.get(eta)
        if ea_value is not None:
            get_product("effectiveArea").push_back(ea_value)
            get_product("relativeIso%s_withEA").push_back(
                (chargedHadronIso + max((neutralHadronIso + photonIso) - rho * ea_value, 0.0)) / candidate.pt())
        else:
            get_product("effectiveArea").push_back(-1)  # Not available
            get_product("relativeIso%s_withEA").push_back(-1)  # Not available
    else:
        get_product("effectiveArea").push_back(-1)  # Not available
        get_product("relativeIso%s_withEA").push_back(-1)  # Not available
