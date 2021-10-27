# ============================================================================
# STANDARD  IMPORTS
# ============================================================================

import types
import numpy as np
import os
from collections import OrderedDict, Counter
from functools import cached_property, lru_cache

# ============================================================================
# INTERNAL IMPORTS
# ============================================================================

from symupy.tsc.journey import Path, State, Trip
from symupy.tsc.network import Network
from symupy.parser.xmlparser import XMLParser
from symupy.utils.exceptions import SymupyWarning
from symupy.utils.time import Date
from symupy.abstractions.reader import AbstractNetworkReader, AbstractTrafficDataReader

# ============================================================================
# CLASS AND DEFINITIONS
# ============================================================================


class SymuFlowNetworkReader(AbstractNetworkReader):
    """Short summary.

    Parameters
    ----------
    file : type
        Description of parameter `file`.
    remove_comments : type
        Description of parameter `remove_comments`.

    Attributes
    ----------
    _file : type
        Description of attribute `_file`.
    _parser : type
        Description of attribute `_parser`.
    _prefix : type
        Description of attribute `_prefix`.
    _id : type
        Description of attribute `_id`.
    _ext : type
        Description of attribute `_ext`.

    """

    _ext = "xml"

    def __init__(self, file, remove_comments=True):
        super().__init__()

        assert file.split(".")[-1] == "xml"
        self._file = file
        self._parser = XMLParser(self._file)

        root = self._parser.get_root()
        if root.tag == "OUT":
            self._prefix = "OUT/IN"
        elif root.tag == "ROOT_SYMUBRUIT":
            self._prefix = "ROOT_SYMUBRUIT"

        self._id = self._parser.xpath(f"{self._prefix}/RESEAUX/RESEAU/@id")

    @cached_property
    def _links(self):
        return self._parser.xpath(f"{self._prefix}/RESEAUX/RESEAU/TRONCONS")

    @cached_property
    def _sensors(self):
        return self._parser.xpath(
            f"{self._prefix}/TRAFICS/TRAFIC/PARAMETRAGE_CAPTEURS/CAPTEURS"
        )

    @cached_property
    def _termination_zones(self):
        return self._parser.xpath(f"{self._prefix}/TRAFICS/TRAFIC/ZONES_DE_TERMINAISON")

    @cached_property
    def _public_transport(self):
        return self._parser.xpath(
            f"{self._prefix}/RESEAUX/RESEAU/PARAMETRAGE_VEHICULES_GUIDES/LIGNES_TRANSPORT_GUIDEES"
        )

    @cached_property
    def _repartiteur(self):
        return self._parser.xpath(
            f"{self._prefix}/RESEAUX/RESEAU/CONNEXIONS/REPARTITEURS"
        )

    @cached_property
    def _parking(self):
        return self._parser.xpath(f"{self._prefix}/TRAFICS/TRAFIC/PARKINGS")

    @cached_property
    def _carrefourfeux(self):
        return self._parser.xpath(
            f"{self._prefix}/RESEAUX/RESEAU/CONNEXIONS/CARREFOURSAFEUX"
        )

    @cached_property
    def _giratoire(self):
        return self._parser.xpath(
            f"{self._prefix}/RESEAUX/RESEAU/CONNEXIONS/GIRATOIRES"
        )

    @cached_property
    def _extremity(self):
        return self._parser.xpath(
            f"{self._prefix}/RESEAUX/RESEAU/CONNEXIONS/EXTREMITES"
        )

    def iter_links(self):
        return self._links.iterchildrens()

    def get_links(self):
        iterator = self.iter_links()
        return {tr.attr["id"]: tr.attr for tr in iterator}

    def get_network(self):
        troncons = self.iter_links()
        net = Network(self._id)
        try:
            parents = [
                ("CARREFOURAFEUX", "_carrefourfeux"),
                ("REPARTITEUR", "_repartiteur"),
                ("GIRATOIRE", "_giratoire"),
                ("EXTREMITE", "_extremity"),
                ("PARKING", "_parking"),
            ]
            for parent, prop in parents:
                [
                    net.add_node(elem.attr["id"], parent)
                    for elem in getattr(self, prop).iterchildren()
                ]

        except AttributeError:
            SymupyWarning(f"Parameter {parent} not found")
            pass

        for tr in troncons:
            net.add_link(
                tr.attr["id"],
                tr.attr["id_eltamont"],
                tr.attr["id_eltaval"],
                np.fromstring(tr.attr["extremite_amont"], sep=" "),
                np.fromstring(tr.attr["extremite_aval"], sep=" "),
            )
            if "vit_reg" in tr.attr.keys():
                net.links[tr.attr["id"]]["speed_limit"] = float(tr.attr["vit_reg"])
            internal_points = tr.find_children_tag("POINTS_INTERNES")
            if internal_points is not None:
                elt = internal_points.getchildrens()
                net.links[tr.attr["id"]]["internal_points"] = np.array(
                    [
                        np.fromstring(e.attr["coordonnees"], sep=" ")
                        for e in elt
                        if "coordonnees" in e.attr.keys()
                    ]
                )

        for id in self.info_sensors():
            net.add_sensor(id, list(self.iter_sensor(id)))

        for id in self.info_termination_zones():
            net.add_termination_zone(id, list(self.iter_termination_zones(id)))
        return net

    def nb_troncons(self):
        troncons = self._links
        size = len(troncons.getchildrens())
        return size

    def info_sensors(self):
        if self._sensors is not None:
            return {cpt.attr["id"]: cpt.tag for cpt in self._sensors.iterchildrens()}
        else:
            return dict()

    def iter_sensor(self, id):
        if self._sensors is not None:
            cpt = self._sensors.find_children_attr("id", id)
            if "troncon" in cpt.attr.keys():
                yield cpt.attr["troncon"]
                return
            else:
                troncons = cpt.find_children_tag("TRONCONS").iterchildrens()
                for tr in troncons:
                    yield tr.attr["id"]
        else:
            yield from ()

    def info_termination_zones(self):
        if self._termination_zones is not None:
            return [zn.attr["id"] for zn in self._termination_zones.iterchildrens()]
        else:
            return list()

    def iter_termination_zones(self, id):
        if self._termination_zones is not None:
            zn = self._termination_zones.find_children_attr("id", id)
            troncons = zn.find_children_tag("TRONCONS").iterchildrens()
            for tr in troncons:
                yield tr.attr["id"]
        else:
            yield from ()

    def info_public_transport(self):
        if self._public_transport is not None:
            return [pt.attr["id"] for pt in self._public_transport]
        else:
            return list()

    def iter_public_transport(self, id):
        if self._public_transport is not None:
            pt = self._public_transport.find_children_attr("id", id)
            troncons = pt.find_children_tag("TRONCONS").iterchildrens()
            for tr in troncons:
                yield tr.attr["id"]
        else:
            yield from ()


class SymuFlowTrafficDataReader(AbstractTrafficDataReader):
    """Reader for output of SymuFlow simulation.

    Parameters
    ----------
    traficdatafile : str
        Path to the SymuFlow output xml file.
    lru_cache_size : int
        Description of parameter `lru_cache_size`.

    Attributes
    ----------
    _file : type
        Description of attribute `_file`.
    parser : type
        Description of attribute `parser`.
    _inst : type
        Description of attribute `_inst`.
    _vehs : type
        Description of attribute `_vehs`.
    _get_ids_from_inst : type
        Description of attribute `_get_ids_from_inst`.
    _ext : type
        Description of attribute `_ext`.

    """

    _ext = "xml"

    def __init__(self, traficdatafile, lru_cache_size=None):
        super().__init__()
        self._file = traficdatafile
        self.parser = XMLParser(self._file)
        sim = self.parser.xpath("OUT/SIMULATION")
        for elem in sim.iterchildrens():
            if elem.tag == "INSTANTS":
                self._inst = elem
            elif elem.tag == "VEHS":
                self._vehs = elem
                break
        self._start_sim = Date(sim.attr["debut"])
        self.get_ids_from_inst = lru_cache(maxsize=lru_cache_size)(
            self._get_ids_from_inst
        )
        self.get_veh_element = lru_cache(maxsize=lru_cache_size)(self._get_veh_element)

    def _get_veh_element(self, vehid):
        return self._vehs.find_children_attr("id", str(vehid))

    def _get_states(self, vehid):
        states = list()
        for inst in self._inst.iterchildrens():
            trajs = self.get_ids_from_inst(inst)
            if vehid in trajs.keys():
                vehtraj = trajs[vehid]
                abs = float(vehtraj.attr["abs"])
                ord = float(vehtraj.attr["ord"])
                acc = float(vehtraj.attr["acc"])
                vit = float(vehtraj.attr["vit"])
                voie = int(vehtraj.attr["voie"])
                curv_pos = float(vehtraj.attr["dst"])
                tron = vehtraj.attr["tron"]
                time = Date(float(inst.attr["val"])) + self._start_sim
                states.append(
                    State(
                        time=time,
                        absolute_position=np.array([abs, ord]),
                        curvilinear_abscissa=curv_pos,
                        acceleration=acc,
                        speed=vit,
                        lane=voie,
                        link=tron,
                    )
                )
        return states

    def get_OD(self, origin, destination, start_period=None, end_period=None):
        OD = (origin, destination)
        result = list()
        if start_period is None and end_period is None:
            for el in self._vehs.iterchildrens():
                if OD == (el.attr["entree"], el.attr["sortie"]):
                    veh_el = self.get_veh_element(el.attr["id"])
                    path = Path(veh_el.attr["itineraire"].split(" "))
                    result.append(path)
        else:
            start = Date(start_period)
            end = Date(end_period)
            for el in self._vehs.iterchildrens():
                inst = (
                    Date(float(el.attr.get("instE", el.attr["instC"])))
                    + self._start_sim
                )
                if OD == (el.attr["entree"], el.attr["sortie"]) and (
                    start <= inst <= end
                ):
                    veh_el = self.get_veh_element(el.attr["id"])
                    path = Path(veh_el.attr["itineraire"].split(" "))
                    result.append(path)
        return result

    def count_OD(self, period=None):
        if period is None:
            c = Counter(
                [
                    (el.attr["entree"], el.attr["sortie"])
                    for el in self._vehs.iterchildrens()
                ]
            )
        else:
            start = Date(period[0])
            end = Date(period[1])
            c = Counter(
                [
                    (el.attr["entree"], el.attr["sortie"])
                    for el in self._vehs.iterchildrens()
                    if start
                    <= Date(float(el.attr.get("instE", el.attr["instC"])))
                    + self._start_sim
                    <= end
                ]
            )
        return c

    def get_trip(self, vehid):
        states = self._get_states(vehid)
        veh_el = self.get_veh_element(vehid)
        path = Path(veh_el.attr["itineraire"].split(" "))
        origin = veh_el.attr["entree"]
        dest = veh_el.attr["sortie"]
        departure_time = veh_el.attr.get("instE")
        arrival_time = veh_el.attr["instS"]

        return Trip(
            states=states,
            path=path,
            departure_time=departure_time,
            arrival_time=arrival_time,
            origin=origin,
            destination=dest,
            vehicle=vehid,
        )

    def get_path(self, vehid):
        veh_el = self.get_veh_element(vehid)
        path = Path(veh_el.attr["itineraire"].split(" "))

        return path

    def clear_cache(self):
        self.get_ids_from_inst.cache_clear()
        self.get_veh_element.cache_clear()

    def _get_ids_from_inst(self, inst):
        """From XMLElement of INSTANT return a dict of TRAJ.

        Parameters
        ----------
        inst : symupy.parser.xmlparser.XMLElement
            XMLElement of tag INSTANT

        Returns
        -------
        dict
            dict with veh id as key and TRAJ XMLElement as value

        """
        trajs = inst.find_children_tag("TRAJS")
        return {el.attr["id"]: el for el in trajs.iterchildrens()}


if __name__ == "__main__":
    import symupy
    import os

    # file = os.path.dirname(symupy.__file__)+'/../tests/mocks/bottlenecks/bottleneck_001.xml'
    file = "/Users/florian.gacon/Work/SymuTools/data/ref_153000_163000_traf.xml"
    reader = SymuFlowTrafficDataReader(file)
    c = reader.get_OD(("A_Init_L1_OE", "CAF_Laf_Duguesclin"))
    c = reader.count_OD()
    cp = reader.count_OD(("15:30:00", "15:30:05"))
    # t1 = reader.get_trip('1')
    # E_Moliere_S, S_Crequi_N
    # 15:30:00, 15:30:05
