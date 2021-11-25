"""
Parser for Input XML file
=========================
    This is a parser
"""

class XMLObject(object):
    def __init__(self, args: dict):
        self.attrs = args
        self.childs = []
        self.level = 0

    def add_child(self, child):
        self.childs.append(child)
        child.level = self.level + 1

    def __str__(self):
        if self.attrs:
            attr = " "+" ".join([f'{key}="{val}"' for key, val in self.attrs.items()])
            balise = "\t"*self.level+f"<{self.__class__.__name__}{attr}"
        else:
            balise = "\t"*self.level+f"<{self.__class__.__name__}"
        if self.childs:
            res = "\n".join([balise+">"]+[child.__str__() for child in self.childs]+["\t"*self.level+f"</{self.__class__.__name__}>"])
        else:
            res = balise + "/>"
        return res


class ROOT_SYMUBRUIT(XMLObject):
    def __init__(self, xmlnsxsi="http://www.w3.org/2001/XMLSchema-instance", xsi_noNamespaceSchemaLocation="reseau.xsd", version="2.05"):
        super(ROOT_SYMUBRUIT, self).__init__({"xmlns:xsi":xmlnsxsi, "xsi:noNamespaceSchemaLocation":xsi_noNamespaceSchemaLocation, "version": version})


class PLAGES_TEMPORELLES(XMLObject):
    def __init__(self, debut, type):
        super(PLAGES_TEMPORELLES, self).__init__({"debut": debut, "type": type})


class PLAGE_TEMPORELLE(XMLObject):
    def __init__(self, id, debut, fin):
        super(PLAGE_TEMPORELLE, self).__init__({"id": id, "debut": debut, "fin": fin})


class SIMULATIONS(XMLObject):
    def __init__(self):
        super(SIMULATIONS, self).__init__({})


class SIMULATION(XMLObject):
    def __init__(self, id, pasdetemps, debut, fin, loipoursuite='exact', comportementflux="iti", date="1985-01-17", titre="", proc_decelation="false", seed="1"):
        super(SIMULATION, self).__init__(dict(id=id, pasdetemps=pasdetemps, debut=debut, fin=fin, loipoursuite=loipoursuite,
                                              comportementflux=comportementflux, date=date, titre=titre, proc_decelation=proc_decelation,
                                              seed=seed))


class RESTITUTION(XMLObject):
    def __init__(self, trace_route="false", trajectoires="true", debug="false", debug_matrice_OD="false", debug_SAS="false"):
        super(RESTITUTION, self).__init__(dict(trace_route=trace_route, trajectoires=trajectoires, debug=debug,
                                               debug_matrice_OD=debug_matrice_OD, debug_SAS=debug_SAS))


if __name__ == "__main__":

    root = ROOT_SYMUBRUIT()

    plage = PLAGES_TEMPORELLES("06:00:00", "horaire")
    root.add_child(plage)
    plage.add_child(PLAGE_TEMPORELLE("P01", "06:00:00", "07:00:00"))
    plage.add_child(PLAGE_TEMPORELLE("P02", "07:00:00", "08:00:00"))

    sims = SIMULATIONS()
    root.add_child(sims)

    sim = SIMULATION("simID", "1", "06:00:00", "07:00:00")
    sims.add_child(sim)
    sim.add_child(RESTITUTION())

    print(root)