import networkx as nx
import numpy as np
from lxml import etree
from collections import defaultdict


def export_to_nx(file):
    troncons = defaultdict(dict)
    junctions = dict(
        caf=defaultdict(dict), rep=defaultdict(dict), gir=defaultdict(dict)
    )

    parser = etree.XMLParser(remove_comments=True)
    contents = etree.parse(file, parser=parser)
    root = contents.getroot()

    tron = root.xpath("/ROOT_SYMUBRUIT/RESEAUX/RESEAU/TRONCONS")[0]

    for tr_elem in tron.iterchildren():
        data = dict(tr_elem.attrib)
        ind = data.pop("id")
        coords_amont = np.fromstring(data["extremite_amont"], sep=" ")
        coords_aval = np.fromstring(data["extremite_aval"], sep=" ")
        points = [coords_amont]
        reserved_lane = []
        for tr_child in tr_elem.iterchildren():
            if tr_child.tag == "POINTS_INTERNES":
                for internal_points in tr_child.iterchildren():
                    points.append(
                        np.fromstring(internal_points.attrib["coordonnees"], sep=" ")
                    )
            if tr_child.tag == "VOIES_INTERDITES":
                for lane_elem in tr_child.iterchildren():
                    if lane_elem.attrib["id_typesvehicules"] == "VL":
                        reserved_lane.append(lane_elem.attrib["num_voie"])
        points.append(coords_aval)
        length = np.sum(
            [np.linalg.norm(points[i + 1] - points) for i in range(len(points) - 1)]
        )
        data["length"] = length

        if len(reserved_lane) < int(tr_elem.attrib.get("nb_voie", 1)):
            troncons[ind] = data
        else:
            print("Skipping link", ind, "(Public transportation)")

    caf = root.xpath("/ROOT_SYMUBRUIT/RESEAUX/RESEAU/CONNEXIONS/CARREFOURSAFEUX")[0]
    rep = root.xpath("/ROOT_SYMUBRUIT/RESEAUX/RESEAU/CONNEXIONS/REPARTITEURS")[0]
    gir = root.xpath("/ROOT_SYMUBRUIT/RESEAUX/RESEAU/CONNEXIONS/GIRATOIRES")[0]

    for elem, data in zip([caf, rep], [junctions["caf"], junctions["rep"]]):
        for caf_elem in elem.iterchildren():
            mov = caf_elem.xpath("MOUVEMENTS_AUTORISES")
            data[caf_elem.attrib["id"]] = defaultdict(list)
            if mov:
                for auth_elem in mov[0].iterchildren():
                    tr_am = auth_elem.attrib["id_troncon_amont"]
                    if tr_am in troncons:
                        out = auth_elem.xpath("MOUVEMENT_SORTIES")[0]
                        for out_elem in out.iterchildren():
                            tr_av = out_elem.attrib["id_troncon_aval"]
                            if tr_av in troncons:
                                data[caf_elem.attrib["id"]][tr_am].append(tr_av)

    data = junctions["gir"]
    for elem in gir.iterchildren():
        data[elem.attrib["id"]] = list()
        connected_tr = elem.attrib["troncons"].split(" ")
        for tr in connected_tr:
            if tr in troncons:
                data[elem.attrib["id"]].append(tr)

    G = nx.DiGraph()

    for tr, data in troncons.items():
        coords_amont = np.fromstring(data["extremite_amont"], sep=" ").tolist()
        coords_aval = np.fromstring(data["extremite_aval"], sep=" ").tolist()
        G.add_node("NAV_" + tr, coords=coords_aval, id_elt=data["id_eltaval"])
        G.add_node("NAM_" + tr, coords=coords_amont, id_elt=data["id_eltamont"])
        G.add_edge("NAM_" + tr, "NAV_" + tr, length=data["length"], id_elt=tr)

    for data in [junctions["rep"], junctions["caf"]]:
        for ind, connect in data.items():
            for tr_amont, tr_avals in connect.items():
                [
                    G.add_edge("NAV_" + tr_amont, "NAM_" + tr_av, length=0)
                    for tr_av in tr_avals
                ]

    for ind, tr_list in junctions["gir"].items():
        avals = list()
        amonts = list()
        for tr_i in tr_list:
            if troncons[tr_i]["id_eltamont"] == ind:
                amonts.append(tr_i)
            elif troncons[tr_i]["id_eltaval"] == ind:
                avals.append(tr_i)

        for tr_av in avals:
            for tr_am in amonts:
                G.add_edge("NAV_" + tr_av, "NAM_" + tr_am, length=0)

    return G
